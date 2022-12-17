'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# 6-month cumulative return.
def equation(x):
    x['mom6m'] = x['Mclsprc'].pct_change(periods=6).shift(1)
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Mclsprc']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'mom6m']]
    return df_output