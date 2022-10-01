import discord
import requests
import random
async def chegg(ctx, arg):
    try:


        if "https://www.chegg.com/homework-help/" not in arg: 
            await ctx.channel.send(ctx.author.mention + "This is not a chegg link!")
            return
        else:
            

            
            page = session.get(arg,headers=headers)
            pageContent = page.content
            soup = BeautifulSoup(pageContent,"html.parser")

            answerDiv = soup.find("div",{"class":"answer-given-body ugc-base"})
            answerImages = answerDiv.findAll('img')
            answerText = answerDiv.getText()


        
            for image in answerImages:
                await ctx.author.send(image['src'])

            if(not answerText):
                return

            await ctx.author.send('#######################################')
            


            file = open('answer.txt', 'w')
            file.write(answerText)
            file.close()
            my_files = [discord.File('answer.txt')]
            await ctx.author.send(files=my_files)
    except:
        await ctx.author.send("there is no text to send or something went wrong!")
        pass