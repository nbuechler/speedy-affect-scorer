from flask import jsonify
import requests

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
        return jsonify(r.json())

def get_ten_words(words):
    if words and len(words) == 10:
        for word in words:
            print word
            #TODO: Do mongodb stuff
        return 'Success'
    else:
        print 'MESSAGE: No valid input, sorry'
        return 'Error'

'''
********************************************************************************

This is a way to keep all the corpus stuff in one file. I will refactor later.

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
    print r
    w = r.get('words')
    return get_ten_words(w)

@corpus.route('/100', methods=['GET', 'POST'])
def hundred_words_view(words=None):
    print 'Not Implemented'

@corpus.route('/500', methods=['GET', 'POST'])
def five_hundred_words_view(words=None):
    print 'Not Implemented'
