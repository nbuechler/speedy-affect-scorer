from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

joy = Blueprint('joy', __name__)

@joy.route('/')
def default():
    return 'Hello joy!'

@joy.route('/alt/')
def controller_default():
    return controllers.default()
