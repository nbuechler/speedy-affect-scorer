from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.probability import FreqDist

from flask import jsonify
import requests, operator

from bson.json_util import loads, dumps

'''
********************************************************************************

This is a way to keep all the corpus database stuff in one file. I might this refactor later.

======
This section is for databases
======

********************************************************************************
'''

from app import app
from flask.ext.pymongo import PyMongo

app.config['MONGOCORPUSRAW_DBNAME'] = 'affect-corpus'
mongo_corpus = PyMongo(app, config_prefix='MONGOCORPUSRAW')

app.config['MONGOCORPUSSTORAGE_DBNAME'] = 'affect-synopsis'
mongo_corpus_synopsis = PyMongo(app, config_prefix='MONGOCORPUSSTORAGE')


'''
********************************************************************************

======
This a section for actual controller logic
======

********************************************************************************
'''

'''
********************************************************************************
emotion_sets
********************************************************************************
'''

'''
The first 83 inspired by emotionml
'''
emotionml_inspired = ['acceptance', 'admiration', 'affection', 'amusement', 'anger', 'anticipation', 'anxiety', 'appreciation', 'arousal', 'arrogance', 'awe', 'blame', 'boredom', 'calmness', 'compassion', 'compromise', 'concern', 'confidence', 'confusion', 'contempt', 'contentment', 'curiosity', 'denial', 'depression', 'desire', 'despair', 'disappointment', 'disgust', 'dissonance', 'distress', 'dread', 'ecstasy', 'edginess', 'embarrassment', 'enjoyment', 'enthusiasm', 'envy', 'eroticism', 'excitement', 'exuberance', 'fear', 'grace', 'gratification', 'gratitude', 'grief', 'happiness', 'harmony', 'hate', 'hope', 'humility', 'indifference', 'interest', 'irritation', 'jealousy', 'joy', 'love', 'lunacy', 'lust', 'mania', 'melancholy', 'pain', 'panic', 'patience', 'perturbation', 'pity', 'pleasure', 'pride', 'rage', 'relief', 'remorse', 'reproach', 'resentment', 'resignation', 'sadness', 'satisfaction', 'shame', 'shock', 'stress', 'surprise', 'triumph', 'trust', 'wonder', 'worry']

