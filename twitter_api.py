import requests
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
from tweepy import API, Client, OAuth1UserHandler
from screenshot_practice import create_screenshot_dark, create_screenshot_light


API_KEY = "joOiKQ6lTTIUjASX2HREWjYTm"
API_SECRET_KEY = "RRl12ScYrpNgISFx2q8gYLXXWusaa9mDYGRjnwbUu1Px7LLvxT"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAP4LawEAAAAA0Ebpy3uA8Ogu8Lz61QNrQVZP3Hw%3DOkr5xe7yjeEfiWeLHADn8LUHUpt4foToDCHcK9JcwK18y0Pf9S"
ACCESS_TOKEN = "1506919072214179840-6NEeuN9HWiOugaH0IOe9lGdycQaY5p"
ACCESS_TOKEN_SECRET = "GQgje9G7NcTxGzVdj66HiU7pIvDSK2RPAScZKETqoac4p"

auth = OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

api = API(auth)
mentions = api.mentions_timeline(count=500)

# replied_id = mentions[1].in_reply_to_status_id


def get_tweet_info(id):
    replied_to = api.get_status(
        id, include_ext_alt_text=True, include_entities=True, tweet_mode="extended"
    )
    user_info = replied_to.user
    date_created = replied_to.created_at.strftime("%H:%M . %b %d, %Y")
    profile_url = user_info.profile_image_url
    try:
        profile_picture = Image.open(urlopen(profile_url))
    except:
        profile_picture = Image.open("default_profile.png")
        profile_picture = profile_picture.convert("RGB")
    return {
        "name": user_info.name,
        "username": user_info.screen_name,
        "verified": user_info.verified,
        "text": replied_to.full_text,
        "image": profile_picture,
        "date": date_created,
    }


# https://twitter.com/SultanAlQassemi/status/?t=44ri8WDho05EfWZC8E2lLg&s=19
info_1 = get_tweet_info(1518894259268734976)
img = create_screenshot_dark(
    info_1["text"],
    info_1["image"],
    info_1["username"],
    info_1["name"],
    info_1["date"],
    info_1["verified"],
)
img.save("pictured_light.jpg")
plt.imshow(img)
plt.show()
