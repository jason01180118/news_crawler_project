import json
from nltk.corpus import wordnet as wn
import sqlite3

correct = 0
data_sum = 0
f = open('keyword.json')
datas = json.load(f)
f.close()
datas = {"e": ["Environmental"], "s": ["Social"], "g": ["Governance"]}
tags = ['e', 's', 'g']
conn = sqlite3.connect('D:\\nlp_project_data\\esgnews\\output_same_long.db')
cur = conn.cursor()
cur.execute(
    "select * from OUTPUTS")
sentences = cur.fetchall()
for sentence in sentences:
    sentence_weights = []
    for word in sentence[0].split(' '):
        word_weight = {"e": 0, "s": 0, "g": 0}
        if word != '':
            for tag in tags:
                weight = []
                for data in datas[tag]:
                    for test in data.split(' '):
                        if test != '':
                            word_datas = wn.synsets(word)
                            test_datas = wn.synsets(test)
                            if word_datas != [] and test_datas != []:
                                weight.append(max([0 if word_data.path_similarity(test_data) == None else word_data.path_similarity(
                                    test_data) for word_data in word_datas for test_data in test_datas]))
                weight.sort(reverse=True)
                word_weight[tag] = 0 if len(weight) == 0 else max(weight)
        sentence_weights.append(word_weight)
    avg_e = sum(0 if len(sentence_weights) == 0 else sentence_weight['e']
                for sentence_weight in sentence_weights)/len(sentence_weights)
    avg_s = sum(0 if len(sentence_weights) == 0 else sentence_weight['s']
                for sentence_weight in sentence_weights)/len(sentence_weights)
    avg_g = sum(0 if len(sentence_weights) == 0 else sentence_weight['g']
                for sentence_weight in sentence_weights)/len(sentence_weights)
    if avg_e >= avg_s and avg_e >= avg_g and sentence[1] == "1":
        correct += 1
    elif avg_s >= avg_e and avg_s >= avg_g and sentence[1] == "2":
        correct += 1
    elif avg_g >= avg_s and avg_g >= avg_e and sentence[1] == "3":
        correct += 1
    data_sum += 1
conn.commit()
conn.close()
print(correct/data_sum)
