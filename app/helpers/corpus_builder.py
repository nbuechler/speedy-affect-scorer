from flask import jsonify
import requests
from datetime import datetime

'''
********************************************************************************

This is a way to keep all the corpus stuff in one file. I will refactor later.

======
This section is for databases
======

********************************************************************************
'''

from app import app
from flask.ext.pymongo import PyMongo

app.config['MONGOCORPUS_DBNAME'] = 'affect-corpus'
mongo_corpus = PyMongo(app, config_prefix='MONGOCORPUS')


'''
********************************************************************************

This is a way to keep all the corpus stuff in one file. I will refactor later.

======
This section is for controllers
======

********************************************************************************
'''

'''
The aim of corpus_builder.py is to build a corpus of synonyms around a primary word.

i.e.
Affect
  it has synonyms
     those synonyms have synonyms
       and after the 4th level deep is likely where we don't care.

Moreover, the words will be stored as follows:

{
  "word": <added by what word>
  "response": <json response from bighugelabs>
  "utc": <utc date>
}

This gets stored in a mongo database. Collections are named after the inital parent.
In this case that parent is 'Affect'. To be clear, this is probably not the best way
to build a corpus, but it is a quick and effective way for getting started.
'''

def verify_bhl_api(api_key):
    r = requests.get('http://words.bighugelabs.com/api/2/' + api_key + '/affect/json')
    if(r.raise_for_status()):
        return 'error'
    else:
        return jsonify(r.json())

def get_single_word(api_key, word):
    r = requests.get('http://words.bighugelabs.com/api/2/' + api_key + '/' + word + '/json')
    if(r.raise_for_status()):
        return 'error'
    else:
        return r.json()

def save_word(word, data, collection):
    # print word
    print '======' + word + '======'
    result = mongo_corpus.db[collection].insert_one({
      "word": word,
      "response": data,
      "utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    })
    # print data
    print result.inserted_id
    print data
    print '------------------'
    return data

def get_word_or_words(word_length, api_key, words, collection):
    if api_key and words and len(words) == int(word_length):
        # Level One
        for word in words:
            response = get_single_word(api_key, word)
            data = save_word(word, response, collection)
        return 'Success'
    else:
        print 'MESSAGE: No valid input, sorry'
        return 'Error'

'''
********************************************************************************

This is a way to keep all the corpus stuff in one file. I will refactor later.

======
This section is for views
======

********************************************************************************
'''

from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import json

corpus = Blueprint('corpus', __name__)

'''
Flask views below as an endpoint
'''

@corpus.route('/')
def default():
    return 'Hello corpus_builder!'

@corpus.route('/1', methods=['GET', 'POST'])
def one_word_view():
    r = request.get_json()
    k = r.get('key')
    w = r.get('words')
    c = r.get('collection')
    return get_word_or_words(1, k, w, c)

@corpus.route('/10', methods=['GET', 'POST'])
def ten_words_view():
    r = request.get_json()
    k = r.get('key')
    w = r.get('words')
    c = r.get('collection')
    return get_word_or_words(10, k, w, c)

@corpus.route('/100', methods=['GET', 'POST'])
def hundred_words_view(words=None):
    r = request.get_json()
    k = r.get('key')
    w = r.get('words')
    c = r.get('collection')
    return get_word_or_words(100, k, w, c)

@corpus.route('/500', methods=['GET', 'POST'])
def five_hundred_words_view(words=None):
    r = request.get_json()
    k = r.get('key')
    w = r.get('words')
    c = r.get('collection')
    return get_word_or_words(500, k, w, c)