'''
uses the entire synopsis of emotions in the corpora
'''
all_emotions = ['abandonment', 'abhorrence', 'abomination', 'absorption', 'abstinence', 'acceptance', 'admiration', 'adoration', 'affection', 'affectionateness', 'affliction', 'aggravation', 'aggressiveness', 'agony', 'alarm', 'alienation', 'aliveness', 'aloofness', 'alteration', 'amazement', 'ambiance', 'amusement', 'anger', 'angst', 'anguish', 'animation', 'anticipation', 'antipathy', 'anxiety', 'apathy', 'appraisal', 'appreciation', 'arousal', 'arrogance', 'assimilation', 'astonishment', 'attraction', 'audaciousness', 'aversion', 'avoidance', 'awareness', 'awe', 'awfulness', 'awkwardness', 'badness', 'bashfulness', 'belief', 'bewilderment', 'bitterness', 'blame', 'blessedness', 'boldness', 'boredom', 'bravery', 'brightness', 'calmness', 'capableness', 'cautiousness', 'certainty', 'chastity', 'cheerfulness', 'cleverness', 'closeness', 'cloudiness', 'coercion', 'coldness', 'compassion', 'composure', 'compromise', 'compulsion', 'concern', 'confidence', 'conformity', 'confusion', 'consciousness', 'consideration', 'consonance', 'contempt', 'content', 'contentment', 'contrariness', 'courage', 'courageousness', 'covetousness', 'criticalness', 'crossness', 'curiosity', 'darkness', 'decency', 'defeat', 'defiance', 'delight', 'denial', 'depression', 'desire', 'desolation', 'despair', 'despicableness', 'determination', 'devastation', 'devotion', 'diffidence', 'diligence', 'dimension', 'disappointment', 'disbelief', 'disdain', 'disgrace', 'disgust', 'disillusionment', 'dislike', 'dismay', 'disorientation', 'disrespect', 'dissonance', 'distance', 'distress', 'distrust', 'disturbance', 'dominance', 'doubt', 'doubtfulness', 'dread', 'dullness', 'eagerness', 'earnestness', 'easiness', 'ecstasy', 'edginess', 'ego', 'elation', 'embarrassment', 'empathy', 'emptiness', 'encouragement', 'endurance', 'engagement', 'engrossment', 'enjoyment', 'enlightenment', 'enragement', 'enthusiasm', 'envy', 'eroticism', 'euphoria', 'exasperation', 'excitation', 'excitement', 'exhaustion', 'exploitation', 'exuberance', 'familiarity', 'fascination', 'fate', 'fatigue', 'fear', 'festivity', 'flatness', 'fondness', 'foolishness', 'forgiveness', 'fortune', 'freedom', 'fright', 'friskiness', 'frustration', 'fulfillment', 'furiousness', 'fury', 'gallantry', 'gayness', 'glee', 'gloominess', 'gluttony', 'goodness', 'grace', 'gratification', 'gratitude', 'greatness', 'greed', 'grief', 'guilt', 'happiness', 'hardiness', 'harmony', 'hate', 'helplessness', 'hesitance', 'hesitancy', 'honor', 'hope', 'hopefulness', 'horror', 'hostility', 'hotness', 'humbleness', 'humiliation', 'humility', 'hurt', 'ignorance', 'importance', 'impulse', 'impulsiveness', 'inadequacy', 'inadequateness', 'incapableness', 'indifference', 'inducement', 'indulgence', 'infatuation', 'infection', 'inferiority', 'inflammation', 'infuriation', 'innocence', 'inquisitiveness', 'insecurity', 'insignificance', 'inspiration', 'insult', 'intensity', 'intentness', 'interest', 'intimacy', 'intrigue', 'invulnerability', 'irritation', 'isolation', 'jealousy', 'joy', 'jubilance', 'keenness', 'kindness', 'liberality', 'liberation', 'lifelessness', 'liveliness', 'lividness', 'loathing', 'loneliness', 'loss', 'lousiness', 'love', 'luck', 'luckiness', 'lunacy', 'lust', 'mania', 'melancholy', 'merriness', 'misery', 'modesty', 'motivation', 'mournfulness', 'negation', 'negativeness', 'neglect', 'nervousness', 'neutrality', 'nonchalance', 'nostalgia', 'numbness', 'obsession', 'offensiveness', 'openness', 'optimism', 'outrage', 'pain', 'panic', 'paralysis', 'passion', 'passionateness', 'patience', 'peacefulness', 'permanence', 'perplexity', 'persuasion', 'perturbation', 'pessimism', 'petrification', 'pity', 'playfulness', 'pleasantness', 'pleasure', 'positiveness', 'potency', 'power', 'powerfulness', 'powerlessness', 'preoccupation', 'pride', 'provocation', 'quietness', 'quirkiness', 'rage', 'reassurance', 'rebellion', 'rebelliousness', 'reception', 'receptiveness', 'reenforcement', 'regret', 'reinforcement', 'rejection', 'relaxation', 'reliability', 'relief', 'reluctance', 'remorse', 'reproach', 'resentment', 'reservation', 'resignation', 'resistance', 'respect', 'restlessness', 'revulsion', 'ridicule', 'sadness', 'safety', 'saltiness', 'sarcasm', 'satisfaction', 'scorn', 'sensitivity', 'serenity', 'seriousness', 'shakiness', 'shame', 'shock', 'shyness', 'skepticism', 'sloth', 'snoopiness', 'sobriety', 'sourness', 'spirit', 'spiritedness', 'spite', 'stolidity', 'straightness', 'strength', 'stress', 'stubbornness', 'stupidity', 'submission', 'subversion', 'sulkiness', 'sulky', 'sullenness', 'sunniness', 'sureness', 'surprise', 'suspicion', 'sweetness', 'sympathy', 'tearfulness', 'tenaciousness', 'tenacity', 'tenderness', 'tenseness', 'terribleness', 'terror', 'thoughtfulness', 'threat', 'thrill', 'tolerance', 'tragedy', 'triumph', 'trust', 'uncertainty', 'understanding', 'uneasiness', 'unhappiness', 'unification', 'uniqueness', 'unity', 'unpleasantness', 'unpredictability', 'uselessness', 'valence', 'validation', 'vanity', 'veneration', 'vengefulness', 'victimization', 'vigor', 'vileness', 'vulnerability', 'warmness', 'weariness', 'withdrawal', 'withdrawnness', 'woe', 'woefulness', 'wonder', 'wonderfulness', 'worry', 'worthlessness', 'wrath']


'''
inspired by paul ekman, conforms to emotionml
'''
big_6 = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']


'''
********************************************************************************
metrics
********************************************************************************
'''

def calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3):
    ## Score of the affect, based on weights in the order
    r_affect_score = (
        ((is_in_order_1 * 0.7) + (is_in_order_2 * 0.2) + (is_in_order_3 * 0.1))/3
    )
    return r_affect_score

def calculate_normalized_r_score(normalized_order_1, normalized_order_2, normalized_order_3):
    ## Score of the affect, based on weights in the order
    normalized_r_score = (
        ((normalized_order_1 * 0.7) + (normalized_order_2 * 0.2) + (normalized_order_3 * 0.1))/3
    )
    return normalized_r_score

