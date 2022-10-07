# gma: Revenue minus cost of goods sold divided by lagged total assets.
# 'B001100000' : Total Revenue
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# df['A001000000'] -> Total Asset
#
def parameter():
    para = {}
    para['predictor'] = 'gma'
    para['relate_finance_index'] = ['B001100000','C001001000','A001000000']
    return para
def equation(df):
    df = df.copy()
    df['gma'] = (df['B001100000'] - df['C001001000']) / df['A001000000'].shift(3)
    return df