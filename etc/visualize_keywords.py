from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import torch
import pandas as pd

class VisualizeKeywords:
    def __init__(self):
        self.model = BertForQuestionAnswering.from_pretrained(
            './model/3_BERT_squad/')
        self.tokenizer = BertTokenizer.from_pretrained(
            './model/3_BERT_squad/')
        self.NUM_TOKENS = 25

    def get_scores(self, question, answer_text):
        input_ids = self.tokenizer.encode(question, answer_text)
        # Get the token strings
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        # Search the input_ids for the first instance of the `[SEP]` token.
        sep_index = input_ids.index(self.tokenizer.sep_token_id)
        # The number of segment A tokens includes the [SEP] token istelf.
        num_seg_a = sep_index + 1
        # The remainder are segment B.
        num_seg_b = len(input_ids) - num_seg_a
        # Construct the list of 0s and 1s.
        segment_ids = [0]*num_seg_a + [1]*num_seg_b
        # There should be a segment_id for every input token.
        assert len(segment_ids) == len(input_ids)

        # Run our example through the model.
        start_scores, end_scores = self.model(
            # The tokens representing our input text.
            torch.tensor([input_ids]),
            # The segment IDs to differentiate question from answer_text
            token_type_ids=torch.tensor([segment_ids])) 

        # Find the tokens with the highest `start` and `end` scores.
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)

        # Combine the tokens in the answer and print it out.
        answer = ' '.join(tokens[answer_start:answer_end+1])

        # Pull the scores out of PyTorch Tensors and convert them to 1D numpy arrays.
        s_scores = start_scores.detach().numpy().flatten()
        e_scores = end_scores.detach().numpy().flatten()

        token_labels = []
        for (i, token) in enumerate(tokens):
            token_labels.append('{:} - {:>2}'.format(token, i))        

        df = pd.DataFrame({
            'tokens': token_labels,
            'start': s_scores,
        })

        # Sort by starting tokens
        df = df.sort_values(by=['start'], ascending=False)

        # Get top 25 tokens
        df = df[:self.NUM_TOKENS]

        return {'keywords': df['tokens'].tolist(), 
                'scores': df['start'].tolist()}