from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from flask import jsonify
import requests, operator, math

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

# TODO: Store these in a database along with a description of their origin
'''
The first 83 included from the emotionml
'''
emotionml_inspired = ['acceptance', 'admiration', 'affection', 'amusement', 'anger', 'anticipation', 'anxiety', 'appreciation', 'arousal', 'arrogance', 'awe', 'blame', 'boredom', 'calmness', 'compassion', 'compromise', 'concern', 'confidence', 'confusion', 'contempt', 'contentment', 'curiosity', 'denial', 'depression', 'desire', 'despair', 'disappointment', 'disgust', 'dissonance', 'distress', 'dread', 'ecstasy', 'edginess', 'embarrassment', 'enjoyment', 'enthusiasm', 'envy', 'eroticism', 'excitement', 'exuberance', 'fear', 'grace', 'gratification', 'gratitude', 'grief', 'happiness', 'harmony', 'hate', 'hope', 'humility', 'indifference', 'interest', 'irritation', 'jealousy', 'joy', 'love', 'lunacy', 'lust', 'mania', 'melancholy', 'pain', 'panic', 'patience', 'perturbation', 'pity', 'pleasure', 'pride', 'rage', 'relief', 'remorse', 'reproach', 'resentment', 'resignation', 'sadness', 'satisfaction', 'shame', 'shock', 'stress', 'surprise', 'triumph', 'trust', 'wonder', 'worry']

