import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.summarization.bm25 import get_bm25_weights
corpus = [
    ["black", "cat", "white", "cat"],
    ["cat", "outer", "space"],
    ["wag", "dog"]
]
result = get_bm25_weights(corpus)
tfidf = TfidfVectorizer(corpus,use_idf=True)
print(result)
print(tfidf.idf_)