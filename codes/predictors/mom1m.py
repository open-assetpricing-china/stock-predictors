# 1-month cumulative return.
# 'Mclsprc'
def equation(x):
    x['mom1m'] = x['Mclsprc'].pct_change().shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Mclsprc']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'mom1m']]
    return df_output