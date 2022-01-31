from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import nltk
import re
import os
import pickle
from nltk.corpus import stopwords
import math
from nltk.stem import PorterStemmer
from nltk import wordnet
from collections import Counter
import pandas as pd
import numpy as np
from vncorenlp import VnCoreNLP
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080","http://192.168.1.18:8080","https://qtpsearch.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/query/{query}")
def get_Query(query: str):
    
    # Load rdrsegmenter from VnCoreNLP
    rdrsegmenter = VnCoreNLP("VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')
    stopwords_file = r"vietnamese-stopwords.txt"
    stopwords = []
    with open(stopwords_file, encoding='utf-8', mode='r') as f:
        text = f.read()
        res = text.replace(" ", "_")
        stopwords = res.split("\n")

    # preprocess
    def preprocess_text(text):
        processed_text = text.lower()
        processed_text = processed_text.replace("’", " ")
        processed_text = processed_text.replace("'", " ")
        processed_text = processed_text.replace("“", '"')
        processed_text = processed_text.replace("”", '"')
        processed_text = processed_text.replace("&", 'và')
        non_words = re.compile(r"[\W\d]")
        processed_text = re.sub(non_words, ' ', processed_text)
        return processed_text

    def get_words_from_text(text):
        '''words tokenization'''

        processed_text = preprocess_text(text)
        processed_text = rdrsegmenter.tokenize(processed_text)
        processed_words = [word for word in processed_text[0] if word not in stopwords]
        return processed_words
    ##
    input_sav_file = r"term_idf.sav"
    input_csv_file = r"document-term_matrix_tfidf_normalized.csv"
    links = pd.read_csv("Links.csv",header=None)
    titles = list(links[1])
    links = list(links[0])

    file = open(input_sav_file, 'rb')
    terms_idf = pickle.load(file)
    document_term_matrix = pd.read_csv(input_csv_file, index_col=0)
    query_term_frequency_dict = dict(Counter(get_words_from_text(query)))

    query_vector_dict = {}

    for i in list(query_term_frequency_dict.keys()):
        if i in list(terms_idf.keys()):
            query_vector_dict[i] = query_term_frequency_dict[i] * terms_idf[i]

    l = np.linalg.norm(list(query_vector_dict.values()))

    for i in list(query_vector_dict.keys()):
        query_vector_dict[i] = query_vector_dict[i] / l

    ## print results
    temp = document_term_matrix.to_dict(orient='index')
    res = []

    for i in list(temp.keys()):
        keys = set(list(query_vector_dict.keys())).intersection(list(temp[i].keys()))
        dot_product = sum(query_vector_dict[k] * temp[i][k] for k in keys)
        if dot_product != 0:
            res.append((i, dot_product))

    res = sorted(res, key=lambda tup: tup[1], reverse=True)
    final = []
    for i in res[]:
        if i[0]<861: 
            t = 1
        elif i[0] > 1310:
            t = 3
        else:
            t = 2
        final.append({'id':i[0],'link':links[i[0]-1],'title': titles[i[0]-1],'type': t,'cosi':round(i[1],6)})

    return final