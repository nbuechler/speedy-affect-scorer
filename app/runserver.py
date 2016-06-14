from app import app
import sys
from helpers.views import helpers
from anticipation.views import anticipation
from disgust.views import disgust
from fear.views import fear
from joy.views import joy
from sadness.views import sadness
from surprise.views import surprise
from trust.views import trust

app.register_blueprint(helpers, url_prefix='/helpers')
app.register_blueprint(anticipation, url_prefix='/anticipation')
app.register_blueprint(disgust, url_prefix='/disgust')
app.register_blueprint(fear, url_prefix='/fear')
app.register_blueprint(joy, url_prefix='/joy')
app.register_blueprint(sadness, url_prefix='/sadness')
app.register_blueprint(surprise, url_prefix='/surprise')
app.register_blueprint(trust, url_prefix='/trust')


'''
********************************************************************************
TODO: Refactor this out later
'''
from helpers.corpus_builder import corpus
app.register_blueprint(corpus, url_prefix='/corpus')
'''
********************************************************************************
'''

# Sets the port, or defaults to 80
if (len(sys.argv) > 1):
    port = int(sys.argv[1])
else:
    port=80

app.run(debug=True, host='0.0.0.0', port=port)
