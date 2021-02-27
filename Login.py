#from selenium.webdriver import Chrome 
from instascrape import *
from firebase import Firebase
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from time import sleep,strftime
from random import randint, choice
from bs4 import BeautifulSoup
import requests
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import random, datetime

# req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list() #this will create proxy list

# PROXY = proxies[0].get_address()
# webdriver.DesiredCapabilities.SAFARI['proxy']={
#     "httpProxy":PROXY,
#     "ftpProxy":PROXY,
#     "sslProxy":PROXY,
    
#     "proxyType":"MANUAL",
    
# }

#setup firebase
config = {
  "apiKey" : "AIzaSyCh43Ccaiur1STouAfXWx5sGTUtXTLAENs",
  "authDomain" : "ig-scraper-fyp.firebaseapp.com",
  "databaseURL": "https://ig-scraper-fyp-default-rtdb.firebaseio.com",
  "storageBucket": "ig-scraper-fyp.appspot.com"
}

firebase = Firebase(config)

#connect to database
db = firebase.database()
#set header to create session
headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid = 1474556397%3AVg2e9MIy7n7xzX%3A22;"
}

#scrapping
Target1 = 'travel'
Target2 = ['adventurous', 'backpacking', 'budget', 'chillout' ,'cruise', 'culturevulture','exotic','foodie','golocal','nature','luxurious','photography','rail','train','roadtrip','romantic','shopaholic','spontaneous','sporty','thrilling','vegan','youngwildandfree','bars','nightlife','biking','cycling','cafehopping','camping','extremesports','festivals','flying','gliding','hiking','historical','hotspring','museums','galleries','outdooradventure','scubadiving','shopping','sightseeing','snorkelling','snowsports','skiing','snowboarding','spa','themeparks','winetasting','zoo','aquariums','sunshine','beach','sports','motorcycling','DIY','chillout']
element_count = [0]*54
count = 0

webdriver = webdriver.Safari()
pic_url=[]
pic_url_clean=[]
scrape_time = random.uniform(5.1,9.9)

webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher') 
sleep(scrape_time)
username = webdriver.find_element_by_name('username') 
username.send_keys('IIMT4701_255') 
password = webdriver.find_element_by_name('password') 
password.send_keys('iimt4701')
click_login = webdriver.find_element_by_css_selector(".sqdOP.L3NKy").click() 
sleep(scrape_time)


webdriver.get('https://www.instagram.com/explore/tags/'+ Target1 + '/')


# SCROLL_PAUSE_TIME = 5

# # Get scroll height
# last_height = webdriver.execute_script("return document.body.scrollHeight")

# while True:
for iter in range(5):
    # Scroll down to bottom
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(scrape_time)

    pic_link = webdriver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]')
    for x in pic_link :
        link= x.find_element_by_xpath('.//a').get_attribute('href')
        pic_url.append(link)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = webdriver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

pic_url = list(dict.fromkeys(pic_url))

# target_hashtag = Hashtag('https://www.instagram.com/explore/tags/travel')
# target_hashtag.scrape()
# pic_url = target_hashtag.get_recent_posts()

#print(pic_url)

for post in pic_url :
    count += 1 
    print('Loading post ',count)
    # target_post = Post(post)
    try:
        target_post = Post(post)
        target_post.scrape()
        sleep(scrape_time)
        date = datetime.datetime.fromtimestamp(target_post['timestamp'])
        element_pointer = 0
        for item in Target2:
            if item in target_post['hashtags']:
                db.child("Test_Scrape8_Content").push(data = {"Hastag": target_post['hashtags'],"Location": target_post['location'],"Timestamp":target_post['timestamp']})
                element_count[element_pointer]+=1
                print('Inputted to Database')
                break
            else: 
                element_pointer+=1
    except:
        print('Error Occured')
        continue

loop = 0
for counter in element_count:
    db.child("Test_Scrape8_Count").push(data = {Target2[loop]: counter})
    print('Inputted Count ',loop+1)
    loop+=1