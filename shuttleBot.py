import discord
import json,sys,os,random
import requests


configs = {}


with open(sys.path[0] + '/config.json', 'r+') as openfile:
    json_object = json.load(openfile)
    configs = json_object
apiKey = configs['apiKey']



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



        if message.content.startswith('>apod'):
            chan = message.channel
            response = requests.get('https://api.nasa.gov/planetary/apod?api_key={}'.format(apiKey))
            if response.status_code == 200:
                vals = response.json()
                await chan.send("Today's Title is: " + vals['title'])
                await chan.send(vals['url'])

        if message.content.startswith('>help'):
            await message.reply("Hey, heard a SOS! Here's all you need to know: \n Prefix : > \n 1. hello : Know the bot \n 2. apod : Astronomical Picture Of The Day")


client = MyClient()
client.run(configs['token'])