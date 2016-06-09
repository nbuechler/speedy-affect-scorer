from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

sadness = Blueprint('sadness', __name__)

@sadness.route('/')
def default():
    return 'Hello sadness!'

@sadness.route('/alt/')
def controller_default():
    return controllers.default()

@sadness.route('/score/')
def get_score():
    return 'Not Implemented'
