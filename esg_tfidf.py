import sqlite3
import json
from sklearn.feature_extraction.text import TfidfVectorizer

f = open('keyword2.json')
datas = json.load(f)
f.close()
results = []

conn = sqlite3.connect('D:\\nlp_project_data\\output_tfidf.db')
cur = conn.cursor()
cur.execute("update OUTPUTS SET ESGtag=?", [0])
cur.execute(
    "select * from OUTPUTS")
sentences = cur.fetchall()
#--- tokenize
tv = TfidfVectorizer(use_idf=True, smooth_idf=True, norm=None)
tokenized_corpus = []
for index, sentense in enumerate(sentences):
    for key, value in datas.items():
        tokenized_corpus.append(sentense[0]
                                for val in value if val in sentense[0])

#tokenized_corpus = [sentense[0] for sentense in sentences]

#--- initiate
tv_fit = tv.fit_transform(tokenized_corpus)
weight = tv_fit.toarray()
print(weight.shape)

#tag = {"e": 1, "s": 2, "g": 4}
#
# for key, value in datas.items():
#    # query --> 要查詢的 字詞
#    tokenized_query = value
#
#    # 計算 BM25 score (log)
#    scores = bm.get_scores(tokenized_query)
#    idx = scores.argmax()
#    for count, score in enumerate(scores):
#        if score > 0:
#            cur.execute("select ESGtag from OUTPUTS where text=?",
#                        [sentences[count][0]])
#            esgtag = cur.fetchone()
#            cur.execute("update OUTPUTS SET ESGtag=? where text=?",
#                        (esgtag[0]+tag[key], sentences[count][0]))
#
# cur.execute(
#    "select ESGtag from OUTPUTS")
#sentences = cur.fetchall()
#result = []
# for sentence in sentences:
#    result.append(sentence[0])
# print(result.count(0))
# print(result.count(1))
# print(result.count(2))
# print(result.count(3))
# print(result.count(4))
# print(result.count(5))
# print(result.count(6))
conn.commit()
conn.close()
