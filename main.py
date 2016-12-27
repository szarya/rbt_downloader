import os

from bs4 import BeautifulSoup
import urllib
import http.cookiejar
import re
from slugify import slugify

import settings


def get_episodes():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    url = 'http://braintrust.iwtstudents.com/users/login/'

    payload = {
        'data[User][email]': settings.USERNAME,
        'data[User][password]': settings.PASSWORD,
        'data[User][remember_me]': '1',
        '_method' : 'POST'
    }
    data = urllib.parse.urlencode(payload).encode('UTF-8')
    response = urllib.request.urlopen(url, data=data)

    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    episodes = []
    for ep in soup.find_all("span",string='Issue'):
        title_parts = list(filter(None,ep.parent.parent.text.split('\n')))
        episode_num = title_parts[0][6:]
        title,_, author = re.split(' (--|—) ',title_parts[1])
        link = ep.parent.parent.find('a')['href']
        episodes.append((episode_num, title, author, link))

    return episodes


def get_episode_files(episode):
    episode_num, title, author, link = episode
    new_title = '{0}_{1}'.format(episode_num, slugify('{0}-{1}'.format(title, author)).replace('-', '_'))
    # Download HTML
    yield {
            'url' : 'http://braintrust.iwtstudents.com' + link ,
            'type' : 'html',
            'title' : new_title
        }
    for link_name in ['transcript_link/','video_download_link/','audio_link/',]:
        url = ('http://braintrust.iwtstudents.com' + link + link_name).replace('/view/', '/download/')
        type = link_name[:5]

        yield {
            'url' : url,
            'type' : type,
            'title' : new_title
        }


def remove_js(filename):
    with open(filename, "rb") as f:
        html = f.read().decode('UTF-8')
    soup = BeautifulSoup(html, "html.parser")
    HEADER = '<head><link rel="stylesheet" type="text/css" href="css/bootstrap.css" /><link rel="stylesheet" type="text/css" href="css/slabtext.css" /></head>'

    output_html = '<html>{0}\n{1}</html>'.format(HEADER, str(soup.body))
    with open(filename, "wb") as f:
        f.write(output_html.encode('UTF-8'))


def download_css_files():
    for css_file in 'bootstrap.css', 'slabtext.css':
        file_path = 'RBT/css/{0}'.format(css_file)
        if not os.path.exists(os.path.join('RBT',css_file)):
            url = 'http://braintrust.iwtstudents.com/theme/BrainTrust/css/{0}'.format(css_file)
            result = urllib.request.urlopen(url)
            with open(file_path, "wb") as f:
                f.write(result.read())


def make_sure_dirs_exist():
    for d in ('RBT', 'RBT/css'):
        if not os.path.exists(d):
            os.makedirs(d)


def main():
    make_sure_dirs_exist()

    files = []
    for episode in get_episodes():
        for file in get_episode_files(episode):
            files.append(file)

    download_css_files()

    for file in files:
        result = urllib.request.urlopen(file['url'])
        if file['type'] == 'video':
            extension = '.mp4'
        elif file['type'] == 'audio':
            extension = '.mp3'
        elif file['type'] == 'html':
            extension = '.html'
        else:
            extension = '.pdf'
        filename = 'RBT/' + file['title'] + extension
        if os.path.exists(filename):
            print(filename + ' already exists')
            continue
        with open(filename + '.tmp', "wb") as f:
            print("Downloading {0}".format(filename))
            while not result.closed:
                buffer = result.read(64 * 1024)
                if not buffer:
                    break
                f.write(buffer)
        os.rename(filename + '.tmp', filename)
        if file['type'] == 'html':
            remove_js(filename)
        print('Downloaded ' + filename)

if __name__ == '__main__':
    main()