# /bin/python

import re
import json
from string import Template

import requests
from bs4 import BeautifulSoup

def dowload_top_100():
    '''This script will download Top 100 books of last 30 days from Project 
    Gutenberg and saves them with appropriate file name'''
    base_url = 'http://www.gutenberg.myebook.bg/'
    response = requests.get('http://www.gutenberg.org/browse/scores/top')
    soup = BeautifulSoup(response.text)
    h_tag = soup.find(id='books-last30')
    ol_tag = h_tag.next_sibling.next_sibling
    for a_tag in ol_tag.find_all('a'):
        m = re.match(r'(.*)(\(\d+\))', a_tag.text)
        book_name = m.group(1).strip()
        m = re.match(r'/ebooks/(\d+)', a_tag.get('href'))
        book_id = m.group(1)
        # ugh, I know this is ugly.
        url = base_url + '/'.join(list(book_id[:-1])) + '/' + book_id + '/' + book_id + '.txt'
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            # print 'Downloaded... ', file_name
            with open(file_name, 'w') as f:
                f.write(r.text.encode('UTF-8'))
        else:
            print 'Failed for ', book_id

def cleanse(text_corpus):
    '''Removes all the punctuation and special characters from corpus'''
    return re.sub(r'[^\w-]', ' ', text_corpus)

def get_high_frequency_words():
    hf_words = json.loads(open('hf_words.json').read())
    for record in hf_words:
        yield record['term']

if __name__ == '__main__':
    pass