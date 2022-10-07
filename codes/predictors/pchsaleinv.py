# pchsaleinv : Quarterly percentage change in sales-to-inventory.
# D000113000 : Decrease of Inventories
#
def parameter():
    para = {}
    para['predictor'] = 'pchsaleinv'
    para['relate_finance_index'] = ['D000113000']
    return para
#
def equation(df):
    df = df.copy()
    df['pchsaleinv'] = df['D000113000'].pct_change(periods=3)
    return df
#