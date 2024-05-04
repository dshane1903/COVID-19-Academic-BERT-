# Progress Tracker

Week 1

-   [x] (Tim) Fine tune model o (https://towardsdatascience.com/covid-19-bert-literature-search-engine-4d06cdac08bd)
-   [x] (Tim) Create embeddings dataset by preprocessing articles
-   [x] (Tim) Get basic model working in Javascript
-   [x] (Shane) Create prototype user interface (React.js, https://material-ui.com/)

Week 2

-   [x] (Shane) Make app able to process user questions
-   [x] (Shane) implement similarity mechanisms.
-   [x] (Tim) Multiple answers & confidence scores. (test to make sure it works with test cases)
-   [x] (Shane) 8bit Quantization
-   [x] (Shane) Start rolling questions

Week 3

-   [x] Could haves (summarization, Read this).

# Milestones (MoSCow):

### “Must have”

Training side

-   Fine tune model for covid research
-   Preprocess all research articles into embeddings dataset
-   Save model in format for javascript (savedmodel/tfjs)

Application side

-   Develop front end interface (Material Design)
-   Code to load model
-   Code to process user’s question using model
-   Some similarity algorithm (cosine similarity/KNN)
-   Static/Nodejs/Flask?
-   Feature: (Multiple answers with confidence scores)

### “Should have”

-   Rolling questions (Questions suggestions using Named Entity Recognition)
-   Use spacy to collect NERs… into a bad of NERs… then randomly generate questions by concat (Whats/Where/Hows/When/Who...)
-   Quantization ?
-   Test cases… to verify that our system works… make edge cases or idk

### “Could have”

-   Text Summarization (https://towardsdatascience.com/summarization-has-gotten-commoditized-thanks-to-bert-9bb73f2d6922)
-   Different flavours of BERT (Research selling points and have options to choose...DistilBERT..RoBERTa...TinyBERT...MobileBERT… we get it)
-   Visualize attention weights as matrix or distribution
-   Cosine Similarity to create ‘dissimilar questions’

### “Won’t have”

-   Custom Tokenizer
-   Chrome extension

## Meeting Notes:

(https://www.kaggle.com/theamrzaki/covid-19-bert-researchpapers-semantic-search?fbclid=IwAR2WS4FkkJVlv9unbyEN2xdNb45RvcALE-d46IGmMNMiOH85UxWd1MFGMOU#COVID-19-BERT-ResearchPapers-Semantic-Search)
(https://towardsdatascience.com/covid-19-bert-literature-search-engine-4d06cdac08bd)
(https://towardsdatascience.com/covid-19-bert-literature-search-engine-4d06cdac08bd)
(https://covid-19-apis.postman.com/?fbclid=IwAR3boRIKqRlubyk_hdM4W1KBgYz1F9K0IzWiIQ57N7yYVKCP4YptccesGfc)

Implement a similarity function using javascript

Shane's brainstorm

What we have:

-   TFJS
-   Quantization
-   Node.js / Static app thing

Ideas (Question Answering System, applied to website link):

-   Rolling Questions…
-   Answers
-   Multiple answers
-   Where did you find those answers
-   Confidence scores for those
-   Suggest questions (https://www.tensorflow.org/lite/models/bert_qa/overview)

Other things:

-   Visualize Attention weights
-   Custom tokenizer not that important
-   Different flavours, (option: finding out which BERT works best, menu)
-   Test cases (Link: covid-19.com) => Scrapes all sub-links and sub-texts from this website to train for Question Answering
-   Test with EM/F1
-   App (Node.js vs ) (https://www.npmjs.com/package/bert-tokenizer)

## Resources

Tensorflow.js Doc:
<https://js.tensorflow.org/api_node/1.3.1/#tf.node.TFSavedModel.predict>

Hugging Face Models Doc:
<https://huggingface.co/transformers/model_doc/distilbert.html#distilbertforquestionanswering>

Hugging Face Node.js Question Answering Example
<https://github.com/huggingface/node-question-answering/>

DYNAMIC QUANTIZATION ON BERT
https://pytorch.org/tutorials/intermediate/dynamic_quantization_bert_tutorial.html

node-question-answering.js.

BERT quantization using PyTorch.

Try Quantization using Tensorflow.js
https://itnext.io/shrink-your-tensorflow-js-web-model-size-with-weight-quantization-6ddb4fcb6d0d
