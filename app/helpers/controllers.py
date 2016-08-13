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

'''
********************************************************************************
emotion_sets
********************************************************************************
'''

'''
The first 85 inspired by emotionml
'''
emotionml_inspired = ['acceptance', 'admiration', 'affection', 'amusement', 'anger', 'anticipation', 'anxiety', 'appraisal', 'appreciation', 'arousal', 'arrogance', 'awe', 'blame', 'boredom', 'calmness', 'compassion', 'compromise', 'concern', 'confidence', 'confusion', 'contempt', 'contentment', 'curiosity', 'denial', 'depression', 'desire', 'despair', 'dimension', 'disappointment', 'disgust', 'dissonance', 'distress', 'dread', 'ecstasy', 'edginess', 'embarrassment', 'enjoyment', 'enthusiasm', 'envy', 'eroticism', 'excitement', 'exuberance', 'fear', 'grace', 'gratification', 'gratitude', 'grief', 'happiness', 'harmony', 'hate', 'hope', 'humility', 'indifference', 'interest', 'irritation', 'jealousy', 'joy', 'love', 'lunacy', 'lust', 'mania', 'melancholy', 'pain', 'panic', 'patience', 'perturbation', 'pity', 'pleasure', 'pride', 'rage', 'relief', 'remorse', 'reproach', 'resentment', 'resignation', 'sadness', 'satisfaction', 'shame', 'shock', 'stress', 'surprise', 'triumph', 'trust', 'wonder', 'worry']

'''
inspired by paul ekman, conforms to emotionml
'''
big_6 = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']



'''
********************************************************************************
metrics
********************************************************************************
'''

def calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3):
    ## Score of the affect, based on weights in the order
    r_affect_score = (
        ((is_in_order_1 * 0.5) + (is_in_order_2 * 0.3) + (is_in_order_3 * 0.2))/3
    )
    return r_affect_score

def calculate_r_density_score(r_affect_score, length_words_no_stop):
    ## But this one is based on density
    r_affect_density_score = r_affect_score/length_words_no_stop * 100
    return r_affect_density_score

'''
********************************************************************************
Start of actual Logic
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
2. Do something with it ---- this the 'process_emotion' method
3. Return results
4. Repeat for all emotions in a set ---- this is the 'process_emotion_set' method
'''

# TODO: Error Handling needed!
def process_emotion(doc, lang, emotion):

    # TODO: Make this better
    order_1 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-1']
    order_2 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-2']
    order_3 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-3']


    stop_words = stopwords.words(lang)
    list_of_words = [i for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]

    is_in_order_1 = 0
    is_in_order_2 = 0
    is_in_order_3 = 0

    length_words_no_stop = len(list_of_words)

    for word in list_of_words:
        if word in order_1:
            is_in_order_1+=1
        if word in order_2:
            is_in_order_2+=1
        if word in order_3:
            is_in_order_3+=1

    # Create a rudimentry scores
    # order one gets

    r_affect_score = calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3)
    r_affect_density_score = calculate_r_density_score(r_affect_score, length_words_no_stop)

    # TODO: Make a model for this?
    processed_doc_metadata = {
        "emotion": emotion,
        "is_in_order_1": is_in_order_1,
        "is_in_order_2": is_in_order_2,
        "is_in_order_3": is_in_order_3,
        "length_words_no_stop": length_words_no_stop,
        "r_affect_score": r_affect_score,
        "r_affect_density_score": r_affect_density_score,
    }

    # print process_doc_metadata
    return processed_doc_metadata


# TODO: Error Handling needed!
def process_emotion_set(doc, lang, emotion_set):

    processed_doc_list_metadata = []

    e_set = None
    # pick emotion_set
    if emotion_set == 'big_6':
        e_set = big_6
    if emotion_set == 'emotion_ml':
        e_set = emotionml_inspired

    for emotion in e_set:
        processed_doc_list_metadata.append(process_emotion(doc, lang, emotion))

    print processed_doc_list_metadata

    return processed_doc_list_metadata
