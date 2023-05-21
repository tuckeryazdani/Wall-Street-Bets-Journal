# Module Imports
from variables import *

# Library Imports
import datetime
import requests
import pandas as pd
import io
import yfinance as yf
import typing

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_stock_price_delta(stocksFound : typing.Union[list,dict]):
    '''
    Returns a dictionary containing popular stock trends from the list/dictionary input.
    Parameters:
    stocksFound - List or Dictionary containing the name of companies we are interested in analyzing. NOTE: If using a dctionary the keys must be company names.
    Output:
    Returns a dictionary of stocks and how much their value has changed in the past 7 days. 
    '''
    stock_price_change={}
    
    for stock in stocksFound:
        ticker = yf.Ticker(COMPANY_NAME_TO_TICKER[stock]).history(period="7d")["Close"]
        stock_price_change[stock] = round(ticker[-1]-ticker[0],2)
    
    return stock_price_change

def identify_season(date : datetime.date):
    '''
    Given a date this function will return what season it is in. It will set the year to be "2000" to include leap year day.
    Parameters:
    date - datetime date that we want to find the season of.
    Output:
    Returns string value of the season of the input date.
    '''
    date = date.replace(year=2000)
    if (date >= START_OF_YEAR and date <= END_OF_WINTER) or (date >= START_OF_WINTER and date <= END_OF_YEAR):
        return 'Winter'
    elif date >= START_OF_SPRING and date <= END_OF_SPRING:
        return 'Spring'
    elif date >= START_OF_SUMMER and date <= END_OF_SUMMER:
        return 'Summer'
    elif date >= START_OF_FALL and date <= END_OF_FALL:
        return 'Fall'

def get_seasonal_trends(ticker : str):
    '''
    Get stock information from NASDAQ and determine the seasonal averages for a specific stock.
    Parameters:
    ticker - String value of the company's ticker symbol.
    Output:
    seasonal_values - Dictionary that has a key value of one of the four seasons and a value pair that is the average value of the stock durring that season.
    '''
    # Swap META ticker for FB ticker to get historical data. (META is a newer ticker symbol)
    if ticker == 'META':
        ticker = 'FB'
    
    ticker_url = f'https://data.nasdaq.com/api/v3/datasets/WIKI/{ticker}.csv'
    
    with requests.Session() as s:
        response = s.get(ticker_url,headers={'Accept': 'application/json'})
        response = response.content.decode('utf-8')

    # print(f'Response for {ticker_url}: {response}')
    data = io.StringIO(response)
    df_nasdaq = pd.read_csv(data,delimiter=',')

    # Only keep columns we are interested in
    df_nasdaq = df_nasdaq[['Date','Open','Close']]

    # Cast "Date" column to datetime
    df_nasdaq['Date'] = pd.to_datetime(df_nasdaq['Date'])
    df_nasdaq['Season'] = df_nasdaq['Date'].apply(lambda x: identify_season(x))
    
    unique_years = df_nasdaq['Date'].dropna().dt.year.nunique()
    print(f'Unique Years in NASDAQ flat file: {unique_years}')
    
    seasonal_values = {'Winter':None,'Spring':None,'Summer':None,'Fall':None}
    max_possible_row_count = float('inf')
    for season in seasonal_values:
        if len(df_nasdaq[df_nasdaq['Season'] == season]) <= max_possible_row_count:
            max_possible_row_count = len(df_nasdaq[df_nasdaq['Season'] == season])
    
    for season in seasonal_values:
        seasonal_values[season] = round(df_nasdaq[df_nasdaq['Season'] == season]['Close'].head(max_possible_row_count).mean()/unique_years,2)
    
    return seasonal_values