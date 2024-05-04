import time
import random
from flask import Flask
from flask import jsonify
from sentence_embeddings import SentenceEmbeddings
from pos_tagging import POS_Tagging
from tf_idf import TF_IDF

sentence_embeddings = SentenceEmbeddings()
pos_tagging = POS_Tagging()
tfidf = TF_IDF()

def create_app():
    app = Flask(__name__)

    @app.route('/query/<question>')
    def query(question):
        # Generate search results using sentence embeddings
        answer = sentence_embeddings.query(question)

        # print(answer)

        # Generate context using answer.
        context = []
        for doc in answer['abstract']:
            context.append(doc)
        
        # Generate suggestions based on context using POS tagging
        POS_tagging_set = set()
        for doc in context:
            try:
                question_list = pos_tagging.parse(doc)
            except:
                pass

            # Append non-empty questions
            for question in question_list:
                if len(question) > 1:
                    # Adding to a set() ensures questions are unique
                    POS_tagging_set.add(question)
        suggestions = list(POS_tagging_set)
        
        # Generate keywords based on context using TDIDF
        keywords, scores = tfidf.get_top_words(context)

        output = {
            'answer': answer,
            'suggestions': suggestions,
            'keywords': keywords,
            'scores': scores
        }

        return jsonify(output)

    return app
