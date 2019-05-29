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
        r = None
        try:            
            # call the api
            r = requests.get(user_url)
            print(r)
        except Exception as e:
            print("Unable to get URL. Please make sure it's valid and try again.")
            print(repr(e))
        if r:
            # text processing
            raw = BeautifulSoup(r.text, 'html.parser').get_text()
            # split sentences into words
            tokens = word_tokenize(raw)
            
            # convert it to nltk.Text
            text = nltk.Text(tokens)
            
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            print(raw_word_count)

            # get stopwords           
            stop_words = set(stopwords.words('english'))
            
            # remove stopwords from our words list and also remove any word whose length is less than 3
            # stopwords are commonly occuring words like is, am, are, they, some, etc.
            words = [word for word in raw_words if word.lower() not in stop_words and len(word) > 3]
            
            # now, get the words and their frequency
            words_freq = Counter(words)
            
            # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
            # so, lets convert out word_freq in the respective format
            words_json = [{'text': word, 'weight': count} for word, count in words_freq.items()]
            
            # now convert it into a string format and return it

            print('Done!')
            return json.dumps(words_json)    
    return '[]'


if __name__ == '__main__':
    app.run(debug=True) 
 