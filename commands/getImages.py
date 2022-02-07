

import random
import requests
import geograpy

async def mars(channel, apiKey) :
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
        
async def apod(chan,apiKey):
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key={}'.format(apiKey))
    if response.status_code == 200:
        vals = response.json()
        await chan.send("Today's Title is: " + vals['title'])
        await chan.send(vals['url'])

async def splash(channel,response,splashKey):
    ids = {'3d':'CDwuwXJAbEw', 'arch':'M8jVbLbTRws','event':'BJJMtteDJA4','exp':'qPYsDzvJOYc','fashion' : 'S4MKLAsBB74', 'food' : 'xjPR4hlkBGA','nature' : '6sMVjTLSkeQ', 'street' : 'xHxYTMHLgOc', 'travel' : 'Fzo3zuOHN6w','rawr':'Jpg6Kidl-Hk'}
    genreTag = {"3d-renders" : '3d', 'architecture-interior' : 'arch','current-events' : 'event', 'experimental' : 'exp', 'fashion' : 'fashion', 'food-drink' : 'food', 'nature' : 'nature', 'street-photography' : 'street','travel' : 'travel','animals':'rawr'}
    genreName = {v: k for k, v in genreTag.items()}
    vals = response.split()
    if len(vals) == 1:
        response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}'.format(splashKey))
        if response.status_code == 200:
            vals = response.json()
            await channel.send('Here is a photo that got sent in my family satellite group :satellite_orbital:')
            await channel.send(vals['urls']['small'])
    else:
        if len(vals) != 2 or vals[1] not in ids:
            genreMsg = 'Here are the genres and its tags\n'
            for (k,v) in genreTag.items():
                genreMsg += k + ' -> ' + v + '\n'
            await channel.send("Splash takes only one or two inputs \n If you use '>splash' a random photo will be generated \n If you use '>splash {genreTag}' a particular genre specific photo shall be generated")
            await channel.send(genreMsg)
        elif vals[1] in ids:
            print(vals[1])
            response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}&topics={}'.format(splashKey,ids[vals[1]]))
            if response.status_code == 200:
                supreme = response.json()
                await channel.send('Here is a photo of {} that got sent in my family satellite group :satellite_orbital:'.format(genreName[vals[1]]))
                await channel.send(supreme['urls']['small'])
async def travel(channel,response,splashKey,message):
    cName = response.split()[1]
    cName = cName[0].upper() + cName[1:]
    text = 'I am from ' + cName
    placeName = geograpy.get_place_context(text=text)
    if len(placeName.cities) > 0:
        response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.cities[0]))
        if response.status_code == 200:
            vals = response.json()
            await channel.send('Here is a photo from {} for you :wink:'.format(placeName.cities[0]))
            await channel.send(vals['urls']['small'])
    elif len(placeName.countries) > 0:
        response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.countries[0]))
        if response.status_code == 200:
            vals = response.json()
            await channel.send('Here is a photo from {} for you :wink:'.format(placeName.countries[0]))
            await channel.send(vals['urls']['small'])
    

    elif len(placeName.regions) > 0:
        response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.regions[0]))
        if response.status_code == 200:
            vals = response.json()
            await channel.send('Here is a photo from the country {} for you :wink:'.format(placeName.regions[0]))
            await channel.send(vals['urls']['small'])
    else:
        await message.reply("A man who is said to be from the ocean stole some of our drives :astronaut:, maybe this unknown place's info was in it <:sadge:886538902352068628>")
