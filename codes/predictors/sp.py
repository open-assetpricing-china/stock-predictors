# sp: Quarterly sales divided by quarter-end market capitalization
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
# 'size'
# 'Msmvttl' : size
def equation(x):
    x['sp'] = (x['C001001000'] / x['Msmvttl']).shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'Msmvttl', 'C001001000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'sp']]
    return  df_output