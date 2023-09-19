import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from github.config import BASE_URL, USERNAME, PASSWORD

class Github():
    
    def __init__(self) -> None:
        self.url=BASE_URL
        self.username=USERNAME
        self.password=PASSWORD
        self.followers=[]

        self.driver=webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()

    def signIn(self):
        login=self.driver.find_element(By.CSS_SELECTOR,'[href="/login"]') 
        login.click()
        self.driver.implicitly_wait(2)

        self.driver.find_element(By.CSS_SELECTOR, '[name="login"]').send_keys(self.username)
        self.driver.find_element(By.CSS_SELECTOR, '[name="password"]').send_keys(self.password)
        
        self.driver.find_element(By.CSS_SELECTOR, '[name="commit"]').send_keys(Keys.ENTER)

        time.sleep(2)
        self.driver.get(self.url+self.username)
        time.sleep(5)






