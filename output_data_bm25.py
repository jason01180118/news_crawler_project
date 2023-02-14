import pandas as pd
from nltk.tokenize import sent_tokenize
from rank_bm25 import BM25Okapi
import json
import numpy as np

f = open('keyword3.json')
datas = json.load(f)
f.close()
tags = []
for values in datas.values():
    for key in values.keys():
        tags.append(key)

df = pd.read_csv('D:\\nlp_project_data\\output.csv', names=['text', 'tag'])

sentences = []
results = []

for text in df['text'].fillna("").tolist():
    if len(text.split()) >= 10:
        sentences.append(text.split())
        results.append(text)

sentence_score = np.zeros(
    (len(tags), len(sentences)))


bm = BM25Okapi(sentences)

num = 0
for key, values in datas.items():
    for key, value in values.items():
        tokenized_query = value
        print(key, value)
        # 計算 BM25 score (log)
        scores = bm.get_scores(tokenized_query)

        for count, score in enumerate(scores):
            if score > 0:
                sentence_score[num][count] = 1
        num += 1


data_text = pd.DataFrame(results, columns=['text'])
data_tags = pd.DataFrame(sentence_score.reshape(np.shape(sentence_score)[
                         1], np.shape(sentence_score)[0]), columns=tags)

data = pd.merge(data_text, data_tags, left_index=True, right_index=True)

#data.drop(data[(data == 0).astype(int).sum(axis=1) == 9].index, inplace=True)

data.to_csv('D:\\nlp_project_data\\output_result_multiple.csv',
            encoding='utf-8', index=False)
