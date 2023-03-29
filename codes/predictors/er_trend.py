'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# er_trend: This trend factor is constructed following the definition in Liu et al. (2020)
# python pandas ewm 一次指数加权移动平均 : https://blog.csdn.net/small__roc/article/details/123482186
# ['Dnshrtrd'] = '日个股交易股数' # 流通股本
import statsmodels.api as sm
import numpy as np
import pandas as pd
def get_ma_mv(x, lag):
    x1 = x.copy()
    x1.dropna(subset=['Clsprc', 'Dnshrtrd'], inplace=True)
    #print('len(x1):', len(x1))
    if len(x1) > 0:
        last_p = x1['Clsprc'].iloc[-1].item()
        last_v = x1['Dnshrtrd'].iloc[-1].item()
        if len(x1) > lag:
            x['MP'] = x1['Clsprc'].iloc[-lag:].mean() / last_p
            x['MV'] = x1['Dnshrtrd'].iloc[-lag:].mean() /last_v
        else:
            x['MP'] = x1['Clsprc'].mean() / last_p
            x['MV'] = x1['Dnshrtrd'].mean() / last_v
        return x
    else:
        x['MP'] = np.nan
        x['MV'] = np.nan
        return x
#
def get_MP(x, lag):
    x1 = x.copy()
    x1.dropna(subset=['Clsprc', 'Dnshrtrd'], inplace=True)
    if len(x1) > 0:
        last_p = x1['Clsprc'].iloc[-1].item()
        if len(x1) > lag:
            MP = x1['Clsprc'].iloc[-lag:].mean() / last_p
        else:
            MP = x1['Clsprc'].mean() / last_p
        return MP
    else:
        MP= np.nan
        return MP
#
def get_MV(x, lag):
    x1 = x.copy()
    x1.dropna(subset=['Clsprc', 'Dnshrtrd'], inplace=True)
    #print('len(x1):', len(x1))
    if len(x1) > 0:
        last_v = x1['Dnshrtrd'].iloc[-1].item()
        if len(x1) > lag:
            MV = x1['Dnshrtrd'].iloc[-lag:].mean() /last_v
        else:
            MV = x1['Dnshrtrd'].mean() / last_v
        return MV
    else:
        MV = np.nan
        return MV
#
def get_Clsprc(x):
    x1 = x.copy()
    x1.dropna(subset=['Clsprc'], inplace=True)
    if len(x1) > 0:
        return x1['Clsprc'].iloc[-1].item()
    else:
        return np.nan
#
def daily_to_month(x):
    x = x.copy()
    x.drop_duplicates(subset=['month'], keep='last', inplace=True, ignore_index=True)
    return x

#
def cross_sectional_regression(x):
    #x.dropna(subset=['MP', 'MV'], inplace=True) #
    x1 = x.copy()
    x1.replace([np.inf, -np.inf], np.nan, inplace=True)
    x1.dropna(subset=['MP', 'MV'], inplace=True)
    #x1['MP','MV'].replace([np.inf, -np.inf], np.nan).dropna(axis=1)
    #x['MP'].fillna(value=0, inplace = True)
    #x['MV'].fillna(value=0, inplace = True)
    if len(x1) > 0:
        r = np.array(list(x1['Clsprc'])).T
        mp = list(x1['MP'])
        mv = list(x1['MV'])
        m = np.array([mp, mv]).T
        #print('m: \n', m)
        params = sm.OLS(r, sm.add_constant(m)).fit().params
        x['alpha'] = params[0]
        x['beta_mp'] = params[1]
        x['beta_mv'] = params[2]
        return x
    else:
        x['alpha'] = np.nan
        x['beta_mp'] = np.nan
        x['beta_mv'] = np.nan
        return x
#
def month_lag(x, lag):
    x['beta_mp'] = x['beta_mp'].shift(lag)
    x['beta_mv'] = x['beta_mv'].shift(lag)
    return x
#
def E_moving_average(x, la):
    x['E_beta_mp'] = x['beta_mp'].ewm(alpha=la,adjust=False).mean()
    x['E_beta_mv'] = x['beta_mv'].ewm(alpha=la, adjust=False).mean()
    return x
#
def equation(x):
    x['er_trend'] = x['E_beta_mp'] * x['MP'] + x['E_beta_mv'] * x['MV']
    return x
#
def calculation(df_input):
    df_output = df_input['daily'][['stkcd','day','month','Clsprc','Dnshrtrd']]
    #df_output = df_output.groupby(['stkcd', 'month']).apply(lambda x: get_ma_mv(x,lag=10)).reset_index(drop=True)
    #df_output = df_output.groupby('stkcd').apply(lambda x: daily_to_month(x)).reset_index(drop=True)
    df_output_MP = df_output.groupby(['stkcd', 'month']).apply(lambda x: get_MP(x,lag=10)).reset_index()
    df_output_MP.rename(columns={list(df_output_MP.columns)[-1]:'MP'}, inplace=True)
    #
    df_output_MV = df_output.groupby(['stkcd', 'month']).apply(lambda x: get_MV(x, lag=10)).reset_index()
    df_output_MV.rename(columns={list(df_output_MV.columns)[-1]:'MV'}, inplace=True)
    #
    df_output_Clsprc = df_output.groupby(['stkcd', 'month']).apply(lambda x: get_Clsprc(x)).reset_index()
    df_output_Clsprc.rename(columns={list(df_output_Clsprc.columns)[-1]:'Clsprc'}, inplace=True)
    #
    if len(df_output_MP) >= len(df_output_MV):
        df_output_ = pd.merge(df_output_MP,df_output_MV, on=['stkcd', 'month'], how='left')
    else:
        df_output_ = pd.merge(df_output_MP,df_output_MV, on=['stkcd', 'month'], how='right')
    if len(df_output_) >= len(df_output_Clsprc):
        df_output_1 = pd.merge(df_output_,df_output_Clsprc, on=['stkcd','month'],how='left')
    else:
        df_output_1 = pd.merge(df_output_,df_output_Clsprc, on=['stkcd', 'month'], how='right')
    # 做截面回归
    df_output_1 = df_output_1.groupby('month').apply(lambda x: cross_sectional_regression(x)).reset_index(drop=True)
    # 滞后一期
    df_output_1 = df_output_1.groupby('stkcd').apply(lambda x: month_lag(x, lag=1)).reset_index(drop=True)
    # 计算指数移动平均
    df_output_1 = df_output_1.groupby('stkcd').apply(lambda x: E_moving_average(x,la=0.02)).reset_index(drop=True)
    #
    df_output_1 = df_output_1.groupby('stkcd').apply(equation).reset_index(drop=True)
    return df_output_1[['stkcd', 'month', 'er_trend']]

