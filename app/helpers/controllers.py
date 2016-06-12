from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

def default():
    print 'Here'
    return 'Thanks controller, hello helpers!'

def length_no_stop(doc, lang):

    stop_words = set(stopwords.words(lang))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation

    list_of_words = [i for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]

    return len(list_of_words)
