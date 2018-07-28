'''
A simple program to call the Oxford Dictionary API.
app_id and app_key are strored in a json file

Author: Kristopher Buote 7/28/2018
'''
import requests
import json

config = json.loads(open('config.json').read())
app_id = config['dictionary_api']["app_id"]
app_key = config['dictionary_api']["app_key"]
base = config['dictionary_api']["baseURL"]

language = 'en/'
service = 'entries/'

def define(word):
    requestUrl = base + service + language + word

    request = requests.get(requestUrl, headers={'app_id': app_id, 'app_key': app_key})

    data = request.json()
    senses = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
    firstDefinition = senses[0]['definitions'][0]
    shortDefinition = senses[0]['short_definitions'][0]

    return firstDefinition, shortDefinition
