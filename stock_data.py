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
    stockChange={}
    
    if "microsoft" in stocksFound:
        msft = yf.Ticker("MSFT").history(period="7d")["Close"]
        msftChange=msft[-1]-msft[0]
        stockChange["microsoft"] = msftChange
        
    if "google" in stocksFound:
        goog = yf.Ticker("GOOG").history(period="7d")["Close"]
        googChange=goog[-1]-goog[0]
        stockChange["google"] = googChange
        
    if "meta" in stocksFound:
        fb=yf.Ticker("META").history(period="7d")["Close"]
        fbChange=fb[-1]-fb[0]
        stockChange["meta"] = fbChange
        
    if "amazon" in stocksFound:
        amzn=yf.Ticker("AMZN").history(period="7d")["Close"]
        amznChange=amzn[-1]-amzn[0]
        stockChange["amazon"] = amznChange
        
    if "netflix" in stocksFound:
        nflx = yf.Ticker("NFLX").history(period="7d")["Close"]
        nflxChange=nflx[-1]-nflx[0]
        stockChange["netflix"] = nflxChange
        
    return stockChange

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
    ticker_url = f'https://data.nasdaq.com/api/v3/datasets/WIKI/{ticker}.csv'

    with requests.Session() as s:
        response = s.get(ticker_url,headers={'Accept': 'application/json'})
        response = response.content.decode('utf-8')

    data = io.StringIO(response)
    df_nasdaq = pd.read_csv(data,delimiter=',')

    # Only keep columns we are interested in
    df_nasdaq = df_nasdaq[['Date','Open','Close']]

    # Cast "Date" column to datetime
    df_nasdaq['Date'] = pd.to_datetime(df_nasdaq['Date'])
    df_nasdaq['Season'] = df_nasdaq['Date'].apply(lambda x: identify_season(x))
        
    seasonal_values = {'Winter':None,'Spring':None,'Summer':None,'Fall':None}
    max_possible_row_count = float('inf')
    for season in seasonal_values:
        if len(df_nasdaq[df_nasdaq['Season'] == season]) <= max_possible_row_count:
            max_possible_row_count = len(df_nasdaq[df_nasdaq['Season'] == season])
    
    for season in seasonal_values:
        seasonal_values[season] = df_nasdaq[df_nasdaq['Season'] == season]['Close'].head(max_possible_row_count).mean()
    
    return seasonal_values