def findall(cur, index=0):
    cur.execute("select href from REPORTS where title!='invalid' ORDER BY time")
    hrefs = cur.fetchall()
    for href in hrefs:
        index += 1
        print(f"num:{index} report:{href}")
    return index
