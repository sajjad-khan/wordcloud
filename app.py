from flask import Flask, request, render_template, session
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

import hashlib, uuid # for salted hashes
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

from flask_mysqldb import MySQL
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Haripur@1'
app.config['MYSQL_DB'] = 'wordscloudapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['USE_UNICODE'] = True
# use_unicode=True

# init MySQL
mysql = MySQL(app)

url = None

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
            
            norm_words_counts_sorted = norm_words_counts.most_common()

            norm_words_counts_sorted_100 =  norm_words_counts_sorted[:2]

            # print("final: ", len(norm_words_counts_sorted_100))
            print("most common")
            for letter, count in norm_words_counts_sorted_100:
                e = encode(letter)
                d = decode(e)
                print('original : ', [letter])
                print('encoded : ', [e])
                print('decoded : ', [d])

                print (' =  = {}'.format(len(e)))

            print("most common end")
            # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
            # so, lets convert out word_freq in the respective format
            words_json = [{'text': word, 'weight': count} for word, count in norm_words_counts_sorted_100]
            
            #print(words_json)
            save_words(norm_words_counts_sorted_100)

            print('Done!')
            # now convert it into a string format and return it
            return json.dumps(words_json)    
    return '[]'

def save_words(final_words):
    # Create cursor
    cur = mysql.connection.cursor()

    # MySQL query string
    query = '''INSERT INTO 
                topwords(word_shash, word, count) 
                VALUES(%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                count = VALUES(count)
                '''
    # values list
    values = [(get_word_salted_hash(word), encode(word).encode('utf8'), count) for word, count in final_words]
    
    # Insert Single row    
    # cur.execute(query, values)

    try:
        # Insert Multiple rows
        result  = cur.executemany(query, values)
        print(result)

        # Commit to DB
        mysql.connection.commit()
    except:
        mysql.connection.rollback() 

    # Close connection
    cur.close()

# uuid is used to generate a random number
salt = uuid.uuid4().hex

def get_word_salted_hash(password):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def get_word_from_salted_hash(hashed_word, word):
    password, salt = hashed_word.split(':')
    return password == hashlib.sha256(salt.encode() + word.encode()).hexdigest()

secret_key = '1234567890123456' # store somewhere safe

import six, base64

def encode(string):
    key = secret_key
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

def decode(string):
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
    # Create curser
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM topwords ORDER BY count DESC")
    words_list = cur.fetchall()

    if(result > 0):
            # values list
        # plain_words_list = [{'hword': hword, 'word': decode(eword), 'frequency': count} for hword, eword, count in words_list]
        # plain_words_list = [(get_word_from_salted_hash(word), decode(word), count) for word, count in words_list]
        for word_row in words_list:
            word_row['word'] = 'word'
            print(" == ", word_row['word'], " == ", decode(word_row['word']))
            # d = decode(e)

        plain_words_list = words_list
        return render_template('admin.html', plain_words_list=plain_words_list)
    else:
        msg = 'No Words Found'
        return render_template('admin.html', msg=msg)

    cur.close()

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True) 
 