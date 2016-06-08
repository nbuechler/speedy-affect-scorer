from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

anticipation = Blueprint('anticipation', __name__)

@anticipation.route('/')
def default():
    return 'Hello anticipation!'

@anticipation.route('/alt/')
def controller_default():
    return controllers.default()
