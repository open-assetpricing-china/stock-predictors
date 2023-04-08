'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# pchsale_pchrect: Quarterly percentage change in sales minus quarterly percentage change
# in receivables
# 'B001100000' : Total operating revenue, ==> sales
# 'A001111000' : Net Accounts Receivable
#
def equation(x):
    x['pchsale_pchrect'] = x['B001100000'].pct_change(periods=3) - \
                           x['A001111000'].pct_change(periods=3)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchsale_pchrect'] = x['pchsale_pchrect'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A001111000',]]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchsale_pchrect' ]]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output