from harpFinance.fetcher import Fetcher
from harpFinance.statistician import GlobalStats, RollingStats
from harpFinance.optimizer import PortfolioOpt
import matplotlib.pyplot as plt

stockNm = ['BAC','FIT','RENN','SVU', 'SIRI', 'GRPN']
startDate = '2016-07-20'
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
portfolio_optimizer = PortfolioOpt(stockNm,(startDate, endDate))
portfolio_optimizer.optimizePortfolio()
print portfolio_optimizer.get_optimal_allocation()
portfolio_optimizer.plot_optimal_portfolio()
plt.show()
