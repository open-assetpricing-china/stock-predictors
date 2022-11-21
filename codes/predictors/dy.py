# dy: Total dividends divided by market capitalization at year end
# 'A002115000' : Dividends Payable
# 'Msmvttl': 'size'
def equation(x):
    x['dy'] = x['A002115000'] / x['Msmvttl']
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A002115000', 'Msmvttl']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'dy']]
    return df_output