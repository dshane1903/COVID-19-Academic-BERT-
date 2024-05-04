# Implements Text Similarity using word2vec, Smooth Inverse Frequency (SIF) and
# Cosine Similarity

# References:
# https://medium.com/@Intellica.AI/comparison-of-different-word-embeddings-on-text-similarity-a-use-case-in-nlp-e83e08469c1c
# https://medium.com/@adriensieg/text-similarities-da019229c894
# https://radimrehurek.com/gensim/models/word2vec.html
# https://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/


# Installation
# 1) Libraries
# pip install gensim
# pip install nltk
# 2) Run this script and click download all NLTK files, except for models.
# import nltk
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download()
# 3) Download word2vec pretrained model here and store in ./models/
# https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit


import string
import itertools
from collections import Counter

import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
from gensim.models import Word2Vec, KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarity:
    def __init__(self):
        """Fetching the model takes a few seconds..."""
        self.word_emb_model = KeyedVectors.load_word2vec_format(
            './model/GoogleNews-vectors-negative300.bin', binary=True)

    def get_text_similarity(self, sentence1, sentence2):
        """
        Process 2 sentences, compute their feature vectors, and returns the
        cosine similarity.
        """
        processed_sentence1 = self.pre_process(sentence1)
        processed_sentence2 = self.pre_process(sentence2)

        # Feature vectors is a list of size 2
        feature_vectors = self.get_sif_feature_vectors(
            processed_sentence1, processed_sentence2)

        return self.get_cosine_similarity(
            feature_vectors[0], feature_vectors[1])

    def pre_process(self, corpus):
        # Lower case
        corpus = corpus.lower()
        # Remove stop words
        stopset = stopwords.words('english') + list(string.punctuation)
        corpus = " ".join(
            [i for i in word_tokenize(corpus) if i not in stopset])
        # Remove non-ascii characters
        corpus = unidecode(corpus)
        return corpus

    def map_word_frequency(self, document):
        """Count word frequency"""
        return Counter(itertools.chain(*document))

    def get_sif_feature_vectors(self, sentence1, sentence2):
        """Computes Smooth Inverse Frequency (SIF) between 2 sentences."""
        sentence1 = [token for token in sentence1.split()
                     if token in self.word_emb_model.vocab]
        sentence2 = [token for token in sentence2.split()
                     if token in self.word_emb_model.vocab]

        word_counts = self.map_word_frequency((sentence1 + sentence2))
        embedding_size = 300
        a = 0.001
        sentence_set = []
        for sentence in [sentence1, sentence2]:
            vs = np.zeros(embedding_size)
            sentence_length = len(sentence)
            for word in sentence:
                a_value = a / (a + word_counts[word])
                # vs += sif * word_vector
                vs = np.add(vs, np.multiply(a_value,
                                            self.word_emb_model.wv[word]))
            # weighted average
            vs = np.divide(vs, sentence_length)
            sentence_set.append(vs)
        return sentence_set

    def get_cosine_similarity(self, feature_vec_1, feature_vec_2):
        """Computes cosine similarity between 2 vectors"""
        return cosine_similarity(
            feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]
