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
import requests
from bs4 import BeautifulSoup

# Seasonal data for the year 2000. (Leap year)
START_OF_YEAR = datetime.date(2000,1,1)
END_OF_YEAR = datetime.date(2000,12,31)

START_OF_WINTER = datetime.date(2000,12,21)
END_OF_WINTER   = datetime.date(2000,3,19)

START_OF_SPRING = datetime.date(2000,3,20)
END_OF_SPRING   = datetime.date(2000,6,20)

START_OF_SUMMER = datetime.date(2000,6,21)
END_OF_SUMMER   = datetime.date(2000,9,22)

START_OF_FALL = datetime.date(2000,9,23)
END_OF_FALL   = datetime.date(2000,12,20)
# End seasonal data for year 2000. (Leap year)

# Define a function to get the company name to ticker dictionary
def get_company_name_to_ticker_dict():
    # Use a constant for the URL
    URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    # Get the page content and parse it with BeautifulSoup
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Find the table element with the class 'wikitable sortable'
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    # Find all the table rows
    rows = table.findAll('tr')
    
    # Initialize an empty dictionary
    company_name_to_ticker = {}
    
    # Loop through the rows, skipping the header row
    for row in rows[1:]:
        # Find all the table cells in the row
        data = row.findAll('td')
        
        # Get the ticker and name from the first and second cell
        ticker = data[0].text.strip()
        name = data[1].text.strip()
        
        # Handle some special cases for Google and Meta
        if ticker == 'GOOGL':
            name = 'Google'
        elif ticker == 'META':
            name = 'Meta'
        
        # Add the name and ticker to the dictionary, using lower case for name and upper case for ticker
        company_name_to_ticker[name.lower()] = ticker.upper()
    
    # Return the dictionary
    return company_name_to_ticker
    
def get_stock_price_change(stocksFound : typing.Union[list,dict], COMPANY_NAME_TO_TICKER: dict):
    '''
    Returns a dictionary containing popular stock trends from the list/dictionary input.
    Parameters:
    stocksFound - List or Dictionary containing the name of companies we are interested in analyzing. NOTE: If using a dctionary the keys must be company names.
    Output:
    Returns a dictionary of stocks and how much their value has changed in the past 7 days. 
    '''
    stock_price_change={}
    
    for stock in stocksFound:
        # Create a Yahoo finance Ticker object by converting the company names to their ticker strings ie "Tesla" -> "TSLA" then get the price data for the past 7 days.
        ticker = yf.Ticker(COMPANY_NAME_TO_TICKER[stock]).history(period="7d")["Close"]
        # Get the difference in price for the past 7 days rounded for currency.
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

    # Set the year to be "2000" to include leap year day
    date = date.replace(year=2000)
    # Check which season the date falls in and return the corresponding string
    if (date >= pd.Timestamp(START_OF_YEAR) and date <= pd.Timestamp(END_OF_WINTER)) or (date >= pd.Timestamp(START_OF_WINTER) and date <= pd.Timestamp(END_OF_YEAR)):
        return 'Winter'
    elif date >= pd.Timestamp(START_OF_SPRING) and date <= pd.Timestamp(END_OF_SPRING):
        return 'Spring'
    elif date >= pd.Timestamp(START_OF_SUMMER) and date <= pd.Timestamp(END_OF_SUMMER):
        return 'Summer'
    elif date >= pd.Timestamp(START_OF_FALL) and date <= pd.Timestamp(END_OF_FALL):
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
    
    # Modify base URL to query NASDAQ for ticker data.
    ticker_url = f'https://data.nasdaq.com/api/v3/datasets/WIKI/{ticker}.csv'
    
    # Query NASDAQ using the requests library.
    with requests.Session() as s:
        response = s.get(ticker_url,headers={'Accept': 'application/json'})
        response = response.content.decode('utf-8')

    # Convert NASDAQ data into a Pandas dataframe.
    data = io.StringIO(response)
    df_nasdaq = pd.read_csv(data,delimiter=',')

    # Only keep columns we are interested in
    df_nasdaq = df_nasdaq[['Date','Close']]

    # Cast "Date" column to datetime
    df_nasdaq['Date'] = pd.to_datetime(df_nasdaq['Date'])
    
    # Identify the season of every date in the dataframe.
    df_nasdaq['Season'] = df_nasdaq['Date'].apply(lambda x: identify_season(x))
    
    # Get unique years included in the NASDAQ data.
    unique_years = df_nasdaq['Date'].dropna().dt.year.nunique()
    print(f'Unique Years in NASDAQ flat file: {unique_years}')
    
    # Create dictionary to store seasonal price data.
    seasonal_values = {'Winter':None,'Spring':None,'Summer':None,'Fall':None}
    
    # Get the maximum number of rows for every season to avoid having one season that has more days than another.
    max_possible_row_count = float('inf')
    for season in seasonal_values:
        if len(df_nasdaq[df_nasdaq['Season'] == season]) <= max_possible_row_count:
            max_possible_row_count = len(df_nasdaq[df_nasdaq['Season'] == season])
    
    # Get average seasonal stock price information rounded for currency.
    for season in seasonal_values:
        seasonal_values[season] = round(df_nasdaq[df_nasdaq['Season'] == season]['Close'].head(max_possible_row_count).mean()/unique_years,2)
    
    return seasonal_values