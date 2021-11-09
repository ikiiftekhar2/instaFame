import requests
from PIL import Image
from io import BytesIO
import random
import random
import schedule
from instapy import InstaPy
from instapy import smart_run
import json
import time

def getQuotes():
    qurl = "https://api.quotable.io/random?maxLength=50"
    response = requests.get(qurl)
    data1 = response.json()
    return data1["content"]

def gettags(seed):
    av2 = ""
    qqrl = "https://api.ritekit.com/v1/stats/auto-hashtag?post=" + str(seed) + "&maxHashtags=10&hashtagPosition=auto&client_id=" + av2
    payload={}
    headers = {}
    response = requests.request("GET", qqrl, headers=headers, data=payload)
    jsono = response.json()
    hashtags = jsono["post"]
    return hashtags

def linkFetch(sample,seed):
    n = random.randint(2,7)
    url = "https://api.unsplash.com/search/photos?page="+ str(n) +"&query=" + str(sample) + "&client_id=DNeKm3Ysvgia4Sk6z9BgFoSpmGatYBl5PaQ1tZLg0hk"

    response = requests.get(url)
    data = response.json()
    post_no = random.randint(0,7)
    target_url  = data["results"][int(post_no)]['urls']['regular']
    quote = getQuotes()
    hashy = gettags(seed)
    #tags = data["results"][int(post_no)]["tags"][0]["source"]["ancestry"]['category']['pretty_slug']
    usernae = data["results"][int(post_no)]["user"]['username']
    return [target_url,usernae,quote,hashy]

import os
import shutil


#https://stackoverflow.com/questions/44370469/python-image-resizing-keep-proportion-add-white-background
def resize(image_pilo):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
 
    image_pil = (Image.open(image_pilo, 'r')) #Usar a diretoria como stuff
    width = 1000
    height = 1000
 
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    savex = background.convert('RGB')
    try:
        savex.save(str(image_pilo))
    except IOError:
        print("cannot create thumbnail for")

def cleanup(dirpath, folder_to_exclude):
    for root, dirs, files in os.walk(dirpath, topdown=True):
        for file_ in files:
            full_path = os.path.join(root, file_)
            if folder_to_exclude not in full_path:
                print ('removing -> ' + full_path)
                os.remove(full_path)
        for folder in dirs:
            full_path = os.path.join(root, folder)
            if folder_to_exclude not in full_path:
                os.remove(full_path)

tag_list = "  #likeforlikes #like #follow #followforfollowback #likeforfollow #instagood #love #photography #photooftheday #instalike #instadaily #picoftheday #followme #beautiful #followback #followers #likeforlike #comment #follow"

