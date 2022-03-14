import sqlalchemy
import pymysql
import pandas as pd
import requests
import numpy as np
import ta

pymysql.install_as_MySQLdb()
engine = sqlalchemy.create_engine('mysql://root:Tdan2118!@127.0.0.1:3306/')

#getTables() is a method that takes the etf as an string input and retrieves price data from MySQL for the etf you pass
# in, returning a dataframe object

def getTables(etf):
    #In order to communicate to MySQL from Python script, you must use string with 3 quotes
    mySQlquery = f"""SELECT table_name FROM information_schema.tables WHERE table_schema ='{etf}'"""
    df = pd.read_sql(mySQlquery, engine)
    #this next statement is necessary for the getPrices method below, we are creating a new column named Schema in our
    #our data frame
    df['Schema'] = etf
    return df


#this getPrices() method takes a dataframe object as a parameter and traverses through the matching SQL schema to get
# price data for each stock in the SQL schema

def getPrices(etf):
    priceList = []
    #loop that communicates with MySQL and traverses through the schemas and tables for the ticker that you choose
    for table, schema in zip(etf.TABLE_NAME, etf.Schema):
        #must use the special quotes inside the formatted string in order to communicate with MySQL
        #We are adding the closing prices stored in MySQL database to the empty priceList
        mySQLdata = schema+'.'+f'`{table}`'
        priceList.append(pd.read_sql(f"SELECT Date, Close FROM {mySQLdata}", engine))
    return priceList

#this MACDindicator() method takes a dataframe as input and uses Python's technical analysis library to add new columns
# to our dataframe, then uses the MACD methods to compare subsequent rows in our dataframe, this method is called upon in the
# applyMACD() method below

def MACDindicator(priceFrame):
    priceFrame['MACD_value']= ta.trend.macd_diff(priceFrame.Close)
    priceFrame['MACD decision']= np.where((priceFrame.MACD_value > 0) & (priceFrame.MACD_value > priceFrame.MACD_value.shift(1)),True, False)


def applyMACD(etf):
    prices=getPrices(etf)
    for frame in prices:
        MACDindicator(frame)
    return prices

xle = getTables('XLE')
print(xle.loc[1], applyMACD(xle)[1])

