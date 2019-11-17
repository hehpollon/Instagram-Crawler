import json
import os
import time

import requests
from docopt import docopt
from tqdm import tqdm
from bs4 import BeautifulSoup
import lxml

from utils.browser import Browser


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
            file.write(str(i) + "\n")
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


def extractLikes(data):
    result = ""
    try:
        result = data.find("div", class_="Nm9Fw").text[0:-6]
    except Exception as e:
        pass
        result = ""
    return result


def extractComments(data):
    result = []
    try:
        result = data.find_all("div", class_="C4VMK")
    except Exception as e:
        pass
        result = []
    return result


def extractDateTime(data):
    result = ""
    try:
        result = data.find("time").get("datetime")
    except Exception as e:
        pass
        result = ""
    return result


def extractCommentsMessage(data):
    results = []
    try:
        for one in data:
            results.append(one.contents[0].text + ": " + one.contents[1].text)
    except Exception as e:
        pass
        results = []
    return results


def extractCaption(data):
    result = ""
    try:
        result = data.get("alt")
    except Exception as e:
        pass
        result = ""
    return result


def runCrawl(limitNum=0, queryList=[], is_all_comments=False, userinfo={}):
    browser = Browser("driver/chromedriver")
    if userinfo != {}:
        print('Start logging in')
        browser.goToPage('https://www.instagram.com/accounts/login/?hl=en')
        if browser.log_in(userinfo):
            print('Success to log in')
        else:
            print('Fail to log in')
            return
    else:
        print('Continue Without logging in')
    for query in queryList:
        browser.clearLink()
        makeDir("data")
        makeDir("data/" + query)
        mUrl = ""
        if query[0] == "#":
            mUrl = "https://www.instagram.com/explore/tags/" + query[1:] + "/?hl=en"
        else:
            mUrl = "https://www.instagram.com/" + query + "/?hl=en"
        browser.goToPage(mUrl)
        print("collecting url of " + query + "...")
        browser.scrollPageToBottomUntilEnd(browser.collectDpageUrl, limitNum)
        print("finish scoll collecting!")

        print("collecting data...")
        slist = list(set(browser.urlList))
        for url in tqdm(slist):
            dirName = url.split("/")[4]
            # skip if already crawled 
            if not makeDir("data/" + query + "/" + dirName):
                continue
            browser.goToPage(url)
            if is_all_comments:
                browser.expandComments()
            cur = browser.getPageSource()
            writeToFile("data/" + query + "/" + dirName + "/raw.html", [cur])
            infoData = BeautifulSoup(cur, "lxml")
            imageData = infoData.find("img", class_="FFVAD")
            # extract data
            likes = extractLikes(infoData)
            comments_list = extractComments(infoData)
            comments = comments_list.__len__()
            caption = extractCaption(imageData)
            dateTime = extractDateTime(infoData)
            commentMessages = extractCommentsMessage(comments_list)
            # print("likes:",likes," comments:", comments," caption:", caption, 
            #     "commentMessages:", commentMessages, "dateTime:", dateTime)
            writeToFile(
                "data/" + query + "/" + dirName + "/info.txt",
                [
                    "likes: ", likes, "",
                    "comments: ", comments, "",
                    "caption: ", caption, "",
                    "commentMessages: ", commentMessages, "",
                    "dateTime: ", dateTime, ""
                ]
            )
            # download image
            imageUrl = imageData.get("srcset")
            downloadImage(imageUrl, "data/" + query + "/" + dirName + "/image.jpg")
            time.sleep(1)
        print("query " + query + " collecting finish")

    time.sleep(2)
    browser.driver.quit()
    print("FINISH!")


def main():
    args = docopt("""
        Usage:
            crawl.py [-q QUERY] [-n NUMBER] [--a] [--l] [-h HELP]

        Options:
            -q QUERY  username, add '#' to search for hashtags, e.g. 'username' or '#hashtag'
                      For multiple query seperate with comma, e.g. 'username1, username2, #hashtag'

            -n NUM    number of returned posts [default: 1000]

            --a       collect all comments
            
            --l       get log in to instagram
            
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
    is_login = args.get('--l', False)
    limitNum = int(args.get('-n', 1000))
    query = args.get('-q', "")
    is_all_comments = args.get('--a', False)

    userinfo = {}
    if is_login:
        with open('./userinfo.json') as json_file:
            userinfo = json.load(json_file)

    if not query:
        print('Please input query!')
    else:
        queryList = query.replace(" ", "").split(",")
        runCrawl(limitNum=limitNum, queryList=queryList, is_all_comments=is_all_comments, userinfo=userinfo)

main()