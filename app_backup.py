from flask import Flask, request, render_template
import operator
import re
import nltk
from nltk.corpus import stopwords  # to get a list of stopwords
from nltk.tokenize import word_tokenize  # to split sentences into words
from collections import Counter
from bs4 import BeautifulSoup
import requests  # this we will use to call API and get data
import json  # to convert python dictionary to string format
import operator
import urllib.request
import html2text

from sample_data import SampleWords

app = Flask(__name__)

url = None

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/word_cloud', methods=['GET'])
def word_cloud():
    user_url = request.args.get('user_url')
    print(user_url)    
    if user_url:
        return get_news_words(user_url)
    # GET method
    print('printing sample data')
    return json.dumps(SampleWords())

def get_news_words(user_url):
    if user_url:
        raw_html = None
        try:            
            # call the api
            raw_html = urllib.request.urlopen(user_url).read()
            # print(raw_html)
        except Exception as e:
            print("Unable to get URL. Please make sure it's valid and try again.")
            print(repr(e))
        if raw_html:
            # text processing
            raw = BeautifulSoup(raw_html, 'html.parser').get_text()
            # nltk.data.path.append('./nltk_data/')  # set the path
            h = html2text.HTML2Text()
            # Ignore converting links from HTML
            h.ignore_links = True
            raw = h.handle(raw)
            # print(raw)

            tokens = word_tokenize(raw)
            text = nltk.Text(tokens)
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            print("Raw words count : {}".format(len(raw_word_count)))
            
            # stop words
            stop_words = set(stopwords.words('english'))

            no_stop_words = [w for w in raw_words if w.lower() not in stop_words and len(w) > 3 and len(w) < 50]
            no_stop_words_count = Counter(no_stop_words)
            print("Filtered unique words count : {}".format(len(no_stop_words_count)))
            # save the results
            
            # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
            # so, lets convert out word_freq in the respective format
            words_json = [{'text': word, 'weight': count} for word, count in no_stop_words_count.items()]

            parse_urltext(user_url)
            #bcount = len(bl)
            #print('from bucky {} '.format(bcount))
                    
            print('Done!')
            # now convert it into a string format and return it
            return json.dumps(words_json)    
    return '[]'

def parse_urltext(url):
    # url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)

if __name__ == '__main__':
    app.run(debug=True) 
 