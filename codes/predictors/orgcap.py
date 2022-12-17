'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# orgcap: Capitalized management expenses.
# This characteristic uses expense data acquired from CSMAR and is constructed
# according to the definition in Eisfeldt and Papanikolaou (2013)
#
def equation(x):
    x['orgcap'] = x['B001300000'] / x['A003000000'].shift(3)
    return x

def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A003000000','B001300000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'orgcap']]
    return df_output