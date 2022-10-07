#
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
# 'A001000000': Total Assets
#
def parameter():
    para = {}
    para['predictor'] = 'chato'
    para['relate_finance_index'] = ['C001001000','A001000000']
    return para
def equation(df):
    df = df.copy()
    df['chato'] = df['C001001000'].diff() / df['A001000000']
    return df