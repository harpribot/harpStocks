import numpy as np
import pandas as pd
from fetcher import Fetcher
from statistician import GlobalStats
from scipy import optimize
from numpy import random

class PortfolioOpt:
    def __init__(self, stockList, date_range):
        self.stockList = stockList
        self.startDate, self.endDate = date_range
        self.daily_returns = self.__fetch_daily_returns()


    def __fetch_daily_returns(self):
        fetcher = Fetcher(list(self.stockList))
        fetcher.fetch_history(self.startDate, self.endDate)
        self.df = fetcher.get_dataframe('Adj_Close')

        globalStats = GlobalStats(self.df)

        return globalStats.get_daily_returns()


    def optimizePortfolio(self):
        def optimizerfunc(allocation):
            portfolio = self.daily_returns.copy()
            portfolio_ret = allocation * portfolio
            weighted_sum = portfolio_ret.sum(axis = 1)
            portfolio['portfolio_ret'] = weighted_sum
            globalStats = GlobalStats(portfolio)
            sharpe_lst = globalStats.get_sharpe()
            sharpe_val = sharpe_lst['portfolio_ret']
            return -sharpe_val

        # initialize allocations
        portfolio_sz = len(self.stockList)
        allocation_init = random.rand(portfolio_sz)
        allocation_init = allocation_init/ np.sum(allocation_init)

        constraints = ({ 'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs) })
        bounds = [(0.,1.)] * portfolio_sz
        result = optimize.minimize(optimizerfunc, allocation_init, bounds= bounds, constraints=constraints)

        self.optimalAllocation = result.x


    def get_optimal_allocation(self):
        return zip(self.stockList,self.optimalAllocation)


    def plot_optimal_portfolio(self):
        portfolio = self.df.copy()
        # adds the optimal portfolio
        weighted_df = self.optimalAllocation * portfolio
        optimal_df = weighted_df.sum(axis = 1)
        # adds the equal weighted portflio
        total_stocks = self.optimalAllocation.size
        same_alloc = np.ones(total_stocks, dtype=float)
        same_alloc = same_alloc/ total_stocks
        equal_df = same_alloc * portfolio
        comparison_df = equal_df.sum(axis = 1)

        # now add these data to a dataframe and plot
        df = self.df.copy()
        df['optimal'] = optimal_df
        df['equal_foot'] = comparison_df
        # normalize the dataframe to see that what was the % improvement
        df = df/df.ix[0,:]
        df.plot()
