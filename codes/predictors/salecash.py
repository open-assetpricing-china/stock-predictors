# salecash: Quarterly sales divided by cash and cash equivalents
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'A001101000' : cash and cash equivalents
#

def equation(x):
    x['salecash'] = x['C001001000'] / x['A001101000']
    return x

def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month','C001001000', 'A001101000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'salecash']]
    return df_output