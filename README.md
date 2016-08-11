# speedy-affect-scorer
The idea is to score basic afffects - quickly! As of now, the project also includes a 'corpus_builder.py' file which will most likely be seperated into a sperate project.

# Here is the inital scope, it's small
anticipation,
disgust,
fear,
joy,
sadness,
surprise,
and trust...

(and the addition of lots of other words!)

# The extended scope includes a better scoring like so

## Score of the affect, based on weights in the order
```
r_affect_score = (
    ((is_in_order_1 * 0.5) + (is_in_order_2 * 0.3) + (is_in_order_3 * 0.2))/3
)
```

## But this one is based on density
```
r_affect_density_score = r_affect_score/length_words_no_stop * 100
```

# Here is the extedned scope, it's larger,
58 or more that exist in copious-affect-corpus

see: https://en.wikipedia.org/wiki/Robert_Plutchik

# Tech stack
It will use Flask to do the api, and NLTK to do some of the processing. It will probably also be structured in a way that it can be used in other projects, otherwise this wouldn't be MIT Licensed.


# Steps
* first, install virtualenv if not done so already -- https://virtualenv.pypa.io/en/latest/installation.html(https://virtualenv.pypa.io/en/latest/installation.html)
* then, run this command: $ virtualenv venv
* (make sure you get the'.'): $ . venv/bin/activate
* pip install -r requirements.txt

# Run Server

```
python app/runserver.py 5000
```


# Requirements

* Flask==0.10.1
* Flask-Cors==2.1.0
* itsdangerous==0.24
* Jinja2==2.8
* MarkupSafe==0.23
* six==1.10.0
* Werkzeug==0.11.3
* wheel==0.24.0
* nltk==3.2.1
* requests==2.10.0
* Flask-PyMongo==0.3.1
* pymongo==2.9.3


# TODO:
-Also do think about things like analytic ----- intutive (as a spectrum)

# License

MIT
