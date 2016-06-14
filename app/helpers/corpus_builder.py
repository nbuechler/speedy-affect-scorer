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

def get_single word(api_key, word):
    r = requests.get('http://words.bighugelabs.com/api/2/' + api_key + '/' + word + '/json')
    if(r.raise_for_status()):
        return 'error'
    else:
        return jsonify(r.json())
