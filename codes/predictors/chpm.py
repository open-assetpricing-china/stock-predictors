# chpm: Change in income before extraordinary items scaled by scales.
#
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
# 'B001400000': Non-operating Income
def parameter():
    para = {}
    para['predictor'] = 'chpm'
    para['relate_finance_index'] = ['B001400000','C001001000']
    return para
def equation(df):
    df = df.copy()
    df['chpm'] = df['B001400000'].diff() / df['C001001000']
    return df