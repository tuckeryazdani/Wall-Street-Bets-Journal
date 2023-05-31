# Module Imports
from variables import *
# Library Imports
import openai
import time

# Define OpenAI API key
openai.api_key = OPEN_AI_API_KEY

def reply_to_tweet(tweet : str):
    '''
    Parameters:
    tweet - String. This will be the tweet this function responds to.
    This function uses the ChatGPT AI to respond to tweets to give funny responses. This feature is only for fun. Due to me being on the free tier of ChatGPT, I've had to implement
    this function using a try/except that will recursively call itself if the failure it got was due to my free account reaching the rate limit.
    '''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": OPEN_AI_CHARACTER},
                    {"role": "user", "content": 'Respond to this tweet: ' + tweet},
                ]
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        print(result)
        return result
    
    except Exception as e:
        if 'Rate limit reached for default-gpt-3.5-turbo in organization org-1CORpX5iaSNo6Yl4yM9oVi2E on requests per min.' in str(e):
            time.sleep(60)
            reply_to_tweet(tweet)
        else:
            print(e)