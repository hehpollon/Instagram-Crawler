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

    def log_in(self, user_info):
        username = user_info['username']
        password = user_info['password']
        wait = WebDriverWait(self.driver, 3)

        element = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        element.send_keys(username)
        self.driver.find_element_by_name('password').send_keys(password)

        element = wait.until(EC.element_to_be_clickable((By.XPATH,
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')))
        element.click()

        try:
            wait.until(EC.presence_of_element_located((By.ID, 'slfErrorAlert')))  # check id password
            return False
        except:
            try:
                Err_msg = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))  # Login Verification
                if 'Unusual' in Err_msg.text:
                    # send security code
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,
                        '//*[@id="react-root"]/section/div/div/div[3]/form/span/button')))
                    element.click()
                    isOK = True

                    sec_code_area = self.driver.find_element_by_id('security_code')
                    submit = self.driver.find_element_by_xpath(
                        '//*[@id="react-root"]/section/div/div/div[2]/form/span/button')

                    while isOK:
                        isOK = False
                        # get input
                        print("Input 'exit' if u don't want to log in")
                        key = input('Input the code that sent to your e-mail: ')
                        if key == 'exit':
                            return False

                        sec_code_area.clear()
                        sec_code_area.send_keys(key)
                        submit.click()

                        # input valid?
                        wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, ".W1Bne")))
                        self.driver.find_element_by_id('form_error')
                        isOK = True
                        print('Error Check Code')
                else:
                    return True
            except:
                return True

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass