import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GlobalStats:
    def __init__(self, df):
        self.df = df

    def get_mean(self):
        return self.df.mean()

    def get_median(self):
        return self.df.median()

    def get_std(self):
        return self.df.std()

    def get_sum(self):
        return self.df.sum()

    def get_mode(self):
        return self.df.mode()

class RollingStats:
    def __init__(self, df, stock, window):
        self.df = df[stock]
        self.stock = stock
        self.window = window
        self.roller = self.df.rolling(window = self.window, center = False)

    def get_rolling_mean(self):
        return self.roller.mean(), "Rolling Mean"

    def get_rolling_median(self):
        return self.roller.median(), "Rolling Median"

    def get_rolling_std(self):
        return self.roller.std(), "Rolling Std. Deviation"

    def get_rolling_sum(self):
        return self.roller.sum(), "Rolling Sum"

    def get_rolling_max(self):
        return self.roller.max(), "Rolling Max"

    def get_rolling_min(self):
        return self.roller.min(), "Rolling Min"


    def get_bollinger_bands(self, roll_mean, roll_std):
        upper_band = roll_mean + 2 * roll_std
        lower_band = roll_mean - 2 * roll_std
        return upper_band, lower_band


    def plot_statistics(self, df_rolling, label, ax):
        df_rolling.plot(label = label, ax = ax)

    def plot_list(self, df_list):
        plt.figure()
        df,label = df_list[0]
        ax = df.plot(title = "Rolling Statistics", fontsize = 12)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        for df in df_list[1:]:
            df, label = df
            df.plot(label = label, ax = ax)

        plt.legend()



    def plotter(self, bollinger = True):
        plt.figure()
        ax = self.df.plot(title = self.stock + '-Rolling Statistics', fontsize = 12)
        df_rolling_mean = self.get_rolling_mean()
        df_rolling_mean, label = df_rolling_mean
        #self.plot_statistics(df_rolling=df_rolling_mean,label=label, ax=ax)
        df_rolling_mean.plot(label = label, ax = ax)

        if bollinger:
            df_rolling_std, label = self.get_rolling_std()
            upper_band, lower_band = self.get_bollinger_bands(df_rolling_mean, df_rolling_std)
            upper_band.plot(label = "upper band", ax = ax)
            lower_band.plot(label = "lower band", ax = ax)

        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
