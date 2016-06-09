from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

import controllers

surprise = Blueprint('surprise', __name__)

@surprise.route('/')
def default():
    return 'Hello surprise!'

@surprise.route('/alt/')
def controller_default():
    return controllers.default()

@surprise.route('/score/')
def get_score():
    return 'Not Implemented'
