from bs4 import BeautifulSoup
from urllib import urlopen

START_URL = '/wiki/Cat'
URL_BASE = 'https://en.wikipedia.org'
MAX_LINKS = 1000
DOC_DIRECTORY = 'test_docs/'

def run():
    visited = set()
    links = {START_URL}
    while len(visited) < MAX_LINKS:
        v, l = crawl(links, visited)
        visited |= v
        links |= l


def crawl(links, visited):
    new_links = set()
    
    for link in links:
        cur_link = URL_BASE + link
        if len(visited) > MAX_LINKS:
            break;
        if link not in visited:
            try:
                text = download(cur_link)
                visited.add(link)
                filename = '%stest%d.html' % (DOC_DIRECTORY, len(visited))
                write_to_file(text, filename)
                new_links |= (find_links(BeautifulSoup(text, 'lxml')))
            except IOError:
                print('%s failed to download.' % link)
                continue
            
    return (visited, new_links)


def download(link):
    return urlopen(link).read()

def write_to_file(text, filename):
    with open(filename, 'w') as outfile:
        outfile.write(text)
    
def find_links(soup):
    return set(filter(proper_url, [a.get('href') for a in soup.find_all('a')]))

def proper_url(url):
    if url is None:
        return False
    else:
        return '//' not in url

if __name__ == '__main__':
    run()
