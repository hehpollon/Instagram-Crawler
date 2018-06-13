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
        ranker.py [-q QUERY] [-u upper] [-l lower] [-f FOLDER]
    
    Options:
        -q QUERY  username, add '#' to search for hashtags, e.g. 'username' or '#hashtag'
                  For multiple query seperate with comma, e.g. 'username1, username2, #hashtag'

        -u upper  upper number of likes

        -l lower  lower number of likes

        -f FOLDER name of folder

    """)
    makeDir("../s_data")
    highNum = int(args.get('-u', "10000"))
    lowNum = int(args.get('-l', "0"))
    query = args.get('-q', "")
    folderName = args.get('-f', "")
    print(lowNum, "<=", folderName, "<=", highNum)
    newPath = "../s_data/"+query+"/"+folderName
    if not query or highNum <= lowNum or not folderName:
        print('Please input query!')
    else:
        if os.path.exists(newPath):
            # remove exist folder
            shutil.rmtree(newPath)

        # make new folder
        makeDir("../s_data/"+query)
        makeDir(newPath)

        path = "../data/"+query
        count = 0
        totalCount = 0
        for i in os.listdir(path):
            try:
                fPath = path+"/"+i+"/info.txt"
                if not os.path.exists(fPath):
                    continue
                f = open(fPath)
                f.readline()
                data = f.readline()[:-1]
                likes = int(data)
                totalCount += 1
                if likes <= highNum and likes >= lowNum:
                    shutil.copytree(path+"/"+i, newPath+"/"+i)
                    count += 1
            except:
                pass
            finally:
                f.close()

        print(str(count)+"/"+str(totalCount)+" matched!")
main()


