import discord
import os
import random
import requests
import io
from PIL import Image, ImageDraw
import gpt_2_simple as gpt2
import tarfile
import gdown
import sys
import geograpy
import nltk
from commands import getImages,gptCommands,imageManipulationCommands,college
nltk.download('all')
url = 'https://drive.google.com/uc?id=1EVvLwJA1f507iF1fteBOZaJUK6CbBvl-'
output = 'checkpoint_run1.tar'
gdown.download(url, output, quiet=False)
files = os.listdir()
print(files)


file_path = 'checkpoint_run1.tar'


with tarfile.open(file_path, 'r') as tar:
    tar.extractall()
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')

print('ALL DONE')

apiKey = os.environ.get('apiKey')
token = os.environ.get('token')
splashKey = os.environ.get('splashKey')

class MyClient(discord.Client):
    global apiKey

    async def on_ready(self):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Astronaut In The Ocean"))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    possibleIntros = ['Hi, My name is Shuttle. Hope I can get some space here', "Hello, I'm Shuttle! I am tasked to orbit this server",
                      "Hey, My name is Shuttle. My sensors are telling me that you might be a star", "Hello, I am Shuttle. You seem to radiate some good vibes"]

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        chan = message.channel

        resp = message.content
        if resp[0] == '>':
            resp = resp[1:].lower()
            if resp == 'hello':
                await message.reply(random.choice(self.possibleIntros), mention_author=True)
                
            elif resp == 'mars':
                getImages.mars(chan,apiKey)

            elif resp == 'apod':
                getImages.apod(chan,apiKey)

            elif resp == 'plot':
                gptCommands.gpt2(chan,sess)

            elif resp.startswith('earth'):
                imageManipulationCommands.earth(message,chan)

            elif resp == 'help':
                commands = ["1. hello : Know the bot",
                            "2. apod : Astronomical Picture Of The Day",
                            "3. mars : NAVCAM picture from planet Mars", 
                            "4. earth: Become the planet Earth, a 6 septillion kg blue ball",
                            "5. plot : DM the nearest satellite for a new movie plot",
                            "6. splash: Generate random photos. Use >splash help to learn more",
                            "7. travel : Enter 'travel <placeName>' to get an image from there" ]
                msg = "Hey, heard a SOS! Here's all you need to know: \n Prefix : > \n"
                for val in commands:
                    msg += val + '\n'
                await message.reply(msg)
            
            elif resp.startswith('splash'):
                getImages.splash(chan,resp,splashKey)

            elif resp.startswith('travel'):
                getImages.apod(chan,resp,splashKey,message)
            elif resp.startswith('cie'):
                college.getCie(resp,message,chan,client)
                
            
            else:
                await message.reply("Hey! Why'd you call me? Know your place human, I am a busy rocket. Use >help and learn what I do, then hit the blast off button <:superAngry:843088789349335050>")



client = MyClient()
client.run(token)
