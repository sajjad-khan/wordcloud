from flask import Flask, request, render_template, logging
from nltk.tokenize import word_tokenize  # to split sentences into words
from nltk.corpus import stopwords  # to get a list of stopwords
from collections import Counter  # to get words-frequency
import requests  # this we will use to call API and get data
import json  # to convert python dictionary to string format
from sample_data import SampleWords

app = Flask(__name__)

# get API key from NewsAPI.org
NEWS_API_KEY = "4a6b916f97594a31a6aaa9163cb3d5e0"

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        app.logger.info('POST')
        
    return render_template('index.html')

@app.route('/word_cloud', methods=['GET', 'POST'])
def word_cloud():
    if request.method == 'POST':
        try:
            # url for articles endpoint
            # I'm using bbc-news source, you can choose a source of your choice
            # or can pull data from multiple sources
            url = "https://newsapi.org/v1/articles?source=bbc-news&apiKey="+NEWS_API_KEY

            
            # call the api
            response = requests.get(url)
            
            # get the data in json format
            result = response.json()
            
            # all the news articles are listed under 'articles' key
            # we are interested in the description of each news article
            sentences = ""
            for news in result['articles']:
                description = news['description']
                sentences = sentences + " " + description
            
            # split sentences into words
            words = word_tokenize(sentences)
            
            # get stopwords
            stop_words = set(stopwords.words('english'))
            
            # remove stopwords from our words list and also remove any word whose length is less than 3
            # stopwords are commonly occuring words like is, am, are, they, some, etc.
            words = [word for word in words if word not in stop_words and len(word) > 3]
            
            # now, get the words and their frequency
            words_freq = Counter(words)
            
            # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
            # so, lets convert out word_freq in the respective format
            words_json = [{'text': word, 'weight': count} for word, count in words_freq.items()]
            
            # now convert it into a string format and return it

            return json.dumps(words_json)
        except Exception as e:
            app.logger.error('Failed to upload to ftp: '+ repr(e))
            return '[]'

    # GET method
    return json.dumps(SampleWords())

if __name__ == '__main__':
    app.run(debug=True) 
 