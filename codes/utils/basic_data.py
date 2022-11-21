#
import pandas as pd
class DataForPredictors(object):
    def __init__(self):
        self.df_monthly_path = '../data/build_data/basic_monthly_data.parquet'
        self.df_weekly_path = '../data/build_data/basic_weekly_data.parquet'
        self.df_daily_path = '../data/build_data/basic_daily_data.parquet'
    def monthly(self):
        df = pd.read_parquet(self.df_monthly_path)
        return df
    def weekly(self):
        df = pd.read_parquet(self.df_weekly_path)
        return df
    def daily(self):
        df = pd.read_parquet(self.df_daily_path)
        return df
#
