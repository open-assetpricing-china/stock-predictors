# lev : Total liabilities divided by quarter-end market capitalization
# 'A002000000': Total Liabilities
# 'Msmvttl': 'size'
def equation(x):
    x['lev'] = (x['A002000000'] / x['Msmvttl']).shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A002000000','Msmvttl']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'lev']]
    return df_output