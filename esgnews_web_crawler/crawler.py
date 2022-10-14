from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import sqlite3
import re
from findall import findall
from record import record

conn = sqlite3.connect('./mydb.db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS REPORTS ('title' TEXT,'href' TEXT PRIMARY KEY,'text' TEXT,'ESGtag' TEXT,'othertag' TEXT,'time' TEXT)")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=Service(
    executable_path=ChromeDriverManager().install()), options=options)
tags = ['governance', 'environment', 'social']
p = re.compile('[0-9]+')
for tag in tags:
    driver.get("https://esgnews.com/?s="+tag)
    pages = driver.find_element(
        By.CLASS_NAME, "page-numbers").find_elements(By.TAG_NAME, "a")
    max_page = 0
    for page in pages:
        if p.match(page.text):
            max_page = max(max_page, int(page.text))
    for i in range(1, max_page+1):
        print(f"page:{i}")
        index = 0
        driver.get("https://esgnews.com/page/"+str(i)+"/?s="+tag)
        articles = driver.find_elements(
            By.CLASS_NAME, "tt-post")
        for article in articles:
            href = article.find_element(
                By.CLASS_NAME, "tt-post-title").get_attribute('href')
            cur.execute("select * from REPORTS where href=?", [href])
            if cur.fetchone() == None:
                index += 1
                cur.execute(
                    "Insert or ignore into REPORTS Values(?,?,?,?,?,?)", ('',  href, '', tag, '', ''))
            print(href)
        if index == 0:
            break
    print(max_page)
cur.execute(
    "select * from REPORTS where title=''")
rows = cur.fetchall()
index = 0
for row in rows:
    driver.get(row[1])
    print(f"now{index}:{row[1]}")
    try:
        title = driver.find_element(
            By.CLASS_NAME, "c-h1").text
    except NoSuchElementException:
        title = 'invalid'
    article = ''
    try:
        sentences = driver.find_element(
            By.CLASS_NAME, "tt-content").find_elements(By.TAG_NAME, "p")
    except NoSuchElementException:
        title = 'invalid'
        sentences = None
    if sentences != None:
        for sentence in sentences:
            article += sentence.text+'\n'
    othertag = ''
    try:
        others = driver.find_element(
            By.CLASS_NAME, "tt-tags").find_elements(By.TAG_NAME, "a")
    except NoSuchElementException:
        others = None
    if others != None:
        for other in others:
            othertag += other.text+'\n'
    try:
        time = driver.find_element(By.CLASS_NAME, "tt-post-date-single").text
    except NoSuchElementException:
        time = ''
    cur.execute(
        "UPDATE REPORTS set title=?,text=?,othertag=?,time=? where href=?", (title, article, othertag, time, row[1]))
    index += 1
    conn.commit()
record(findall(cur), index)
driver.close()
conn.commit()
conn.close()
print('done')
