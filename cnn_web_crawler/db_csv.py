import sqlite3
import csv

files = ['output']
for file in files:
    conn = sqlite3.connect('D:\\nlp_project_data\\cnn\\'+file+'.db')
    cur = conn.cursor()
    cur.execute("select * from OUTPUTS")
    texts = cur.fetchall()
    with open('D:\\nlp_project_data\\cnn\\'+file+'.csv', 'w', encoding='utf-8', newline='') as csvfile:
        for text in texts:
            writer = csv.writer(csvfile)
            writer.writerow([text[0], text[1]])
    conn.commit()
    conn.close()
print('done')
