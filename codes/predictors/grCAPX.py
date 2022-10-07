# grCAPX : Percent change in capital expenditures from year t-2 to year t.
# 'C002006000' : Cash Paid to Acquire and Construct Fixed Assets, Intangible Assets and Other Long-term Assets
#
def parameter():
    para = {}
    para['predictor'] = 'grCAPX'
    para['relate_finance_index'] = ['C002006000']
    return para
def equation(df):
    df = df.copy()
    df['grCAPX'] = df['C002006000'].pct_change(24)
    return df