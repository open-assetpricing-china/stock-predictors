'''
@Author: Yi Tian
@Email: 12232985@mail.sustech.edu.cn
'''
# turn: Average monthly trading volume for month t-3 to t-1 scaled
# by number of shares outstanding in month t.
# 平均交易量 / 总股本
# 'Msmvttl' : size
def equation(x):
    x['trd_v'] = x['Mnshrtrd'].rolling(3).mean()
    x['trd_v_1'] = x['trd_v'].shift()
    x['turn'] = x['trd_v_1'] / (x['Msmvttl'] / x['Mclsprc']).shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'Mclsprc', 'Msmvttl', 'Mnshrtrd']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'turn']]
    return df_output
#