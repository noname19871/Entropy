from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import numpy
from random import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib


# Класс для хранения помеченных предложений
class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # проверяем что ключи не совпадают
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences


def train():
    model_filename = 'models/imdb/classifier.joblib.pkl'
    features_filename = 'models/imdb/word2vec.d2v'
    sources = {'datasets/imdb/test-neg.txt': 'TEST_NEG',
               'datasets/imdb/test-pos.txt': 'TEST_POS',
               'datasets/imdb/train-neg.txt': 'TRAIN_NEG',
               'datasets/imdb/train-pos.txt': 'TRAIN_POS' }
    sentences = LabeledLineSentence(sources)

    model = Doc2Vec(min_count=1, window=10, vector_size=100, sample=1e-4, negative=5, workers=8)
    model.build_vocab(sentences.to_array())
    model.epochs = 20
    model.train(sentences.sentences_perm(), total_examples=model.corpus_count, epochs=model.epochs)

    model.save(features_filename)

    train_arrays = numpy.zeros((25000, 100))
    train_labels = numpy.zeros(25000)
    for i in range(12500):
        prefix_train_pos = 'TRAIN_POS_' + str(i)
        prefix_train_neg = 'TRAIN_NEG_' + str(i)
        train_arrays[i] = model[prefix_train_pos]
        train_arrays[12500 + i] = model[prefix_train_neg]
        train_labels[i] = 1
        train_labels[12500 + i] = 0

    classifier = LogisticRegression()
    classifier.fit(train_arrays, train_labels)
    joblib.dump(classifier, model_filename, compress=3)


train()
model = Doc2Vec.load('models/imdb/word2vec.d2v')
classifier = joblib.load('models/imdb/classifier.joblib.pkl')

test_arrays = numpy.zeros((25000, 100))
test_labels = numpy.zeros(25000)
for i in range(12500):
    prefix_test_pos = 'TEST_POS_' + str(i)
    prefix_test_neg = 'TEST_NEG_' + str(i)
    test_arrays[i] = model[prefix_test_pos]
    test_arrays[12500 + i] = model[prefix_test_neg]
    test_labels[i] = 1
    test_labels[12500 + i] = 0

for i in range(25000):
    print(classifier.predict(test_arrays[i].reshape(1, -1)))
