from flask import jsonify
import requests

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

app.config['MONGOCORPUS'] = 'test'
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
  word: <string of word>
  response: <json response from bighugelabs>
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

def get_ten_words(api_key, words):
    if api_key and words and len(words) == 10:
        for word in words:
            print '======' + word + '======'
            #TODO: Do mongodb stuff
            # data = get_single_word(api_key, word)
            # print data
            print jsonify({u'noun': {u'syn': [u'feeling']}})
            print '------------------'
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

@corpus.route('/10', methods=['GET', 'POST'])
def ten_words_view():
    r = request.get_json()
    # print r
    k = r.get('key')
    w = r.get('words')
    return get_ten_words(k, w)

@corpus.route('/100', methods=['GET', 'POST'])
def hundred_words_view(words=None):
    print 'Not Implemented'

@corpus.route('/500', methods=['GET', 'POST'])
def five_hundred_words_view(words=None):
    print 'Not Implemented'
