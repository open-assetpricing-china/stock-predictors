# cinvest : Change over one quarter in fixed assets divided by sales - average of this variable for
# prior 3 quarters
# 'A001212000' :  Net Fixed Assets
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
#
def equation(x):
    x['cinvest'] = (x['A001212000'] / x['C001001000']).diff(periods=3) - (
            x['A001212000'] / x['C001001000']).rolling(9).mean().shift(3)
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output= df[['stkcd', 'month', 'A001212000', 'C001001000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'cinvest']]
    return df_output