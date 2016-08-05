from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

from flask import jsonify
import requests

from bson.json_util import loads, dumps

'''
********************************************************************************

This is a way to keep all the corpus database stuff in one file. I might this refactor later.

======
This section is for databases
======

********************************************************************************
'''

from app import app
from flask.ext.pymongo import PyMongo

app.config['MONGOCORPUSRAW_DBNAME'] = 'affect-corpus'
mongo_corpus = PyMongo(app, config_prefix='MONGOCORPUSRAW')

app.config['MONGOCORPUSSTORAGE_DBNAME'] = 'affect-synopsis'
mongo_corpus_synopsis = PyMongo(app, config_prefix='MONGOCORPUSSTORAGE')


'''
********************************************************************************

======
This a section for actual controller logic
======

********************************************************************************
'''

def default():
    print 'Here'
    return 'Thanks controller, hello helpers!'

def verify_bhl_api(api_key):
    r = requests.get('http://words.bighugelabs.com/api/2/' + api_key + '/affect/json')
    if(r.raise_for_status()):
        return 'error'
    else:
        return jsonify(r.json())

def length_no_stop_punct(doc, lang):

    stop_words = set(stopwords.words(lang))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation

    list_of_words = [i for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]

    return len(list_of_words)


'''
Business logic below

1. Take an emotion
2. Do something with it
3. Return results
4. Repeat for all emotions
'''


def process_emotion(doc, lang, emotion):

    # TODO: Make this better
    order_1 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-1']
    order_2 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-2']
    order_3 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-3']


    stop_words = stopwords.words(lang)
    list_of_words = [i for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]
    # print list_of_words

    print order_3

    for word in list_of_words:
        print '+++++++++++++'
        print 'This is the word: ' + word
        print word in order_3
        print '+++++++++++++'

    return 'Not Implemented'
