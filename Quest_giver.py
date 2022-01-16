from importlib.resources import read_binary
import discord
import os
from jira import JIRA
import json
from os import getenv
from dotenv import load_dotenv

#Authorization
with open('authorization.json') as f:
    dict_authorization = json.loads(f.read())

#Heroku authorization
jira_token = getenv('API_TOKEN_JIRA')
jira_username = getenv('USERNAME_JIRA')
discord_token = getenv('DISCORD_TOKEN')

#Подключение к нашей Jira
jira_host='https://quest-giver.atlassian.net'
auth_jira = JIRA(jira_host, basic_auth=(jira_username, jira_token))
jql_string ='project = QG order by created DESC'
jira_list_raw = auth_jira.search_issues(jql_string)

#Создание словаря
jira_list = {}
for issue in jira_list_raw:
    dict_issue = {}
    #dict_issue['key'] = issue
    dict_issue['status'] = issue.fields.status.name
    dict_issue['summary'] = issue.fields.summary
    jira_list[str(issue)] = dict_issue

#Подключение к Discord
client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#Message
    if message.content.startswith('hello'):
        await message.channel.send('Hello, world!')
    if message.content.startswith('jira'):
        await message.channel.send(jira_list)

#Write_DB
def write_db():
    with open('database.json', 'w', encoding='utf8') as f:
        json.dump(jira_list, f, ensure_ascii=False)

#Read_DB
def read_db():
    with open('database.json', 'r', encoding='utf8') as f:
        return json.loads(f.read())
#print(read_db())

#Compare. Find new tasks
differece = set(jira_list.keys()) - set(read_db().keys())
print(differece)



#Запуск бота
client.run(dict_authorization['DISCORD_TOKEN'])




