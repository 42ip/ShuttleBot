import discord
import requests
import random

async def mars(channel,apiKey):
    arr = []
    while arr == []:
        num = random.randint(1, 3250)
        response = requests.get(
            'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={}&camera=navcam&api_key={}'.format(str(num), apiKey))
        if response.status_code == 200:
            vals = response.json()
            arr = vals['photos']
            if len(arr) > 0:
                photo = random.choice(arr)
                await channel.send("Here's a picture from the red planet near us")
                await channel.send(photo['img_src'])