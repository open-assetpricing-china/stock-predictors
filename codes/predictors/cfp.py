# 'D000100000' : Net Cash Flow from Operating Activities
def parameter():
    para = {}
    para['predictor'] = 'cfp'
    para['relate_finance_index'] = ['size','D000100000']
    return para
def equation(df):
    df = df.copy()
    df['cfp'] = df['D000100000'] / df['size']
    return df