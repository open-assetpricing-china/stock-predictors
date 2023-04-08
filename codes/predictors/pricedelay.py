'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# The proportion of variation in weekly returns for 36 months ending in month t
# explained by 4 lages of weekly market returns incremental to
# contemporanuous market return.
#===============================================================================
import statsmodels.api as sm
import numpy as np
# 'Wsmvttl' : size
def regression(x, lag, periods):
    x['pricedelay'] = np.nan
    if len(x) > periods + lag:
        for it in range(periods+lag, len(x)):
            list_wret = list(x['wret'].iloc[it-periods:it])
            list_vwret = list(x['vw_ret'].iloc[it-periods-lag:it-lag])
            model = sm.OLS(np.array(list_wret).T,sm.add_constant(np.array(list_vwret).T)).fit()
            x['pricedelay'].iloc[it] = model.rsquared  # print(model.intercept_) # print(model.coef_)
    else:
        x['pricedelay'] = np.nan
    return x
#
def week_to_month(x):
    x.drop_duplicates(subset=['month'], keep='last', inplace=True, ignore_index=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pricedelay'] = x['pricedelay'].shift()
    return x
def calculation(df_input):
    df = df_input['weekly']
    df_output = df[['stkcd', 'week', 'month', 'Wsmvttl','wret']]
    df_output = df_output.copy()
    df_output['vw_ret'] = df_output.groupby('week').apply(lambda x: (x['wret'] * x['Wsmvttl']).sum() / x['Wsmvttl'].sum()).reset_index(drop=True)
    df_output.sort_values('week', inplace=True)
    df_output['vw_ret'].fillna(method='ffill', inplace=True)
    df_output['wret'].fillna(method='ffill', inplace=True)
    df_output.dropna(subset = ['wret', 'vw_ret'], inplace = True)
    df_output.sort_values(by=['stkcd','week'], inplace=True)
    df_output = df_output.groupby('stkcd').apply(lambda x: regression(x=x, lag=4, periods=4*36)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(lambda x: week_to_month(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'week', 'month', 'pricedelay']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output