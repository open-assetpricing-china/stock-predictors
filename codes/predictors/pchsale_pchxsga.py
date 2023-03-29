'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# pchsale_pchxsga: Quarterly percentage change in sales minus quarterly
# percentage change in management expenses.
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'B0F1208000' : Business and Management Expenses
#*******************************************************
def equation(x):
    x['pchsale_pchxsga'] = x['C001001000'].pct_change(periods=3) - x['B0F1208000'].pct_change(periods=3)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchsale_pchxsga'] = x['pchsale_pchxsga'].shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'C001001000', 'B0F1208000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchsale_pchxsga']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return  df_output