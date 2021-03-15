#from selenium.webdriver import Chrome 
from instascrape import *
#from firebase import Firebase
from firebase import firebase
from time import sleep,strftime
from random import randint, choice
import requests
#from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import random, datetime, math

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
# config = {
#   "apiKey" : "AIzaSyCJQCY2V2rNWThAtkypMSq-_OvAyW98ads",
#   "authDomain" : "ig-scraper-d10a3.firebaseapp.com",
#   "databaseURL": "https://ig-scraper-d10a3-default-rtdb.firebaseio.com",
#   "storageBucket": "ig-scraper-d10a3.appspot.com"
# }

# firebase = Firebase(config)

#connect to database
# db = firebase.database()
#set header to create session
headers1 = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid = 45781691217%3AbuqvhiSUXpuIfi%3A9;"
}

headers2 = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid = 46425926367%3ATKOFF0QUixWcji%3A9;"
}

#test if string is NaN
def isNaN(string):
    return string != string

#scrapping
Target1 = 'travel'
Target2 = ['adventurous', 'backpacking', 'budget', 'chillout' ,'cruise', 'culturevulture','exotic','foodie','golocal','nature','luxurious','photography','rail','train','roadtrip','romantic','shopaholic','spontaneous','sporty','thrilling','vegan','youngwildandfree','bars','nightlife','biking','cycling','cafehopping','camping','extremesports','festivals','flying','gliding','hiking','historical','hotspring','museums','galleries','outdooradventure','scubadiving','shopping','sightseeing','snorkelling','snowsports','skiing','snowboarding','spa','themeparks','winetasting','zoo','aquariums','sunshine','beach','sports','motorcycling','DIY','chillout']
element_count = [0]*54
count = 0

pic_url=[]
pic_url_clean=[]
scrape_time = random.uniform(5.1,9.9)

firebase = firebase.FirebaseApplication('https://ig-scraper-d10a3-default-rtdb.firebaseio.com', None)
result = firebase.get('-MVZfqBFib6E9GqxiN2l', 'URL')
#result = firebase.post('/Test', {'Hashtag': 'test'})


for post in result :
    count += 1 
    print('Loading post ',count)
    # target_post = Post(post)
    if count >999 and count<1400:
        try:
            target_post = Post(post)
            # choice = random.random()
            # if (choice<= 0.5):
            #     target_post.scrape(headers=headers1)
            # else:
            #     target_post.scrape(headers=headers2)
            target_post.scrape(headers=headers1)
            sleep(scrape_time)
            #date = datetime.datetime.fromtimestamp(target_post['timestamp'])
            element_pointer = 0
            location_select = target_post['location']
            for item in Target2:
                if item in target_post['hashtags']:
                    if isNaN(location_select) or (not location_select):
                        data = {
                            'Hashtag' : target_post['hashtags'],
                            'Timestamp':target_post['timestamp']
                        }
                    else:
                        data = {
                            'Hashtag' : target_post['hashtags'],
                            'Location': target_post['location'],
                            'Timestamp':target_post['timestamp']
                        }

                    upload = firebase.post('/Scrape_Content', data)
                    element_count[element_pointer]+=1
                    print('Inputted to Database')
                    break
                else: 
                    element_pointer+=1
        # except IndexError as e:
        #     print(e)
        #     continue
        except:
            print('Error Occured')
            continue

# loop = 0
# for counter in element_count:

#     upload_count = firebase.post('/Scrape_Count',{Target2[loop]: counter})
#     print('Inputted Count ',loop+1)
#     loop+=1

result = firebase.get('Scrape_Count',None)
loop = 0
for counter in result:
    existing = firebase.get('Scrape_Count',counter)
    for key in existing:
        existing[key] = int(existing[key])
        existing[key]+=element_count[loop]
        update = firebase.put('/Scrape_Count',counter, {Target2[loop]: existing[key]})
    print('Inputted Count ',loop+1)
    loop+=1