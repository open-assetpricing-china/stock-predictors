'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# cinvest : Change over one quarter in fixed assets divided by sales - average of this variable for
# prior 3 quarters
# 'A001212000' :  Net Fixed Assets
# 'B001100000' : Total operating revenue, ==> sales
def equation(x):
    x['cinvest'] = (x['A001212000'] / x['B001100000']).diff(periods=3) - (
            x['A001212000'] / x['B001100000']).rolling(9).mean().shift(3)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['cinvest'] = x['cinvest'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output= df[['stkcd', 'month', 'A001212000', 'B001100000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'cinvest']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output