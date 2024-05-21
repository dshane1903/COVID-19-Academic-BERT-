from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import torch

# model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# model.save_pretrained('./my_saved_model_directory/')
# tokenizer.save_pretrained('./my_saved_model_directory/')

model = BertForQuestionAnswering.from_pretrained('./3_BERT_squad/')
tokenizer = BertTokenizer.from_pretrained('./3_BERT_squad/') 

question = "Bayesian Inference"
answer_text = """we consider extensions to previous models for patient level nosocomial infection in several ways provide a specification of the likelihoods for these new models specify new update steps required for stochastic integration and provide programs that implement these methods to obtain parameter estimates and model choice statistics previous susceptibleinfected models are extended to allow for a latent period between initial exposure to the pathogen and the patient becoming themselves infectious and the possibility of decolonization we allow for multiple facilities such as acute care hospitals or longterm care facilities and nursing homes and for multiple units or wards within a facility patient transfers between units and facilities are tracked and accounted for in the models so that direct importation of a colonized individual from one facility or unit to another might be inferred we allow for constant transmission rates rates that depend on the number of colonized individuals in a unit or facility or rates that depend on the proportion of colonized individuals statistical analysis is done in a bayesian framework using markov chain monte carlo methods to obtain a sample of parameter values from their joint posterior distribution cross validation deviance information criterion and widely applicable information criterion approaches to model choice fit very naturally into this framework and we have implemented all three we illustrate our methods by considering model selection issues and parameter estimation for data on methicilinresistant staphylococcus aureus surveillance tests over 1 year at a veterans administration hospital comprising seven wards || https://academic.oup.com/imammb/article-pdf/35/Supplement_1/i29/25802099/dqx010.pdf"""

input_ids = tokenizer.encode(question, answer_text) 

# BERT only needs the token IDs, but for the purpose of inspecting the 
# tokenizer's behavior, let's also get the token strings and display them.
tokens = tokenizer.convert_ids_to_tokens(input_ids)

# Search the input_ids for the first instance of the `[SEP]` token.
sep_index = input_ids.index(tokenizer.sep_token_id)

# The number of segment A tokens includes the [SEP] token istelf.
num_seg_a = sep_index + 1

# The remainder are segment B.
num_seg_b = len(input_ids) - num_seg_a

# Construct the list of 0s and 1s.
segment_ids = [0]*num_seg_a + [1]*num_seg_b

# There should be a segment_id for every input token.
assert len(segment_ids) == len(input_ids)

# Run our example through the model.
start_scores, end_scores = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                 token_type_ids=torch.tensor([segment_ids])) # The segment IDs to differentiate question from answer_text

# Find the tokens with the highest `start` and `end` scores.
answer_start = torch.argmax(start_scores)
answer_end = torch.argmax(end_scores) 

# Combine the tokens in the answer and print it out.
answer = ' '.join(tokens[answer_start:answer_end+1])

print('Answer: "' + answer + '"') 

# Pull the scores out of PyTorch Tensors and convert them to 1D numpy arrays.
s_scores = start_scores.detach().numpy().flatten()
e_scores = end_scores.detach().numpy().flatten()

# We'll use the tokens as the x-axis labels. In order to do that, they all need
# to be unique, so we'll add the token index to the end of each one.
token_labels = []
for (i, token) in enumerate(tokens):
    token_labels.append('{:} - {:>2}'.format(token, i))

import numpy as np
import pandas as pd 

df = pd.DataFrame({
    'tokens': token_labels,
    'start': s_scores,
    'end': e_scores,
})

sorted_df = df.sort_values(by=['start'], ascending=False)

top_sorted_df = sorted_df[1:20]

print(top_sorted_df.to_json(orient='records'))
