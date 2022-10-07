# pchquick: Percentage change in quick ratio.
# Quick Ratio = (Current assets - Inventory - Prepaid expenses) / Current Liabilities
# 'A001100000' : Total Current Assets
# 'A001123000' : Net inventories
# 'A001112000' : Net Prepayments
# 'A002100000' : Total Current Liabilities
#
def parameter():
    para = {}
    para['predictor'] = 'pchquick'
    para['relate_finance_index'] = ['A001100000', 'A001123000', 'A001112000', 'A002100000']
    return para
#
def equation(df):
    df = df.copy()
    df['pchquick'] = ((df['A001100000'] - df['A001123000'] - df['A001112000'] ) / df['A002100000']
                           ).pct_change()
    return df
