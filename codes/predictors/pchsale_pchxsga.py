# pchsale_pchxsga: Quarterly percentage change in sales minus quarterly
# percentage change in management expenses.
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'B0F1208000' : Business and Management Expenses
#*******************************************************
# 注意在 df_input['monthly'] 数据中找不到 'B0F1208000' 列
def equation(x):
    x['pchsale_pchxsga'] = x['C001001000'].pct_change(periods=3) - x['B0F1208000'].pct_change(periods=3)
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'C001001000', 'B0F1208000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchsale_pchxsga']]
    return  df_output