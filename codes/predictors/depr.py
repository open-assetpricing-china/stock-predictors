'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# depr: Depreciation divided by fixed assets.
# 'D000103000' : Depreciation of Fixed Assets, Oil and Gas Assets, and Bearer Biological Assets
# 'A001212000' :  Net Fixed Assets
def equation(x):
    x['depr'] = x['D000103000'] / x['A001212000']
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['depr'] = x['depr'].shift()
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'D000103000', 'A001212000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'depr']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output

