# speedy-affect-scorer
The idea is to score basic affects - quickly!

# About the project
#### Affect
Affect is the measurable observation of an emotion.

	 e.g. A particularly relevant affect is natural language

	 Suggestion:  Learn about Affective Computing

Affects are defined by the observed reality (via some kind of sign) of a person.

	 Suggestion:  Learn about Semiotics

	Examples of affect include a facial expression, natural language sentence (Syntagram), tone, body temperature and/or another aspect of their person.

#### 'Representational' Emotions (R-EMOTION)
Linguistic labels (signifier/signified pairs) used to define an emotion.

	 Affects can be recorded and observed in sets of multiple R-EMOTION s.

	 e.g. A particularly popular set: Paul Ekman's Big 6

	 Suggestion:  Learn about EmotionML, see: https://www.w3.org/TR/emotion-voc/xml

#### 'Inferential' Emotions (I-EMOTION)
I-EMOTION s are an interpretation of how culture (as an emergent quality of human systems) constructs signifier/signified pairs of emotion where I-EMOTION s represent these as a vector of multiple R-EMOTION s.

	 Suggestion:  Learn about Anthropology

	 Suggestion:  Learn about Complexity Theory

	 Important: R-EMOTION s are symbolic and are not the same as 'Inferential' Emotions (I-EMOTION).

# History
The project originally included a file called 'corpus_builder.py' file which was separated into a different project called: 'copious-affect-corpus'

Find the project here: https://github.com/nbuechler/copious-affect-corpus

* Approximately 400 representational emotions are categorized by speedy-affect-scorer, these do not absolutely map to the inferential emotion of a human, which will be described later
* A representation of an emotion is a label like 'Love' which reminds us humans of signifier/signified pairs (see semiotics)
* Usually, one human maps their signifier/signified pairs to single a representation
* This project introduces the newer concept of an 'Inferential Emotion'
* The emotion that humans experience via the 'lens of culture' are not representational but rather inferential - and to best understand the meaning we ought to rely more on a scientific process rather than a simple signifier/signified pairs (label) that acts as a representation.
* One-to-one relationships of 'Inferential Emotion' to 'Representational Emotions' are not common with culture due to the 'Complexity of Culture'. Humans might sometimes confuse and argue with each other about emotions due to this complexity, and their lack of understanding of emergence (see complexity theory). Remember, a label/word is only a representation (sign) of an idea. 'Anger' - the word/label - is not an inferential emotion (in all but a one case, where culture is homogeneously angry). The inferential emotion therefore might be represented by something like a set of words; e.g. A combination of n-set of labels (Anger, Sadness, Fear, etc.)

# Build your database/corpus
Build your database/corpus by also cloning 'copious-affect-corpus' here: https://github.com/nbuechler/copious-affect-corpus

Make sure to follow the instructions in that git project.

# Completed Phases
#### Scope 1
Score based on the emotion set referenced by Paul Eckman's big 6: anger, happiness, surprise, disgust, sadness, and fear.

#### Scope 2
Score based on the addition of lots of emotion sets and words which includes the 400 representational emotions mentioned above.

#### Scope 3
Use AI to make an enhanced version of this scoring method (see OmegaHorizonResearch)

# Additional scope goals
* The set of scope includes a corpus of ~400 r-emotions only mapping to semantic data. (DONE)
* Include process in README (DONE)
* Remove other stop-emotion-words like the word 'emotion' (DONE)
* Visualize the data (DONE - see ample-affect-exhibit)
* Research this, critique it: https://en.wikipedia.org/wiki/Robert_Plutchik
* Also, think about different kinds of emotional state. For example like this spectrum
```
analytic ----- intutive
```
* Ask more questions like this: Is it possible to analytically angry or intuitively happy?
* Write a scientific paper about this to gain insight from the academic community
* Setup a github page to host some of this content, it could be a sub-domain or something on other sites
* We can also move past linguistic/semantic data into other kinds of emotive data

# Most exciting future plans
If I begin working with a friend of mine (likely 2016), it would be useful to intercept the data and send it to a machine learning model to notice trends in affect. This machine learning model would be in a separate project. (in 2016)

# Process for making the initial corpora
* Write the script and coding, and tweak the technical implementation of gathering all the synonyms
* Make sure that all the Emotions in emotionML are nouns. There are anywhere between a small number, like 4, to an infinite amount of emotions -- similar to that of color... or sounds, etc.
* Run the querying, from big huge thesaurus. Doing no more than 1000 per day. This made it easier and less redundant for me, but also made me think more about what I was doing. The limit of 1000 is because the API is free to use below that amount.

Here's the endpoint and an example JSON form to submit:

```
-root-/corpus/y

{
    "words":  [
		"courageousness"
	],
    "key": "YOUR_API_KEY",
    "collection": "courageousness-corpus-only-syn-unq",
    "levels": "3",
    "include_synonyms": "1",
    "include_antonyms": "0"
}
```

* Stored the result with a logfile (as an extra and redundant storage mechanism), and also in MongoDB (specifically in  affect-corpus as a database name).

# Process for making the synopsis
* Write an API to make the _affect-corpus_ more understandable, it allows for calling each collection in _affect-corpus_.
* Use the API to take the flat words in _affect-corpus_ and organize them in _affect-synopsis_.

# Getting Started
* First, install virtualenv if not done so already -- https://virtualenv.pypa.io/en/latest/installation.html(https://virtualenv.pypa.io/en/latest/installation.html)
* Then, run this command:
<pre>
  <code>
    $ virtualenv venv
  </code>
</pre>
* Next, activate the virtual environment (make sure you get the'.'):
<pre>
  <code>
    $ . venv/bin/activate
  </code>
</pre>
* Last, install the requirements with pip:
<pre>
  <code>
    $ pip install -r requirements.txt
  </code>
</pre>


# Start databases - if they are not already running
_From a terminal, start mongo:_
<pre>
  <code>
    mongod
  </code>
</pre>

_From a terminal start Neo4j:_
<pre>
  <code>
    sudo /etc/init.d/neo4j-service start
  </code>
</pre>

# Run the application
<pre>
  <code>
    python app/runserver.py 5000
  </code>
</pre>

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

# Tech stack
The project uses Flask to do the RESTful API, and NLTK to do some of the processing. It is also structured in a way that it can be used in other projects.

# License
MIT
