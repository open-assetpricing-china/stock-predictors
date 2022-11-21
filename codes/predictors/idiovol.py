import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import numpy as np
#
# 'Wsmvttl': 'size'
def regression(x, periods1, periods2):
    x['idiovol'] = np.nan
    #lr = LinearRegression()
    if (len(x) > periods1) and (len(x) < periods2):
        for it in range(periods1, len(x)):
            list_wret = list(x['wret'].iloc[it-periods1:it])
            list_ewret = list(x['ew_ret'].iloc[it-periods1:it])
            params_resid = sm.OLS(np.array(list_wret).T,sm.add_constant(np.array(list_ewret).T)).fit().resid
            #model = lr.fit(X=np.array(list_vwret).reshape(-1,1),y=np.array(list_wret).reshape(-1,1))
            x['idiovol'].iloc[it] = np.std(np.array(params_resid))  # print(model.intercept_) # print(model.coef_)
    elif len(x) > periods2:
        for it in range(periods2, len(x)):
            list_wret = list(x['wret'].iloc[it-periods2:it])
            list_ewret = list(x['ew_ret'].iloc[it-periods2:it])
            params_resid = sm.OLS(np.array(list_wret).T,sm.add_constant(np.array(list_ewret).T)).fit().resid
            #model = lr.fit(X=np.array(list_vwret).reshape(-1,1),y=np.array(list_wret).reshape(-1,1))
            x['idiovol'].iloc[it] = np.std(np.array(params_resid))  # print(model.intercept_) # print(model.coef_)
    else:
        x['idiovol'] = np.nan
    return x
#
def week_to_month(x):
    x.drop_duplicates(subset=['month'], keep='last', inplace=True, ignore_index=True)
    return x
#
def calculation(df_input):
    df = df_input['weekly']
    df_output = df[['stkcd', 'week', 'month', 'Wsmvttl','wret']]
    df_output = df_output.copy()
    df_output['ew_ret'] = df_output.groupby('week').apply(lambda x: (x['wret'].sum()) / len(x)).reset_index(drop=True)
    df_output.sort_values('week', inplace=True)
    df_output['ew_ret'].fillna(method='ffill', inplace=True)
    df_output['wret'].fillna(method='ffill', inplace=True)
    df_output.dropna(subset = ['wret', 'ew_ret'], inplace = True)
    df_output.sort_values(by=['stkcd','week'], inplace=True)
    df_output = df_output.groupby('stkcd').apply(lambda x: regression(x=x,periods1=52, periods2=3*52)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(lambda x: week_to_month(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'week', 'month', 'idiovol']]
    return df_output