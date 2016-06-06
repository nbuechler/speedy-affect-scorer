from flask import Flask
from flask import render_template, redirect, url_for, jsonify

# CORS dependecies
from flask.ext.cors import CORS

app = Flask(__name__)

#CORS instance
cors = CORS(app, resources={r"/*": {"origins": "*"}}) #CORS :WARNING everything!


#TODO: List out more apis for specific calls I need
@app.route('/')
def home_page():
    return 'hello world'
