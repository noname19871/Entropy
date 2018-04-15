from sklearn.model_selection import cross_val_score
from sklearn_deltatfidf import DeltaTfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib


import pandas as pd
import pymorphy2

def text_cleaner(text):
    # приводим весь текст к нижнему регистру
    text = text.lower()

    # оставляем только русские буквы и пробелы
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    cleaned_text = ''
    for char in text:
        if (char[0] in alphabet) or (char == ' '):
            cleaned_text += char

    morph = pymorphy2.MorphAnalyzer()

    # лемматизируем
    result = []
    for word in cleaned_text.split():
        result.append(morph.parse(word)[0].normal_form)
    return ' '.join(result)

def Bayes(in_data):
    word_weights = joblib.load('models/tweets/features-bayes.joblib.pkl')
    clf = joblib.load('models/tweets/classifier-bayes.joblib.pkl')

    tmp_data = []
    for sentence in in_data:
        new_sentence = text_cleaner(sentence)
        if new_sentence != '':
            tmp_data.append(text_cleaner(sentence))

    if len(tmp_data) == 0:
        return [[0, 0]]
    new_data = word_weights.transform(tmp_data)
    predicted = clf.predict_proba(new_data)
    return predicted

def linear(in_data):
    word_weights = joblib.load('models/tweets/features-linear.joblib.pkl')
    clf = joblib.load('models/tweets/classifier-linear.joblib.pkl')

    tmp_data = []
    for sentence in in_data:
        new_sentence = text_cleaner(sentence)
        if new_sentence != '':
            tmp_data.append(text_cleaner(sentence))

    if len(tmp_data) == 0:
        return [[1, 1]]
    new_data = word_weights.transform(tmp_data)
    predicted = clf.predict_proba(new_data)
    return predicted

def predict(msg):
    return(Bayes(msg)[0][1])


