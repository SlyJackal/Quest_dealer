import discord
import os
from jira import JIRA
import json

#Authorization
with open('authorization.json') as f:
    templates = json.load(f)

print(templates)

print('1')

print('3')
#Подключение к нашей Jira
jira_host='https://quest-giver.atlassian.net'
auth_jira = JIRA(jira_host, basic_auth=(username, api_token))
print('4')
print('Введите JQL запрос для выбора задач')
jql_string='project = QG order by created DESC'
jira_list = auth_jira.search_issues(jql_string)
print('Jira first task:')
print(jira_list[0])
print('Jira list:')
print(jira_list)


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello, world!')

client.run('TOKEN')
