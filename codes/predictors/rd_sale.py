# Total Operating Revenue:df['B001100000']
# R&D expenses:df['A001219000']
def parameter():
    para = {}
    para['predictor'] = 'rd_sale'
    para['relate_finance_index'] = ['B001100000', 'A001219000']
    return para
def equation(df):
    df = df.copy()
    df['rd_sale'] = df['A001219000'] / df['B001100000']
    return df