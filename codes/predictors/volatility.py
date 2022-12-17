'''
@Author: Yi Tian
@Email: 12232985@mail.sustech.edu.cn
'''
#
def equation(x):
    return x['dret'].std()
#
def lag_one_month(x):
    x = x.copy()
    x['volatility'] = x['volatility'].shift()
    return x

def calculation(df_input):
    df_output = df_input['daily'][['stkcd', 'day', 'month', 'dret']]
    df_output = df_output.groupby(['stkcd','month']).apply(equation).reset_index()
    df_output.rename(columns={list(df_output.columns)[-1]:'volatility'}, inplace=True)
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True) # lag one month
    return df_output[['stkcd', 'month', 'volatility']]