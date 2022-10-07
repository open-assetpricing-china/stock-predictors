# dy: Total dividends divided by market capitalization at year end
# 'A002115000' : Dividends Payable
#
def parameter():
    para = {}
    para['predictor'] = 'dy'
    para['relate_finance_index'] = ['A002115000', 'size']
    return para
def equation(df):
    df = df.copy()
    df['dy'] = df['A002115000'] / df['size']
    return df
#
