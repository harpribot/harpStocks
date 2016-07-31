from harpFinance.fetcher import Fetcher
import matplotlib.pyplot as plt

stockNm = ['FIT', 'YHOO', 'GOOG', 'SPY', 'GLD']

fetcher = Fetcher(stockNm)

startDate = '2016-07-01'
endDate = '2016-07-29'
fetcher.fetch_history(startDate, endDate)
google = fetcher.get_json('GOOG')

df = fetcher.get_dataframe('High')
print df

df.plot()
plt.show()
