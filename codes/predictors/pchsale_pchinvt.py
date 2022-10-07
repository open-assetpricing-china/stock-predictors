# Quarterly percentage change in sales minus quarterly percentage change in inventory.
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'A001123000' : Net inventories
#
#
def parameter():
    para = {}
    para['predictor'] = 'pchsale_pchinvt'
    para['relate_finance_index'] = ['C001001000', 'A001123000']
    return para
#
def equation(df):
    df = df.copy()
    df['pchsale_pchinvt'] = df['C001001000'].pct_change(periods=3) - df['A001123000'].pct_change(periods=3)
    return df