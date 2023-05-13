import tweepy
import datetime
from variables import *

class Twitter_API:
    
    def __init__(self):
        self.twitter = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN,access_token=TWITTER_ACCESS_TOKEN,access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,consumer_key=TWITTER_API_KEY,consumer_secret=TWITTER_API_SECRET)        

    def __init__(self,bearer_token,access_token,access_token_secret,consumer_key,consumer_secret):
        self.twitter = tweepy.Client(bearer_token=bearer_token,access_token=access_token,access_token_secret=access_token_secret,consumer_key=consumer_key,consumer_secret=consumer_secret)        
    
    def post_to_twitter(self, tweet : str):
        try:
            self.twitter.create_tweet(text=tweet)
        except Exception as e:
            # Open file with 'a' parameter for appending only.
            with open('logs.txt','a') as f:
                f.write(f'{datetime.date.today()}\n{e}\n\n')
            raise e