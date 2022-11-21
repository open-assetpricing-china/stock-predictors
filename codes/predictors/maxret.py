#
# Maximum daily return from returns during month t-1.
#
def equation(x):
    return x['dret'].max()
#
def month_shift(x):
    x['maxret'] = x['maxret'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['daily'][['stkcd', 'day', 'month', 'dret']]
    df_output = df_output.groupby(['stkcd', 'month']).apply(equation).reset_index()
    new_column = list(df_output.columns)[-1]
    df_output.rename(columns={new_column:'maxret'}, inplace=True)
    df_output = df_output.groupby('stkcd').apply(month_shift).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'maxret']]
    return df_output