# Module Imports
from Reddit_API import Reddit_API
from Twitter_API import Twitter_API
import stock_data
from variables import *

# Library Imports
import pandas as pd
import datetime
import pandas as pd

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    reddit_client = Reddit_API(client_id = REDDIT_CLIENT_ID, client_secret = REDDIT_CLIENT_SECRET, user_agent = REDDIT_USER_AGENT, username = REDDIT_USERNAME, password = REDDIT_PASSWORD, stocks = list(COMPANY_NAME_TO_TICKER.keys()))
    stock_names_found = reddit_client.get_stock_mentions(DESIRED_SUBREDDIT)
    print(f'Stocks Found: {stock_names_found}')
    stockChanges = stock_data.get_stock_price_delta(stock_names_found)
    print(f'Stock Changes: {stockChanges}')

    # Find the stock with the most mentions, how many mentions it has, and how it is changing in the stock market.
    most_mentioned_stock = max(stock_names_found,key=stock_names_found.get)
    most_mentioned_stock_count = stock_names_found[most_mentioned_stock]
    most_mentioned_stock_price_delta = stockChanges[most_mentioned_stock]
        
    seasonal_trends = stock_data.get_seasonal_trends(COMPANY_NAME_TO_TICKER[most_mentioned_stock])
    current_season = stock_data.identify_season(datetime.date.today())
    
    print(f'Seasonal Trends for {most_mentioned_stock}: {seasonal_trends}')
    print(f'Current Season: {current_season}')
    
    seasonal_avg = 0
    for season in seasonal_trends:
        seasonal_avg += seasonal_trends[season]
    seasonal_avg /= 4
    print(f'Seasonal Average for {most_mentioned_stock} is {seasonal_avg}.')

    if seasonal_trends[current_season] > seasonal_avg:
        seasonal_information = f'{most_mentioned_stock.title()} ({COMPANY_NAME_TO_TICKER[most_mentioned_stock]}) stock price tends to be higher in the {current_season}.'# by ${seasonal_trends[current_season] - seasonal_avg}.'
    else:
        seasonal_information = f'{most_mentioned_stock.title()} ({COMPANY_NAME_TO_TICKER[most_mentioned_stock]}) stock price tends to be lower in the {current_season}.'# by ${seasonal_trends[current_season] - seasonal_avg}.' 
    
    next_season = list(seasonal_trends.keys())[(list(seasonal_trends.keys()).index(current_season)+1)%4]
    
    if seasonal_trends[next_season] > seasonal_trends[current_season]:
        seasonal_information += f'\nNext season ({next_season}) tends to be higher than {current_season}.'
    else:
        seasonal_information += f'\nNext season ({next_season}) tends to be lower than {current_season}.'
    
    # stock_with_highest_delta = max(stockChanges.items(), key=lambda x: abs(x[1]))[0]
    # highest_delta_information = f'Highest Change in price: {stock_with_highest_delta.title()} {COMPANY_NAME_TO_TICKER[stock_with_highest_delta]} ${stockChanges[stock_with_highest_delta]}.'

    
    # Create tweet.
    tweet=f"""
Top trending stock on Wall Street Bets
({datetime.date.today()})

Stock: {most_mentioned_stock.title()}
{str(most_mentioned_stock_count)} mention(s) 

${most_mentioned_stock_price_delta} change in value the past 7 days.
{seasonal_information}
"""
    print(f'Tweet length: {len(tweet)}')
    print(f'Tweet:\n {tweet}')
    
    twitter_client = Twitter_API(bearer_token=TWITTER_BEARER_TOKEN,access_token=TWITTER_ACCESS_TOKEN,access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,consumer_key=TWITTER_API_KEY,consumer_secret=TWITTER_API_SECRET)
    # Post Tweet
    twitter_client.post_to_twitter(tweet)
    return tweet

if __name__ == '__main__':
    tweet = main()
    print(tweet)