'''
uses the entire synopsis of emotions in the corpora
'''
all_emotions = ['abandonment', 'abhorrence', 'abomination', 'absorption', 'abstinence', 'acceptance', 'admiration', 'adoration', 'affection', 'affectionateness', 'affliction', 'aggravation', 'aggressiveness', 'agony', 'alarm', 'alienation', 'aliveness', 'aloofness', 'alteration', 'amazement', 'ambiance', 'amusement', 'anger', 'angst', 'anguish', 'animation', 'anticipation', 'antipathy', 'anxiety', 'apathy', 'appraisal', 'appreciation', 'arousal', 'arrogance', 'assimilation', 'astonishment', 'attraction', 'audaciousness', 'aversion', 'avoidance', 'awareness', 'awe', 'awfulness', 'awkwardness', 'badness', 'bashfulness', 'belief', 'bewilderment', 'bitterness', 'blame', 'blessedness', 'boldness', 'boredom', 'bravery', 'brightness', 'calmness', 'capableness', 'cautiousness', 'certainty', 'chastity', 'cheerfulness', 'cleverness', 'closeness', 'cloudiness', 'coercion', 'coldness', 'compassion', 'composure', 'compromise', 'compulsion', 'concern', 'confidence', 'conformity', 'confusion', 'consciousness', 'consideration', 'consonance', 'contempt', 'content', 'contentment', 'contrariness', 'courage', 'courageousness', 'covetousness', 'criticalness', 'crossness', 'curiosity', 'darkness', 'decency', 'defeat', 'defiance', 'delight', 'denial', 'depression', 'desire', 'desolation', 'despair', 'despicableness', 'determination', 'devastation', 'devotion', 'diffidence', 'diligence', 'dimension', 'disappointment', 'disbelief', 'disdain', 'disgrace', 'disgust', 'disillusionment', 'dislike', 'dismay', 'disorientation', 'disrespect', 'dissonance', 'distance', 'distress', 'distrust', 'disturbance', 'dominance', 'doubt', 'doubtfulness', 'dread', 'dullness', 'eagerness', 'earnestness', 'easiness', 'ecstasy', 'edginess', 'ego', 'elation', 'embarrassment', 'empathy', 'emptiness', 'encouragement', 'endurance', 'engagement', 'engrossment', 'enjoyment', 'enlightenment', 'enragement', 'enthusiasm', 'envy', 'eroticism', 'euphoria', 'exasperation', 'excitation', 'excitement', 'exhaustion', 'exploitation', 'exuberance', 'familiarity', 'fascination', 'fate', 'fatigue', 'fear', 'festivity', 'flatness', 'fondness', 'foolishness', 'forgiveness', 'fortune', 'freedom', 'fright', 'friskiness', 'frustration', 'fulfillment', 'furiousness', 'fury', 'gallantry', 'gayness', 'glee', 'gloominess', 'gluttony', 'goodness', 'grace', 'gratification', 'gratitude', 'greatness', 'greed', 'grief', 'guilt', 'happiness', 'hardiness', 'harmony', 'hate', 'helplessness', 'hesitance', 'hesitancy', 'honor', 'hope', 'hopefulness', 'horror', 'hostility', 'hotness', 'humbleness', 'humiliation', 'humility', 'hurt', 'ignorance', 'importance', 'impulse', 'impulsiveness', 'inadequacy', 'inadequateness', 'incapableness', 'indifference', 'inducement', 'indulgence', 'infatuation', 'infection', 'inferiority', 'inflammation', 'infuriation', 'innocence', 'inquisitiveness', 'insecurity', 'insignificance', 'inspiration', 'insult', 'intensity', 'intentness', 'interest', 'intimacy', 'intrigue', 'invulnerability', 'irritation', 'isolation', 'jealousy', 'joy', 'jubilance', 'keenness', 'kindness', 'liberality', 'liberation', 'lifelessness', 'liveliness', 'lividness', 'loathing', 'loneliness', 'loss', 'lousiness', 'love', 'luck', 'luckiness', 'lunacy', 'lust', 'mania', 'melancholy', 'merriness', 'misery', 'modesty', 'motivation', 'mournfulness', 'negation', 'negativeness', 'neglect', 'nervousness', 'neutrality', 'nonchalance', 'nostalgia', 'numbness', 'obsession', 'offensiveness', 'openness', 'optimism', 'outrage', 'pain', 'panic', 'paralysis', 'passion', 'passionateness', 'patience', 'peacefulness', 'permanence', 'perplexity', 'persuasion', 'perturbation', 'pessimism', 'petrification', 'pity', 'playfulness', 'pleasantness', 'pleasure', 'positiveness', 'potency', 'power', 'powerfulness', 'powerlessness', 'preoccupation', 'pride', 'provocation', 'quietness', 'quirkiness', 'rage', 'reassurance', 'rebellion', 'rebelliousness', 'reception', 'receptiveness', 'reenforcement', 'regret', 'reinforcement', 'rejection', 'relaxation', 'reliability', 'relief', 'reluctance', 'remorse', 'reproach', 'resentment', 'reservation', 'resignation', 'resistance', 'respect', 'restlessness', 'revulsion', 'ridicule', 'sadness', 'safety', 'saltiness', 'sarcasm', 'satisfaction', 'scorn', 'sensitivity', 'serenity', 'seriousness', 'shakiness', 'shame', 'shock', 'shyness', 'skepticism', 'sloth', 'snoopiness', 'sobriety', 'sourness', 'spirit', 'spiritedness', 'spite', 'stolidity', 'straightness', 'strength', 'stress', 'stubbornness', 'stupidity', 'submission', 'subversion', 'sulkiness', 'sulky', 'sullenness', 'sunniness', 'sureness', 'surprise', 'suspicion', 'sweetness', 'sympathy', 'tearfulness', 'tenaciousness', 'tenacity', 'tenderness', 'tenseness', 'terribleness', 'terror', 'thoughtfulness', 'threat', 'thrill', 'tolerance', 'tragedy', 'triumph', 'trust', 'uncertainty', 'understanding', 'uneasiness', 'unhappiness', 'unification', 'uniqueness', 'unity', 'unpleasantness', 'unpredictability', 'uselessness', 'valence', 'validation', 'vanity', 'veneration', 'vengefulness', 'victimization', 'vigor', 'vileness', 'vulnerability', 'warmness', 'weariness', 'withdrawal', 'withdrawnness', 'woe', 'woefulness', 'wonder', 'wonderfulness', 'worry', 'worthlessness', 'wrath']

'''
included from paul ekman, conforms to emotionml
'''
big_6 = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']

'''
everday categories included from the emotion_ml section
'''
everday_categories = ['affection', 'anxiety', 'amusement', 'anger', 'boredom', 'confidence', 'satisfaction', 'disappointment', 'excitement', 'joy', 'curiosity', 'love', 'pride', 'calmness', 'sadness', 'harmony', 'worry']

'''
OCC (Ortony, Clore and Collins) categories included from the emotion_ml section
'''
occ_categories = ['admiration', 'anger', 'disappointment', 'distress', 'fear', 'dread' , 'triumph', 'gratification', 'gratitude', 'appreciation', 'hate' , 'hope', 'joy', 'love', 'pity' , 'pride', 'relief', 'remorse', 'reproach', 'resentment', 'satisfaction', 'embarrassment']

