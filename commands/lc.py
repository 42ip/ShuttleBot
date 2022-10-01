import requests
import json

async def prob(channel):
    r = requests.post("https://leetcode.com/graphql",  json = {"query" : "\n    query questionOfToday {\n  activeDailyCodingChallengeQuestion {\n    date\n    userStatus\n    link\n    question {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      hasVideoSolution\n      hasSolution\n      topicTags {\n        name\n        id\n        slug\n      }\n    }\n  }\n}\n    "})
    link = "https://leetcode.com" + json.loads(r.text)["data"]["activeDailyCodingChallengeQuestion"]["link"]
    await channel.send("Here is a question for you to solve from Leetcode! \n" + link)