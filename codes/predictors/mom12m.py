'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# mom12m: 11-month cumulative returns ending one month before month end.
#
def equation(x):
    x['mom12m'] = x['Mclsprc'].pct_change(periods=12).shift(1)
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Mclsprc']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'mom12m']]
    return df_output