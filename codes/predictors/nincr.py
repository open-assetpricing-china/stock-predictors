'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# nincr: Number of consecutive quarters (up to eight quarters) with an
# increase in earnings.
# Net Profit : 'B002000000'
#
def equation(x):
    x['earn_diff'] = x['B002000000'] - x['B002000000'].shift(3)
    x['earn_dummy'] = x['earn_diff'].apply(lambda x: 1 if x>=0 else 0)
    x['nincr'] = x['earn_dummy'].rolling(24).sum()
    x.drop(columns=['earn_diff', 'earn_dummy'], inplace=True)
    return x
def lag_one_month(x):
    x = x.copy()
    x['nincr'] = x['nincr'].shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B002000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'nincr']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output