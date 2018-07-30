# twitter-dictionary-bot
A twitter bot that replies to tweeter's requests for definitions.

Tweepy is used to manage the Twitter API. The Oxford Dictionary is used for definitions.

The bot responds to '@DefineMyWord define xxx'. It also listens to the Twitter stream for anyone who includes 'what is the definition of xxx' in their tweet and automatically replies to them with the definition. The main definition is offered in reply, or a shortened version is offered if it's too long for a tweet.

The API keys are stored in a config.json file and loaded in.
