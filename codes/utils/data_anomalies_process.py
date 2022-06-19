import pandas as pd
#==================================================================================================
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
def split_size_10(x, var):
    x.loc[x[var] >= x[var].quantile(0.9), 'group_' + var] = 'S10'
    x.loc[(x[var] >= x[var].quantile(0.8)) & (x[var] < x[var].quantile(0.9)), 'group_' + var] = 'S9'
    x.loc[(x[var] >= x[var].quantile(0.7)) & (x[var] < x[var].quantile(0.8)), 'group_' + var] = 'S8'
    x.loc[(x[var] >= x[var].quantile(0.6)) & (x[var] < x[var].quantile(0.7)), 'group_' + var] = 'S7'
    x.loc[(x[var] >= x[var].quantile(0.5)) & (x[var] < x[var].quantile(0.6)), 'group_' + var] = 'S6'
    x.loc[(x[var] >= x[var].quantile(0.4)) & (x[var] < x[var].quantile(0.5)), 'group_' + var] = 'S5'
    x.loc[(x[var] >= x[var].quantile(0.3)) & (x[var] < x[var].quantile(0.4)), 'group_' + var] = 'S4'
    x.loc[(x[var] >= x[var].quantile(0.2)) & (x[var] < x[var].quantile(0.3)), 'group_' + var] = 'S3'
    x.loc[(x[var] >= x[var].quantile(0.1)) & (x[var] < x[var].quantile(0.2)), 'group_' + var] = 'S2'
    x.loc[x[var] < x[var].quantile(0.1), 'group_' + var] = 'S1'
    return x
def split_anomaly_10(x, var):
    x.loc[x[var] >= x[var].quantile(0.9), 'group_' + var] = 'A10'
    x.loc[(x[var] >= x[var].quantile(0.8)) & (x[var] < x[var].quantile(0.9)), 'group_' + var] = 'A9'
    x.loc[(x[var] >= x[var].quantile(0.7)) & (x[var] < x[var].quantile(0.8)), 'group_' + var] = 'A8'
    x.loc[(x[var] >= x[var].quantile(0.6)) & (x[var] < x[var].quantile(0.7)), 'group_' + var] = 'A7'
    x.loc[(x[var] >= x[var].quantile(0.5)) & (x[var] < x[var].quantile(0.6)), 'group_' + var] = 'A6'
    x.loc[(x[var] >= x[var].quantile(0.4)) & (x[var] < x[var].quantile(0.5)), 'group_' + var] = 'A5'
    x.loc[(x[var] >= x[var].quantile(0.3)) & (x[var] < x[var].quantile(0.4)), 'group_' + var] = 'A4'
    x.loc[(x[var] >= x[var].quantile(0.2)) & (x[var] < x[var].quantile(0.3)), 'group_' + var] = 'A3'
    x.loc[(x[var] >= x[var].quantile(0.1)) & (x[var] < x[var].quantile(0.2)), 'group_' + var] = 'A2'
    x.loc[x[var] < x[var].quantile(0.1), 'group_' + var] = 'A1'
    return x
