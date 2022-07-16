import discord
import requests
import random

async def apod(channel,apiKey):
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key={}'.format(apiKey))
    if response.status_code == 200:
        vals = response.json()
        await channel.send("Today's Title is: " + vals['title'])
        await channel.send(vals['url'])