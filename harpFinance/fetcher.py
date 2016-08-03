import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    import json
except ImportError:
    import simplejson as json

from yahoo_finance import Share

class Fetcher:
    def __init__(self, stockList):
        if 'SPY' in stockList:
            self.SPY_added = False
            self.stockList = stockList
        else:
            self.SPY_added = True
            stockList.append('SPY')
            self.stockList = stockList
        self.stock = {}
        self.stockInfo = {}
        self.__fetch_stock_objects()

    def __fetch_stock_objects(self):
        for stockNm in self.stockList:
            self.stock[stockNm] = Share(stockNm)

    def fetch_history(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        for stockNm in self.stockList:
            stock = self.stock[stockNm]
            self.stockInfo[stockNm] = stock.get_historical(startDate, endDate)

        for stockNm in self.stockList:
            self.__json2dataframe(stockNm)


    def get_json(self, stockNm):
        return self.stockInfo[stockNm]

    def __json2dataframe(self, stockNm):
        stock_data = self.stockInfo[stockNm]
        stock_names = stock_data[0].keys()
        stockList = [[x[y] for y in stock_names] for x in stock_data]
        stockFrame = pd.DataFrame(stockList, columns = stock_names)
        stockFrame['Date'] = pd.to_datetime(stockFrame['Date'])
        stockFrame.set_index('Date', inplace=True)
        #print stockFrame
        self.stockInfo[stockNm] = stockFrame

    def __join_frames(self, factor, makeFloat = True):
        dates = pd.date_range(self.startDate, self.endDate, name = 'Date')
        df_base = pd.DataFrame(dates)
        df_base.set_index('Date', inplace = True)
        # sort the dataframe by time
        df_SPY = self.stockInfo['SPY'][[factor]].rename(columns = {factor: 'SPY'})
        df_base = df_base.join(df_SPY, how='inner')

        for stockNm in self.stockList:
            if stockNm != 'SPY':
                df = self.stockInfo[stockNm].ix[:,[factor]]
                df = df.rename(columns = {factor: stockNm})
                df_base = df_base.join(df,how='inner')

        self.df = df_base.sort()
        # Do the gorward fill followed by backward fill
        self.df.fillna(method='ffill', inplace = True)
        self.df.fillna(method='bfill', inplace = True)
        if self.SPY_added:
            self.df.drop('SPY', axis=1, inplace=True)
        if makeFloat:
            self.df = self.df.astype(float)

    def get_dataframe(self, factor):
        self.__join_frames(factor)
        return self.df

    def normalize_data(self, df):
        df = df/ df.ix[0,:]
        return df

    def plot_dataframe(self, title = "Stock Prices", normalization = True):
        if normalization:
            df = self.normalize_data(self.df)
        else:
            df = self.df

        ax = df.plot(title=title,fontsize = 12)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
