# pchdepr : Percentage change in depreciation
# 'D000103000' : Depreciation of Fixed Assets, Oil and Gas Assets, and Bearer Biological Assets.
#
def parameter():
    para = {}
    para['predictor'] = 'pchdepr'
    para['relate_finance_index'] = ['D000103000']
    return para
#
def equation(df):
    df = df.copy()
    df['pchdepr'] = df['D000103000'].pct_change()
    return df