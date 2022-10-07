# pchgm_pchsale : Percentage change in gross margin minus Percentage
# change in sales.
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'B001209000' : Selling Expenses
def parameter():
    para = {}
    para['predictor'] = 'pchgm_pchsale'
    para['relate_finance_index'] = ['C001001000', 'B001209000']
    return para
#
def equation(df):
    df = df.copy()
    df['pchgm_pchsale'] = ((df['C001001000'] - df['B001209000']) / df['C001001000']
                           ).pct_change() - df['C001001000'].pct_change()
    return df