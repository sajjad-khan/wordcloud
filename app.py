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
from urllib.parse import unquote

app = Flask(__name__)

url = None

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/word_cloud', methods=['GET'])
def word_cloud():
    user_url = request.args.get('user_url')
    user_url = unquote(user_url)
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
            # nltk.data.path.append('./nltk_data/')  # set the path
            tokens = word_tokenize(raw)
            text = nltk.Text(tokens)
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            print("Raw words count : {}".format(len(raw_word_count)))
            
            # stop words
            stop_words = set(stopwords.words('english'))

            norm_words = [w for w in raw_words if w.lower() not in stop_words and len(w) > 3 and len(w) < 50]
            norm_words_counts = Counter(norm_words)
            print("Filtered unique words count : {}".format(len(norm_words_counts)))
            # save the results
            
            norm_words_count_sorted = norm_words_counts.most_common()

            norm_words_counts_sorted_100 =  norm_words_count_sorted[:100]
            
            print("final: ", len(norm_words_counts_sorted_100))
            print("most common")
            for letter, count in norm_words_counts_sorted_100:
                print ('{} == {}'.format(letter, count))

            print("most common end")
            # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
            # so, lets convert out word_freq in the respective format
            words_json = [{'text': word, 'weight': count} for word, count in norm_words_counts_sorted_100]
            
            #print(words_json)
            print('Done!')
            # now convert it into a string format and return it
            return json.dumps(words_json)    
    return '[]'


if __name__ == '__main__':
    app.run(debug=True) 
 