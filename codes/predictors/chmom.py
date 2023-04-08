'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# chmom : Cumulative returns from months t - 6 to t - 1 minus months t - 12 to t - 7.
def equation(x):
    x['chmom'] = (x['Mclsprc'].shift(1) - x['Mclsprc'].shift(6)) / x[
        'Mclsprc'].shift(6) - (x['Mclsprc'].shift(7) - x['Mclsprc'].shift(12)) / x['Mclsprc'].shift(12)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['chmom'] = x['chmom'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Mclsprc']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chmom']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output