from calendar import different_locale
from email import message
import discord
import os
from jira import JIRA
import json
from os import getenv
from dotenv import load_dotenv
import psycopg2



#PGSQL environment
uri = getenv('URI')
#Connected to DB
conn = psycopg2.connect(uri, sslmode='require')
cur = conn.cursor()
#Authorization
with open('authorization.json') as f:
    dict_authorization = json.loads(f.read())

#Heroku authorization environment
jira_token = getenv('API_TOKEN_JIRA')
jira_username = getenv('USERNAME_JIRA')
discord_token = getenv('DISCORD_TOKEN')

#Подключение к нашей Jira
jira_host='https://quest-giver.atlassian.net'
auth_jira = JIRA(jira_host, basic_auth=(jira_username, jira_token))
jql_string ='project = QG order by created DESC'
jira_list_raw = auth_jira.search_issues(jql_string)

#Create issues list from Jira
# jira_list = []
# for issue in jira_list_raw:
#     list_issue = [str(issue), issue.fields.status.name, issue.fields.summary]
#     jira_list.append(list_issue)

dict_jira = {}
for issue in jira_list_raw:
    dict_jira[str(issue)] = [issue.fields.status.name, issue.fields.summary]
print(dict_jira)

#Подключение к Discord
client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



#Write DB
def write_db():
    cur.execute ("""
    INSERT INTO public.jira_tasks (key, status, summary) VALUES
    ('QG-4', 'Working', 'Работа пример');
    """)
    conn.commit()

#Read DB
def read_db():
    cur.execute ("""
    SELECT key, status, summary
	FROM public.jira_tasks;;
    """)
    list_result = cur.fetchall()
    dict_db = {}
    for issue in list_result:
        dict_db[issue[0]] = [issue[1], issue[2]]
    return dict_db
dict_db_save = read_db()
print(read_db())

#Difference keys. Find new tasks.
def diff_keys():
    keys_db = list(read_db().keys())
    keys_jira = list(dict_jira.keys())
    difference = [x for x in keys_db + keys_jira if x not in keys_db]
    return difference
print(diff_keys())

#Changed status.
def change_status():
    announce_dict = {}
    for key in dict_jira.keys():
        if key in dict_db_save and dict_jira[key][0] != dict_db_save[key][0]:
           announce_dict[key] = dict_jira[key][0]
    return announce_dict



print(change_status())
  
#print(change_status())


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #Message
    if message.content.startswith('hello'):
        await message.channel.send('Hello, world!')








#Launch bot
#client.run(discord_token)




