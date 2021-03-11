import time
import os
import requests
from utils.browser import Browser
from docopt import docopt
from tqdm import tqdm
import html

def downloadImage(imageUrl, imagePath):
    img_data = requests.get(imageUrl).content
    with open(imagePath, 'wb') as handler:
        handler.write(img_data)

def writeToFile(filePath, data):
    file = open(filePath, 'w', encoding='utf8')
    for i in data:
        if type(i) is list:
            i = "\n".join(i)
        try:
            file.write(str(i)+"\n")
        except Exception as e:
            pass
    file.close()

def makeDir(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    else:
        if len(os.listdir(dirPath)) == 3:
            return False
    return True

def extractLang(data):
    result = ""
    try:
        result = data.split('lang="')[1].split('"')[0]
    except Exception as e:
        pass
    return result

def extractLikes(data, lang="en"):
    result = ""
    try:
        if lang == "en":
            result = data[0][1:]
        else:
            result = data[1][:-2]
    except Exception as e:
        pass
        result = ""
    return result

def extractComments(data, lang="en"):
    result = ""
    try:
        if lang == "en":
            result = data[2]
        else:
            result = data[3][:-1]
    except Exception as e:
        pass
        result = ""
    return result

def extractDateTime(data):
    result = ""
    try:
        result = data.split('datetime="')[1].split('"')[0]
    except Exception as e:
        pass
        result = ""
    return result

def extractCommentsMessage(data):
    results = []
    try:
        sp = data.split("sqdOP yWX7d     _8A5w5   ZIAjV")
        if len(sp) > 2:
            for i in range(len(sp)):
                if i > 1:
                    name = sp[i].split(">")[1].split("<")[0]
                    message = sp[i].split(">")[5].split("<")[0]
                    results.append(name+": "+message)
    except Exception as e:
        pass
        results = []
    return results

def extractCaption(data):
    result = ""
    try:
        splitData = data.split('<img alt="')
        if len(splitData) > 1:
            result = splitData[1].split('"')[0]
        else:
            # only english?
            result = data.split('{"node":{"text":"')[1].split('"}')[0]
            result = result.encode('utf-8').decode('unicode-escape')
    except Exception as e:
        pass
        result = ""
    return result

def runCrawl(limitNum = 0, queryList = [], is_all_comments=False):
    browser = Browser("driver/chromedriver")
    for query in queryList:
        browser.clearLink()
        makeDir("data")
        makeDir("data/"+query)
        mUrl = ""
        if query[0] == "#":
            mUrl = "https://www.instagram.com/explore/tags/"+query[1:]+"/?hl=en"
        else:
            mUrl = "https://www.instagram.com/"+query+"/?hl=en"
        browser.goToPage(mUrl)
        print("collecting url of " + query + "...")
        browser.scrollPageToBottomUntilEnd(browser.collectDpageUrl, limitNum)
        print("finish scoll collecting!")

        print("collecting data...")
        slist = list(set(browser.urlList))
        for url in tqdm(slist):
            dirName = url.split("/")[4]
            # skip if already crawled 
            if not makeDir("data/"+query+"/"+dirName):
                continue
            browser.goToPage(url)
            if is_all_comments:
                browser.expandComments()
            cur = browser.getPageSource()
            writeToFile("data/"+query+"/"+dirName+"/raw.html", [cur])
            infoData = cur.split("<meta content=")[1].split(" ")
            # extract data
            lang = extractLang(cur)
            likes = extractLikes(infoData, lang)
            comments = extractComments(infoData, lang)
            caption = extractCaption(cur)
            dateTime = extractDateTime(cur)
            commentMessages = extractCommentsMessage(cur)
            # print("likes:",likes," comments:", comments," caption:", caption, 
            #     "commentMessages:", commentMessages, "dateTime:", dateTime)
            writeToFile(
                "data/"+query+"/"+dirName+"/info.txt", 
                [   
                    "likes: ", likes, "",
                    "comments: ", comments, "",
                    "caption: ", caption, "",
                    "commentMessages: ", commentMessages, "",
                    "dateTime: ", dateTime, ""
                ]
            )
            # download image
            imageUrl = html.unescape(cur.split('meta property="og:image" content="')[1].split('"')[0])
            downloadImage(imageUrl,"data/"+query+"/"+dirName+"/image.jpg")
            time.sleep(1)
        print("query " + query + " collecting finish")

    time.sleep(2)
    browser.driver.quit()
    print("FINISH!")

def main():
    args = docopt("""
    Usage:
        crawl.py [-q QUERY] [-n NUMBER] [--a] [-h HELP]
    
    Options:
        -q QUERY  username, add '#' to search for hashtags, e.g. 'username' or '#hashtag'
                  For multiple query seperate with comma, e.g. 'username1, username2, #hashtag'

        -n NUM    number of returned posts [default: 1000]

        --a       collect all comments

        -h HELP   show this help message and exit
    """)
    hasChromeDriver = False
    for i in os.listdir("./driver"):
        if "chromedriver" in i:
            hasChromeDriver = True
            break
    if not hasChromeDriver:
        print("ERROR! NO 'chromedriver' Found")
        print("Please install chromedriver at https://sites.google.com/a/chromium.org/chromedriver/")
        return
    limitNum = int(args.get('-n', 1000))
    query = args.get('-q', "")
    is_all_comments = args.get('--a', False)
    if not query:
        print('Please input query!')
    else:
        queryList = query.replace(" ","").split(",")
        runCrawl(limitNum=limitNum, queryList=queryList, is_all_comments=is_all_comments)

main()