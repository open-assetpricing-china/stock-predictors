import pandas as pd
# 读取 csmar 月度交易数据
class csmar_trading(object):
    def __init__(self):
        self.trading_data_path = '../data/csmar/csmar_trade/csmar_t_mnth.sas7bdat'
        self.std_columns = ['Stkcd', 'Trdmnt', 'Opndt', 'Mopnprc', 'Clsdt', 'Mclsprc', 'Msmvttl','Ndaytrd','Mretwd',
                            'Mnvaltrd']
        self.columns_rename = {'Stkcd': 'stkcd','Trdmnt': 'month','Opndt': 'open_day','Mopnprc': 'opnprc',
                               'Clsdt': 'close_day','Mclsprc': 'clsprc','Msmvttl': 'size','Ndaytrd': 'trdday',
                               'Mretwd': 'mret', 'Mnvaltrd': 'mtrdvalue'}
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
        df = df[(df.month > '1999-12') & (df.month < '2022-01')]
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
        df = df[(df.month > '1999-12') & (df.month < '2022-01')]
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
        date_range = pd.date_range(start='2000-01', end='2022-01', freq='1M')
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
    #
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
#
class csmar_basic_predictor_postprocess(object):
    def __init__(self):
        self.df = pd.read_csv('../output/predictors/predictors.csv')  # 读取 predictors 数据
        self.para = pd.read_csv('../data/para_file/para_construct_portfolio.csv')  # 读取 predictors name list  数据
    def get_predictor_list(self):
        self.para.set_index('key', inplace=True)
        para_dict = {x: self.para.T.to_dict()[x]['value'] for x in self.para.T.to_dict().keys()}
        self.predictor_list = eval(para_dict['anomaly_list'])
    def scale_minus1to1_rank(self): # 将 predictors scale to range (-1, 1),
        print('Scale the predictors to range (-1, 1)') # 采用对 rank 的方式
        self.get_predictor_list()
        print('predictors: \n', self.predictor_list)
        for ii in range(len(self.predictor_list)):
            it = self.predictor_list[ii]
            unique_count = self.df.dropna(subset=[it]).groupby(['month'])[it].unique().apply(len)
            unique_count = pd.DataFrame(unique_count).reset_index()
            unique_count.columns = ['month', 'count']
            self.df = pd.merge(self.df, unique_count, how='left', on=['month'])
            # ranking, and then standardize the data
            self.df['%s_rank' % it] = self.df.groupby(['month'])['%s' % it].rank(method='dense')
            self.df['rank_%s' % it] = (self.df['%s_rank' % it] - 1) / (self.df['count'] - 1) * 2 - 1
            self.df = self.df.drop(['%s_rank' % it, '%s' % it, 'count'], axis=1)
            self.df.rename(columns={'rank_%s' % it : it}, inplace=True)
        #self.df = self.df.fillna(0) # 如果将空值全部填零，会导致做 decile 的时候，有的 predictor 不能给出全部十分位数
    def output_predictor(self):
        self.scale_minus1to1_rank()  # 采用 rank 的方式 scale to (-1,1) 好处是排除异常打和异常小的情况，缺点是从小到大分布太平均
        self.df.to_csv('../output/predictors/predictors.csv')
