'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# turn: Average monthly trading volume for month t-3 to t-1 scaled
# by number of shares outstanding in month t.
# 平均交易量 / 总股本
# 'Mnshrtrd' = '月个股交易股数'
# 'Msmvttl' : size
def equation(x):
    x['trd_v'] = x['Mnshrtrd'].rolling(3).mean()
    x['trd_v_1'] = x['trd_v'].shift() # lag one month
    x['turn'] = x['trd_v_1'] / (x['Msmvttl'] / x['Mclsprc']).shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'Mclsprc', 'Msmvttl', 'Mnshrtrd']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'turn']]
    return df_output
#