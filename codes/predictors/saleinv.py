'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# saleinv: Quarterly sales divided by total inventory
# 'B001100000' : Total operating revenue, ==> sales
# 'A001123000' : Net inventories

def equation(x):
    x['saleinv'] = (x['B001100000'] / x['A001123000']).shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month','B001100000', 'A001123000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'saleinv']]
    return df_output