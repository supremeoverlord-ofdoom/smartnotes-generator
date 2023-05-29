import re
import pandas as pd
import numpy as np
# Library to import pre-trained model for sentence embeddings
from sentence_transformers import SentenceTransformer
# Calculate similarities between sentences
from sklearn.metrics.pairwise import cosine_similarity
from scipy.signal import argrelextrema
import math


class SubtitleProcessor:
    def read_text_from_file(self, file_path):
        with open(file_path, 'r') as file:
            prompt_text = file.read()
        return prompt_text
    
    def remove_webvtt(self, text):
    # Define the pattern to match the lines to be removed
        pattern = r"(WEBVTT|Kind: captions|Language: en-US)"

        # Use regular expressions to remove the matched lines
        modified_text = re.sub(pattern, "", text)
        # print(modified_text)
        return modified_text
    
    def clean_subtitles(self, subtitle_text):
        # Remove timestamps and '&nbsp;' instances
        subtitle_text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n|&nbsp;', '', subtitle_text)
        
        # Split text into sentences
        sentences = subtitle_text.split('. ')
        
        # Format sentences into bullet points
        clean_text = ''
        for sentence in sentences:
            if sentence.strip() != '':
                clean_text += '' + sentence.strip() + '.\n'
        
        return clean_text
    
    def join_subtitles(self, text):
        lines = text.split("\n")
        # lines = (line.strip() for line in text)
        joined_lines = []

        for line in lines:
                joined_lines.append(line)

        joined_text = " ".join(joined_lines)
        return joined_text
    
    
    def save_temp_file(self, joined_text):
        #intermediate step not ideal but prep_text_string() only works if it's read in through one long string
        temp_file = 'temp/temp_string_text.txt'
        with open(temp_file, "w") as notes_file:
            notes_file.write(joined_text)
        return temp_file
    
    def prep_text_string(self, temp_file):
        with open(temp_file) as f:
            doc = f.readlines()
            f.close()
        doc = doc[0].replace("?", ".")
        sentences = doc.split('. ')
        return sentences
    
    def unify_sentence_length(self, sentence_text):
        # length of each sentence
        sentence_length = [len(each) for each in sentence_text]
        # find longest outlier
        long = np.mean(sentence_length) + np.std(sentence_length) *2
        # find shortest outlier
        short = np.mean(sentence_length) - np.std(sentence_length) *2
        # Shorten the long sentences
        text = ''
        for each in sentence_text:
            if len(each) > long:
                # replace all the commas with dots
                comma_splitted = each.replace(',', '.')
            else:
                text+= f'{each}. '
        sentence_text = text.split('. ')
        # concatenate short ones
        text = ''
        for each in sentence_text:
            if len(each) < short:
                text+= f'{each} '
            else:
                text+= f'{each}. '
        return text
    def embed_sentences(self, text):
        # Split text into sentences
        uniform_sentences = text.split('. ')
        # Embed the sentences
        model = SentenceTransformer.load('model/')
        embeddings = model.encode(uniform_sentences)
        
        return embeddings, uniform_sentences
    
    def similarities_matrix(self, embeddings):
        # make similarities matrix
        similarities = cosine_similarity(embeddings)
        return similarities
    
    # find splitting points
    def rev_sigmoid(self, x:float)->float:
        return (1 / (1 + math.exp(0.5*x)))
    
    # I'm not a data scientist and math is scary, so using this function, the source code can be found: https://github.com/poloniki/quint
    def activate_similarities(self, similarities:np.array, p_size=10)->np.array:
            """ Function returns list of weighted sums of activated sentence similarities
            Args:
                similarities (numpy array): it should square matrix where each sentence corresponds to another with cosine similarity
                p_size (int): number of sentences are used to calculate weighted sum 
            Returns:
                list: list of weighted sums
            """
            # To create weights for sigmoid function we first have to create space. P_size will determine number of sentences used and the size of weights vector.
            x = np.linspace(-10,10,p_size)
            # Then we need to apply activation function to the created space
            y = np.vectorize(self.rev_sigmoid) 
            # Because we only apply activation to p_size number of sentences we have to add zeros to neglect the effect of every additional sentence and to match the length ofvector we will multiply
            activation_weights = np.pad(y(x),(0,similarities.shape[0]-p_size))
            ### 1. Take each diagonal to the right of the main diagonal
            diagonals = [similarities.diagonal(each) for each in range(0,similarities.shape[0])]
            ### 2. Pad each diagonal by zeros at the end. Because each diagonal is different length we should pad it with zeros at the end
            diagonals = [np.pad(each, (0,similarities.shape[0]-len(each))) for each in diagonals]
            ### 3. Stack those diagonals into new matrix
            diagonals = np.stack(diagonals)
            ### 4. Apply activation weights to each row. Multiply similarities with our activation.
            diagonals = diagonals * activation_weights.reshape(-1,1)
            ### 5. Calculate the weighted sum of activated similarities
            activated_similarities = np.sum(diagonals, axis=0)
            return activated_similarities
        
    def relative_minima(self, activated_similarities):
        minmimas = argrelextrema(activated_similarities, np.less, order=2) #order controls how frequent should be splits, don't change
        return minmimas
    
    def split_text_to_paragraph(self, minmimas, uniform_sentences):
        split_points = [each for each in minmimas[0]]
        text = ''
        for num,each in enumerate(uniform_sentences):
            if num in split_points:
                text+=f'\n\n {each}. '
            else:
                text+=f'{each}. '
        # print(text)
        return text
        
    def process_subtitles(self, input_file_path, output_file_path):
        raw_text = self.read_text_from_file(input_file_path)
        modified_text = self.remove_webvtt(raw_text)
        output_text = self.clean_subtitles(modified_text)
        joined_text = self.join_subtitles(output_text)
        temp_file = self.save_temp_file(joined_text)
        sentences = self.prep_text_string(temp_file)
        unified_sentences = self.unify_sentence_length(sentences)
        
        embeddings, uniform_sentences = self.embed_sentences(unified_sentences)
        activated_similarities = self.activate_similarities(embeddings)
        minima_indices = self.relative_minima(activated_similarities)
        paragraph_text = self.split_text_to_paragraph(minima_indices, uniform_sentences)
        
        with open(output_file_path, "w") as notes_file:
            notes_file.write(paragraph_text)