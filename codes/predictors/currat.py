# currrat: The ratio of current assets to current liabilities
# 'A001100000', current assets
# 'A002100000', current liabilities
def parameter():
    para = {}
    para['predictor'] = 'currat'
    para['relate_finance_index'] = ['A001100000', 'A002100000']
    return para
def equation(df):
    df = df.copy()
    df['currat'] = df['A001100000'] / df['A002100000']
    return df
