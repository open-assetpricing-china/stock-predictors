'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# roic: Quarterly earnings before interest and taxes minus nonoperating
# income divided by non-cash enterprise value
# 'B001000000' : Total profit (earnings before interest and taxes)
# 'B001400000' : Non-operating Income
#Enterprise Value(企业价值) = Market Capitalization(市值) +Debt(负债) – Cash(现金)
# 'Msmvttl' : size = market capitalization
# 'A002000000' : Total Liabilities
# 'A001101000' : cash and cash equivalents
#
def equation(x):
    EV = x['Msmvttl'] + x['A002000000'] - x['A001101000']
    x['roic'] = (x['B001000000'] - x['B001400000']).shift() / EV.shift() # lag one month
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001000000', 'B001400000',
                                     'A002000000', 'A001101000', 'Msmvttl']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roic']]
    return df_output
#