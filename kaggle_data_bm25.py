import pandas as pd
from nltk.tokenize import sent_tokenize
from rank_bm25 import BM25Okapi
import json
import csv

f = open('keyword2.json')
datas = json.load(f)
f.close()
tag = {"e": 1, "s": 2, "g": 4}

df = pd.read_csv('D:\\nlp_project_data\\ESG_daily_news.csv')

sentences = []
results = []

for text in df['text'].fillna("").tolist():
    for sentence in sent_tokenize(text):
        sentences.append(sentence.split())
        results.append(sentence)

sentence_score = [0]*len(sentences)

bm = BM25Okapi(sentences)

for key, value in datas.items():
    # query --> 要查詢的 字詞
    tokenized_query = value

    # 計算 BM25 score (log)
    scores = bm.get_scores(tokenized_query)

    for count, score in enumerate(scores):
        if score > 2:
            sentence_score[count] += tag[key]

print(sentence_score)
print(sentence_score.count(0))
print(sentence_score.count(1))
print(sentence_score.count(2))
print(sentence_score.count(3))
print(sentence_score.count(4))
print(sentence_score.count(5))
print(sentence_score.count(6))

with open("D:\\nlp_project_data\\ESG_daily_result.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for index, result in enumerate(results):
        writer.writerow([result, sentence_score[index]])