#===================================================================================
class anomalies_group_quantile(object):
    def neutral_split(self, df, para):
        df1 = df.copy()
        df1 = df1.groupby(['month']).apply(split_size_10, var = para['neutral_var']).reset_index(drop=True) # 对 neutral_var 进行10分组
        return df1
    def anomay_split(self,df,para):
        df1 = df.copy()
        if para['Is_neutral'] == 'yes':
            df1 = self.neutral_split(df=df1,para=para)
            df1 = df1.groupby(['month', 'group_'+para['neutral_var']]).apply(
                split_anomaly_10, var = para['anomaly']).reset_index(drop=True) # 采用序贯分组
            df1['portfolio_name'] = df1['group_' + para['neutral_var']]  + '/' + df1['group_' + para['anomaly']] #得到分组组合名称
        elif para['Is_neutral'] == 'no':
            df1 = df1.groupby('month').apply(
                split_anomaly_10, var = para['anomaly']).reset_index(drop=True) # 对 anomaly 进行分组
            df1['portfolio_name'] = df1['group_'+para['anomaly']] # # 得到分组组合名称
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        return df1
class anomalies_ret_group(object):
    def portfolio_ret(self,df,para): # para['way_weight'] 方式进行求加权收益
        port_ret = df.groupby(['month', 'portfolio_name']).apply(
            lambda x: (x['ret'] * x[para['way_weight']]).sum() / x[para['way_weight']].sum()) # 按para['way_weight]加权
        port_ret = port_ret.reset_index()
        port_ret.rename(columns={port_ret.columns[-1]: 'ret'}, inplace=True)
        ''' 得到 portfolio return 的透视图'''
        port_ret = port_ret.pivot(index='month', columns='portfolio_name', values='ret')
        return port_ret
    def portfolio_ret_ew(self,df): # ew: equal weighted ret 平权的收益
        port_ret = df.groupby(['month', 'portfolio_name']).apply(
            lambda x: x['ret'].sum() / len(x['ret']))
        port_ret = port_ret.reset_index()
        port_ret.rename(columns={port_ret.columns[-1] : 'ret_ew'}, inplace=True)
        ''' 得到 portfolio return 的透视图'''
        port_ret = port_ret.pivot(index='month', columns='portfolio_name', values='ret_ew')
        return port_ret
    def anomaly_ret_long_short(self,port_ret,port_ret_ew,para):
        port_ret = port_ret.copy()
        port_ret_ew = port_ret_ew.copy()
        if para['Is_neutral'] == 'yes':
            port_ret['1-10'] = (port_ret['S1/A1'] + port_ret['S2/A1'] + port_ret['S3/A1'] + port_ret['S4/A1'] +
                                port_ret['S5/A1'] + port_ret['S6/A1'] + port_ret['S7/A1'] + port_ret['S8/A1'] +
                                port_ret['S9/A1'] + port_ret['S10/A1']) / 10 - \
                               (port_ret['S1/A10'] + port_ret['S2/A10'] + port_ret['S3/A10'] + port_ret['S4/A10'] +
                                port_ret['S5/A10'] + port_ret['S6/A10'] + port_ret['S7/A10'] + port_ret['S8/A10'] +
                                port_ret['S9/A10'] + port_ret['S10/A10']) / 10
            port_ret_ew['1-10'] = (port_ret_ew['S1/A1'] + port_ret_ew['S2/A1'] + port_ret_ew['S3/A1'] + port_ret_ew['S4/A1'] +
                                   port_ret_ew['S5/A1'] + port_ret_ew['S6/A1'] + port_ret_ew['S7/A1'] + port_ret_ew['S8/A1'] +
                                   port_ret_ew['S9/A1'] + port_ret_ew['S10/A1']) / 10 - \
                                  (port_ret_ew['S1/A10'] + port_ret_ew['S2/A10'] + port_ret_ew['S3/A10'] + port_ret_ew['S4/A10'] +
                                   port_ret_ew['S5/A10'] + port_ret_ew['S6/A10'] + port_ret_ew['S7/A10'] + port_ret_ew['S8/A10'] +
                                   port_ret_ew['S9/A10'] + port_ret_ew['S10/A10']) /10
        elif para['Is_neutral'] == 'no':
            port_ret['1-10'] = port_ret['A1'] - port_ret['A10']
            port_ret_ew['1-10'] = port_ret_ew['A1'] - port_ret_ew['A10']
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        '''得到 anomaly_ret'''
        anomaly_ret = port_ret.loc[:, ['1-10']].copy()
        anomaly_ret = anomaly_ret.reset_index()
        anomaly_ret.columns = ['month', '1-10']

        anomaly_ret_ew = port_ret_ew.loc[:, ['1-10']].copy()
        anomaly_ret_ew = anomaly_ret_ew.reset_index()
        anomaly_ret_ew.columns = ['month', '1-10']
        anomaly_ret_ew.rename(columns={'1-10':'1-10-ew'},inplace=True)

        df_anomaly_ret = pd.merge(anomaly_ret,anomaly_ret_ew,on='month')
        return df_anomaly_ret
    def anomaly_ret_long_short_(self, port_ret,para):
        port_ret = port_ret.copy()
        if para['Is_neutral'] == 'yes':
            port_ret['1-10'] = (port_ret['S1/A1'] + port_ret['S2/A1'] + port_ret['S3/A1'] + port_ret['S4/A1'] +
                                port_ret['S5/A1'] + port_ret['S6/A1'] + port_ret['S7/A1'] + port_ret['S8/A1'] +
                                port_ret['S9/A1'] + port_ret['S10/A1']) / 10 - \
                               (port_ret['S1/A10'] + port_ret['S2/A10'] + port_ret['S3/A10'] + port_ret['S4/A10'] +
                                port_ret['S5/A10'] + port_ret['S6/A10'] + port_ret['S7/A10'] + port_ret['S8/A10'] +
                                port_ret['S9/A10'] + port_ret['S10/A10']) / 10
        elif para['Is_neutral'] == 'no':
            port_ret['1-10'] = port_ret['A1'] - port_ret['A10']
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        # 得到 anomaly_ret
        anomaly_ret = port_ret.loc[:, ['1-10']].copy()
        anomaly_ret = anomaly_ret.reset_index()
        anomaly_ret.columns = ['month', '1-10']
        anomaly_ret.rename(columns={'1-10': para['anomaly']}, inplace=True)
        return anomaly_ret
#====================================================================
class anomalies_ret_canonical_form(object):
    def __init__(self,anomaly_ret,para):
        self.anomaly_ret = anomaly_ret
        self.para = para
    def canonicalize(self):
        columns = {'1-10': self.para['std_columns'][1],
                   '1-10-ew':self.para['std_columns'][2]}
        self.anomaly_ret = self.anomaly_ret.rename(columns=columns)
        self.anomaly_ret = self.anomaly_ret[self.para['std_columns']]
        return self.anomaly_ret
    def canonicalize_(self):
        self.anomaly_ret = self.anomaly_ret[self.para['columns']]
        return self.anomaly_ret

