from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

from flask import jsonify
import requests

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

    print mongo_corpus_synopsis.db['lingustic-affects'].find({'word': emotion})

    stop_words = stopwords.words(lang)
    list_of_words = [i for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]
    print list_of_words


    return 'Not Implemented'
