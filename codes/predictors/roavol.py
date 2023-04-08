'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Standard deviation of 16 quarters of income before extraordinary items divided by average total assets.
# 'B001100000': Total Operating Revenue, The sum of all income arising from operating business of the company.
# 'A001000000': Total assets
def equation(x):
    x['roavol'] = x['B001100000'].rolling(48).std() / x['A001000000'].rolling(48).mean()
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['roavol'] = x['roavol'].shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001000000', 'B001100000' ]]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roavol']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output