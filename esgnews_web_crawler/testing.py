import sqlite3

length = []
conn = sqlite3.connect('D:\\nlp_project_data\\esgnews\\output.db')
cur = conn.cursor()
cur.execute("select * from OUTPUTS")
texts = cur.fetchall()
for text in texts:
    sentences = text[0].split(' ')
    length.append(len(sentences))
length.sort()
print(length[len(length)//10*2], length[len(length)//10*8])
conn.commit()
conn.close()
print('done')
