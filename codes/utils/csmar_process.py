import pandas as pd
import numpy as np
# 读取 csmar 月度交易数据
class csmar_trading(object):
    def __init__(self):
        self.trading_data_path = '../data/download_data/csmar_t_mnth.sas7bdat'
        #self.trading_data_path = '../data/csmar/csmar_trade/csmar_t_mnth.parquet'
        self.columns_rename = {'Stkcd': 'stkcd', 'Trdmnt': 'month', 'Mretwd': 'mret'}
    def capitalize_columns_name(self, df): #capitalize()函数，将首字母都转换成大写，其余小写
        columns = list(df.columns)
        new_columns = [it.capitalize() for it in columns] # 字符串的第一个字母改为大写
        rename_dict = dict(zip(columns, new_columns))
        df.rename(columns=rename_dict, inplace=True)
        return df
    def get_raw_trading_data(self):
        df = pd.read_sas(self.trading_data_path)
        #df = pd.read_parquet(self.trading_data_path)
        return df
    def chg_columns_name(self, df):
        df = df.copy()
        df.rename(columns=self.columns_rename, inplace=True)
        return df
    def canonicalize(self, df):
        df = df.copy()
        #df['stkcd'] = df['stkcd'].apply(lambda x: str(x)[2:8])
        df.month = df.month.apply(lambda x: str(x)[:4] + '-' + str(x)[4:6])
        df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d')
        df.month = df.month.dt.strftime('%Y-%m')
        df = df[(df.month > '1990-11') & (df.month < '2022-01')]
        return df
    def output_trading_data(self):
        df = self.get_raw_trading_data()
        df = self.capitalize_columns_name(df=df) # 将columns首字母大写
        df = self.chg_columns_name(df=df)
        df = self.canonicalize(df=df)
        return df
#
#===========================================================================================
#
class csmar_finance_raw(object):
    # 输出原始的 csmar_finance data, 不挑选特定的 financial_index, 保留全部的financial_indexes
    def __init__(self):
        self.financial_data_path = '../data/download_data/csmar_master.sas7bdat'
        #self.financial_data_path = '../data/csmar/csmar_finance/csmar_master.parquet'
        self.columns_rename = {'Stkcd' : 'stkcd', 'Accper': 'month'}
    def get_raw_finance_data(self):
        df = pd.read_sas(self.financial_data_path)
        #df = pd.read_parquet(self.financial_data_path)
        return df
    def capitalize_columns_name(self, df): #capitalize()函数，将首字母都转换成大写，其余小写
        columns = ['stkcd', 'accper', 'typrep']
        new_columns = [it.capitalize() for it in columns] # 字符串的第一个字母改为大写
        rename_dict = dict(zip(columns, new_columns))
        df.rename(columns=rename_dict, inplace=True)
        return df
    def upper_columns_name(self, df): # upper()函数，将所有字母都转换成大写
        df_columns = list(df.columns)
        columns_1 = ['Stkcd', 'Accper', 'Typrep']
        columns = list(set(df_columns) - set(columns_1))
        new_columns = [it.upper() for it in columns ] # 字符串的第一个字母改为大写
        rename_dict = dict(zip(columns, new_columns)) # # upper()函数，将所有字母都转换成大写
        df.rename(columns=rename_dict, inplace=True)
        return df
    def chg_columns_name(self, df):
        df = df.copy()
        df.rename(columns=self.columns_rename, inplace=True)
        return df
    def canonicalize(self, df):
        df = df.copy()
        #df['stkcd'] = df['stkcd'].apply(lambda x: str(x)[2:8])
        df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d')
        df.month = df.month.dt.strftime('%Y-%m')
        df = df[(df.month > '1990-11') & (df.month < '2022-01')]
        return df
    def output_finance_data(self):
        df = self.get_raw_finance_data()
        df = self.capitalize_columns_name(df=df)
        df = self.upper_columns_name(df=df)
        df = self.chg_columns_name(df=df)
        df = self.canonicalize(df=df)
        return df
