# cinvest : Change over one quarter in fixed assets divided by sales - average of this variable for
# prior 3 quarters
# 'A001212000' :  Net Fixed Assets
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
#
def parameter():
    para = {}
    para['predictor'] = 'cinvest'
    para['relate_finance_index'] = ['A001212000', 'C001001000']
    return para
def equation(df):
    df = df.copy()
    df['cinvest'] = (df['A001212000'] / df['C001001000']).diff(periods=3) - (
            df['A001212000'] / df['C001001000']).rolling(9).mean().shift(3)
    return df
