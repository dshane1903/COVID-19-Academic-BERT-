# Installation Instructions:
# pip install nltk
# pip install textblob
# python -m textblob.download_corpora

import sys
from textblob import TextBlob
from textblob import Word
import nltk


class POS_Tagging:
    def __init__(self):
        self.BoW = {}

    def parse(self, answer):
        text = TextBlob(answer)

        question_list = []

        # Generate questions based on sentences
        for sentence in text.sentences:
            question_list.append(self.generate_question(sentence))
        
        return question_list

    def generate_question(self, line):
        if isinstance(line, str):
            line = TextBlob(line)

        POS = {}

        for i, j in enumerate(line.tags):
            if j[1] not in POS:
                POS[j[1]] = i

        question = ""

        # .....................................................................
        # NNS     Noun, plural
        # JJ  Adjective
        # NNP     Proper noun, singular
        # VBG     Verb, gerund or present participle
        # VBN     Verb, past participle
        # VBZ     Verb, 3rd person singular present
        # VBD     Verb, past tense
        # IN      Preposition or subordinating conjunction
        # PRP     Personal pronoun
        # NN  Noun, singular or mass
        # .....................................................................
        
        # Create a list of tag-combination
        l1 = ['NNP', 'VBG', 'VBZ', 'IN']
        l2 = ['NNP', 'VBG', 'VBZ']

        l3 = ['PRP', 'VBG', 'VBZ', 'IN']
        l4 = ['PRP', 'VBG', 'VBZ']
        l5 = ['PRP', 'VBG', 'VBD']
        l6 = ['NNP', 'VBG', 'VBD']
        l7 = ['NN', 'VBG', 'VBZ']

        l8 = ['NNP', 'VBZ', 'JJ']
        l9 = ['NNP', 'VBZ', 'NN']

        l10 = ['NNP', 'VBZ']
        l11 = ['PRP', 'VBZ']
        l13 = ['NN', 'VBZ']



        # 'NNP', 'VBG', 'VBZ', 'IN'
        if all(key in POS for key in l1):
            question = 'What' + ' ' + line.words[POS['VBZ']] + ' ' + \
                line.words[POS['NNP']] + ' ' + line.words[POS['VBG']] + '?'

        # 'NNP', 'VBG', 'VBZ'
        elif all(key in POS for key in l2):
            question = 'What' + ' ' + line.words[POS['VBZ']] + ' ' + \
                line.words[POS['NNP']] + ' ' + line.words[POS['VBG']] + '?'

        # 'PRP', 'VBG', 'VBZ', 'IN'
        elif all(key in POS for key in l3):
            question = 'What' + ' ' + line.words[POS['VBZ']] + ' ' + \
                line.words[POS['PRP']] + ' ' + line.words[POS['VBG']] + '?'

        # 'PRP', 'VBG', 'VBZ'
        elif all(key in POS for key in l4):
            question = 'What ' + line.words[POS['PRP']] + ' ' + ' does ' + \
                line.words[POS['VBG']] + ' ' + line.words[POS['VBG']] + '?'

        # 'NN', 'VBG', 'VBZ'
        elif all(key in POS for key in l7):
            question = 'What' + ' ' + line.words[POS['VBZ']] + ' ' + \
                line.words[POS['NN']] + ' ' + line.words[POS['VBG']] + '?'

        # 'NNP', 'VBZ', 'JJ'
        elif all(key in POS for key in l8):
            question = 'What' + ' ' + \
                line.words[POS['VBZ']] + ' ' + line.words[POS['NNP']] + '?'

        # 'NNP', 'VBZ', 'NN'
        elif all(key in POS for key in l9):
            question = 'What' + ' ' + \
                line.words[POS['VBZ']] + ' ' + line.words[POS['NNP']] + '?'

        #'NNP', 'VBZ' in sentence.
        elif all(key in POS for key in l10): 
            question = 'What' + ' does ' + line.words[POS['NNP']] + ' ' + \
                        line.words[POS['VBZ']].singularize() + '?'

        #'PRP', 'VBZ' in sentence.
        elif all(key in POS for key in l11): 
            if line.words[POS['PRP']] in ['she','he']:
                question = 'What' + ' does ' + line.words[POS['PRP']].lower() \
                            + ' ' + line.words[POS['VBZ']].singularize() + '?'

        #'NN', 'VBZ' in sentence.
        elif all(key in POS for key in l13): 
            question = 'What' + ' ' + line.words[POS['VBZ']] + ' ' + \
                        line.words[POS['NN']] + '?'

        # When the tags are generated 's is split to ' and s. To overcome this
        # issue.
        if 'VBZ' in POS and line.words[POS['VBZ']] == "’":
            question = question.replace(" ’ ", "'s ")

        if question != '':
            return question

        return ''
