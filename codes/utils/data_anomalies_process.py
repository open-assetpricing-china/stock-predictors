import pandas as pd
import numpy as np
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
def split_size_2(x, var):  # 2 groups
    x.loc[x[var] >= x[var].quantile(0.5), 'group_' + var] = 'S2'
    x.loc[x[var] < x[var].quantile(0.5), 'group_' + var] = 'S1'
    return x
def split_anomaly_10(x, var):
    x1 = x.copy()
    x1.dropna(subset=[var], inplace = True)
    if len(x1) >= 2:
        if x[var].quantile(0.9) == x[var].max() and x[var].quantile(0.1) == x[var].min():
            x.loc[x[var] >= x[var].quantile(0.9), 'group_' + var] = 'A10'
            x.loc[(x[var] >= x[var].quantile(0.8)) & (x[var] < x[var].quantile(0.9)), 'group_' + var] = 'A9'
            x.loc[(x[var] >= x[var].quantile(0.7)) & (x[var] < x[var].quantile(0.8)), 'group_' + var] = 'A8'
            x.loc[(x[var] >= x[var].quantile(0.6)) & (x[var] < x[var].quantile(0.7)), 'group_' + var] = 'A7'
            x.loc[(x[var] >= x[var].quantile(0.5)) & (x[var] < x[var].quantile(0.6)), 'group_' + var] = 'A6'
            x.loc[(x[var] >= x[var].quantile(0.4)) & (x[var] < x[var].quantile(0.5)), 'group_' + var] = 'A5'
            x.loc[(x[var] >= x[var].quantile(0.3)) & (x[var] < x[var].quantile(0.4)), 'group_' + var] = 'A4'
            x.loc[(x[var] >= x[var].quantile(0.2)) & (x[var] < x[var].quantile(0.3)), 'group_' + var] = 'A3'
            x.loc[(x[var] > x[var].quantile(0.1)) & (x[var] < x[var].quantile(0.2)), 'group_' + var] = 'A2'
            x.loc[x[var] <= x[var].quantile(0.1), 'group_' + var] = 'A1'
        elif x[var].quantile(0.9) == x[var].max() and x[var].quantile(0.1) > x[var].min():
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
        elif x[var].quantile(0.9) < x[var].max() and x[var].quantile(0.1) == x[var].min():
            x.loc[x[var] > x[var].quantile(0.9), 'group_' + var] = 'A10'
            x.loc[(x[var] > x[var].quantile(0.8)) & (x[var] <= x[var].quantile(0.9)), 'group_' + var] = 'A9'
            x.loc[(x[var] > x[var].quantile(0.7)) & (x[var] <= x[var].quantile(0.8)), 'group_' + var] = 'A8'
            x.loc[(x[var] > x[var].quantile(0.6)) & (x[var] <= x[var].quantile(0.7)), 'group_' + var] = 'A7'
            x.loc[(x[var] > x[var].quantile(0.5)) & (x[var] <= x[var].quantile(0.6)), 'group_' + var] = 'A6'
            x.loc[(x[var] > x[var].quantile(0.4)) & (x[var] <= x[var].quantile(0.5)), 'group_' + var] = 'A5'
            x.loc[(x[var] > x[var].quantile(0.3)) & (x[var] <= x[var].quantile(0.4)), 'group_' + var] = 'A4'
            x.loc[(x[var] > x[var].quantile(0.2)) & (x[var] <= x[var].quantile(0.3)), 'group_' + var] = 'A3'
            x.loc[(x[var] > x[var].quantile(0.1)) & (x[var] <= x[var].quantile(0.2)), 'group_' + var] = 'A2'
            x.loc[x[var] <= x[var].quantile(0.1), 'group_' + var] = 'A1'
        elif x[var].quantile(0.9) < x[var].max() and x[var].quantile(0.1) > x[var].min():
            x.loc[x[var] > x[var].quantile(0.9), 'group_' + var] = 'A10'
            x.loc[(x[var] > x[var].quantile(0.8)) & (x[var] <= x[var].quantile(0.9)), 'group_' + var] = 'A9'
            x.loc[(x[var] > x[var].quantile(0.7)) & (x[var] <= x[var].quantile(0.8)), 'group_' + var] = 'A8'
            x.loc[(x[var] > x[var].quantile(0.6)) & (x[var] <= x[var].quantile(0.7)), 'group_' + var] = 'A7'
            x.loc[(x[var] > x[var].quantile(0.5)) & (x[var] <= x[var].quantile(0.6)), 'group_' + var] = 'A6'
            x.loc[(x[var] > x[var].quantile(0.4)) & (x[var] <= x[var].quantile(0.5)), 'group_' + var] = 'A5'
            x.loc[(x[var] > x[var].quantile(0.3)) & (x[var] <= x[var].quantile(0.4)), 'group_' + var] = 'A4'
            x.loc[(x[var] > x[var].quantile(0.2)) & (x[var] <= x[var].quantile(0.3)), 'group_' + var] = 'A3'
            x.loc[(x[var] >= x[var].quantile(0.1)) & (x[var] <= x[var].quantile(0.2)), 'group_' + var] = 'A2'
            x.loc[x[var] < x[var].quantile(0.1), 'group_' + var] = 'A1'
        else:
            raise Exception('wrong split 10 groups')
    else:
        x['group_' + var] = np.nan
    return x
