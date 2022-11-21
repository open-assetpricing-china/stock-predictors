# roic: Quarterly earnings before interest and taxes minus nonoperating income divided by non-cash enterprise value
# Total Profit: B001000000
# Non-operating Income: B001400000
# Total Liabilities: A002000000
# Ending Balance of Cash and Cash Equivalents: C006000000
# 'Msmvttl' : size
def equation(x):
    EV = x['Msmvttl'] + x['A002000000'] - x['C006000000']
    x['roic'] = (x['B001000000'] - x['B001400000']).shift() / EV.shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001000000', 'B001400000',
                                     'A002000000', 'C006000000', 'Msmvttl']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roic']]
    return df_output