# Standard deviation of 16 quarters of income before extraordinary items divided by average total assets.
# Total assets: A001000000
# Total Comprehensive Income: df['B006000000']

def equation(x):
    x['roavol'] = x['B006000000'].rolling(48).std() / x['A001000000'].rolling(48).mean()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001000000', 'B006000000' ]]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roavol']]
    return df_output