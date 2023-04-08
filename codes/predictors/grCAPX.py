'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# grCAPX : Percent change in capital expenditures from year t-2 to year t.
# 'C002006000' : Cash Paid to Acquire and Construct Fixed Assets, Intangible Assets and Other Long-term Assets
#
def equation(df):
    df['grCAPX'] = df['C002006000'].pct_change(24)
    return df
#
def lag_one_month(x):
    x = x.copy()
    x['grCAPX'] = x['grCAPX'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'C002006000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'grCAPX']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output