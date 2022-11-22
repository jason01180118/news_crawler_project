import sqlite3
from nltk.tokenize import sent_tokenize

conn = sqlite3.connect('D:\\nlp_project_data\\cnn\\mydb.db')
cur = conn.cursor()
cur.execute("select text from REPORTS")
texts = cur.fetchall()
conn.close()
conn = sqlite3.connect('D:\\nlp_project_data\\cnn\\output.db')
cur = conn.cursor()
for text in texts:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS OUTPUTS ('text' TEXT PRIMARY KEY,'ESGtag' INTEGER)")
    sentences = sent_tokenize(str(text)[2:-3].strip().replace('\\n', ''))
    for sentence in sentences:
        if sentence != '':
            cur.execute(
                "Insert or ignore into OUTPUTS Values(?,?)", (sentence, 0))
conn.commit()
conn.close()

print('done')
