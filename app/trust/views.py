from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

trust = Blueprint('trust', __name__)

@trust.route('/')
def default():
    return 'Hello trust!'

@trust.route('/alt/')
def controller_default():
    return controllers.default()
