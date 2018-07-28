'''
This is a Twitter Bot program that automatically replies to requests to define words.
Tweepy is used to manage the Twitter API.
The Oxford Dictionary is used to get definitions.

Author: Kristopher Buote 7/28/2018

'''
import tweepy
from dictAPI import *
import json

# Load config file containing API keys and tokens
config = json.loads(open("config.json").read()) # keys stored in json file named 'config'
consumer_key, consumer_secret = config["twitter_api"]["consumer_key"], config["twitter_api"]["consumer_secret"]
access_token, access_token_secret = config["twitter_api"]["access_token"], config["twitter_api"]["access_token_secret"]

# Authenticate with tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

savedStatuses = []
keywords = ['define', 'definition of']

def searchTweets(searchTerm):
    """
    gets 50 search results of the string, search, and returns them as a list
    of tweet objects
    """
    searchResults = [status for status in tweepy.Cursor(api.search, q=searchTerm).items(50)]
    return searchResults


def _newStatuses(_searchResults, savedStatuses):
    '''Compares new search results with saved results to filter out tweets already replied to.'''
    _newStatuses = [status for status in _searchResults if status not in savedStatuses]
    return _newStatuses


def findWord(_text):
    ''' Finds the word after the word 'define' in the tweeter's text. '''
    if keywords[0] in _text: #if 'define' in tweet text
        keyword = keywords[0]
        text_after_keyword = _text.split(keyword + ' ')[1] # Split text string after 'define '
        _word = text_after_keyword.split(' ')[0].split(',')[0].split('.')[0].split(';')[0].split('!')[0] # isolate the word requesting to be defined
        return _word
    else:
        return None

def replyWithDefinition(_status):
    ''' Replies to new tweets if they contain 'define [word]'  '''
    try:
        _text = _status.text # The tweet's text
        user_handle = _status.user.screen_name # Who sent the tweet
        _word = findWord(_text) # Find the word they want defined

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
            print("Tweet sent to @" + str(user_handle))

    except Exception as e: print(e)

def replyToTweets(_newStatuses):
    ''' Reply to the new tweets that haven't been replied to yet.'''
    for i in range(len(_newStatuses)):
        _status = _newStatuses[i]
        replyWithDefinition(_status)


while True:

    searchResults = searchTweets('@DefineMyWord') #find tweets with a keyword 'definition of'
    newStatuses = _newStatuses(searchResults, savedStatuses) # separate new statuses from old ones that have been replied to
    replyToTweets(newStatuses) # Reply to new statuses (if applicable)
    savedStatuses = searchResults # Updated saved statuses



