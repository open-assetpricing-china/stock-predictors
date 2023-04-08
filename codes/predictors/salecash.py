'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# salecash: Quarterly sales divided by cash and cash equivalents
# 'B001100000' : Total operating revenue, ==> sales
# 'A001101000' : cash and cash equivalents
#
def equation(x):
    x['salecash'] = (x['B001100000'] / x['A001101000']).shift() # lag one month
    return x

def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month','B001100000', 'A001101000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'salecash']]
    return df_output