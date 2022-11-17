import sqlite3

length = []
conn = sqlite3.connect('D:\\nlp_project_data\\esgclarity\\output.db')
cur = conn.cursor()
cur.execute("select * from OUTPUTS")
texts = cur.fetchall()
conn.commit()
conn.close()
conn = sqlite3.connect(
    'D:\\nlp_project_data\\esgclarity\\output_without_over.db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS OUTPUTS ('text' TEXT PRIMARY KEY,'ESGtag' TEXT)")
for text in texts:
    sentences = text[0].split(' ')
    length.append(len(sentences))
length.sort()
print(length[len(length)//10*3], length[len(length)//10*9])
for text in texts:
    sentences = text[0].split(' ')
    if len(sentences) >= length[len(length)//10*3] and len(sentences) <= length[len(length)//10*9]:
        cur.execute("Insert or ignore into OUTPUTS Values(?,?)",
                    (text[0], text[1]))
conn.commit()
conn.close()
print('done')
