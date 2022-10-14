from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import sqlite3
from findall import findall
from record import record

conn = sqlite3.connect('./mydb.db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS REPORTS ('title' TEXT,'subtitle' TEXT,'href' TEXT PRIMARY KEY,'text' TEXT,'ESGtag' TEXT,'othertag' TEXT,'time' TEXT)")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=Service(
    executable_path=ChromeDriverManager().install()), options=options)
tags = ['governance', 'environment', 'social']
for tag in tags:
    driver.get("https://esgclarity.com/?s="+tag)
    pages = driver.find_element(
        By.CLASS_NAME, "nav-links").find_elements(By.TAG_NAME, "a")
    max_page = 0
    for page in pages:
        if page.text != '':
            max_page = max(max_page, int(page.text))
    for i in range(1, max_page+1):
        print(f"page:{i}")
        index = 0
        driver.get("https://esgclarity.com/page/"+str(i)+"/?s="+tag)
        articles = driver.find_element(
            By.CLASS_NAME, "article-section").find_elements(By.TAG_NAME, "a")
        for article in articles:
            href = article.get_attribute('href')
            cur.execute("select * from REPORTS where href=?", [href])
            if cur.fetchone() == None:
                index += 1
                cur.execute(
                    "Insert or ignore into REPORTS Values(?,?,?,?,?,?,?)", ('', '',  href, '', tag, '', ''))
            print(href)
        if index == 0:
            break
    print(max_page)
conn.commit()
cur.execute(
    "select * from REPORTS where title=''")
rows = cur.fetchall()
index = 0
for row in rows:
    driver.get(row[2])
    print(f"now:{row[2]}")
    try:
        title = driver.find_element(
            By.CLASS_NAME, "content-section").find_element(By.TAG_NAME, "h1").text
    except NoSuchElementException:
        title = 'invalid'
    try:
        subtitle = driver.find_element(
            By.CLASS_NAME, "content-section").find_element(By.TAG_NAME, "h3").text
    except NoSuchElementException:
        title = 'invalid'
        subtitle = 'invalid'
    article = ''
    try:
        sentences = driver.find_element(
            By.CLASS_NAME, "entry-content").find_elements(By.TAG_NAME, "p")
    except NoSuchElementException:
        title = 'invalid'
        sentences = None
    if sentences != None:
        for sentence in sentences:
            article += sentence.text+'\n'
    othertag = ''
    try:
        others = driver.find_element(
            By.CLASS_NAME, "tags-links").find_elements(By.TAG_NAME, "a")
    except NoSuchElementException:
        others = None
    if others != None:
        for other in others:
            othertag += other.text+'\n'
    try:
        time = driver.find_element(By.CLASS_NAME, "entry-date").text
    except NoSuchElementException:
        time = ''
    cur.execute(
        "UPDATE REPORTS set title=?,subtitle=?,text=?,othertag=?,time=? where href=?", (title, subtitle, article, othertag, time, row[2]))
    index += 1
    conn.commit()
record(findall(cur), index)
driver.close()
conn.close()
print('done')
