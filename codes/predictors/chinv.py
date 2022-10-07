# chinv: Change in inventory scaled by total assets
# 'A001123000' : Net Inventories 净存货
# 'A001000000' :  total asset
#
def parameter():
    para = {}
    para['predictor'] = 'chinv'
    para['relate_finance_index'] = ['A001123000','A001000000']
    return para
def equation(df):
    df = df.copy()
    df['chinv'] = df['A001123000'].diff() / df['A001000000']
    return df