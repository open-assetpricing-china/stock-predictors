#
import pandas as pd
#=============================================
# 两分组函数
def split_2(x, var):
    # you might change your parameter here
    # rename 'B', 'S' for each group
    x.loc[x[var] >= x[var].mean(), 'group_' + var] = 'B'
    x.loc[x[var] < x[var].mean(), 'group_' + var] = 'S'
    return x
# 三分组函数
def split_3(x, var):
    # you might change your parameter here
    # rename 'H', 'M', 'L' for each group # reset '0.7', '0.3' for each threshold
    x.loc[x[var] >= x[var].quantile(0.7), 'group_' + var] = 'H'
    x.loc[(x[var] >= x[var].quantile(0.3)) & (x[var] < x[var].quantile(0.7)), 'group_' + var] = 'M'
    x.loc[x[var] < x[var].quantile(0.3), 'group_' + var] = 'L'
    return x
def split_10(x, var):
    x.loc[x[var] >= x[var].quantile(0.9), 'group_' + var] = 'L10'
    x.loc[(x[var] >= x[var].quantile(0.8)) & (x[var] < x[var].quantile(0.9)), 'group_' + var] = 'L9'
    x.loc[(x[var] >= x[var].quantile(0.7)) & (x[var] < x[var].quantile(0.8)), 'group_' + var] = 'L8'
    x.loc[(x[var] >= x[var].quantile(0.6)) & (x[var] < x[var].quantile(0.7)), 'group_' + var] = 'L7'
    x.loc[(x[var] >= x[var].quantile(0.5)) & (x[var] < x[var].quantile(0.6)), 'group_' + var] = 'L6'
    x.loc[(x[var] >= x[var].quantile(0.4)) & (x[var] < x[var].quantile(0.5)), 'group_' + var] = 'L5'
    x.loc[(x[var] >= x[var].quantile(0.3)) & (x[var] < x[var].quantile(0.4)), 'group_' + var] = 'L4'
    x.loc[(x[var] >= x[var].quantile(0.2)) & (x[var] < x[var].quantile(0.3)), 'group_' + var] = 'L3'
    x.loc[(x[var] >= x[var].quantile(0.1)) & (x[var] < x[var].quantile(0.2)), 'group_' + var] = 'L2'
    x.loc[x[var] < x[var].quantile(0.1), 'group_' + var] = 'L1'
    return x

#=============================================
class factor_ret_preprocessing(object):
    def __init__(self,df,para):
        self.df = df
        self.para = para
    def get_ep(self):
        df = self.df.copy()
        df['ep'] = 1 / df['pe']
        return df
class factor_ret_group_by_factor_quantile(object):
    def ep_and_size(self,df,para):
        # you might change your parameter here  rename 'var1', 'var2' for each characteristic
        df1 = df.copy()
        df1 = df1.groupby('month').apply(split_2, var='size').reset_index(drop=True)  # 对 size 进行2分组
        df1 = df1.groupby('month').apply(split_3, var='ep').reset_index(drop=True)  # 对 ep 进行 3 分组。
        # df2=df2.groupby(['month','group_size']).apply(split_3, var='ep').reset_index(drop=True) # 序贯分组
        df1['portfolio_name'] = df1['group_size'] + '/' + df1['group_ep']  # 得到分组组合名称
        return df1
class factor_ret_group_portfolio_ret(object):
    def portfolio_ret(self,df,):
        port_ret = df.groupby(['month', 'portfolio_name']).apply(
            lambda x: (x['ret'] * x['size']).sum() / x['size'].sum())
        port_ret = port_ret.reset_index()
        port_ret.rename(columns={port_ret.columns[-1]: 'ret'}, inplace=True)
        ''' 得到 portfolio return 的透视图'''
        port_ret = port_ret.pivot(index='month', columns='portfolio_name', values='ret')
        return port_ret
    def portfolio_ret_to_ep_and_size(self,port_ret):
        port_ret = port_ret.copy()
        port_ret['SMB'] = (port_ret['S/L'] + port_ret['S/M'] + port_ret['S/H']) / 3 - (
                port_ret['B/L'] + port_ret['B/M'] + port_ret['B/H']) / 3
        port_ret['HML'] = (port_ret['S/H'] + port_ret['B/H']) / 2 - (port_ret['S/L'] + port_ret['B/L']) / 2
        '''得到 factor_ret'''
        factor_ret = port_ret.loc[:, ['SMB', 'HML']].copy()
        factor_ret = factor_ret.reset_index()
        factor_ret.columns = ['month', 'SMB', 'HML']
        factor_ret = factor_ret.rename(columns={'SMB':'smb', 'HML':'vmg'})
        return factor_ret
    def portfolio_ret_to_market(self,df, factor_ret,rf):
        df = df.copy()
        factor_ret = factor_ret.copy()
        rf = rf.copy()
        rf['month'] = pd.to_datetime(rf['month'], format='%Y-%m-%d')
        rf.month = rf.month.dt.strftime('%Y-%m')
        factor_ret = pd.merge(rf, factor_ret, left_on='month', right_on='month')
        df = df.sort_values(by=['month','stkcd'])
        mkt = df.groupby('month').apply(
            lambda x: (x['mret'] * x['size']).sum() / x['size'].sum()).reset_index(drop=True)
        factor_ret['mkt'] = mkt
        factor_ret['mkt'] = factor_ret['mkt'] - factor_ret['rf']
        factor_ret=factor_ret[['month','mkt','smb','vmg']]
        return factor_ret
class factor_ret_canonical_form(object):
    def __init__(self,factor_ret,para):
        self.factor_ret = factor_ret
        self.para = para
    def canonicalize(self):
        self.factor_ret = self.factor_ret[self.para['std_columns']]
        self.factor_ret['month'] = pd.to_datetime(self.factor_ret['month'], format='%Y-%m-%d')
        self.factor_ret.month = self.factor_ret.month.dt.strftime('%Y-%m')
        return self.factor_ret