def calculate_r_density_score(r_affect_score, length_words_no_stop):
    ## But this one is based on density
    r_affect_density_score = r_affect_score/length_words_no_stop * 100
    return r_affect_density_score

'''
********************************************************************************
Start of actual Logic
********************************************************************************
'''

def default():
    print 'Here'
    return 'Thanks controller, hello helpers!'

def verify_bhl_api(api_key):
    r = requests.get('http://words.bighugelabs.com/api/2/' + api_key + '/affect/json')
    if(r.raise_for_status()):
        return 'error'
    else:
        return jsonify(r.json())

def length_no_stop_punct(doc, lang):

    stop_words = set(stopwords.words(lang))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation

    list_of_words = [i for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]

    return len(list_of_words)


'''
Business logic below

1. Take an emotion
2. Do something with it ---- this the 'process_emotion' method
3. Return results
4. Repeat for all emotions in a set ---- this is the 'process_emotion_set' method
'''

# TODO: Error Handling needed!
def process_emotion(doc, lang, emotion):

    # TODO: Make this better
    order_1 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-1']
    order_2 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-2']
    order_3 = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})['order-3']
    order_1_length = len(order_1)
    order_2_length = len(order_2)
    order_3_length = len(order_3)

    stop_words = stopwords.words(lang)
    list_of_words = [i for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]

    is_in_order_1 = 0
    is_in_order_2 = 0
    is_in_order_3 = 0

    list_of_order_1 = list()
    list_of_order_2 = list()
    list_of_order_3 = list()

    length_words_no_stop = len(list_of_words)

    for word in list_of_words:
        if word in order_1:
            is_in_order_1+=1
            list_of_order_1.append(word)
        if word in order_2:
            is_in_order_2+=1
            list_of_order_2.append(word)
        if word in order_3:
            is_in_order_3+=1
            list_of_order_3.append(word)

    pre_order_1_fdist = dict(FreqDist(list_of_order_1))
    pre_order_2_fdist = dict(FreqDist(list_of_order_2))
    pre_order_3_fdist = dict(FreqDist(list_of_order_3))

    order_1_fdist = sorted(pre_order_1_fdist.items(), key=lambda x: (x[1],x[0]))
    order_2_fdist = sorted(pre_order_2_fdist.items(), key=lambda x: (x[1],x[0]))
    order_3_fdist = sorted(pre_order_3_fdist.items(), key=lambda x: (x[1],x[0]))

    # Create a rudimentry scores
    # order one gets

    normalized_order_1 = float(is_in_order_1)/order_1_length * 100
    normalized_order_2 = float(is_in_order_2)/order_2_length * 100
    normalized_order_3 = float(is_in_order_3)/order_3_length * 100

    r_affect_score = calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3)
    normalized_r_score = calculate_normalized_r_score(normalized_order_1, normalized_order_2, normalized_order_3)
    r_affect_density_score = calculate_r_density_score(r_affect_score, length_words_no_stop)

    # TODO: Make a model for this? Maybe also not overload it!
    processed_doc_metadata = {
        "emotion": emotion,
        "is_in_order_1": is_in_order_1,
        "is_in_order_2": is_in_order_2,
        "is_in_order_3": is_in_order_3,
        'list_of_order_1': list_of_order_1,
        'list_of_order_2': list_of_order_2,
        'list_of_order_3': list_of_order_3,
        'order_1_fdist': order_1_fdist,
        'order_2_fdist': order_2_fdist,
        'order_3_fdist': order_3_fdist,
        "order_1_length": order_1_length,
        "order_2_length": order_2_length,
        "order_3_length": order_3_length,
        "normalized_order_1": normalized_order_1,
        "normalized_order_2": normalized_order_2,
        "normalized_order_3": normalized_order_3,
        "length_words_no_stop": length_words_no_stop,
        "r_affect_score": r_affect_score,
        "normalized_r_score": normalized_r_score,
        "r_affect_density_score": r_affect_density_score,
    }

    # print process_doc_metadata
    return processed_doc_metadata


# TODO: Error Handling needed!
def process_emotion_set(doc, lang, emotion_set):

    processed_doc_list_metadata = []

    e_set = None
    # pick emotion_set
    if emotion_set == 'emotion_ml':
        e_set = emotionml_inspired
    if emotion_set == 'all_emotions':
        e_set = all_emotions
    if emotion_set == 'big_6':
        e_set = big_6

    for emotion in e_set:
        processed_doc_list_metadata.append(process_emotion(doc, lang, emotion))

    print '---Creating an affect list!---'
    return processed_doc_list_metadata
