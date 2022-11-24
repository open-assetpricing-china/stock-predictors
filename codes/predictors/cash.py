# 'A001101000' : cash and cash equivalents
# df['A001000000'] -> Total Asset
def lag_one_month(x):
    x = x.copy()
    x['cash'] = x['cash'].shift()
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001101000', 'A001000000']]
    df_output = df_output.copy()
    df_output['cash'] = (df_output['A001101000'] / df_output['A001000000']).shift()
    df_output = df_output[['stkcd', 'month', 'cash']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output
