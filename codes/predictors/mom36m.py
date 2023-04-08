'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Cumulative returns from months t-36 to t-13
#
def equation(x):
    x['mom36m'] = (x['Mclsprc'].shift(13) - x['Mclsprc'].shift(36)
                    ) / x['Mclsprc'].shift(36)
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Mclsprc']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'mom36m']]
    return df_output