'''
FSRE (ontaine, Scherer, Roesch and Ellsworth) categories included from emotion_ml section
'''
fsre_categories = ['anger', 'anxiety', 'pain', 'compassion', 'contempt', 'contentment', 'despair', 'disappointment', 'disgust', 'fear', 'guilt', 'happiness', 'hate', 'interest', 'irritation', 'jealousy', 'joy', 'love', 'pleasure', 'pride', 'sadness', 'shame', 'stress', 'surprise']

'''
Nico Frijda's proposal of action tendencies included from the emotion_ml section
'''
frijda_categories = ['anger', 'arrogance', 'desire', 'disgust', 'enjoyment', 'fear', 'humility', 'indifference', 'interest', 'resignation', 'shock', 'surprise']

'''
Dimensions included from the emotion_ml section
'''
dimensions = ['pleasure', 'arousal', 'dominance', 'valence', 'potency', 'unpredictability', 'intensity']


'''
********************************************************************************
statistics
********************************************************************************
'''

def display_affect_word_similarities(include_word=None, truncated=None, upper_bound=None, lower_bound=None):

    cursor = mongo_corpus_synopsis.db['affect-word-frequency'].find({})

    final_stats = []
    stats = []
    if include_word == "3":
        for doc in cursor:
            stats.append({
                'emotion-count': doc['emotion-count'],
                'word': doc['word'],
            })
    elif include_word == "2":
        for doc in cursor:
            stats.append(doc['word'])
    elif include_word == "1":
        for doc in cursor:
            stats.append({
                'emotion-count': doc['emotion-count'],
                'word': doc['word'],
            })
    elif include_word == "0":
        for doc in cursor:
            stats.append(doc['emotion-count'])


    if include_word != "2":
        sorted_stats = sorted(stats, reverse=True)
    else:
        sorted_stats = sorted(stats)

    j = 0
    trunc_stats = []
    if truncated == "1":
        for stat in sorted_stats:
            if (j % 160 == 0):
                trunc_stats.append(stat)
            j =+ j + 1

    if truncated == "1":
        final_stats = trunc_stats
    elif truncated == "0":
        final_stats = sorted_stats
    else:
        final_stats = sorted_stats

    # There is a little overlap between ranges due to to rounding...
    if upper_bound != None and lower_bound != None:
        upper_bound_percent_to_number = int(math.ceil(len(final_stats) * int(upper_bound) / 100))
        lower_bound_percent_to_number = int(math.ceil(len(final_stats) * int(lower_bound) / 100))
        final_stats = final_stats[(upper_bound_percent_to_number):(len(final_stats)-lower_bound_percent_to_number)]
    elif upper_bound != None:
        upper_bound_percent_to_number = int(math.ceil(len(final_stats) * int(upper_bound) / 100))
        final_stats = final_stats[0:(upper_bound_percent_to_number)]
    elif lower_bound != None:
        lower_bound_percent_to_number = int(math.ceil(len(final_stats) * int(lower_bound) / 100))
        final_stats = final_stats[(len(final_stats)-lower_bound_percent_to_number):len(final_stats)]


    affect_word_list = []
    if include_word == "3":
        for stat in final_stats:
            affect_word_list.append(stat['word'])

        final_stats = affect_word_list

    return final_stats

'''
********************************************************************************
metrics
********************************************************************************
'''

# TODO Incorporate overlapping orders in some way
def calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3):
    ## Score of the affect, based on weights in the order
    r_affect_score = (
        ((is_in_order_1 * 0.7) + (is_in_order_2 * 0.2) + (is_in_order_3 * 0.1))/3
    )
    return r_affect_score

# TODO Incorporate overlapping orders in some way
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

'''
Find the 'stop words' that are very common in each affect corpus
'''
def find_emotion_stop_words(upper_bound=None, lower_bound=None):

    result = []
    ub = display_affect_word_similarities(include_word="3", upper_bound=upper_bound)
    lb = display_affect_word_similarities(include_word="3", lower_bound=lower_bound)
    result = ub + lb

    return list(set(result))

'''
Business logic below

1. Take an emotion
2. Do something with it ---- this the 'process_emotion' method
3. Return results
4. Repeat for all emotions in a set ---- this is the 'process_emotion_set' method
'''

