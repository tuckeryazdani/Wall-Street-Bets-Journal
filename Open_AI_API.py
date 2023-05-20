# Module Imports
from variables import *

# Library Imports
import openai

openai.api_key = OPEN_AI_API_KEY

def reply_to_tweet(tweet):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a chatbot. Respond to messages as if you are a memeber of the subreddit WallStreetBets. Do this excessively and annoyingly. You are the Wall Street Bets Journal. Be more excessive and energetic. You are a trader/journalist. Have fun with it. Use more emotes. You MUST keep the character limit to your reply under 200 characters including spaces. Do not use words like age and degenerate. Be extremely energetic, ambitious, and especially funny."},
                {"role": "user", "content": 'Respond to this tweet: '+tweet},
            ]
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    print(result)
    return result