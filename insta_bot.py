from selenium import webdriver
import time
import random

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.base_url = 'https://www.instagram.com'
        self.driver = webdriver.Chrome('chromedriver.exe')

        self.login()


    def login(self):
        self.driver.get('{}/accounts/login/?hl=ru&source=auth_switcher'.format(self.base_url))
        time.sleep(1)
        self.driver.find_element_by_name('username').send_keys(self.username)
        time.sleep(1)
        self.driver.find_element_by_name('password').send_keys(self.password)
        time.sleep(1)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Войти')]")[0].click()
        time.sleep(2)

    def close_browser(self):
        self.driver.close()

    def nav_user(self, user):
        self.driver.get('{}/{}/'.format(self.base_url, user))

    def follow_user(self, user):
        self.nav_user(user)
        follow_button= self.driver.find_elements_by_xpath("//button[contains(text(), 'Подписаться')]")[0]
        follow_button.click()

    def like_photo(self, hashtag):
        driver = self.driver
        driver.get('{}/explore/tags/'.format(self.base_url) + hashtag + "/")
        time.sleep(2)

        #picking up photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                #get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                #get relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

            except Exception:
                continue

        #Liking photos
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2,4))
                driver.find_elements_by_xpath("//button/span[@aria-label='Нравится']")[0].click()
                time.sleep(3)
            except Exception as e:
                print('Didn't like')
                time.sleep(2)


if __name__ == '__main__':
    ig_bot = InstagramBot('your_login', 'your_password')
    hashtags = ['place your hastags here']

    while True:
        try:
            tag = random.choice(hashtags)
            ig_bot.like_photo(tag)
        except Exception as e:
            print(e)
            ig_bot.close_browser()
            time.sleep(60)
            ig_bot = InstagramBot('your_login', 'your_password')
