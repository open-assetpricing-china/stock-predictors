'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# invest : The sum of annual change in fixed assets and annual change in
# inventories divided by lagged total assets.
#  'A001123000' :  Net Inventories 净存货
#  'A001212000' :  Net Fixed Assets
#  'A001000000' :  Total Assets
#
def equation(x):
    x['invest'] = (x['A001212000'].diff(periods=12) + x['A001123000'].diff(periods=12)
                    ) / x['A001000000'].shift(12)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['invest'] = x['invest'].shift()
    return x

def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001123000', 'A001212000', 'A001000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'invest']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output

