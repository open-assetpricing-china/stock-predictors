import pandas as pd
# 读取 csmar 月度交易数据
class csmar_trading(object):
    def __init__(self):
        self.trading_data_path = '../data/csmar/csmar_trade/csmar_t_mnth.sas7bdat'
        self.std_columns = ['Stkcd', 'Trdmnt', 'Opndt', 'Mopnprc', 'Clsdt', 'Mclsprc', 'Msmvttl','Ndaytrd','Mretwd']
        self.columns_rename = {'Stkcd': 'stkcd','Trdmnt': 'month','Opndt': 'open_day','Mopnprc': 'opnprc',
                               'Clsdt': 'close_day','Mclsprc': 'clsprc','Msmvttl': 'size','Ndaytrd': 'trdday',
                               'Mretwd': 'mret'}
    def get_raw_trading_data(self):
        df = pd.read_sas(self.trading_data_path)
        return df
    def chg_columns_name(self, df):
        df = df.copy()
        df = df[self.std_columns]
        df.rename(columns=self.columns_rename, inplace=True)
        return df
    def canonicalize(self, df):
        df = df.copy()
        df['stkcd'] = df['stkcd'].apply(lambda x: str(x)[2:8])
        # 截取时间段
        df.month = df.month.apply(lambda x: str(x)[:4] + '-' + str(x)[4:6])
        df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d')
        df.month = df.month.dt.strftime('%Y-%m')
        df = df[(df.month > '1999-12') & (df.month < '2020-01')]
        return df
    def output_trading_data(self):
        df = self.get_raw_trading_data()
        df = self.chg_columns_name(df=df)
        df = self.canonicalize(df=df)
        return df
#
#===========================================================================================
class csmar_finance_raw(object):
    # 输出原始的 csmar_finance data, 不挑选特定的 financial_index, 保留全部的financial_indexes
    def __init__(self):
        self.financial_data_path = '../data/csmar/csmar_finance/csmar_master.sas7bdat'
        self.std_columns = ['Stkcd', 'Accper']
        self.columns_rename = {'Stkcd' : 'stkcd', 'Accper': 'month'}
    def get_raw_finance_data(self):
        df = pd.read_sas(self.financial_data_path)
        return df
    def chg_columns_name(self, df):
        df = df.copy()
        df.rename(columns=self.columns_rename, inplace=True)
        return df
    def canonicalize(self, df):
        df = df.copy()
        df['stkcd'] = df['stkcd'].apply(lambda x: str(x)[2:8])
        df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d')
        df.month = df.month.dt.strftime('%Y-%m')
        df = df[(df.month > '1999-12') & (df.month < '2020-01')]
        return df
    def output_finance_data(self):
        df = self.get_raw_finance_data()
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
        date_range = pd.date_range(start='2000-01', end='2020-01', freq='1M')
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
#
class csmar_basic_add_predictor(object):
    def __init__(self,df,para):
        self.df = df
        self.para = para
    def add_predictor(self):
        predictor_list = self.para['predictor']
        r_f_index = self.para['relate_finance_index']
        equation = self.para['equation']
        columns_list = list(self.df.columns)
        df = self.df.copy()
        p_list = [] # 存储最终成功生成的 predictors
        for it in predictor_list:
            eq = equation[it]
            f_index = r_f_index[it]
            comm_index = list(set(columns_list) & set(f_index))
            diff_index = list(set(f_index) - set(comm_index))
            try:
                df = df.groupby('stkcd').apply(eq).reset_index(drop=True)
            except KeyError as e:
                print('key error', e)
                print('get predictor ' + it + ' failed may due to wrong definition or '
                                               'typo of: ' + ' '.join(diff_index))
            else:
                df = df.copy()
                p_list.append(it)
        return df, p_list