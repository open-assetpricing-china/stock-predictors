#
# Monthly percent change in shares outstanding
def parameter():
    para = {}
    para['predictor'] = 'chcsho'
    para['relate_finance_index'] = ['size','clsprc']
    return para
def equation(df):
    df = df.copy()
    df['chcsho'] = (df['size'] / df['clsprc']).pct_change()
    return df