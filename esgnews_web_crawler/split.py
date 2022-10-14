import sqlite3
import csv
from nltk.tokenize import sent_tokenize

conn = sqlite3.connect('./mydb.db')
cur = conn.cursor()
tags = {'governance': 3, 'environment': 1, 'social': 2}
for tag in tags.keys():
    cur.execute(
        "select text from REPORTS where ESGtag=?", [tag])
    texts = cur.fetchall()
    for text in texts:
        sentences = sent_tokenize(str(text)[2:-3].strip().replace('\\n', ''))
        with open('output.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for sentence in sentences:
                if sentence != '':
                    writer.writerow([sentence, tags[tag]])

conn.commit()
conn.close()
print('done')
