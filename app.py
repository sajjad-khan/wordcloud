from flask import Flask, request, render_template, session, logging, redirect, url_for
import requests  # this we will use to call API and get data
import json  # to convert python dictionary to string format
from functools import wraps # for authentication purposes
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

from sample_data import SampleWords # sample starter words list

# custom modules
from db_ctrl import DbCtrl
from url_interpreter import UrlInterpreter
from salted_hash import SaltedHash
from cust_encryption import CustEncryption
from aes_encryption import AESEncryption

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
# encryptor = CustEncryption()
encryptor = AESEncryption()

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
    url_parser = UrlInterpreter(user_url)
    text = url_parser.get_all_text_sim()
    top_counts_100 = url_parser.get_word_frequencies(text, 100)
    
    if len(top_counts_100) > 0:
        # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
        # so, lets convert out word_freq in the respective format
        words_json = [{'text': word, 'weight': count} for word, count in top_counts_100]
        
        # save the results into db
        save_words(top_counts_100)

        app.logger.info('Done!')

        # now convert it into a string format and return it
        return json.dumps(words_json)    

    return '[]'

def save_words(final_words):
    values = [(hasher.get_salted_hash(word), encryptor.encypt(word), count) for word, count in final_words]
    
    mysql.insert_many(values)

# Login form class
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.Length(min=4, max=50)])

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This is for illustration purposes only, 
    credentials should come from e.g. users table
    where password stored in encrypted hash form
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'root':
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('admin'))
        else:
            error = 'Invalid login'
            return render_template('login.html', error = error)
    
    # GET case
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# logouts the user
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
@is_logged_in
def admin():
    # Get all words
    result = mysql.list()

    if(len(result) > 0):
        for word_row in result:
            word_row['word'] = encryptor.decrypt(word_row['word'])

        return render_template('admin.html', plain_words_list=result)
    else:
        return render_template('admin.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True) 
 