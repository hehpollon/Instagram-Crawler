from docopt import docopt
import os
import shutil

def makeDir(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    else:
        if len(os.listdir(dirPath)) == 3:
            return False
    return True

def main():
    args = docopt("""
    Usage:
        ranker.py [-q QUERY] [-n NUMBER] [-h HELP]
    
    Options:
        -q QUERY  username, add '#' to search for hashtags, e.g. 'username' or '#hashtag'
                  For multiple query seperate with comma, e.g. 'username1, username2, #hashtag'

        -n NUM    number of split likes

        -h HELP   show this help message and exit
    """)
    makeDir("../s_data")
    limitNum = int(args.get('-n', 0))
    query = args.get('-q', "")
    if not query or limitNum == 0:
        print('Please input query!')
    else:
        if os.path.exists("../s_data/"+query):
            # remove exist folder
            shutil.rmtree("../s_data/"+query)

        # make new folder
        makeDir("../s_data/"+query)
        makeDir("../s_data/"+query+"/high")
        makeDir("../s_data/"+query+"/low")

        path = "../data/"+query

        for i in os.listdir(path):
            try:
                fPath = path+"/"+i+"/info.txt"
                if not os.path.exists(fPath):
                    continue
                f = open(fPath)
                f.readline()
                data = f.readline()[:-1]
                likes = int(data)
                if likes >= limitNum:
                    shutil.copytree(path+"/"+i, "../s_data/"+query+"/high/"+i)
                else:
                    shutil.copytree(path+"/"+i, "../s_data/"+query+"/low/"+i)
            except:
                pass
            finally:
                f.close()

main()



