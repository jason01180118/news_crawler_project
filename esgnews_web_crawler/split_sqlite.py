import sqlite3
from nltk.tokenize import sent_tokenize

tags = {'governance': 3, 'environment': 1, 'social': 2}
for tag in tags.keys():
    conn = sqlite3.connect('D:\\nlp_project_data\\esgnews\\mydb.db')
    cur = conn.cursor()
    cur.execute(
        "select text from REPORTS where ESGtag=?", [tag])
    texts = cur.fetchall()
    conn.close()
    for text in texts:
        conn = sqlite3.connect('D:\\nlp_project_data\\esgnews\\output.db')
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS OUTPUTS ('text' TEXT PRIMARY KEY,'ESGtag' TEXT)")
        sentences = sent_tokenize(str(text)[2:-3].strip().replace('\\n', ''))
        for sentence in sentences:
            if sentence != '':
                cur.execute(
                    "Insert or ignore into OUTPUTS Values(?,?)", (sentence, tags[tag]))
        conn.commit()
        conn.close()

print('done')