'''
doc > <string>
lang > <string>
emotion > <string>
flags <dict>:
    {
        naturalFlag > <string> (number)
        stemmerFlag > <string> (number)
        lemmaFlag > <string> (number)
    }
emotion_stop_words > (list of <strings>)
word_lists_no_emotion_stop <dict>:
    {
        list_of_words > (list of <strings>)
        stemmed_list > (list of <strings>)
        lemmatized_list > (list of <strings>)
    }
order > <string>
==
Finds the metadata for an order, used and combined with other similar objects to
find metadata for and emotion, see: process emotion
RETURNS:
{
        "order_length": <number>,
        "natural_list_of_order": <list>,
        "stemmer_list_of_order": <list>,
        "lemma_list_of_order": <list>,
        "is_in_order": <number>, # Count of the number of times a word is in the order
        "order_fdist": <list of [<list>,<number>]>,
        "natural_order_fdist": <list of [<list>,<number>]>,
        "stemmer_order_fdist": <list of [<list>,<number>]>,
        "lemma_order_fdist": <list of [<list>,<number>]>,
        "normalized_order": <number>, # A score
}
'''
def process_order(doc, lang, emotion, flags, emotion_stop_words, word_lists_no_emotion_stop, order):

    processed_order = {
        "status": "success",
        "order": order,
    }

    # Select the corpora, get the length of the corpora
    order_corpora = None
    order_corpora_length = 0
    if order == 'order-1' or order == 'order-2' or order == 'order-3' :
        order_corpora = mongo_corpus_synopsis.db['lingustic-affects'].find_one({'word': emotion})[order]
    else:
        order_corpora = mongo_corpus_synopsis.db['lingustic-affects-order-similarities'].find_one({'word': emotion})[order]

    order_corpora_length = len(order_corpora)

    # More of the metadata for the order
    natural_list_of_order = list()
    stemmer_list_of_order = list()
    lemma_list_of_order = list()
    is_in_order = 0

    if flags['naturalFlag'] == '1':
        for word in word_lists_no_emotion_stop['list_of_words']:
            if word in order_corpora:
                is_in_order+=1
                natural_list_of_order.append(word)
    if flags['stemmerFlag'] == '1':
        for stem_word in word_lists_no_emotion_stop['stemmed_list']:
            if stem_word in order_corpora:
                is_in_order+=1
                stemmer_list_of_order.append(stem_word)
    if flags['lemmaFlag'] == '1':
        for lemma_word in word_lists_no_emotion_stop['lemmatized_list']:
            if lemma_word in order_corpora:
                is_in_order+=1
                lemma_list_of_order.append(lemma_word)


    # Calculate Frequency Dist
    pre_natural_order_fdist = dict(FreqDist(pos_tag(natural_list_of_order)))
    pre_stemmer_order_fdist = dict(FreqDist(pos_tag(stemmer_list_of_order)))
    pre_lemma_order_fdist = dict(FreqDist(pos_tag(lemma_list_of_order)))
    natural_order_fdist = sorted(pre_natural_order_fdist.items(), key=lambda x: (x[1],x[0]))
    stemmer_order_fdist = sorted(pre_stemmer_order_fdist.items(), key=lambda x: (x[1],x[0]))
    lemma_order_fdist = sorted(pre_lemma_order_fdist.items(), key=lambda x: (x[1],x[0]))

    # Calculate Normalized Order
    normalized_order = 0
    try:
        normalized_order = float(is_in_order)/order_corpora_length * 100
    except Exception as e:
        pass

    processed_order['order_length'] = order_corpora_length
    processed_order['natural_list_of_order'] = natural_list_of_order
    processed_order['stemmer_list_of_order'] = stemmer_list_of_order
    processed_order['lemma_list_of_order'] = lemma_list_of_order
    processed_order['is_in_order'] = is_in_order
    processed_order['natural_order_fdist'] = natural_order_fdist
    processed_order['stemmer_order_fdist'] = stemmer_order_fdist
    processed_order['lemma_order_fdist'] = lemma_order_fdist
    processed_order['normalized_order'] = normalized_order

    return processed_order

