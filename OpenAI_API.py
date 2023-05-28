# Module Imports
from variables import *
# Library Imports
import openai

# Define OpenAI API key
openai.api_key = OPEN_AI_API_KEY

def reply_to_tweet(tweet : str):
    '''
    Parameters:
    tweet - String. This will be the tweet this function responds to.
    '''
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