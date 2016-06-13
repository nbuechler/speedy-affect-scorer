from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

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
