from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sqlite3
from findall import findall
from record import record

conn = sqlite3.connect('D:\\nlp_project_data\\cnn\\mydb.db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS REPORTS ('title' TEXT PRIMARY KEY,'href' TEXT,'text' TEXT,'tag' TEXT,'innertag' TEXT,'keyword' TEXT,'ESGtag' TEXT,'ESGinnertag' TEXT,'ESGkeyword' TEXT)")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=Service(
    executable_path=ChromeDriverManager().install()), options=options)
tags = ['world', 'business', 'health',
        'entertainment', 'weather']
reports = []
for tag in tags:
    driver.get("https://edition.cnn.com/"+tag)
    elements = driver.find_elements(By.CLASS_NAME, "zn__containers")
    for element in elements:
        articles = element.find_elements(By.TAG_NAME, "a")
        for article in articles:
            title = article.text
            if title != '' and title != None:
                href = article.get_attribute('href')
                if href != None:
                    if 'https://edition.cnn.com/2022/' in href:
                        innertag = href.split('/')[6]
                        for word in href.split('/'):
                            if '-' in word:
                                keyword = word
                        cur.execute(
                            "Insert or ignore into REPORTS Values(?,?,?,?,?,?,?,?,?)", (title, href,  '', tag, innertag, keyword, '', '', ''))
cur.execute(
    "select * from REPORTS where text=''")
rows = cur.fetchall()
index = 0
for row in rows:
    driver.get(row[1])
    text = ''
    contents = driver.find_elements(By.CLASS_NAME, "paragraph")
    for content in contents:
        text += content.text+'\n'
    cur.execute(
        "UPDATE REPORTS set text=? where href=?", (text, row[1]))
    if text != '':
        index += 1
        print(f"num:{index} update:{row[1]}")
cur.execute("delete from REPORTS where text=''")
record(findall(cur), index)
driver.close()
conn.commit()
conn.close()
print('done')
