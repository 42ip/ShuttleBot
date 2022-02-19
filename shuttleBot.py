import discord
import os
import requests
import gpt_2_simple as gpt2
import tarfile
import gdown
import geograpy
import nltk
from commands.apod import apod
from commands.earth import earth
import commands.getCie as getCie
from commands.hello import hello
from commands.help import help as helper
from commands.mars import mars
from commands.splash import splash

nltk.download('all')
found = False
try:
    url = 'https://drive.google.com/uc?id=1-0IYKo6M4ERufKjhgs05GRCsLleTI-Fj'
    output = 'checkpoint_run1.tar'
    gdown.download(url, output, quiet=False)
    files = os.listdir()
    print(files)


    file_path = 'checkpoint_run1.tar'


    with tarfile.open(file_path, 'r') as tar:
        tar.extractall()
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name='run1')
    found = True
except FileNotFoundError:
    print("Oh no, no access")

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

    possibleIntros = ['Hope I can get some space here', "I am tasked to orbit this server",
                      "My sensors are telling me that you might be a star", "You seem to radiate some good vibes", "I don't believe in astrology", "Before organizing any event, remember to PLANET.", "You don't get free milk in the Milky Way <:sadge:886538902352068628>", "Astronauts can't scratch their face or nose once they are in the suit.", "What happens in a black hole, stays in a black hole :)", "Its always been about the sun, he wants to be the center of everything :(", "Concentrate and work! Don't SPACE out"]

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        chan = message.channel

        resp = message.content
        if resp[0] == '>':
            resp = resp[1:].lower()
            if resp == 'hello':
                await hello(introList=self.possibleIntros,channel=chan)


            elif resp == 'mars':
                await mars(channel=chan,apiKey=apiKey)


            elif resp == 'apod':
                await apod(channel=chan,apiKey=apiKey)


            elif resp == 'plot':
                if found:
                    await chan.send('Contacting the nearest satellite for a new movie plot <:peepobigbrain:863049707361665024>')
                    text = gpt2.generate(sess, run_name='run1',
                    length=50,
                    prefix="<|startoftext|>",
                    truncate="<|endoftext|>\n",
                    include_prefix=False,return_as_list = True)
                    print(text[0])
                    await chan.send(text[0])
                else:
                    await chan.send("All the movie satellites are away from me at this moment.")

            elif resp.startswith('earth'):
                await earth(message=message,channel=chan)

            elif resp == 'help':
                await helper(message=message)
            
            elif resp.startswith('splash'):
                await splash(resp=resp,channel=chan,splashKey=splashKey)


            elif resp.startswith('travel'):
                cName = resp.split()[1]
                cName = cName[0].upper() + cName[1:]
                text = 'I am from ' + cName
                placeName = geograpy.get_place_context(text=text)

                if len(placeName.cities) > 0:
                    response = requests.get(
                        'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.cities[0]))
                    if response.status_code == 200:
                        vals = response.json()
                        await chan.send('Here is a photo from {} for you :wink:'.format(placeName.cities[0]))
                        await chan.send(vals['urls']['small'])

                elif len(placeName.countries) > 0:
                    response = requests.get(
                        'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.countries[0]))
                    if response.status_code == 200:
                        vals = response.json()
                        await chan.send('Here is a photo from {} for you :wink:'.format(placeName.countries[0]))
                        await chan.send(vals['urls']['small'])
                

                elif len(placeName.regions) > 0:
                    response = requests.get(
                        'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.regions[0]))
                    if response.status_code == 200:
                        vals = response.json()
                        await chan.send('Here is a photo from the country {} for you :wink:'.format(placeName.regions[0]))
                        await chan.send(vals['urls']['small'])
                
                else:
                    await message.reply("A man who is said to be from the ocean stole some of our drives :astronaut:, maybe this unknown place's info was in it <:sadge:886538902352068628>")

            elif resp.startswith('cie'):
                await getCie.getCie(resp,message,chan,True)
            elif resp.startswith('attendance'):
                await getCie.getCie(resp,message,chan,False)
            else:
                await message.reply("Hey! Why'd you call me? Know your place human, I am a busy rocket. Use >help and learn what I do, then hit the blast off button <:superAngry:843088789349335050>")



client = MyClient()
client.run(token)
