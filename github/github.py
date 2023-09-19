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
        self.repositories=[]
        self.count_repos=0

        self.driver=webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()

    def signIn(self):
        login=self.driver.find_element(By.CSS_SELECTOR,'[href="/login"]') 
        login.click()
        self.driver.implicitly_wait(2)

        self.driver.find_element(By.NAME, "login").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        
        self.driver.find_element(By.NAME, "commit").send_keys(Keys.ENTER)

        time.sleep(2)
        self.driver.get(self.url+self.username)
        time.sleep(5)

    def getRepos(self):
        self.driver.get(self.url+self.username)
        time.sleep(2)
        repos=self.driver.find_element(By.CSS_SELECTOR,'[data-tab-item="repositories"]')
        repos.click()
        time.sleep(2)

        repos_list=self.driver.find_element(By.ID, "user-repositories-list").find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
        
        self.count_repos+=len(repos_list)

        if len(repos_list) >0:
            for rep in repos_list:
                repo_title=rep.find_element(By.CSS_SELECTOR, '[itemprop="name codeRepository"]')
                self.repositories.append(repo_title.text)

        return self.repositories

    def getReposCount(self):
        return self.count_repos

