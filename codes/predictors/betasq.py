'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Stock-level market beta squared.
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import numpy as np
#
# 'Wsmvttl' : size
def regression(x, periods1, periods2):
    x['betasq'] = np.nan
    lr = LinearRegression()
    if (len(x) > periods1) and (len(x) < periods2):
        for it in range(periods1, len(x)):
            list_wret = list(x['wret'].iloc[it-periods1:it])
            list_vwret = list(x['vw_ret'].iloc[it-periods1:it])
            #params = sm.OLS(np.array(list_wret).T,sm.add_constant(np.array(list_vwret).T)).fit().params
            model = lr.fit(X=np.array(list_vwret).reshape(-1,1),y=np.array(list_wret).reshape(-1,1))
            x['betasq'].iloc[it] = model.coef_[0, 0] ** 2  # print(model.intercept_) # print(model.coef_)
    elif len(x) > periods2:
        for it in range(periods2, len(x)):
            list_wret = list(x['wret'].iloc[it-periods2:it])
            list_vwret = list(x['vw_ret'].iloc[it-periods2:it])
            #params = sm.OLS(np.array(list_wret).T,sm.add_constant(np.array(list_vwret).T)).fit().params
            model = lr.fit(X=np.array(list_vwret).reshape(-1,1),y=np.array(list_wret).reshape(-1,1))
            x['betasq'].iloc[it] = model.coef_[0, 0]  # print(model.intercept_) # print(model.coef_)
    else:
        x['betasq'] = np.nan
    return x
#
def week_to_month(x):
    x.drop_duplicates(subset=['month'], keep='last', inplace=True, ignore_index=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['betasq'] = x['betasq'].shift()
    return x
#
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
    df_output = df_output.groupby('stkcd').apply(lambda x: regression(x=x,periods1=52, periods2=3*52)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(lambda x: week_to_month(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'week', 'month', 'betasq']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output
#