#
class csmar_finance_postprocess_raw(object):
    # 由于finance 数据是根据季度报给出的，因此得到的 finance 的日期并不是连续的月份，
    # 需要一个后处理的过程。
    def __init__(self, df):
        self.df = df.copy()
    def get_std_trading_month(self): # 这里可以调整 data_range
        date_range = pd.date_range(start='1990-12', end='2022-01', freq='1M')
        date_range = pd.DataFrame(date_range)
        date_range.rename(columns={0: 'date'}, inplace=True)
        date_range.date = date_range.date.dt.strftime('%Y-%m')
        date_range['month'] = date_range['date']
        return date_range
    def data_expanding(self, df):
        date_range = self.get_std_trading_month()
        # 由于 finance 的数据是按季度发布的，load的数据不是连续的月份, 需要对数据进行填充拓展
        df = df.drop_duplicates(subset='month', keep='first')  # 去除 month 列中相同的元素
        df_mer = pd.merge(date_range, df, on=['month'], how='left')
        df_mer = df_mer.drop(columns='date')
        df_mer['stkcd'] = df_mer['stkcd'].fillna(method='ffill')
        columns = list(df_mer.columns)
        temp_list = ['stkcd','month']
        diff_columns = list(set(columns) - set(temp_list))
        df_mer[diff_columns] = df_mer[diff_columns].fillna(method='ffill')
        return df_mer
    def output_finance_data(self):
        df_fin = self.df.sort_values(by=['stkcd', 'month'])
        df_fin = df_fin.groupby('stkcd').apply(
            lambda x: self.data_expanding(x)).reset_index(drop=True)
        return df_fin
#
class merge_csmar_basic_and_finance_data():
    def __init__(self, df_basic,df_fin):
        self.df_basic = df_basic
        self.df_fin = df_fin
    def keep_consist_form(self):
        self.df_basic = self.df_basic.sort_values(by=['stkcd','month'])
        self.df_fin = self.df_fin.sort_values(by = ['stkcd', 'month'])
    def merge(self):
        self.keep_consist_form()
        df_merge = pd.merge(self.df_basic, self.df_fin, on=['stkcd', 'month'], how='left')
        df_merge = df_merge.copy()
        return df_merge
#==============================================================================================
class csmar_t_co(object):
    def __init__(self):
        self.trading_data_path = '../data/download_data/csmar_t_co.sas7bdat'
        #self.trading_data_path = '../data/csmar/csmar_trade/csmar_t_co.parquet'
    def get_raw_data(self):
        df = pd.read_sas(self.trading_data_path)
        #df = pd.read_parquet(self.trading_data_path)
        return df
    def capitalize_columns_name(self, df): #capitalize()函数，将首字母都转换成大写，其余小写
        columns = list(df.columns)
        new_columns = [it.capitalize() for it in columns] # 字符串的第一个字母改为大写
        rename_dict = dict(zip(columns, new_columns))
        df.rename(columns=rename_dict, inplace=True)
        return df
    def canonicalize(self, df):
        df = df.copy()
        #df['Stkcd'] = df['Stkcd'].apply(lambda x: str(x)[2:8])
        df = df[['Stkcd', 'Nindcd']]
        return df
    def output(self):
        df = self.get_raw_data()
        df = self.capitalize_columns_name(df=df)
        df1 = self.canonicalize(df=df)
        return df1
def add_industry(x, df_ind):
    x = x.copy()
    stock_code = list(x['stkcd'])[0]
    ind_cd = df_ind.loc[df_ind['Stkcd'] == stock_code ]['Nindcd'].item()
    x['ind_cd'] = ind_cd
    return x
class csmar_basic_add_industry(object):
    def __init__(self,df):
        self.df = df
    def add_industry(self):
        industry = csmar_t_co()
        df_ind = industry.output()
        df = self.df.copy()
        df = df.groupby('stkcd').apply(lambda x: add_industry(x=x, df_ind=df_ind)).reset_index(drop=True)
        return df
#=============================================================================================================
class csmar_t_week():
    def __init__(self):
        self.trading_data_path = '../data/download_data/csmar_t_week.sas7bdat'
        #self.trading_data_path = '../data/csmar/csmar_trade/csmar_t_week.parquet'
        self.columns_rename = {'Stkcd': 'stkcd', 'Trdwnt': 'week', 'Wretwd': 'wret'}
    def get_raw_data(self):
        df = pd.read_sas(self.trading_data_path)
        #df = pd.read_parquet(self.trading_data_path)
        return df
    def capitalize_columns_name(self, df): #capitalize()函数，将首字母都转换成大写，其余小写
        columns = list(df.columns)
        new_columns = [it.capitalize() for it in columns] # 字符串的第一个字母改为大写
        rename_dict = dict(zip(columns, new_columns))
        df.rename(columns=rename_dict, inplace=True)
        return df
    def chg_columns_name(self, df):
        df = df.copy()
        #df = df[self.std_columns]
        df.rename(columns=self.columns_rename, inplace=True)
        return df
    def canonicalize(self, df):
        df = df.copy()
        #df['stkcd'] = df['stkcd'].apply(lambda x: str(x)[2:8])
        # 截取时间段
        df['month'] = pd.to_datetime(df['Clsdt'], format='%Y-%m-%d')
        df.month = df.month.dt.strftime('%Y-%m')
        df = df[(df.month < '2022-01')]
        return df
    def output_trading_data(self):
        df = self.get_raw_data()
        df = self.capitalize_columns_name(df=df)
        df = self.chg_columns_name(df=df)
        df = self.canonicalize(df=df)
        return df
