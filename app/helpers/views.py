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
    controllers.process_emotion(doc, lang, emotion)
    return 'Success'
