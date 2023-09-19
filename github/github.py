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
        self.count_followers=0

        self.driver=webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()

    def wait(self,sec=2):
        time.sleep(sec)

    def signIn(self):

        login=self.driver.find_element(By.CSS_SELECTOR,'[href="/login"]') 
        login.click()
        
        # time.sleep(2)
        self.wait()

        self.driver.find_element(By.NAME, "login").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        
        self.driver.find_element(By.NAME, "commit").send_keys(Keys.ENTER)

       
        self.wait()
        self.driver.get(self.url+self.username)
        
        self.wait()


    def loadRepos(self):

        self.driver.get(self.url+self.username)
        
        self.wait()

        repos=self.driver.find_element(By.CSS_SELECTOR,'[data-tab-item="repositories"]')
        repos.click()
    

        while True:

            self.wait()

            repos_list=self.driver.find_element(By.ID, "user-repositories-list").find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')

            self.count_repos+=len(repos_list)

            if self.count_repos > 0:
                for rep in repos_list:
                    repo_title=rep.find_element(By.CSS_SELECTOR, '[itemprop="name codeRepository"]')
                    self.repositories.append(repo_title.text)


            try:

                self.wait()

                next_button=self.driver.find_element(By.CLASS_NAME, "next_page")

                if next_button.is_displayed():
                    #print("Next button exist")

                    #print(next_button.get_attribute("class").split(" "))

                    if "disabled" not in next_button.get_attribute("class").split(" "):
                        next_button.click()
                       
                    else:
                        #print("Next Button is disabled now")
                        break

            except Exception:
                #print("Next Button does not exist")
                break
                
        

    def getRepos(self):

        self.loadRepos()

        return self.repositories


    def getReposCount(self):

        if self.count_repos==0:
            self.loadRepos()

        return self.count_repos
    

    def loadFollowers(self):

        followers_datas=[]

        user_profile_frame=self.driver.find_element(By.ID,"user-profile-frame").find_element(By.CSS_SELECTOR, 'div[data-hpc]')
        followers_table=user_profile_frame.find_elements(By.CLASS_NAME, 'd-table')

        for followers_list in followers_table:
            followers_datas.append(followers_list.find_elements(By.CSS_SELECTOR, 'a[data-hovercard-type="user"]'))


        return followers_datas
    

    def addToFollowers(self):

        followers_datas=self.loadFollowers()  

        for data in followers_datas:

            user_img=data[0].find_element(By.TAG_NAME, 'img').get_attribute('src')
            full_name=data[1].find_element(By.CSS_SELECTOR,'span.Link--primary').text
            user_name=data[1].find_element(By.CSS_SELECTOR,'span.Link--secondary').text

            user_infos={
                'image':user_img,
                'username':user_name,
                'fullname':full_name
            }

            self.followers.append(user_infos)

            self.count_followers+=1
    

    def getFollowers(self):

        url_followers='?tab=followers'
        self.driver.get(self.url+self.username+url_followers)

        self.addToFollowers()

        while True:

            try:
                navigation_bnt=self.driver.find_element(By.CLASS_NAME, 'pagination')

                if navigation_bnt.is_displayed():

                    navigation_bnt=navigation_bnt.find_elements(By.CSS_SELECTOR,'*')
                    next_button=navigation_bnt[1]

                                   
                    if next_button.get_property("rel")=="nofollow":
                        next_button.click()

                        self.wait()

                        self.addToFollowers()

                    else:
                        #print("End of the list")
                        break

            except Exception:
                #print("Link does not exist")
                break
   
        return self.followers
    

    def getFollowersCount(self):
       
        if self.count_followers==0:
           self.getFollowers()
           self.followers=[]


        return self.count_followers