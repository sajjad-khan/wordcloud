from flask import Flask, request, render_template, session, logging
import re # regex import
import nltk # general purpose import of nltk
from nltk.corpus import stopwords  # to get a list of stopwords
from nltk.tokenize import word_tokenize  # to split sentences into words
from collections import Counter
from bs4 import BeautifulSoup # for parsing raw html string
import requests  # this we will use to call API and get data
import json  # to convert python dictionary to string format

from sample_data import SampleWords # sample starter words list
from urllib.parse import unquote # for url encoding

import hashlib, uuid, hashlib, base64 # for salted hash and encryption

# Create flask app
app = Flask(__name__)

from db_ctrl import DB_CTRL
from url_to_words import URL_TO_WORDS

from flask_mysqldb import MySQL

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Haripur@1'
app.config['MYSQL_DB'] = 'wordscloudapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['USE_UNICODE'] = True

# init MySQL and its controller module
mysql = DB_CTRL(MySQL(app))

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/word_cloud', methods=['GET'])
def word_cloud():
    user_url = request.args.get('user_url')
    if user_url:
        user_url = unquote(user_url)
        return get_news_words(user_url)

    # GET method
    app.logger.info('app.logger.infoing sample data')
    return json.dumps(SampleWords())

def get_news_words(user_url):
    if user_url:
        # take out only top 100
        url_parser = URL_TO_WORDS('https://www.google.com/')
        words_sorted_100 = url_parser.parse(100)

        if len(words_sorted_100) > 0:
            # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
            # so, lets convert out word_freq in the respective format
            words_json = [{'text': word, 'weight': count} for word, count in words_sorted_100]
            
            # save the results into db
            save_words(words_sorted_100)

            app.logger.info('Done!')

            # now convert it into a string format and return it
            return json.dumps(words_json)    

    return '[]'

def save_words(final_words):
    values = [(get_word_salted_hash(word), b64_encypt_text(word), count) for word, count in final_words]
    
    mysql.insert_many(values)

# uuid is used to generate a random number to generate salted hash key
salt = uuid.uuid4().hex

def get_word_salted_hash(password):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def get_word_from_salted_hash(hashed_word, word):
    password, salt = hashed_word.split(':')
    return password == hashlib.sha256(salt.encode() + word.encode()).hexdigest()

secret_key = '1234567890123456' # store somewhere safe


def b64_encypt_text(string):
    key = secret_key
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return base64.b64encode(bytes(encoded_string, "utf-8"))

def b64_decrypt_text(string):
    string = str(base64.b64decode(string), encoding = 'utf_8')
    key = secret_key
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

@app.route('/admin')
def admin():
    # Get all words
    result = mysql.list()

    if(len(result) > 0):
        for word_row in result:
            word_row['word'] = b64_decrypt_text(word_row['word'])

        return render_template('admin.html', plain_words_list=result)
    else:
        return render_template('admin.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True) 
 