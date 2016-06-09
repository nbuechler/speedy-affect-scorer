from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

anticipation = Blueprint('anticipation', __name__)

@anticipation.route('/')
def default():
    return 'Hello anticipation!'

@anticipation.route('/alt/')
def controller_default():
    return controllers.default()

@anticipation.route('/score/', methods=['GET', 'POST'])
def get_score():
    response = str(request.form.get('doc'))
    return 'Your anticipation string is ' + str(len(response)) + ' characters!'