#==========================================================================================
class csmar_t_daily():
    def __init__(self):
        self.trading_data_path = '../data/download_data/csmar_t_dalyr.sas7bdat'
        #self.trading_data_path = '../data/csmar/csmar_trade/csmar_t_dalyr.parquet'
        self.columns_rename = {'Stkcd': 'stkcd', 'Trddt': 'day', 'Dretwd': 'dret'}
    def get_raw_data(self):
        df = pd.read_sas(self.trading_data_path)
        #df = pd.read_parquet(self.trading_data_path)
        return df
    def capitalize_columns_name(self, df): #capitalize()函数，将首字母都转换成大写，其余小写
        columns = list(df.columns)
        new_columns = [it.capitalize() for it in columns] # 字符串的第一个字母改为大写
        rename_dict = dict(zip(columns, new_columns))
        df.rename(columns=rename_dict, inplace=True)
        return df
    def chg_columns_name(self, df):
        df = df.copy()
        #df = df[self.std_columns]
        df.rename(columns=self.columns_rename, inplace=True)
        return df
    def canonicalize(self, df):
        df = df.copy()
        #df['stkcd'] = df['stkcd'].apply(lambda x: str(x)[2:8])
        # 截取时间段
        df['month'] = pd.to_datetime(df['day'], format='%Y-%m-%d')
        df.month = df.month.dt.strftime('%Y-%m')
        df = df[ (df.month < '2022-01')]
        return df
    def output_trading_data(self):
        df = self.get_raw_data()
        df = self.capitalize_columns_name(df=df)
        df = self.chg_columns_name(df=df)
        df = self.canonicalize(df=df)
        return df
#
#
class csmar_single_predictor_postprocess(object):
    def __init__(self, df, predictor):
        self.df = df
        self.predictor = predictor
    def max_min_normalization(self,x):
        var_min = x[self.predictor].min()
        var_max = x[self.predictor].max()
        x = x.copy()
        x[self.predictor] = (x[self.predictor] - var_min) / (var_max - var_min)
        return x
    def remove_inf(self):
        self.df.replace([np.inf, -np.inf], np.nan, inplace=True)
    def scale_max_min_normal(self):
        self.df = self.df.groupby('month').apply(lambda x: self.max_min_normalization(x)).reset_index(drop=True)
    def scale_miuns1to1_rank(self):
        unique_count = self.df.dropna(subset=[self.predictor]).groupby(['month'])[self.predictor].unique().apply(len)
        unique_count = pd.DataFrame(unique_count).reset_index()
        unique_count.columns = ['month', 'count']
        self.df = pd.merge(self.df, unique_count, how='left', on=['month'])
        # ranking, and then standardize the data
        self.df['%s_rank' % self.predictor] = self.df.groupby(['month'])['%s' % self.predictor].rank(method='dense')
        self.df['rank_%s' % self.predictor] = (self.df['%s_rank' % self.predictor] - 1) / (self.df['count'] - 1) * 2 - 1
        self.df = self.df.drop(['%s_rank' % self.predictor, '%s' % self.predictor, 'count'], axis=1)
        self.df.rename(columns={'rank_%s' % self.predictor : self.predictor}, inplace=True)
    def output_predictor(self):
        self.remove_inf() # replace inf with nan
        self.scale_max_min_normal() # 采用 max_min normalization method
        self.scale_miuns1to1_rank() # 采用 rank 的方式 scale to (-1,1) 好处是排除异常打和异常小的情况，缺点是从小到大分布太平均
        p_name = self.predictor + '.csv'
        path = '../output/predictors_standard/'
        self.df.to_csv(path + p_name)
    def output_predictor_(self):
        self.remove_inf() # replace inf with nan
        self.scale_max_min_normal() # 采用max_min normalization method
        self.scale_miuns1to1_rank() # 采用 rank 的方式 scale to (-1,1) 好处是排除异常打和异常小的情况，缺点是从小到大分布太平均
        return self.df
#==========================================================================================