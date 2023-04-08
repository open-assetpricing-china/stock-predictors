'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# stdcf : Standard deviation for 16 quarters of net cash flows divided by sales.
# 'D000100000' : Net Cash Flow from Operating Activities
# 'B001100000' : Total operating revenue, ==> sales
#
def equation(df):
    df['stdcf'] = (df['D000100000'] / df['B001100000']).rolling(48).std()
    return df
def lag_one_month(x):
    x = x.copy()
    x['stdcf'] = x['stdcf'].shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month','D000100000', 'B001100000' ]]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'stdcf']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output