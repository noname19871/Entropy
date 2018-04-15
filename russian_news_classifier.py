# coding: utf-8

from nltk import word_tokenize
import numpy as np
import clear_text
import logging
import re
import json
import gensim
import nltk
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



def token_sentences(split_text):
    diction = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    trash = ['»','«','!','@','#','№','$',';','%','^',':','&','?','*','(',')','-','_','=','+','}','{','[',']','*','/','0','1','2','3','4','5','6','7','8','9',',']
    split_text = clear_text.replace(split_text, trash).lower()
    string = ''
    for char in split_text:
        if char in diction or char == ' ':
            string += char
    split_text = string
    return split_text


nltk.download('punkt')
def ru_token(string):
    """russian tokenize based on nltk.word_tokenize. only russian letter remaind."""
    return [i.lower() for i in word_tokenize(string) if re.match(r'[\u0400-\u04ffа́]+$', i)]




def getAvgFeatureVecs(reviews, model, num_features):
    counter = 0
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    for review in reviews:
        # Printing a status message every 1000th review
        if counter%10 == 0:
            print("Review %d of %d"%(counter,len(reviews)))
            
        reviewFeatureVecs[counter] = featureVecMethod(review, model, num_features)
        counter = counter+1
        
    return reviewFeatureVecs


# Function to average all word vectors in a paragraph
def featureVecMethod(words, model, num_features):
    # Pre-initialising empty numpy array for speed
    featureVec = np.zeros(num_features,dtype="float32")
    nwords = 0
    
    # Converting Index2Word which is a list to a set for better speed in the execution.
    index2word_set = set(model.wv.index2word)
    
    for word in  words:
        if word in index2word_set:
            nwords = nwords + 1
            featureVec = np.add(featureVec,model[word])
    
    # Dividing the result by number of words to get average
    featureVec = np.divide(featureVec, nwords)
    return featureVec


def train():
    with open('datasets/news/train.json', encoding="utf8") as f:
        raw_train = json.load(f)
    with open('datasets/news/test.json', encoding="utf8") as f:
        raw_test = json.load(f)

    raw_train[0:int(len(raw_train)/100)]

    data_train_segments = {'id': [], 'text': [], 'sentiment': []}
    data_train_sentences = {'id': [], 'text': [], 'sentiment': []}
    for index, sentences in enumerate(raw_train):
        data_train_segments['id'].append(sentences['id'])
        data_train_segments['text'].append(ru_token(sentences['text']))
        data_train_segments['sentiment'].append(sentences['sentiment'])
        data_train_sentences['id'].append(sentences['id'])
        data_train_sentences['text'].append(token_sentences(sentences['text']))
        data_train_sentences['sentiment'].append(sentences['sentiment'])

    model = gensim.models.FastText(data_train_segments['text'], size=200, window=10, min_count=5, workers=4, sg=1)

    train_array = getAvgFeatureVecs(data_train_segments['text'], model, 200)
    train_labels = []
    for i in range(len(data_train_segments['text'])):
        train_labels.append(data_train_segments['sentiment'][i])

    classifier = LogisticRegression()
    classifier.fit(train_array, train_labels)

    model.save('models/news/model.model')
    joblib.dump(classifier, 'models/news/classifier.joblib.pkl', compress=3)



def predict(str_array):
    model = gensim.models.FastText.load('models/news/model.model')
    classifier = joblib.load('models/news/classifier.joblib.pkl')

    avg = []
    for i in range(len(str_array)):
        str_array[i] = ru_token(str_array[i])
        tmp = getAvgFeatureVecs([str_array[i]],model,200)
        avg.append(classifier.predict_proba(tmp)[0])

    return avg


print(predict(["плохой день, но лучший на этой недел", "Отличный день"]))