#
def split_anomaly_10_sort_method(x, var):
    x1 = x.copy()
    x1.sort_values(by = var, inplace=True)
    #x1.dropna(subset=[var], inplace = True)
    x1['rank'] = list(range(len(x1)))
    #
    if len(x1) >= 10:
        num_stk = round(len(x1) / 10)
        x1.loc[x1['rank'] < num_stk, 'group_' + var] = 'A1'
        x1.loc[(x1['rank'] >= num_stk) & (x1['rank'] < 2 * num_stk), 'group_' + var ] = 'A2'
        x1.loc[(x1['rank'] >= 2 * num_stk) & (x1['rank'] < 3 * num_stk), 'group_' + var] = 'A3'
        x1.loc[(x1['rank'] >= 3 * num_stk) & (x1['rank'] < 4 * num_stk), 'group_' + var] = 'A4'
        x1.loc[(x1['rank'] >= 4 * num_stk) & (x1['rank'] < 5 * num_stk), 'group_' + var] = 'A5'
        x1.loc[(x1['rank'] >= 5 * num_stk) & (x1['rank'] < 6 * num_stk), 'group_' + var] = 'A6'
        x1.loc[(x1['rank'] >= 6 * num_stk) & (x1['rank'] < 7 * num_stk), 'group_' + var] = 'A7'
        x1.loc[(x1['rank'] >= 7 * num_stk) & (x1['rank'] < 8 * num_stk), 'group_' + var] = 'A8'
        x1.loc[(x1['rank'] >= 8 * num_stk) & (x1['rank'] < 9 * num_stk), 'group_' + var] = 'A9'
        x1.loc[(x1['rank'] >= 9 * num_stk), 'group_' + var] = 'A10'
    else:
        x1['group_' + var] = np.nan
    return x1
#
#=========================================================================================
#
class anomalies_group_quantile(object):
    def neutral_split_10(self, df, para):
        df1 = df.copy()
        df1 = df1.groupby(['month']).apply(split_size_10, var = para['neutral_var']).reset_index(drop=True) # 对 neutral_var 进行10分组
        return df1
    def neutral_split_2(self, df, para):
        df1 = df.copy()
        df1 = df1.groupby(['month']).apply(split_size_2, var = para['neutral_var']).reset_index(drop=True) # 对 neutral_var 进行 2 分组
        return df1
    def anomaly_split(self,df,para):
        df1 = df.copy()
        if para['Is_neutral'] == 'yes':
            df1 = self.neutral_split_2(df=df1,para=para)
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
    def anomaly_split_sort_method(self, df, para):
        df1 = df.copy()
        if para['Is_neutral'] == 'yes':
            df1 = self.neutral_split_2(df=df1, para=para)
            df1 = df1.groupby(['month', 'group_' + para['neutral_var']]).apply(
                split_anomaly_10_sort_method, var = para['anomaly']).reset_index(drop=True) # 采用序贯分组
            df1['portfolio_name'] = df1['group_' + para['neutral_var']] + '/' + df1['group_' + para['anomaly']] # 得到分组组合名称
        elif para['Is_neutral'] == 'no':
            df1 = df1.groupby('month').apply(
                split_anomaly_10_sort_method, var = para['anomaly']).reset_index(drop=True) # 对 anomaly 进行分组
            df1['portfolio_name'] = df1['group_' + para['anomaly']] # # 得到分组组合名称
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        return df1
#
def vw_return(x, way_weight):
    x1 = x.copy()
    x1.dropna(subset=['ret', way_weight], inplace = True)
    vw_ret = (x1['ret'] * x1[way_weight] ).sum() / x1[way_weight].sum()
    return vw_ret
