# Code to scrape the results of any student from "http://exam.msrit.edu/"
from collections import defaultdict
import requests
from bs4 import BeautifulSoup as bs
import json
import discord
# username = '1ms19cs045'
# password = '2002-07-17'
 
    
async def getCie(response,message,channel,client):
    isthere = isPrivate = False
    ctx = message
    author = message.author.id
    # user= await client.get_user_info(author)
    isNotPrivate = False
    if isinstance(ctx.channel, discord.channel.DMChannel):
        isNotPrivate = True
    if isNotPrivate:
        await channel.send("Please dm me ;) i wont give cie stuff in groups")
        await message.author.send("Message me here with the command ``` >cie your_usn yyyy-mm-dd if you arent registered or just >cie ``` ")
        # await client.delete_message(message)
        return


    vals = response.split()
    username = password = " "
    if len(vals) == 1:
        j = {}
        with open('auth.json','r') as f:
            j = json.loads(f.read())
        if message.author in j:
            username,password = j[message.author]['username'],j['password']
        else:
            await message.author.send("You arent registered :( run the command in the following manner : ``` >cie your_usn yyyy-mm-dd ```")
            return
    elif len(vals) == 3:
        # assuming person is signing in. this will overwrite creds
        username = vals[1]
        password = vals[2]
        isthere = False
        j = {}
        with open('auth.json','r') as f:
            j = json.load(f.read())
        if message.author in j: isthere = True
        j[message.author] = {'username':username,'password':password}
        await message.author.send("Ah! i see you're updating <wink> " if isthere else "Welcome {} ! I'll send you your Cie stuff shortly..".format(message.author))
        with open('auth.json','w') as f:
            json.dump(j,f)

    data = {'task': 'login', 'option':'com_user','username': username,'passwd': password}
    with requests.Session() as s:
        s.verify = True
        # First sending log in data
        a = s.post("http://parents.msrit.edu/",data=data)
        scode1 = a.status_code
        # logging in
        a = s.get("http://parents.msrit.edu/",auth=(username,password))
        scode2 = a.status_code
        if scode1 != scode2 != 200:
            await message.author.send("Somethings wrong :( Try registering again" )
            return
        # getting the subject data
        r2 = s.get("http://parents.msrit.edu/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard")
        soup = bs(r2.text,'lxml') 
        # each value in the indices array will link to the subject page of particular subject   
        indices = []
        for a in soup.findAll('a',href=True):
            if 'ciedetails' in a['href']:
                indices.append(a['href'])
        d = defaultdict(list)
        for site in indices:
            r = s.get("http://parents.msrit.edu/{}".format(site))
            soup  = bs(r.text,'lxml')
            capt = soup.find('caption').contents[0]
            t = soup.find('table',{'class':'uk-table cn-cie-table uk-table-responsive'})
            headers = []
            datas = []
            for header in t.findAll('th'):
                headers.append(header.contents[0].replace(" ","") + '\t')
            for data in t.findAll('td'):
                datas.append(data.contents[0].replace(" ","") + '\t')
            datas[7] += '\t'
            datas[8] += '\t'
            d[capt] = [headers,datas]
        response = "Here are your CIE details: \n"
        for i in d:
            response += i + '\n'
            response += "".join(d[i][0]) + "\n"
            response += "".join(d[i][1]) + "\n"
            response += "\n"
        await message.author.send(response)