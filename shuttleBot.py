import discord
import json,sys,os,random
class MyClient(discord.Client):
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
configs = {}
with open(sys.path[0] + '/config.json', 'r+') as openfile:
    json_object = json.load(openfile)
    configs = json_object

client = MyClient()
client.run(configs['token'])