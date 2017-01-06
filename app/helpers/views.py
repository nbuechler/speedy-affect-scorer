from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

from datetime import datetime

import controllers

utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],

helpers = Blueprint('helpers', __name__)

@helpers.route('/')
def default():
    return 'Hello helpers!'

@helpers.route('/<api_key>/')
def verify_api_01(api_key):
    response = 'No api'
    if(len(api_key) == 32):
        response = controllers.verify_bhl_api(api_key)
    return response

@helpers.route('/alt/')
def controller_default():
    return controllers.default()


'''
Business logic below

1. Take an emotion
2. Do something with it
3. Return results
4. Repeat for all emotions
'''

'''
analyze_emotion needs a form object:
{
  doc: '<string>', i.e 'The quick brown fox jumped over the lazy dog.'
  lang: '<string>', i.e. 'english'
}
'''
@helpers.route('/analyze_emotion/<emotion>/', methods=['POST'])
def analyze_emotion(emotion):
    r = request.get_json()
    doc = r.get('doc')
    lang = r.get('lang')
    upper_bound = r.get('ub')
    lower_bound = r.get('lb')
    # TODO: Add Error Handling
    natural = r.get('natural')
    stemmer = r.get('stemmer')
    lemma = r.get('lemma')

    emotion_stop_words = []
    if upper_bound == None and lower_bound == None:
        emotion_stop_words = controllers.find_emotion_stop_words(20,20)
    else:
        emotion_stop_words = controllers.find_emotion_stop_words(upper_bound,lower_bound)

    processed_doc_metadata = controllers.process_emotion(doc, lang, emotion, natural, stemmer, lemma, emotion_stop_words)

    print processed_doc_metadata
    return jsonify(processed_doc_metadata)

@helpers.route('/analyze_emotion_set/<emotion_set>/', methods=['POST'])
def analyze_emotion_set(emotion_set):
    r = request.get_json()
    doc = r.get('doc')
    lang = r.get('lang')
    upper_bound = r.get('ub')
    lower_bound = r.get('lb')
    # TODO: Add Error Handling
    natural = r.get('natural')
    stemmer = r.get('stemmer')
    lemma = r.get('lemma')

    emotion_stop_words = []
    if upper_bound == None and lower_bound == None:
        emotion_stop_words = controllers.find_emotion_stop_words(20,20)
    else:
        emotion_stop_words = controllers.find_emotion_stop_words(upper_bound,lower_bound)

    processed_doc_list_metadata = controllers.process_emotion_set(doc, lang, emotion_set, natural, stemmer, lemma, emotion_stop_words)
    return jsonify(emotion_set = processed_doc_list_metadata, name = emotion_set, date = utc)

@helpers.route('/stats/<include_word>')
def display_affect_word_similarities(include_word=None, truncated=None):
    result = controllers.display_affect_word_similarities(include_word=include_word, truncated=truncated)
    return jsonify(statistics = result)

@helpers.route('/stats/<include_word>/truncated/<truncated>')
def display_truncated_affect_word_similarities(include_word=None, truncated=None):
    result = controllers.display_affect_word_similarities(include_word=include_word, truncated=truncated)
    return jsonify(statistics = result)

@helpers.route('/stats/<include_word>/bounds/<upper_bound>,<lower_bound>/')
def display_bounds_affect_word_similarities(include_word=None, upper_bound=None, lower_bound=None):
    result = controllers.display_affect_word_similarities(include_word=include_word, upper_bound=upper_bound, lower_bound=lower_bound)
    return jsonify(statistics = result)

@helpers.route('/stats/<include_word>/bounds/upper/<upper_bound>/')
def display_upper_bounds_affect_word_similarities(include_word=None, upper_bound=None):
    result = controllers.display_affect_word_similarities(include_word=include_word, upper_bound=upper_bound)
    return jsonify(statistics = result)

@helpers.route('/stats/<include_word>/bounds/lower/<lower_bound>/')
def display_lower_bounds_affect_word_similarities(include_word=None, lower_bound=None):
    result = controllers.display_affect_word_similarities(include_word=include_word, lower_bound=lower_bound)
    return jsonify(statistics = result)

'''
upper_bound > number # The upper bound number means the area above this percent
lower_bound > number# The lower bound number means the area below this percent
==
e.g. upper_bound = 25, lower_bound = 25

==========                    ==========
0 ------ 25 ------ 50 ------ 75 ------ 100

**The 'shaded' area are the stop_words. The middle 50 percenet are processed words.

==
returns a list of affect stop words
'''
@helpers.route('/stop_words/affect/bounds/<upper_bound>,<lower_bound>/')
def find_emotion_stop_words(upper_bound=None, lower_bound=None):
    result = controllers.find_emotion_stop_words(upper_bound=upper_bound, lower_bound=lower_bound)
    return jsonify(stop_words = result, total_stop_words= len(result))
