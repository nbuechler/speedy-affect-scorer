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
  "flat-list": <list of all words (syn/ant of verb/noun) for this word>
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

def handle_next_level(raw_response):
    print '*************************************'
    print 'next-level'
    print '*************************************'
    va = []
    vs = []
    na = []
    ns = []
    if(raw_response.get('verb')):
        va = raw_response.get('verb').get('ant') if raw_response.get('verb').get('ant') is not None else []
        print va
        vs = raw_response.get('verb').get('syn') if raw_response.get('verb').get('syn') is not None else []
        print vs
    if(raw_response.get('noun')):
        na = raw_response.get('noun').get('ant') if raw_response.get('noun').get('ant') is not None else []
        print na
        ns = raw_response.get('noun').get('syn') if raw_response.get('noun').get('syn') is not None else []
        print ns
    print '*************************************'
    flat_list = va + vs + na + ns
    print '*-----------------------------------*'
    return flat_list

def save_word(word, raw_response, collection):
    # print word
    print '======' + word + '======'
    flat_list = handle_next_level(raw_response)
    result = {
              "word": word,
              "response": raw_response,
              "utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
              "flat_list": flat_list,
             }
    stored_result = mongo_corpus.db[collection].insert_one(result)
    # print raw_response
    print stored_result.inserted_id
    print raw_response
    print '------------------'
    return result


def get_word_or_words(word_length, api_key, words, collection):
    if api_key and words and len(words) == int(word_length):
        all_flat_lists = []
        # Level One
        for word in words:
            raw_response = get_single_word(api_key, word)
            data = save_word(word, raw_response, collection)
            print json.dumps(data.get('flat_list'))
            all_flat_lists = all_flat_lists + data.get('flat_list')
        print all_flat_lists
        return json.dumps(all_flat_lists)
    else:
        print 'MESSAGE: No valid input, sorry'
        return 'Error'

def get_two_levels(w, k, c):
    # get level one
    get_word_or_words(len(w), k, w, c)
    # get level two
    for value in variable:
        pass
    get_word_or_words(len(w), k, w, c)
    return 'Not Implemented'

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

'''
A human can build a corpus manulally by passing a word list of unknown count
to the method:

unknown_count_word_view()

Make sure to pass three paramaters via a form -- (api_key for BHT, words list, and a collection name)
Then the human can use the flattened list of each of the lists created to generate the next level.
This should also be automated. :-)
'''

# TODO: This should also be automated. :-)
@corpus.route('/x', methods=['GET', 'POST'])
def unknown_count_word_view():
    r = request.get_json()
    k = r.get('key')
    w = r.get('words')
    c = r.get('collection')
    return get_word_or_words(len(w), k, w, c)

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
