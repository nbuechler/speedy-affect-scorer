from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

disgust = Blueprint('disgust', __name__)

@disgust.route('/')
def default():
    return 'Hello disgust!'

@disgust.route('/alt/')
def controller_default():
    return controllers.default()

@disgust.route('/score/')
def get_score():
    return 'Not Implemented'
