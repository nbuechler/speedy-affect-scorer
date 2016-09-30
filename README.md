# speedy-affect-scorer
The idea is to score basic affects - quickly!

# About the project
#### Affect
Affect is the measurable observation of an emotion.

	> e.g. A particularly relevant affect is natural language

	> Suggestion:  Learn about Affective Computing

Affects are defined by the observed reality (via some kind of sign) of a person.

	> Suggestion:  Learn about Semiotics

	Examples of affect include a facial expression, natural language sentence (Syntagam), tone, body temperature and/or another aspect of their person.

#### 'Representational' Emotions (R-EMOTION)
Linguistic labels (signifier/signified pairs) used to define an emotion.

	> Affects can be recorded and observed in sets of multiple R-EMOTION s.

	> e.g. A particularly popular set: Paul Ekman's Big 6

	> Suggestion:  Learn about EmotionML, see: https://www.w3.org/TR/emotion-voc/xml

#### 'Inferential' Emotions (I-EMOTION)
I-EMOTION s are an interpretation of how culture (as an emergent quality of human systems) constructs signifier/signified pairs of emotion where I-EMOTION s represent these as a vector of multiple R-EMOTION s.

	> Suggestion:  Learn about Anthropology

	> Suggestion:  Learn about Complexity Theory

	> Important: R-EMOTION s are symbolic and are not the same as 'Inferential' Emotions (I-EMOTION).

## History
The project originally included a file called 'corpus_builder.py' file which was separated into a different project called: copious-affect-corpus

Find the project here: https://github.com/nbuechler/copious-affect-corpus

* Appoximately 400 representational emotions are categorized by speedy-affect-scorer, these do not absolutely map to the inferential emotion of a human, which will be described later
* A representation of an emotion is a label like 'Love' which reminds us humans of signifier/signified pairs (see semiotics)
* Usually, one human maps their signifier/signified pairs to single a representation
* This project introduces the newer concept of an 'Inferential Emotion'
* The emotion that humans experience via the 'lens of culture' are not representational but rather inferential - and to best understand the meaning we ought to rely more on a scientific process rather than a simple signifier/signified pairs (label) that acts as a representation.
* One-to-one relationships of 'Inferential Emotion' to 'Representational Emotions' are not common with culture due to the 'Complexity of Culture'. Humans might sometimes confuse and argue with each other about emotions due to this complexity, and their lack of understanding of emergence (see complexity theory). Remember, a label/word is only a representation (sign) of an idea. 'Anger' - the word/label - is not an inferential emotion (in all but a one case, where culture is homogeneously angry). The inferential emotion therefore might be represented by something like a set of words; e.g. A combination of n-set of labels (Anger, Sadness, Fear, etc.)


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
* The set of scope includes a corpus of ~400 r-emotions only mapping to semantic data. (DONE)
* Identify better metrics to use (affectics? or emometrics?)
* Use ML to make even more metrics (maybe a different project)
* Do something useful with the data (maybe a different project)
* Research this, challenge it: https://en.wikipedia.org/wiki/Robert_Plutchik

* Also do think about different kinds of emotional state like this spectrum
```
analytic ----- intutive
```
* Analytically angry, intuitively happy?


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


```
*Write a scienctific paper about this.
*Include process in readme
*Setup a github page to host some of this stuff
*subdomain or something like that on nb.com?

# License

MIT
