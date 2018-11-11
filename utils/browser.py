from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import time

class Browser:
    
    def __init__(self, driverPath):
        self.driver = webdriver.Chrome(driverPath)
        self.driver.implicitly_wait(3)
        self.waitTime = 1 # wait 1 second for loading
        self.urlList = []

    def goToPage(self,url):
        self.driver.get(url)
    
    def getPageSource(self):
        return self.driver.page_source

    def expandComments(self):
        try:
            # loading all comments.
            # if all comments is loaded, exception will raise on click function
            while(True):
                expandScript = "return (a = document.getElementsByClassName('Z4IfV')[0].click())"
                self.driver.execute_script(expandScript)
                time.sleep(0.1)
        except:
            pass
    
    def getPageSourceCond(self, element):
        delay = 30
        myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
        return self.getPageSource()

    def scrollPageToBottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def getLinkSize(self):
        return len(self.urlList)

    def clearLink(self):
        self.urlList = []
        
    def scrollPageToBottomUntilEnd(self, mFunc, limitNum):
        dup = 0
        while True:
            curSource = self.getPageSource()
            self.scrollPageToBottom()
            time.sleep(self.waitTime)
            mFunc(curSource)
            nextSource = self.getPageSource()
            # check url link size is limitNum
            if limitNum > 0 and self.getLinkSize() >= limitNum:
                self.urlList = self.urlList[:limitNum]
                break
            # check for end
            if len(curSource) == len(nextSource):
                dup += 1
            else:
                dup = 0
            # retry three more time 
            if dup > 2:
                break
        
    def collectDpageUrl(self, data):
        r = data.split('href="/p/')[1:]
        for i in r:
            dPageLink = "https://www.instagram.com/p/"+i.split('"')[0]+"?hl=en"
            if dPageLink not in self.urlList:
                self.urlList.append(dPageLink)
            
    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass