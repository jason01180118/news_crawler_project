from git import Repo
import os
import time

dirfile = os.path.abspath('')
repo = Repo(dirfile)

seconds = time.time()
local_time = time.ctime(seconds)
g = repo.git
g.add("--all")
g.commit(m=f'feat:{local_time} auto update')
g.push()
print("Successful push!")
