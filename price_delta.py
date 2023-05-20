import requests
import pandas as pd
import io
import datetime
import json

def identify_season(date):
    
    if (date >= begin_year_date and date <= winter_end_date) or (date >= winter_begin_date and end_year_date):
        return 'Winter'
    elif date >= spring_begin_date and date <= spring_end_date:
        return 'Spring'
    elif date >= summer_begin_date and date <= summer_end_date:
        return 'Summer'
    elif date >= fall_begin_date and date <= fall_end_date:
        return 'Fall'
        
def get_seasonal_trends(ticker:str):
    ticker_url = f'https://data.nasdaq.com/api/v3/datasets/WIKI/{ticker}.csv'

    with requests.Session() as s:
        response = s.get(ticker_url,headers={'Accept': 'application/json'})
        response = response.content.decode('utf-8')
        # response = json.loads(response)
        # if "quandl_error" in response:
        #     raise Exception(response['quandl_error']['code'] + ': ' + response['quandl_error']['message'])
            

    data = io.StringIO(response)
    df_nasdaq = pd.read_csv(data,delimiter=',')

    # Only keep columns we are interested in
    df_nasdaq = df_nasdaq[['Date','Open','Close']]

    # Cast "Date" column to datetime
    df_nasdaq['Date'] = pd.to_datetime(df_nasdaq['Date'])

    # df = df[df['Date'] < pd.to_datetime(datetime.date.today() - datetime.timedelta(days=7))]

    df_nasdaq['Season'] = None
    df_nasdaq['Season'] = df_nasdaq['Date'].apply(lambda x: identify_season(x.strftime('%m-%d')))

    if df_nasdaq['Season'].isnull().any() == True:
        raise Exception('Error in fucntion: identify_season')
        
    df_nasdaq['Year'] = df_nasdaq['Date'].dt.strftime('%Y')
    
    unique_years = df_nasdaq['Year'].unique()
    seasons = {'Winter':None,'Spring':None,'Summer':None,'Fall':None}
    
    # df_price_delta = pd.DataFrame(columns=['Year','Season','Delta'])
    
    max_possible_row_count = float('inf')
    for season in seasons:
        if len(df_nasdaq[df_nasdaq['Season'] == season]) <= max_possible_row_count:
            max_possible_row_count = len(df_nasdaq[df_nasdaq['Season'] == season])
    
    for season in seasons:
        seasons[season] = df_nasdaq[df_nasdaq['Season'] == season]['Close'].head(max_possible_row_count).mean()
    
    return seasons
        
    # for year in unique_years:
    #     df_curr_year = df_nasdaq[df_nasdaq['Year'] == year].reset_index(drop=True)
    #     df_curr_year.sort_values(by='Date',ascending=False)

    #     for season in seasons:
    #         print(df_curr_year)
        
    #     first_close = df_curr_year.at[0,'Close']
    #     last_close  = df_curr_year.at[len(df_curr_year)-1,'Close']
        
    #     print(last_close-first_close)
    #     print(df_price_delta)


begin_year_date = datetime.date(2000,1,1).strftime('%m-%d')
end_year_date = datetime.date(2000,12,31).strftime('%m-%d')

winter_begin_date = datetime.date(2000,12,21).strftime('%m-%d')
winter_end_date   = datetime.date(2000,3,19).strftime('%m-%d')

spring_begin_date = datetime.date(2000,3,20).strftime('%m-%d')
spring_end_date   = datetime.date(2000,6,20).strftime('%m-%d')

summer_begin_date = datetime.date(2000,6,21).strftime('%m-%d')
summer_end_date   = datetime.date(2000,9,22).strftime('%m-%d')

fall_begin_date = datetime.date(2000,9,23).strftime('%m-%d')
fall_end_date   = datetime.date(2000,12,20).strftime('%m-%d')

ticker = 'TSLA'

get_seasonal_trends(ticker)


