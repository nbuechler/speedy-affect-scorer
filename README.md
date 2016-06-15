# speedy-affect-scorer
The idea is to score basic afffects - quickly!

# Here is the scope, it's small
anticipation,
disgust,
fear,
joy,
sadness,
surprise,
and trust...

see: https://en.wikipedia.org/wiki/Robert_Plutchik

# Tech stack
It will use Flask to do the api, and NLTK to do some of the processing. It will probably also be structured in a way that it can be used in other projects, otherwise this wouldn't be MIT Licensed.


# Steps

.. first, install virtualenv if not done so already -- https://virtualenv.pypa.io/en/latest/installation.html(https://virtualenv.pypa.io/en/latest/installation.html)

.. then, run this command: $ virtualenv venv

.. (make sure you get the'.'): $ . venv/bin/activate

.. pip install -r requirements.txt

# Run Server

"""
python app/runserver.py 5000
"""


# Requirements

Flask==0.10.1
Flask-Cors==2.1.0
itsdangerous==0.24
Jinja2==2.8
MarkupSafe==0.23
six==1.10.0
Werkzeug==0.11.3
wheel==0.24.0
nltk==3.2.1


# CREDITS
'''
__To build a corpus ('Be Excellent to Each Other')__
'''

_Thesaurus service provided by words.bighugelabs.com (https://words.bighugelabs.com/api.php)_



# TODO:
-Break out the code that doesn't actually have anything to do with affect.

# License

MIT
