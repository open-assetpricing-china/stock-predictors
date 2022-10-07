# Depreciation divided by fixed assets.
# 'D000103000' : Depreciation of Fixed Assets, Oil and Gas Assets, and Bearer Biological Assets
# 'A001212000' :  Net Fixed Assets
#
def parameter():
    para = {}
    para['predictor'] = 'depr'
    para['relate_finance_index'] = ['D000103000', 'A001212000']
    return para
def equation(df):
    df = df.copy()
    df['depr'] = df['D000103000'] / df['A001212000']
    return df
#
