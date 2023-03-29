'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# cashdebt: Earnings divided by total liabilities.
# 'B002000000' : Net Profit
# 'A002000000' :  Total Liabilities
def lag_one_month(x):
    x = x.copy()
    x['cashdebt'] = x['cashdebt'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B002000000','A002000000' ]]
    df_output = df_output.copy()
    df_output['cashdebt'] = (df_output['B002000000'] / df_output['A002000000'])
    df_output = df_output[['stkcd', 'month', 'cashdebt']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output
