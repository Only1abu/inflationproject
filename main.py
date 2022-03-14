

import sqlalchemy
import pymysql
import pandas as pd
import requests
import numpy as np
import ta



pymysql.install_as_MySQLdb()
etfs = ['XSD','XLE','XLF']

def etfToSchema(etf):
    engine= sqlalchemy.create_engine('mysql://root:Tdan2118!@127.0.0.1:3306/')
    engine.execute(sqlalchemy.schema.CreateSchema(etf))

#for i in etfs:
    etfToSchema(i)

# must specify the user agent header in order to use pandas read_html method,
# xleHTML is list object since we passed in the text attribute from requests library as r.text
r = requests.get('https://ycharts.com/companies/XSD/holdings', headers = {'User-Agent':'Mozilla/5.0'})
xsdHTML = pd.read_html(r.text)

#turns list into an array, then turns array to a dataframe due to how the list was pulled from Ycharts website
#We must specify the xsdArray as the 1st list object because requests pulls 2 arrays from Ycharts website
xsdArray = (np.array(xsdHTML, dtype=object)[1])

#turns the array into a dataframe object
xsdDF = pd.DataFrame(xsdArray, columns=['Symbol'])

#turns dataframe column which is a series back to a list since we don't need the other columns info like price, %weight
xsdTickers = ((xsdDF['Symbol']).values.tolist())

#XLE etf data
r2 = requests.get('https://ycharts.com/companies/XLE/holdings',headers = {'User-Agent':'Mozilla/5.0'})
xleHTML = pd.read_html(r2.text)
xleArray = (np.array(xleHTML, dtype=object)[1])
xleDF = pd.DataFrame(xleArray, columns=['Symbol'])
xleTickers = ((xleDF['Symbol']).values.tolist())

#XLF etd data
r3 = requests.get('https://ycharts.com/companies/XLF/holdings',headers = {'User-Agent':'Mozilla/5.0'})
xlfHTML = pd.read_html(r3.text)

xlfArray = (np.array(xlfHTML, dtype=object)[1])
xlfDF = pd.DataFrame(xlfArray, columns=['Symbol'])
xlfTickers = ((xlfDF['Symbol']).values.tolist())

#must change Berhshire Hathaway ticker from BRK.B to BRK-B for yahoo finance listing
xlfTickers[0]='BRK-B'

#Using a dictionary to map our ETFs in MySQL database to tickers
mapper = {'XSD': xsdTickers, 'XLE':xleTickers, 'XLF':xlfTickers}

import yfinance as yf

#nested for loop that fills up the MySQL databases with ticker data from Yahoo finance
#I chose the March 23rd, 2020 date because that was the lowest $SPY closing price during the COVID shock drop
for etf in etfs:
    engine = sqlalchemy.create_engine('mysql://root:Tdan2118!@127.0.0.1:3306/' + etf)
    for ticker in mapper[etf]:
        df= yf.download(ticker, start='2020-03-13')
        df= df.reset_index()
         # You must have reset_index in order to avoid date being the index of the dataframe
         # since that's how Yahoo FInance will return the data frame
        df.to_sql(ticker, engine)







