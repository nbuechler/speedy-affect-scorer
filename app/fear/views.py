from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

fear = Blueprint('fear', __name__)

@fear.route('/')
def default():
    return 'Hello fear!'

@fear.route('/alt/')
def controller_default():
    return controllers.default()
