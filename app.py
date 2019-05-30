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

from flask_mysqldb import MySQL

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Haripur@1'
app.config['MYSQL_DB'] = 'wordscloudapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['USE_UNICODE'] = True

# init MySQL
mysql = MySQL(app)

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
        raw_html = None
        try:            
            # call the api
            raw_html = requests.get(user_url)
            app.logger.info(raw_html)
        except Exception as e:
            app.logger.info("Unable to get URL. Please make sure it's valid and try again.")
            app.logger.info(repr(e))
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
            norm_words_counts_sorted_100 =  norm_words_counts_sorted[:100]

            # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
            # so, lets convert out word_freq in the respective format
            words_json = [{'text': word, 'weight': count} for word, count in norm_words_counts_sorted_100]
            
            # save the results into db
            save_words(norm_words_counts_sorted_100)

            app.logger.info('Done!')

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
    values = [(get_word_salted_hash(word), b64_encypt_text(word), count) for word, count in final_words]
    
    # Insert Single row    
    # cur.execute(query, values)

    try:
        # Insert Multiple rows
        result  = cur.executemany(query, values)
        app.logger.info(result)

        # Commit to DB
        mysql.connection.commit()
    except:
        mysql.connection.rollback() 

    # Close connection
    cur.close()

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
    # Create curser
    cur = mysql.connection.cursor()

    # Get words
    result = cur.execute("SELECT * FROM topwords ORDER BY count DESC")
    words_list = cur.fetchall()
    cur.close()

    if(result > 0):
        for word_row in words_list:
            word_row['word'] = b64_decrypt_text(word_row['word'])

        plain_words_list = words_list
        return render_template('admin.html', plain_words_list=plain_words_list)
    else:
        msg = 'No Words Found'
        return render_template('admin.html', msg=msg)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True) 
 