import discord
import json,sys,os,random
import requests



apiKey = os.environ.get('apiKey')
token = os.environ.get('token')

class MyClient(discord.Client):
    global apiKey
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')



    possibleIntros = ['Hi, My name is Shuttle. Hope I can get some space here', "Hello, I'm Shuttle! I am tasked to orbit this server", "Hey, My name is Shuttle. My sensors are telling me that you might be a star", "Hello, I am Shuttle. You seem to radiate some good vibes"]
    
    
    
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
    
        if message.content.startswith('>hello'):
            await message.reply(random.choice(self.possibleIntros), mention_author=True)

        if message.content.startswith('>mars'):
            chan = message.channel
            arr = []
            while arr == []:
                num = random.randint(1,3250)
                response = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={}&camera=navcam&api_key={}'.format(str(num),apiKey))
                if response.status_code == 200:
                    vals = response.json()
                    arr = vals['photos']
                    if len(arr) > 0:
                        photo = random.choice(arr)
                        await chan.send("Here's a picture from the red planet near us")
                        await chan.send(photo['img_src'])

        if message.content.startswith('>apod'):
            chan = message.channel
            response = requests.get('https://api.nasa.gov/planetary/apod?api_key={}'.format(apiKey))
            if response.status_code == 200:
                vals = response.json()
                await chan.send("Today's Title is: " + vals['title'])
                await chan.send(vals['url'])

        if message.content.startswith('>help'):
            commands = ["1. hello : Know the bot",
            "2. apod : Astronomical Picture Of The Day" , "3. mars : NAVCAM picture from planet Mars"]
            msg = "Hey, heard a SOS! Here's all you need to know: \n Prefix : > \n"
            for val in commands:
                msg += val + '\n'
            await message.reply(msg)


client = MyClient()
client.run(token)