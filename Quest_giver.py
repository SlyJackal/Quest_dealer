import discord
import os
from jira import JIRA, Issue
import json

#Authorization
with open('authorization.json') as f:
    dict_authorization = json.loads(f.read())

#Подключение к нашей Jira
jira_host='https://quest-giver.atlassian.net'
auth_jira = JIRA(jira_host, basic_auth=(dict_authorization['username'], dict_authorization['api_token']))
jql_string='project = QG order by created DESC'
jira_list_raw = auth_jira.search_issues(jql_string)


#Создание словаря
jira_list = {}
for issue in jira_list_raw:
    dict_issue = {}
    #dict_issue['key'] = issue
    dict_issue['status'] = issue.fields.status.name
    dict_issue['summary'] = issue.fields.summary
    jira_list[str(issue)] = dict_issue
    
print(jira_list)

#Подключение к Discord
client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#Сообщения
    if message.content.startswith('hello'):
        await message.channel.send('Hello, world!')
    if message.content.startswith('jira'):
        await message.channel.send(jira_list)


client.run(dict_authorization['TOKEN'])

#Работа с DATABASE.JSON
with open('database.json') as f:
    dict_authorization = json.loads(f.read())