# Module Imports
from variables import *
import OpenAI_API

# Library Imports
import tweepy
import datetime

class Twitter_API:
    
    def __init__(self):
        self.client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN
                                    , access_token=TWITTER_ACCESS_TOKEN
                                    , access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
                                    , consumer_key=TWITTER_API_KEY
                                    , consumer_secret=TWITTER_API_SECRET
                                    , return_type=dict)

        # auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        # auth.set_access_token(TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET)
        # self.api = tweepy.API(auth)

    def post_to_twitter(self, tweet : str):
        if len(tweet) > 280:
            raise Exception('Tweet goes over 280 character limit. Please revise.')
        try:
            self.client.create_tweet(text=tweet)
        except Exception as e:
            # Open file with 'a' parameter for appending only.
            with open('logs.txt','a') as f:
                f.write(f'{datetime.date.today()}\n{e}\n\n')
            raise e
    
    def respond_to_mentions(self):
        # Open .txt file that stores tweet IDs of tweets we responded to in the past
        with open('mentions.txt','r+') as f:
            # Query all tweets that contain "@WSB_Journal"
            tweets = self.client.search_recent_tweets(query='@WSB_Journal',max_results=TWITTER_MAX_QUERY_RESULTS_FOR_MENTIONS)
            # Get list of tweet IDs we have already responded to
            mentions = f.read()
            for tweet in tweets['data']:
                if tweet['id'] not in mentions:
                    # Respond to tweet on Twitter
                    self.client.create_tweet(text=OpenAI_API.reply_to_tweet(tweet['text']),in_reply_to_tweet_id=tweet['id'])
                    # Add tweet ID to the mentions.txt file to store what tweets we have responded to already.
                    f.write(tweet['id']+'\n')
                    # Reset pointer
                    f.seek(0)
                    # Refresh mentions to include the newly added tweet IDs
                    mentions = f.read()

# Manually trigger mention response
if __name__ == '__main__':
    twitter = Twitter_API()
    twitter.respond_to_mentions()
