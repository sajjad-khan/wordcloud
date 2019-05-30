from urllib.parse import unquote # for url encoding
import re # regex import
import nltk # general purpose import of nltk
from nltk.corpus import stopwords  # to get a list of stopwords
from nltk.tokenize import word_tokenize  # to split sentences into words
from collections import Counter
from bs4 import BeautifulSoup # for parsing raw html string
import requests  # this we will use to call API and get data

class UrlToWords:
    def __init__(self, url):
        self.user_url = unquote(url)

    def parse(self, limit):
        raw_html = None
        try:            
            # call the api
            raw_html = requests.get(self.user_url)
            print(raw_html)
        except Exception as e:
            print("Unable to get URL. Please make sure it's valid and try again.")
            print(repr(e))
        if raw_html:
            # text processing
            raw = BeautifulSoup(raw_html.text, 'html.parser').get_text()
            # nltk.data.path.append('./nltk_data/')  # set the path
            tokens = word_tokenize(raw)
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
            norm_words_counts_sorted_100 =  norm_words_counts_sorted[:limit]

            return norm_words_counts_sorted_100
        else:
            return []

def main():
    url_parser = UrlToWords('https://www.google.com/')
    words = url_parser.parse(10)
    for word, count in words:
        print('{} occurred {} times'.format(word, count))

if __name__=='__main__': main()
