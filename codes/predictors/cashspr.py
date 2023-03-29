'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# cashspr: Cash productivity, which is defined as quarter-end market capitalization plus
# long-term debt minus total assets divided by cash and equivalents.
#
# (size + long term debt - total assets) / (cash and cash equivalents)
# 'size': size
# 'A002203000': (Bonds payable) long term debt
# 'A001000000': total assets
# 'A001101000': cash and cash equivalents
# 'Msmvttl' : size
def equation(x):
    x = x.copy()
    x['cashspr'] = (x['Msmvttl'] + x['A002203000'] -x['A001000000']).shift() / x['A001101000'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month','Msmvttl','A002203000', 'A001000000', 'A001101000' ]]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month','cashspr']]
    return df_output