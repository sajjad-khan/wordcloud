from flask import Flask, request, render_template, session, logging
import requests  # this we will use to call API and get data
import json  # to convert python dictionary to string format

from sample_data import SampleWords # sample starter words list

# custom modules
from db_ctrl import DbCtrl
from url_to_words import UrlToWords
from salted_hash import SaltedHash
from cust_encryption import CustEncryption

from flask_mysqldb import MySQL

# Create flask app
app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Haripur@1'
app.config['MYSQL_DB'] = 'wordscloudapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['USE_UNICODE'] = True

# init MySQL and its controller module
mysql = DbCtrl(MySQL(app))

# init hashing object
hasher = SaltedHash()

# init encryption object
cust_encryptor = CustEncryption()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/word_cloud', methods=['GET'])
def word_cloud():
    user_url = request.args.get('user_url')
    if user_url:
        return get_news_words(user_url)

    # GET method
    app.logger.info('app.logger.infoing sample data')
    return json.dumps(SampleWords())

def get_news_words(user_url):
    # take out only top 100
    url_parser = UrlToWords('https://www.google.com/')
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
    values = [(hasher.get_salted_hash(word), cust_encryptor.encypt(word), count) for word, count in final_words]
    
    mysql.insert_many(values)

@app.route('/admin')
def admin():
    # Get all words
    result = mysql.list()

    if(len(result) > 0):
        for word_row in result:
            word_row['word'] = cust_encryptor.decrypt(word_row['word'])

        return render_template('admin.html', plain_words_list=result)
    else:
        return render_template('admin.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True) 
 