'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# Monthly percent change in shares outstanding
# 'Msmvttl' : 'size'
def equation(x):
    x = x.copy()
    x['chcsho'] = (x['Msmvttl'] / x['Mclsprc']).pct_change()
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['chcsho'] = x['chcsho'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'Mclsprc']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chcsho']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output