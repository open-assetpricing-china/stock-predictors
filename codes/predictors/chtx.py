# chtx: Percent change in taxes from quarter t-1 to t.
# 'A002113000' : Taxes Payable
#
def parameter():
    para = {}
    para['predictor'] = 'chtx'
    para['relate_finance_index'] = ['A002113000']
    return para
def equation(df):
    df = df.copy()
    df['chtx'] = df['A002113000'].pct_change(periods=3)
    return df