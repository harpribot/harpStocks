from harpFinance.fetcher import Fetcher
from harpFinance.statistician import GlobalStats, RollingStats
from harpFinance.optimizer import PortfolioOpt
import matplotlib.pyplot as plt

stockNm = ['BAC','FIT','RENN', 'SIRI', 'GRPN']
startDate = '2016-04-20'
endDate = '2016-08-02'

fetcher = Fetcher(stockNm)


fetcher.fetch_history(startDate, endDate)
df = fetcher.get_dataframe('Adj_Close')


fetcher.plot_dataframe(normalization = True)
fetcher.plot_dataframe(normalization = False)


# Now do some global statistics

globalStats = GlobalStats(df)
print "Global Statistics: \n"
print "\nMean:"
print globalStats.get_mean()
print "\nStandard Deviation:"
print globalStats.get_std()
print "\nMode:"
print globalStats.get_mode()
print "\nMedian:"
print globalStats.get_median()
print "\nSum:"
print globalStats.get_sum()

print globalStats.get_sharpe_ratio()
print "\n\n"



# Now do some rolling statistics
window = 4
stock = 'GRPN'
rollingStats = RollingStats(df, stock, window)
print "Rolling Statistics: (See plots)\n"
roll_mean = rollingStats.get_rolling_mean()
roll_median = rollingStats.get_rolling_median()
roll_std = rollingStats.get_rolling_std()
roll_max = rollingStats.get_rolling_max()
roll_min = rollingStats.get_rolling_min()
#roll_sum = rollingStats.get_rolling_sum()
# Show all the plots
rolling_data = [roll_mean, roll_std, roll_max,roll_min, roll_median]
rollingStats.plot_list(rolling_data)
rollingStats.plotter(bollinger = True)
rollingStats.get_daily_returns(plot_hist = True, nBins = 20)
rollingStats.get_cumulative_returns(plot_hist = True, nBins = 20)


# Portfolio Optimization (Maximize the sharpe ratio)
stockNm = ['AAPL','ABT','ACN','AEP','AIG','ALL','AMGN',\
'AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY',\
'C','CAT','CL','COF','COP','COST','CSCO',\
'CTS','CVS','CVX','DD','DIS','DOW','DVN',\
'EBAY','EMC','EMR','EXC','F','FCX','FDX','GD','GE',\
'GILD','GM','GOOG','GS','HAL','HD','HON','HPQ','IBM',\
'INTC','JNJ','JPM','KO','LLY','LMT','LOW','MA','MCD',\
'MDLZ','MDT','MET','MMM','MO','MON','MRK','MS','MSFT',\
'NKE','NOV','NSC','NWSA','ORCL','OXY','PEP','PFE',\
'PG','PM','QCOM','RTN','SBUX','SLB','SO','SPG','T',\
'TGT','TWX','TXN','UNH','UNP','UPS','USB','UTX','V',\
'VZ','WFC','WMB','WMT','XOM']
portfolio_optimizer = PortfolioOpt(stockNm,(startDate, endDate))
#portfolio_optimizer.optimizePortfolio()
portfolio_optimizer.optimizePortfolio(target = 0.005, plot_frontier = True)
print portfolio_optimizer.get_optimal_allocation()
portfolio_optimizer.plot_optimal_portfolio()
plt.show()

# Portfolio Optimization (Markowitz method)
