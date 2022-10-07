# lev : Total liabilities divided by quarter-end market capitalization
# 'A002000000': Total Liabilities
#
def parameter():
    para = {}
    para['predictor'] = 'lev'
    para['relate_finance_index'] = ['A002000000','size']
    return para
def equation(df):
    df = df.copy()
    df['lev'] = df['A002000000'] / df['size']
    return df