def interactions():
    try:
        credentials = open("creds.json",)
        parms = json.load(credentials)
        username = parms["username"]
        password = parms["pw"]
        # get a session!
        session = InstaPy(username= username, password= password, headless_browser=True)

        # let's go! :>
        with smart_run(session):
            hashtags = [  "likeforlikes", "like" , "follow", "followforfollowback", "likeforfollow", "instagood" ,"love", "photography" ,"photooftheday" ,"instalike" ,"instadaily" ,"picoftheday" ,"followme","beautiful" , "followback" ,"followers",  "likeforlike" , "comment" , "follow"]
            random.shuffle(hashtags)
            my_hashtags = hashtags[:2]

            # general settings
            session.set_dont_like(['sad', 'rain', 'depression'])
            session.set_do_follow(enabled=True, percentage=80, times=1)
            session.set_do_comment(enabled=True, percentage=90)
            session.set_comments([
                                    u'What an amazing shot! :heart_eyes: What do. A follow would be appreciated! '
                                    u'you think of my recent shot? . A follow would be appreciated!',
                                    u'What an amazing shot! :heart_eyes: I think '
                                    u'you might also like mine. :wink:. A follow would be appreciated!',
                                    u'Wonderful!! :heart_eyes: Would be awesome if '
                                    u'you would checkout my photos as well!. A follow would be appreciated!',
                                    u'Wonderful!! :heart_eyes: I would be honored '
                                    u'if you would checkout my images and tell me '
                                    u'what you think. :wink:. A follow would be appreciated!',
                                    u'This is awesome!! :heart_eyes: Any feedback '
                                    u'for my photos? :wink:. A follow would be appreciated!',
                                    u'This is awesome!! :heart_eyes:  maybe you '
                                    u'like my photos, too? :wink:. A follow would be appreciated!',
                                    u'I really like the way you captured this. I '
                                    u'bet you like my photos, too :wink:. A follow would be appreciated!',
                                    u'I really like the way you captured this. If '
                                    u'you have time, check out my photos, too. I '
                                    u'bet you will like them. :wink:. A follow would be appreciated!',
                                    u'Great capture!! :smiley: Any feedback for my '
                                    u'recent shot? :wink:. A follow would be appreciated!',
                                    u'Great capture!! :smiley: :thumbsup: What do '
                                    u'you think of my recent photo?. A follow would be appreciated!'],
                                media='Photo')
            session.set_do_like(True, percentage=90)
            session.set_delimit_liking(enabled=True, max_likes=100, min_likes=0)
            session.set_delimit_commenting(enabled=True, max_comments=30, min_comments=0)
            session.set_relationship_bounds(enabled=True,
                                            potency_ratio=None,
                                            delimit_by_numbers=True,
                                            max_followers=300,
                                            max_following=2000,
                                            min_followers=50,
                                            min_following=50)

            session.set_quota_supervisor(enabled=True,
                                        sleep_after=["likes", "follows"],
                                        sleepyhead=True, stochastic_flow=True,
                                        notify_me=True,
                                        peak_likes_hourly=200,
                                        peak_likes_daily=585,
                                        peak_comments_hourly=80,
                                        peak_comments_daily=182,
                                        peak_follows_hourly=48,
                                        peak_follows_daily=None,
                                        peak_unfollows_hourly=35,
                                        peak_unfollows_daily=402,
                                        peak_server_calls_hourly=None,
                                        peak_server_calls_daily=4700)

            session.set_user_interact(amount=20, randomize=True, percentage=80)

            # activity
            session.like_by_tags(my_hashtags, amount=35)
    except:
        print("interaction failed")

def posting():
    try:
        pairs = [("Piano","Aesthetic"),("Guitar","music"),("Toronto","Toronto"),("Canada","canada"),("Dhaka city","aesthetic"),("Piano","music"),("Guitar","aesthetic"),("Dhaka nature","nature"),("Dhaka","beautiful"),("GYM","gym"),("weights","weights"),("dumbell","dumbell"),("programming","programming"),("code","code"),("machine learning","machine learning")]
        dataz = random.choice(pairs)
        sample = dataz[0]
        seed = dataz[1]
        img_url = linkFetch(str(sample),str(seed))
        captionx = img_url[2]  +  " #" + img_url[3] + tag_list  + " Photo uploaded on unsplash by " + img_url[1]
        import os
        if os.path.exists("upload.jpg"):
            os.remove("upload.jpg")
            os.remove("upload.jpg.REMOVE_ME")
        elif os.path.exists("upload.jpg.REMOVE_ME"):
            os.remove("upload.jpg.REMOVE_ME")
        else:
            print("The file does not exist")
        import urllib.request
        image_url = img_url[0] #the image on the web
        save_name = 'upload.jpg' #local name to be saved
        urllib.request.urlretrieve(image_url, save_name)
        yyz = str(captionx)
        resize("upload.jpg")
        import json
        credentials = open("creds.json",)
        parms = json.load(credentials)
        username = parms["username"]
        password = parms["pw"]
        cleanup("config","log")
        from instabot import Bot

        bot = Bot()
        print(yyz)
        bot.login(username = username,
                password = password)
        bot.upload_photo("upload.jpg", caption = yyz)
        print(img_url)
    except:
        print("oopsie on posting")
from discord import Webhook, RequestsWebhookAdapter

schedule.every().day.at("18:00").do(posting) 
schedule.every().day.at("07:11").do(posting)
schedule.every().day.at("03:01").do(posting)
schedule.every().day.at("05:11").do(interactions) 
schedule.every().day.at("18:11").do(interactions)
schedule.every().day.at("00:49").do(interactions)

webhook = Webhook.from_url("https://discordapp.com/api/webhooks/821812873100656682/aSPL5E3fxwn4Jc0SGq0TKvaf2jYn2FhdFbr9DzwO9gjMS5XZHMUMREHG1ezqBGrRcBxv", adapter=RequestsWebhookAdapter())
webhook.send("started the script")

while True:
    schedule.run_pending()
    time.sleep(1)