import time


def record(index, update):
    seconds = time.time()
    local_time = time.ctime(seconds)
    path = 'record.txt'
    f = open(path, 'a', encoding='utf-8')
    f.write(f"目前累計{index}筆資料 本次更新{update}筆資料 紀錄時間:{local_time}\n")
    f.close()
