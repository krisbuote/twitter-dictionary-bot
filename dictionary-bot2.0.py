'''
Twitter bot that uses Tweepy.
The bot auto replies to '@DefineMyWord [word]' and provides the Oxford Dictionary definition.
The bot also searches twitter generally for 'what is the definition of' and provides the definition the user is seeking.

Oxford-Dictionary API is used via dictAPI.py

Author: Kristopher Buote, 7/29/2018
'''
import tweepy
import json
from dictAPI import *

# Load config file containing API keys and tokens
config = json.loads(open("config.json").read()) # keys stored in json file named 'config'
consumer_key, consumer_secret = config["twitter_api"]["consumer_key"], config["twitter_api"]["consumer_secret"]
access_token, access_token_secret = config["twitter_api"]["access_token"], config["twitter_api"]["access_token_secret"]

# Authenticate with tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if trackTerms[0] in status.text: # If contains '@DefineMyWord define'
            replyWithDefinition(status, trackTerms[0])
        elif trackTerms[1] in status.text: # If contains 'what is the definition of a'
            replyWithDefinition(status, trackTerms[1])
        elif trackTerms[2] in status.text: # If contains 'what is the definition of'
            replyWithDefinition(status, trackTerms[2])

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

### Create the streaming object
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

### Track these terms live on Twitter
trackTerms = ['@DefineMyWord define', 'what is the definition of a', 'what is the definition of']
myStream.filter(track=trackTerms, async=True, languages=['en'])


def findWord(_text, _keyword):
    ''' Finds the word after the tracked term in the tweeter's text. '''
    if _keyword in _text:
        text_after_keyword = _text.split(_keyword + ' ')[1] # Split text string after 'define '
        _word = text_after_keyword.split(' ')[0].split(',')[0].split('.')[0].split(';')[0].split('!')[0] # isolate the word requesting to be defined
        return _word
    else:
        return None

def replyWithDefinition(_status, _keyword):
    ''' Replies to new tweets if they contain 'define [word]' or 'what is the definition of [word]'  '''
    try:
        _text = _status.text # The tweet's text
        user_handle = _status.user.screen_name # Who sent the tweet
        _word = findWord(_text, _keyword) # Find the word they want defined

        if _word is not None: # if they correctly asked 'define [word]', reply with definition
            firstDefinition, firstDefinitionShort = define(_word) # Call the api to define the word
            replyBase = '@' + user_handle + ' the definition of ' + _word + ' is: '

            if len(replyBase + firstDefinition) <= 280:
                api.update_status(status=(replyBase + firstDefinition))
            elif len(replyBase + firstDefinitionShort) <= 280:
                api.update_status(status=(replyBase + firstDefinition))
            else:
                _reply = 'Sorry @' + user_handle + ", the definition doesn't fit in a tweet. \
                You can blame Oxford Dictionaries."
                api.update_status(status=_reply)
            print("Definition sent to @" + str(user_handle))

    except Exception as e: print(e)