def process_emotion(doc, lang, emotion, natural, stemmer, lemma, emotion_stop_words):

    print emotion

    flags = {}
    flags['naturalFlag'] = natural
    flags['stemmerFlag'] = stemmer
    flags['lemmaFlag'] = lemma

    valid_orders = ['order-1', 'order-2', 'order-3', 'order_1_and_2', 'order_1_and_3', 'order_2_and_3', 'all_orders']

    processed_doc_metadata = {
        "status": "success",
        "emotion": emotion,
    }

    # Stop Words
    stop_words = stopwords.words(lang)

    '''
    Remove emotion stop words and then return the words lists
    '''
    # TODO: There is a more efficient way to do this
    pre_list_of_words = [i.lower() for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]
    pre_stemmed_list = []
    pre_lemmatized_list = []

    # TODO: Handle language that isn't supported by stemmer!
    stemmer = SnowballStemmer(lang) # This is the stemmer
    lemma = WordNetLemmatizer() # This is the lemma
    for word in pre_list_of_words:
        pre_stemmed_list.append(lemma.lemmatize(word))
        pre_lemmatized_list.append(stemmer.stem(word))

    # Create a dictionary of the three lists without emotion based stop words
    word_lists_no_emotion_stop = {
        'list_of_words': [i for i in pre_list_of_words if i not in emotion_stop_words],
        'stemmed_list': [],
        'lemmatized_list': [],
    }
    # Remove emotion_stop_words only for these if the flag is set to true
    if flags['stemmerFlag'] == '1':
        word_lists_no_emotion_stop['stemmed_list'] = [i for i in pre_stemmed_list if i not in emotion_stop_words]
    if flags['lemmaFlag'] == '1':
        word_lists_no_emotion_stop['lemmatized_list'] = [i for i in pre_lemmatized_list if i not in emotion_stop_words]

    for order in valid_orders:
        order_result = process_order(doc, lang, emotion, flags, emotion_stop_words, word_lists_no_emotion_stop, order)
        if order_result['status'] == 'success':
            processed_doc_metadata[order] = order_result

    # TODO: This needs to be moved
    list_of_words_no_stop = [i for i in wordpunct_tokenize(doc) if i.lower()]
    length_words_no_stop = len(list_of_words_no_stop)

    # Find some scores for each order
    is_in_order_1 = processed_doc_metadata['order-1']['is_in_order']
    is_in_order_2 = processed_doc_metadata['order-2']['is_in_order']
    is_in_order_3 = processed_doc_metadata['order-3']['is_in_order']
    normalized_order_1 = processed_doc_metadata['order-1']['normalized_order']
    normalized_order_2 = processed_doc_metadata['order-2']['normalized_order']
    normalized_order_3 = processed_doc_metadata['order-3']['normalized_order']

    r_affect_score = calculate_r_score(is_in_order_1, is_in_order_2, is_in_order_3)
    normalized_r_score = calculate_normalized_r_score(normalized_order_1, normalized_order_2, normalized_order_3)
    r_affect_density_score = calculate_r_density_score(r_affect_score, length_words_no_stop)

    processed_doc_metadata['r_affect_score'] = r_affect_score
    processed_doc_metadata['normalized_r_score'] = normalized_r_score
    processed_doc_metadata['r_affect_density_score'] = r_affect_density_score
    processed_doc_metadata['length_words_no_stop'] = length_words_no_stop

    # print process_doc_metadata
    return processed_doc_metadata

# TODO: Error Handling needed!
def process_emotion_set(doc, lang, emotion_set, natural, stemmer, lemma, emotion_stop_words):

    processed_doc_list_metadata = []

    e_set = None
    # pick emotion_set
    if emotion_set == 'emotion_ml':
        e_set = emotionml_inspired
    elif emotion_set == 'all_emotions':
        e_set = all_emotions
    elif emotion_set == 'big_6':
        e_set = big_6
    elif emotion_set == 'everday_categories':
        e_set = everday_categories
    elif emotion_set == 'occ_categories':
        e_set = occ_categories
    elif emotion_set == 'fsre_categories':
        e_set = fsre_categories
    elif emotion_set == 'frijda_categories':
        e_set = frijda_categories
    elif emotion_set == 'dimensions':
        e_set = dimensions
    else:
        e_set = []

    # TODO: Better error handling here would be nice!


    print '---Creating an affect list!---'
    for emotion in e_set:
        processed_doc_list_metadata.append(process_emotion(doc, lang, emotion, natural, stemmer, lemma, emotion_stop_words))
    print '---Finished---'

    return processed_doc_list_metadata
