# This module has three varients to parse 
# text from a html page
# and one method using nltk to calculate
# word frequency in a text

from urllib.parse import unquote # for url encoding
import re # regex import
import nltk # general purpose import of nltk
from nltk.corpus import stopwords  # to get a list of stopwords
from nltk.tokenize import word_tokenize  # to split sentences into words
from collections import Counter
from bs4 import BeautifulSoup # for parsing raw html string
import requests  # this we will use to call API and get data
from selectolax.parser import HTMLParser
from urllib.request import urlopen

import justext

class UrlInterpreter:
    def __init__(self, url):
        self.user_url = unquote(url)

    def get_word_frequencies(self, text, limit):
        try:
            tokens = word_tokenize(text)
            text = nltk.Text(tokens)

            # remove punctuation, create raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            
            # stop words
            stop_words = set(stopwords.words('english'))

            norm_words = [w for w in raw_words if w.lower() not in stop_words and len(w) > 3 and len(w) < 50]
            norm_words_counts = Counter(norm_words)
            
            # sort the list according to frequency
            norm_words_counts_sorted = norm_words_counts.most_common()

            # take out only top 100
            norm_words_counts_sorted_limit =  norm_words_counts_sorted[:limit]

            return norm_words_counts_sorted_limit
        except Exception as e:
            print("Unable to count frequencies. Error details :: " , repr(e))

        return []

    def get_all_text_bs(self):
        '''
        Very basic html page parser using BeautifulSoup 
        has a lot of escape/special characters
        '''
        page = self.get_page()
        raw = BeautifulSoup(page, 'html.parser').get_text()
        return raw

    def get_all_text_sim(self):
        '''
        Custom html page parser using BeautifulSoup 
        has very good results but a bit slow
        '''
        page = self.get_page()
        tree = BeautifulSoup(page, 'lxml')
        body = tree.body
        if body is None:
            return None

        for tag in body.select('script'):
            tag.decompose()
        for tag in body.select('style'):
            tag.decompose()

        text = body.get_text(separator=' ')
        return text

    def get_all_text_jt(self):
        '''
        Using justext package
        has very good results but very slow
        '''
        page = self.get_page()
        paragraphs = justext.justext(page, justext.get_stoplist("English"))
        all_text = ''
        for paragraph in paragraphs:
            all_text += ' ' + paragraph.text
            print(paragraph.text)
        return all_text

    def get_page(self):
        ''' Reads in page from url '''
        page = urlopen(self.user_url)
        return page

def main():
    url_parser = UrlInterpreter('https://www.google.com/')
    text = url_parser.get_all_text_sim()
    print(text)
    frequencies = url_parser.get_word_frequencies(text, 100)
    print('\n\n ======= \n\n')
    print(frequencies)
    # for word, count in words:
    #    print('{} occurred {} times'.format(word, count))

if __name__=='__main__': main()
