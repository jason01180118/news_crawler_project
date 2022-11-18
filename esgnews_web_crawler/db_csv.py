import sqlite3
import csv

files = ['output', 'output_without_over', 'output_same_long',
         'output_same_long_lanc', 'output_same_long_port', 'output_same_long_snow']
for file in files:
    conn = sqlite3.connect('D:\\nlp_project_data\\esgnews\\'+file+'.db')
    cur = conn.cursor()
    cur.execute("select * from OUTPUTS")
    texts = cur.fetchall()
    with open('D:\\nlp_project_data\\esgnews\\'+file+'.csv', 'w', encoding='utf-8', newline='') as csvfile:
        for text in texts:
            writer = csv.writer(csvfile)
            writer.writerow([text[0], text[1]])
    conn.commit()
    conn.close()
print('done')
