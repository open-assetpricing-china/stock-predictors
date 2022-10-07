# pchsale_pchxsga: Quarterly percentage change in sales minus quarterly
# percentage change in management expenses.
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'B0F1208000' : Business and Management Expenses
def parameter():
    para = {}
    para['predictor'] = 'pchsale_pchxsga'
    para['relate_finance_index'] = ['C001001000', 'B0F1208000' ]
    return para
#
def equation(df):
    df = df.copy()
    df['pchsale_pchxsga'] = df['C001001000'].pct_change(periods=3) - df['B0F1208000'].pct_change(periods=3)
    return df
#
#
#