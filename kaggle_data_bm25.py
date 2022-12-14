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

df = pd.read_csv('D:\\nlp_project_data\\ESG_daily_news.csv')

sentences = []
results = []

for text in df['text'].fillna("").tolist():
    for sentence in sent_tokenize(text):
        if(len(sentence.split())) > 10:
            sentences.append(sentence.split())
            results.append(sentence)

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
data_tags = pd.DataFrame(sentence_score.T, columns=tags)

data = pd.merge(data_text, data_tags, left_index=True, right_index=True)


data.to_csv('D:\\nlp_project_data\\ESG_daily_result_multiple.csv',
            encoding='utf-8', index=False)
