# inflationproject. 
### Store and analyze large amounts stock data with Python and MySQL (ETL practice)
## Goals in this project.
1. Use what I learned in my Python and SQL courses, while also implementing Python's Pandas, Numpy, and various other libraries.
2. Gain web scraping experience with Python
3. Store large amounts of data in a SQL database.
4. Build familiarity with Python's stock and analysis features with yfinance and ta (technical analyis) libraries.
5. Build a project relevant to our current political and global climate (Inflation is rampant)!

## Major Steps 
### 1. Database Setup.
#### Needed to import the following libraries (sqlalchemy, pymysql)
##### **VIP* When using sqlalchemy's create_engine() function, you can use a different version of SQL. The user root, host, and directory will also differ. 
```
    import sqlalchemy
    import pymysql
    
    pymysql.install_as_MySQLdb()...
    
    def etfToSchema(etf):
    engine= sqlalchemy.create_engine('mysql://root:Tdan2118!@127.0.0.1:3306/')
    engine.execute(sqlalchemy.schema.CreateSchema(etf))
   
``` 

### 2. Webscraping.
#### I scraped ETF data from ycharts. It's imperative to import python's requests library as you will face challenges when using pandas' read_html function without it.
#### [XSD ETF](https://ycharts.com/companies/XSD/holdings)
#### [XLE ETF](https://ycharts.com/companies/XLE/holdings)
#### [XLF ETF](https://ycharts.com/companies/XLF/holdings)



### 3. Importing Stock Data from Yfinance to SQL Database.
#### I chose to March 13th, 2020 as the beginning date because that was the lowest point of the major indices after the Covid shock drop. 
#### Data can also be skewed if extended to March 2022 due to Russian-Ukrainian war and shocking effect on markets.
##### More SQL Database implementation in main python file with the GetTables() and GetPrices() Methods 
```
for etf in etfs:
    engine = sqlalchemy.create_engine('mysql://root:Tdan2118!@127.0.0.1:3306/' + etf)
    for ticker in mapper[etf]:
        df= yf.download(ticker, start='2020-03-13')
        df= df.reset_index()
         # You must have reset_index in order to avoid date being the index of the dataframe
         # since that's how Yahoo FInance will return the data frame
        df.to_sql(ticker, engine)
 ```
 
### 4. Choosing your techinical indicators to assess stock data with.
#### (I chose MACD because I use it heavily when trading stocks and options)

 ```
    def MACDindicator(priceFrame):
    priceFrame['MACD_value']= ta.trend.macd_diff(priceFrame.Close)
    priceFrame['MACD decision']= np.where((priceFrame.MACD_value > 0) & (priceFrame.MACD_value > priceFrame.MACD_value.shift(1)),True, False)


    def applyMACD(etf):
    prices=getPrices(etf)
    for frame in prices:
        MACDindicator(frame)
    return prices
  ```
