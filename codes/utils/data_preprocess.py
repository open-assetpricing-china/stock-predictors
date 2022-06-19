import time
import numpy as np
import pandas as pd
#===========================================================
def get_yearly_trddays(df,period=12,comm_trdday=20):
    # 需要先把排序搞一致，发现一个问题，有几个月份的交易天数 trdday 为 None 值。所以需要先用 comm_trdday 来填充
    df = df.sort_values(['stkcd', 'month'])  # 把数据按股票代码大小和交易月份前后排序。
    df.index = range(len(df))  # 把 index 重新再排序
    df['trdday'] = df['trdday'].fillna(comm_trdday)  # 将 df 中 monthly trdday 中的 nan 值 用 20 替代
    t0 = time.time()
    trdday_lastyr = df.groupby('stkcd')['trdday'].rolling(period).apply(np.sum)  # 注意 groupby 之后，index 序列
    trdday_lastyr = trdday_lastyr.reset_index()
    df['trdday_lastyr_'] = trdday_lastyr['trdday']  # 进行这一步之前注意 index 必须对齐，否则非常容易出错
    df['trdday_cumsum_'] = df.groupby('stkcd')['trdday'].apply(np.cumsum)
    # 将 trdday_lastyr_ 和 trdday_cumsum_ 列合成一个元组列
    df['merged'] = df.apply(lambda x: (x['trdday_lastyr_'], x['trdday_cumsum_']), axis=1)
    # 从元组列生成新的 ‘trdday_lastyr’ 列
    df['trdday_lastyr'] = df['merged'].apply(lambda x: x[1] if pd.isnull(x[0]) == True else x[0])
    # 去掉 'trdday_lastyr_', 'trdday_cumsum_', 'merged' 列
    df = df.drop(columns=['trdday_lastyr_', 'trdday_cumsum_', 'merged'])
    print('spending time of get yearly traddays:', time.time() - t0)
    if np.array(list(df['trdday_lastyr'])).max() > 260:
        raise Exception("trdday_lastyr > 260")
    return df
#
def filter_30(x, var):
    x.loc[x[var] >= x[var].quantile(0.3), 'filter_' + var] = 'keep'
    return x
def filter_bottom_size(x, var, percentage=0.3):
    x.loc[x[var] >= x[var].quantile(percentage), 'filter_' + var] = 'keep'
    return x
#================================================================================
class  df_preprocessing(object):
    def __init__(self, df, para):
        self.df = df
        self.para = para
    def df_date(self):
        if 'month' in list(self.df.columns):
            return self.df
        else:
            self.df['month'] = pd.to_datetime(self.df['date'],format='%Y-%m-%d')
            self.df.month = self.df.month.dt.strftime('%Y-%m')
            self.df = self.df.drop(columns='date')
            return self.df
    def df_size(self, df):
        if 'size' in list(df.columns):
            return df
        else:
            df = df.copy()
            df['size'] = df['share'] * df['clsprc']
            return df
    def df_year_and_mnt_trddays(self):
        self.df = self.df_date()
        self.df = self.df_size(df=self.df)
        self.df = get_yearly_trddays(self.df,
                                     comm_trdday=self.para['mnt_comm_trdday'],
                                     period=self.para['yearly_mnt_period']) # 得到年度交易日数量
        self.df['trdday_lastmon'] = self.df['trdday']  # 得到月度交易日数量
        df = self.df.dropna()
        return df
#
class df_process_size_and_ret(object):
    def df_adopt_last_size_and_next_ret_mntly(self, df, para):
        ''' Adopt size of last month Adopt ret of next month '''
        df1 = df.copy()
        df1['size'] = df1.groupby('stkcd')['size'].shift()
        df1['ret'] = df1.groupby('stkcd')['mret'].shift(-1)  # ret 往前推一个月。
        df1['size'].fillna(method='bfill', inplace=True)
        df1['ret'].fillna(method='ffill', inplace=True)
        return df1
    def df_adopt_last_ret_mntly(self,df,para):
        df1 = df.copy()
        df1['ret'] = df1.groupby('stkcd')['mret'].shift()
        df1['ret'].fillna(method='bfill', inplace=True)
        return df1
    def df_adopt_last_size_and_last_ret_mntly(self,df,para):
        df1 = df.copy()
        df1['size'] = df1.groupby('stkcd')['size'].shift()
        df1['ret'] = df1.groupby('stkcd')['mret'].shift()
        df1['size'].fillna(method='bfill', inplace=True)
        df1['ret'].fillna(method='bfill', inplace=True)
        return df1
    def df_adopt_default_size_and_ret_mntly(self,df,para): # 默认 size 和 ret 不上移也不下移
        df1 = df.copy()
        df1['ret'] = df1['mret']
        return df1
#
class df_process_filter_size(object):
    def df_exclude_bottom_size_stocks(self,df,para):
        #df = self.df_adopt_last_size_and_next_ret_mntly()
        df = df.copy()
        df = df.groupby('month').apply(filter_bottom_size,
                                       var='size',
                                       percentage=para['exclude_bottom_size']).reset_index(drop=True)
        df = df[df['filter_size'] == 'keep'].reset_index(drop=True)  # 得到了排除了市值大小在分位排序中大于30%的股票
        return df
#
class df_process_filter_trddays(object):
    # Exclude stocks with trade days of last month/year less than 10/120 days
    def df_exclude_trddays_last_year_and_mnt(self, df, para):
        df1 = df.copy()
        df1 = df1[(df1['trdday_lastyr'] >= para['exclude_trdday_lsyr']) &
                  (df1['trdday_lastmon'] >= para['exclude_trdday_lsmnt'])].reset_index(drop=True)
        return df1
    def df_exclude_begin_trddays(self,df,para):
        #
        df1 = df.copy()
        df1 = df1[df1['month'] > para['exclude_begin_trdday']].reset_index(drop=True)
        return df1