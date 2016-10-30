from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

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
    # TODO: Add Error Handling
    natural = r.get('natural')
    stemmer = r.get('stemmer')
    lemma = r.get('lemma')
    processed_doc_metadata = controllers.process_emotion(doc, lang, emotion, natural, stemmer, lemma)
    return jsonify(processed_doc_metadata)

@helpers.route('/analyze_emotion_set/<emotion_set>/', methods=['POST'])
def analyze_emotion_set(emotion_set):
    r = request.get_json()
    doc = r.get('doc')
    lang = r.get('lang')
    # TODO: Add Error Handling
    natural = r.get('natural')
    stemmer = r.get('stemmer')
    lemma = r.get('lemma')
    processed_doc_list_metadata = controllers.process_emotion_set(doc, lang, emotion_set, natural, stemmer, lemma)
    return jsonify(emotion_set = processed_doc_list_metadata, name = emotion_set)

@helpers.route('/stats/<include_word>')
def display_affect_word_similarities(include_word=None, truncated=None):
    result = controllers.display_affect_word_similarities(include_word=include_word, truncated=truncated)
    return jsonify(statistics = result)

@helpers.route('/stats/<include_word>/truncated/<truncated>')
def display_truncated_affect_word_similarities(include_word=None, truncated=None):
    result = controllers.display_affect_word_similarities(include_word=include_word, truncated=truncated)
    return jsonify(statistics = result)
