#
def equation(x):
    return x['dret'].std()
#
#def daily_to_monthly(x):
#    x.drop_duplicates(subset=['month'], keep='last', inplace=True, ignore_index=True)
#    return x
#
def calculation(df_input):
    df_output = df_input['daily'][['stkcd', 'day', 'month', 'dret']]
    df_output = df_output.groupby(['stkcd','month']).apply(equation).reset_index()
    df_output.rename(columns={list(df_output.columns)[-1]:'volatility'}, inplace=True)
    return df_output[['stkcd', 'month', 'volatility']]