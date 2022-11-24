# # df['A001000000'] -> total assets
def equation(x):
    x['agr'] = (x['A001000000'] - x['A001000000'].shift(12)) / x['A001000000'].shift(12)
    return x
#
def lag_one_month(x):
    x= x.copy()
    x['agr'] = x['agr'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001000000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'agr']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)# lag one month
    return df_output