def ew_return(x):
    x1 = x.copy()
    x1.dropna(subset=['ret'], inplace = True)
    ew_ret = x1['ret'].sum() / len(x1['ret'])
    return ew_ret
#
def stk_count(x):
    return len(x)
def stk_count_valued_vw(x, way_weight):
    x1 = x.copy()
    x1.dropna(subset=['ret', way_weight], inplace = True)
    return len(x1)
def stk_count_valued_ew(x):
    x1 = x.copy()
    x1.dropna(subset=['ret'], inplace = True)
    return len(x1)
#
class anomalies_ret_group(object):
    def portfolio_ret(self,df,para): # para['way_weight'] 方式进行求加权收益
        #
        port_ret = df.groupby(['month', 'portfolio_name']).apply(
            lambda x: vw_return(x,way_weight=para['way_weight']))
        port_ret = port_ret.reset_index()
        port_ret.rename(columns={port_ret.columns[-1]: 'ret'}, inplace=True)
        ''' 得到 portfolio return 的透视图'''
        port_ret = port_ret.pivot(index='month', columns='portfolio_name', values='ret')
        #
        port_count = df.groupby(['month', 'portfolio_name']).apply(lambda x: stk_count(x))
        port_count = port_count.reset_index()
        port_count.rename(columns={port_count.columns[-1]: 'count'}, inplace=True)
        port_count = port_count.pivot(index='month', columns='portfolio_name', values='count')
        #
        if para['Is_neutral'] == 'yes':
            port_count.rename(columns={'S1/A1':'S1/A1_stk','S1/A2':'S1/A2_stk','S1/A3':'S1/A3_stk',
                                       'S1/A4':'S1/A4_stk','S1/A5':'S1/A5_stk','S1/A6':'S1/A6_stk',
                                       'S1/A7':'S1/A7_stk','S1/A8':'S1/A8_stk','S1/A9':'S1/A9_stk','S1/A10':'S1/A10_stk',
                                       'S2/A1': 'S2/A1_stk', 'S2/A2': 'S2/A2_stk', 'S2/A3': 'S2/A3_stk',
                                       'S2/A4': 'S2/A4_stk', 'S2/A5': 'S2/A5_stk', 'S2/A6': 'S2/A6_stk',
                                       'S2/A7': 'S2/A7_stk', 'S2/A8': 'S2/A8_stk', 'S2/A9': 'S2/A9_stk',
                                       'S2/A10': 'S2/A10_stk',},inplace=True)
        elif para['Is_neutral'] == 'no':
            port_count.rename(columns={'A1':'A1_stk','A2':'A2_stk','A3':'A3_stk',
                                       'A4':'A4_stk','A5':'A5_stk','A6':'A6_stk',
                                       'A7':'A7_stk','A8':'A8_stk','A9':'A9_stk','A10':'A10_stk',},inplace=True)
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        #
        port_count_valued = df.groupby(['month', 'portfolio_name']).apply(
            lambda x: stk_count_valued_vw(x,way_weight=para['way_weight']))
        port_count_valued = port_count_valued.reset_index()
        port_count_valued.rename(columns={port_count_valued.columns[-1]: 'count_valued'}, inplace=True)
        port_count_valued = port_count_valued.pivot(index='month', columns='portfolio_name', values='count_valued')
        #
        if para['Is_neutral'] == 'yes':
            port_count_valued.rename(columns={'S1/A1':'S1/A1_v_stk','S1/A2':'S1/A2_v_stk','S1/A3':'S1/A3_v_stk',
                                              'S1/A4':'S1/A4_v_stk','S1/A5':'S1/A5_v_stk','S1/A6':'S1/A6_v_stk',
                                              'S1/A7':'S1/A7_v_stk','S1/A8':'S1/A8_v_stk','S1/A9':'S1/A9_v_stk','S1/A10':'S1/A10_v_stk',
                                              'S2/A1': 'S2/A1_v_stk', 'S2/A2': 'S2/A2_v_stk', 'S2/A3': 'S2/A3_v_stk',
                                              'S2/A4': 'S2/A4_v_stk', 'S2/A5': 'S2/A5_v_stk', 'S2/A6': 'S2/A6_v_stk',
                                              'S2/A7': 'S2/A7_v_stk', 'S2/A8': 'S2/A8_v_stk', 'S2/A9': 'S2/A9_v_stk',
                                              'S2/A10': 'S2/A10_v_stk',},inplace=True)
        elif  para['Is_neutral'] == 'no':
            port_count_valued.rename(columns={'A1':'A1_v_stk','A2':'A2_v_stk','A3':'A3_v_stk',
                                          'A4':'A4_v_stk','A5':'A5_v_stk','A6':'A6_v_stk',
                                          'A7':'A7_v_stk','A8':'A8_v_stk','A9':'A9_v_stk','A10':'A10_v_stk',},
                                 inplace=True)
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        #
        if len(port_ret) >= len(port_count):
            port_1 = pd.merge(port_ret, port_count, on='month', how='left' )
        else:
            port_1 = pd.merge(port_ret, port_count, on='month', how='right')
        #
        if len(port_1) >= len(port_count_valued):
            port_2 = pd.merge(port_1, port_count_valued, on= 'month', how='left')
        else:
            port_2 = pd.merge(port_1, port_count_valued, on= 'month', how='right')
        return port_2
    #
    def portfolio_ret_ew(self,df, para): # ew: equal weighted ret 平权的收益
        port_ret = df.groupby(['month', 'portfolio_name']).apply(lambda x: ew_return(x))
        port_ret = port_ret.reset_index()
        port_ret.rename(columns={port_ret.columns[-1] : 'ret_ew'}, inplace=True)
        ''' 得到 portfolio return 的透视图'''
        port_ret = port_ret.pivot(index='month', columns='portfolio_name', values='ret_ew')
        #
        port_count = df.groupby(['month', 'portfolio_name']).apply(lambda x: stk_count(x))
        port_count = port_count.reset_index()
        port_count.rename(columns={port_count.columns[-1]: 'count'}, inplace=True)
        port_count = port_count.pivot(index='month', columns='portfolio_name', values='count')
        #
        if para['Is_neutral'] == 'yes':
            port_count.rename(columns={'S1/A1':'S1/A1_stk','S1/A2':'S1/A2_stk','S1/A3':'S1/A3_stk',
                                       'S1/A4':'S1/A4_stk','S1/A5':'S1/A5_stk','S1/A6':'S1/A6_stk',
                                       'S1/A7':'S1/A7_stk','S1/A8':'S1/A8_stk','S1/A9':'S1/A9_stk','S1/A10':'S1/A10_stk',
                                       'S2/A1': 'S2/A1_stk', 'S2/A2': 'S2/A2_stk', 'S2/A3': 'S2/A3_stk',
                                       'S2/A4': 'S2/A4_stk', 'S2/A5': 'S2/A5_stk', 'S2/A6': 'S2/A6_stk',
                                       'S2/A7': 'S2/A7_stk', 'S2/A8': 'S2/A8_stk', 'S2/A9': 'S2/A9_stk',
                                       'S2/A10': 'S2/A10_stk',},inplace=True)
        elif para['Is_neutral'] == 'no':
            port_count.rename(columns={'A1':'A1_stk','A2':'A2_stk','A3':'A3_stk',
                                       'A4':'A4_stk','A5':'A5_stk','A6':'A6_stk',
                                       'A7':'A7_stk','A8':'A8_stk','A9':'A9_stk','A10':'A10_stk',},inplace=True)
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        #
        port_count_valued = df.groupby(['month', 'portfolio_name']).apply(
            lambda x: stk_count_valued_ew(x))
        port_count_valued = port_count_valued.reset_index()
        port_count_valued.rename(columns={port_count_valued.columns[-1]: 'count_valued'}, inplace=True)
        port_count_valued = port_count_valued.pivot(index='month', columns='portfolio_name', values='count_valued')
        #
        if para['Is_neutral'] == 'yes':
            port_count_valued.rename(columns={'S1/A1':'S1/A1_v_stk','S1/A2':'S1/A2_v_stk','S1/A3':'S1/A3_v_stk',
                                              'S1/A4':'S1/A4_v_stk','S1/A5':'S1/A5_v_stk','S1/A6':'S1/A6_v_stk',
                                              'S1/A7':'S1/A7_v_stk','S1/A8':'S1/A8_v_stk','S1/A9':'S1/A9_v_stk',
                                              'S1/A10':'S1/A10_v_stk',
                                              'S2/A1': 'S2/A1_v_stk', 'S2/A2': 'S2/A2_v_stk', 'S2/A3': 'S2/A3_v_stk',
                                              'S2/A4': 'S2/A4_v_stk', 'S2/A5': 'S2/A5_v_stk', 'S2/A6': 'S2/A6_v_stk',
                                              'S2/A7': 'S2/A7_v_stk', 'S2/A8': 'S2/A8_v_stk', 'S2/A9': 'S2/A9_v_stk',
                                              'S2/A10': 'S2/A10_v_stk',},inplace=True)
        elif  para['Is_neutral'] == 'no':
            port_count_valued.rename(columns={'A1':'A1_v_stk','A2':'A2_v_stk','A3':'A3_v_stk',
                                          'A4':'A4_v_stk','A5':'A5_v_stk','A6':'A6_v_stk',
                                          'A7':'A7_v_stk','A8':'A8_v_stk','A9':'A9_v_stk','A10':'A10_v_stk',},
                                 inplace=True)
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        #
        if len(port_ret) >= len(port_count):
            port_1 = pd.merge(port_ret, port_count, on='month', how='left' )
        else:
            port_1 = pd.merge(port_ret, port_count, on='month', how='right')
        #
        if len(port_1) >= len(port_count_valued):
            port_2 = pd.merge(port_1, port_count_valued, on= 'month', how='left')
        else:
            port_2 = pd.merge(port_1, port_count_valued, on= 'month', how='right')
        return port_2
    #
    def anomaly_ret_long_short(self,port_ret,port_ret_ew,para):
        port_ret = port_ret.copy()
        port_ret_ew = port_ret_ew.copy()
        if para['Is_neutral'] == 'yes':
            port_ret['L-S'] = (port_ret['S1/A10'] + port_ret['S2/A10']) / 2 - \
                               (port_ret['S1/A1'] + port_ret['S2/A1'] ) / 2
            port_ret_ew['L-S'] = (port_ret_ew['S1/A10'] + port_ret_ew['S2/A10']) / 2 - \
                                  (port_ret_ew['S1/A1'] + port_ret_ew['S2/A1']  ) /2
        elif para['Is_neutral'] == 'no':
            port_ret['L-S'] = port_ret['A10'] - port_ret['A1']
            port_ret_ew['L-S'] = port_ret_ew['A10'] - port_ret_ew['A1']
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        '''得到 anomaly_ret'''
        anomaly_ret = port_ret.loc[:, ['L-S']].copy()
        anomaly_ret = anomaly_ret.reset_index()
        anomaly_ret.columns = ['month', 'L-S']

        anomaly_ret_ew = port_ret_ew.loc[:, ['L-S']].copy()
        anomaly_ret_ew = anomaly_ret_ew.reset_index()
        anomaly_ret_ew.columns = ['month', 'L-S']
        anomaly_ret_ew.rename(columns={'L-S':'L-S-ew'},inplace=True)

        df_anomaly_ret = pd.merge(anomaly_ret,anomaly_ret_ew,on='month')
        return df_anomaly_ret
    def anomaly_ret_long_short_(self, port_ret,para):
        port_ret = port_ret.copy()
        if para['Is_neutral'] == 'yes':
            try:
                port_ret['L-S'] = (port_ret['S1/A10'] + port_ret['S2/A10'] ) / 2 - \
                                  (port_ret['S1/A1'] + port_ret['S2/A1'] ) / 10
            except KeyError as e:
                print('key error', e)
                print('calculate long-short ret by predictor <' + para['anomaly'] +
                      '> failed may due to incomplete deciles ')
                print('deciles:',port_ret.columns)
                port_ret['L-S'] = np.nan
            else:
                port_ret['L-S'] = (port_ret['S1/A10'] + port_ret['S2/A10'] ) / 2 - \
                                  (port_ret['S1/A1'] + port_ret['S2/A1'] ) / 10
        elif para['Is_neutral'] == 'no':
            try:
                port_ret['L-S'] = port_ret['A10'] - port_ret['A1']
            except KeyError as e:
                print('key error', e)
                print('calculate long-short ret by predictor <' + para['anomaly'] +
                      '> failed may due to incomplete deciles ')
                print('deciles:',port_ret.columns)
                port_ret['L-S'] = np.nan
            else:
                port_ret['L-S'] = port_ret['A10'] - port_ret['A1']
        else:
            raise Exception('set wrong parameter of para[Is_neutral]')
        # 得到 anomaly_ret
        #anomaly_ret = port_ret.loc[:, ['L-S']].copy()
        #anomaly_ret = anomaly_ret.reset_index()
        # anomaly_ret.columns = ['month', 'L-S']
        anomaly_ret = port_ret.copy()
        anomaly_ret.rename(columns={'L-S': para['anomaly']}, inplace=True)
        print('month:', anomaly_ret.index.min(), anomaly_ret.index.max())
        return anomaly_ret
#====================================================================================
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
