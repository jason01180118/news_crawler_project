def findall(cur, index=0):
    cur.execute("select href from REPORTS ORDER BY href")
    hrefs = cur.fetchall()
    for href in hrefs:
        index += 1
        print(f"num:{index} report:{href}")
    return index
