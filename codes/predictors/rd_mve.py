# rd mve: R&D expense divided by end-of-quarter market capitalization.
# R&D expenses:df['A001219000']
# 'Msmvttl' : size
def equation(x):
    x['rd_mve'] = (x['A001219000'] / x['Msmvttl']).shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'Msmvttl', 'A001219000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'rd_mve']]
    return df_output
#
