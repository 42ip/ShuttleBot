import discord
import requests

async def splash(resp,channel,splashKey):
    ids = {'3d':'CDwuwXJAbEw', 'arch':'M8jVbLbTRws','event':'BJJMtteDJA4','exp':'qPYsDzvJOYc','fashion' : 'S4MKLAsBB74', 'food' : 'xjPR4hlkBGA','nature' : '6sMVjTLSkeQ', 'street' : 'xHxYTMHLgOc', 'travel' : 'Fzo3zuOHN6w','rawr':'Jpg6Kidl-Hk'}
    genreTag = {"3d-renders" : '3d', 'architecture-interior' : 'arch','current-events' : 'event', 'experimental' : 'exp', 'fashion' : 'fashion', 'food-drink' : 'food', 'nature' : 'nature', 'street-photography' : 'street','travel' : 'travel','animals':'rawr'}
    genreName = {v: k for k, v in genreTag.items()}
    vals = resp.split()
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