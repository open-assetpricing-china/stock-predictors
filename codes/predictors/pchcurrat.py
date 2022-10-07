# pchcurrat: Percentage change in current ratio (current liabilities divided by
# current asset)
# 'A001100000' : Total Assets
# 'A002100000' : Total Liabilities
def parameter():
    para = {}
    para['predictor'] = 'pchcurrat'
    para['relate_finance_index'] = ['A002100000','A001100000']
    return para
#
def equation(df):
    df = df.copy()
    df['pchcurrat'] = (df['A002100000'] / df['A001100000']).pct_change()
    return df