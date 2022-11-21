# Monthly percent change in shares outstanding
#
# 'Msmvttl' : 'size'
def equation(x):
    x = x.copy()
    x['chcsho'] = (x['Msmvttl'] / x['Mclsprc']).pct_change()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'Mclsprc']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chcsho']]
    return df_output