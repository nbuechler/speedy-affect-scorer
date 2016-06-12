from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers
from helpers.controllers import length_no_stop

anticipation = Blueprint('anticipation', __name__)

@anticipation.route('/')
def default():
    return 'Hello anticipation!'

@anticipation.route('/alt/')
def controller_default():
    return controllers.default()

@anticipation.route('/score/', methods=['GET', 'POST'])
def get_score():
    doc = request.form.get('doc')
    important_length = length_no_stop(doc, 'english')
    return 'Your anticipation string is ' + str(important_length) + ' word(s)!'
