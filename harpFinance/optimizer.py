import numpy as np
import pandas as pd
from fetcher import Fetcher
from statistician import GlobalStats
from scipy import optimize
from numpy import random
import matplotlib.pyplot as plt
import cvxopt as opt
from cvxopt import blas, solvers

np.random.seed(123)
# Turn off progress printing
solvers.options['show_progress'] = False

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


    def optimizePortfolio(self, target = None, plot_frontier = False):
        if not target:
            self.sharpe_optimizer()
        else:
            self.markowitz_optimizer(target, plot_frontier)


    def sharpe_optimizer(self):
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

    def markowitz_optimizer(self, target, plot_frontier):
        returns_df = self.daily_returns.copy()
        portfolio_sz = len(self.stockList)
        returns = np.asmatrix(returns_df)

        # Convert to cvxopt matrices
        S = opt.matrix(np.cov(returns.T))
        pbar = opt.matrix(np.mean(returns, axis=0)).T

        # Create constraint matrices
        G = -opt.matrix(np.eye(portfolio_sz))   # negative n x n identity matrix
        h = opt.matrix(0.0, (portfolio_sz ,1))
        A = opt.matrix(1.0, (1, portfolio_sz))
        b = opt.matrix(1.0)

        if plot_frontier:
            N = 100
            mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
            # Calculate efficient frontier weights using quadratic programming
            portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x']
                          for mu in mus]
            ## CALCULATE RISKS AND RETURNS FOR FRONTIER
            returns = [blas.dot(pbar, x) for x in portfolios]
            risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
            ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
            m1 = np.polyfit(returns, risks, 2)
            if m1[0] != 0:
                x1 = np.sqrt(m1[2] / m1[0])
            else:
                x1 = 0.
            # CALCULATE THE OPTIMAL PORTFOLIO
            wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
            print 'The Optimal Value:\n'
            print np.asarray(wt)
            print 'The Corresponding Return:%f\n' %(x1)
            globalStats = GlobalStats(returns_df)
            means = globalStats.get_mean()
            stds = globalStats.get_std()
            plt.figure()
            plt.plot(stds, means, 'o')
            plt.ylabel('mean')
            plt.xlabel('std')
            plt.plot(risks, returns, 'y-o')

        # get the target portfolio
        target_portfolio = solvers.qp(target * S, -pbar, G, h, A, b)['x']
        target_return = blas.dot(pbar,target_portfolio)
        target_risk = np.sqrt(blas.dot(target_portfolio, S * target_portfolio))

        target_portfolio = np.asarray(target_portfolio)
        self.optimalAllocation = np.array([x[0] for x in target_portfolio])




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
        df[['optimal','equal_foot']].plot()
