#
# cashspr
# (size + long term debt - total assets) / (cash and cash equivalents)
# 'size': size
# 'A002203000': long term debt
# 'A001000000': total assets
# 'A001101000': cash and cash equivalents
def parameter():
    para = {}
    para['predictor'] = 'cashspr'
    para['relate_finance_index'] = ['size','A002203000', 'A001000000', 'A001101000']
    return para
def equation(df):
    df = df.copy()
    df['cashspr'] = (df['size'] + df['A002203000'] -df['A001000000']) / df['A001101000']
    return df