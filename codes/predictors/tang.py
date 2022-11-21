# tang: Cash holdings + 0.715 * receivables + 0.547 * inventory + 0.535 * fixed assets / total assets.
# 'A001101000' : cash and cash equivalents
# 'A001000000' -> Total Asset
# 'A001111000' : Net Accounts Receivable
# 'A001123000' : Net inventories
# 'A001212000' : Net Fixed Assets
#
def equation(x):
    x['tang'] = (x['A001101000'] + 0.715 * x['A001111000'] + 0.547 * x['A001123000'] + \
                 0.535 * (x['A001212000'] / x['A001000000'])).shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001101000', 'A001111000', 'A001123000', 'A001212000', 'A001000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'tang']]
    return df_output