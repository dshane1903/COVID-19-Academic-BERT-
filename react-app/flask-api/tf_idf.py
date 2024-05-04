import math
from textblob import TextBlob as tb

class TF_IDF:
    def __init__(self):
        self.NUM_WORDS = 5

    def get_top_words(self, doc_list):
        # Turn into textblob
        bloblist = [tb(doc) for doc in doc_list]

        word_score_pairs = []
        for i, blob in enumerate(bloblist):
            try:
                # Compute tfidf scores and sort them in descending order
                scores = {word: self.tfidf(word, blob, bloblist) for word in blob.words}
                sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                # Concat top 5 words
                word_score_pairs = word_score_pairs + sorted_words[:self.NUM_WORDS]
            except:
                pass

        # Sort again
        sorted_word_score_pairs = sorted(
            word_score_pairs, key=lambda x: x[1], reverse=True)

        # Get individual lists
        word_list = list(map(lambda x: x[0], sorted_word_score_pairs))
        score_list = list(map(lambda x: x[1], sorted_word_score_pairs))
        
        return word_list, score_list


    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tfidf(self, word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)