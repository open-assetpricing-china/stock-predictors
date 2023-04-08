'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# sp: Quarterly sales divided by quarter-end market capitalization
# 'B001100000' : Total operating revenue, ==> sales
# 'Msmvttl' : size
def equation(x):
    x['sp'] = (x['B001100000'] / x['Msmvttl']).shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'Msmvttl', 'B001100000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'sp']]
    return  df_output