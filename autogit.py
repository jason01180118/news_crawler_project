from git import Repo
import os

dirfile = os.path.abspath('')
repo = Repo(dirfile)

g = repo.git
g.add("--all")
g.commit(m='auto update')
g.push()
print("Successful push!")
