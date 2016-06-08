from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

helpers = Blueprint('helpers', __name__)

@helpers.route('/')
def default():
    return 'Hello helpers!'

@helpers.route('/alt/')
def controller_default():
    return controllers.default()
