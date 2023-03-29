'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# operprof : Quarterly operating profit divided by lagged commom shareholders' equity
# Total shareholders' equity: 'A003000000'
# Operating Profit : 'B001300000'
#
def equation(x):
    x['operprof'] = x['B001300000'] / x['A003000000'].shift(3)
    return x
def lag_one_month(x):
    x = x.copy()
    x['operprof'] = x['operprof'].shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A003000000','B001300000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'operprof']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output