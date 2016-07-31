import numpy as np
import pandas as pd
try:
    import json
except ImportError:
    import simplejson as json

from yahoo_finance import Share

class Fetcher:
    def __init__(self, stockList):
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
        dates = pd.date_range(self.startDate, self.endDate)
        df_base = pd.DataFrame(dates, columns=['Date'])
        df_base.set_index('Date', inplace = True)
        df_SPY = self.stockInfo['SPY'][[factor]].rename(columns = {factor: 'SPY'})
        df_base = df_base.join(df_SPY, how='inner')

        for stockNm in self.stockList:
            if stockNm != 'SPY':
                df = self.stockInfo[stockNm].ix[:,[factor]]
                df = df.rename(columns = {factor: stockNm})
                df_base = df_base.join(df,how='inner')

        self.df = df_base
        if makeFloat:
            self.df = self.df.astype(float)

    def get_dataframe(self, factor):
        self.__join_frames(factor)
        return self.df
