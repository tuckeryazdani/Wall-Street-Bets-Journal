import yfinance as yf
import requests

def getStock(search_term):
    results = []
    query = requests.get(f'https://yfapi.net/v6/finance/autocomplete?region=IN&lang=en&query={search_term}', 
    headers={
        'accept': 'application/json',
        'X-API-KEY': 'API_KEY'
    })
    response = query.json()
    for i in response['ResultSet']['Result']:
        final = i['symbol']
        results.append(final)

    try:
        stock = yf.Ticker(results[0])
        price = stock.info["regularMarketPrice"]
        full_name = stock.info['longName']
        curreny = stock.info["currency"]
    except Exception as e:
        print('Something went wrong')

    return f"The stock price of {full_name} is {price} {curreny}"

stock = input("Enter the company's name: ")
final = getStock(stock)
print(final)