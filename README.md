# speedy-affect-scorer
The idea is to score basic afffects - quickly!

*Appoximately 400 representational emotions are categorized, these do not absolutely map to the neurological emotion of a human
*One human maps the neurological emotion - the one that they experience chemically/electrically - to a representation. This is what we call it via an english word.
*Humans will often map one neurological emotion to their defined preset of many representational emotions. This might be why we confuse and sometimes argue with each other about emotions. Remember that a word is only a representation of an idea. Anger - the word - is not a neurological emotion. The set of neurological impulses is actually the neurological emotion and it might be represented by something like a set of words; e.g. Anger, Sadness, Fear, etc.

## History
The project originally included a file called 'corpus_builder.py' file which was seperated into a different project called: copious-affect-corpus

Find the project here: https://github.com/nbuechler/copious-affect-corpus

## Build your database/corpus by also downloading copious-affect-corpus (the previously mentioned sister project)

Here is the link: https://github.com/nbuechler/copious-affect-corpus

Make sure to follow the instructions in that git project

# Here is the inital scope, it's small

Score the emotion set based on Paul Eckman's big 6.
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

## Additionaly scope goals
*The set of scope includes a corpus of ~400 r-emotions only mapping to semantic data.
*Identify better metrics to use (affectics? or emometrics?)
*Use ML to make even more metrics (maybe a different project)
*Do something useful with the data (maybe a different project)
*Research this, challenge it: https://en.wikipedia.org/wiki/Robert_Plutchik

*Also do think about different kinds of emotional state like this spectrum
```
analytic ----- intutive
```
*Analytically angry, intuitively happy?


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
*Also do think about things like this spectrum
```
analytic ----- intutive
```
*Write a scienctific paper about this.
*Include process in readme
*Setup a github page to host some of this stuff
*subdomain or something like that on nb.com?

# License

MIT
