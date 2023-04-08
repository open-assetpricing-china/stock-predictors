'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# gma: Revenue minus cost of goods sold divided by lagged total assets.
# 'B001100000' : Total Revenue
# 'B001200000' : Total Operating Costs
# 'A001000000' -> Total Asset
#
def equation(x):
    x['gma'] = (x['B001100000'] - x['B001200000']) / x['A001000000'].shift(3)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['gma'] = x['gma'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B001100000','B001200000','A001000000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'gma']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True) # lag one month
    return df_output