# invest : The sum of annual change in fixed assets and annual change in
# inventories divided by lagged total assets.
#  'A001123000' :  Net Inventories 净存货
#  'A001212000' :  Net Fixed Assets
#  'A001000000' :  Total Assets
def parameter():
    para = {}
    para['predictor'] = 'invest'
    para['relate_finance_index'] = ['A001123000', 'A001212000', 'A001000000']
    return para
def equation(df):
    df = df.copy()
    df['invest'] = (df['A001212000'].diff(periods=12) + df['A001123000'].diff(periods=12)
                    ) / df['A001000000'].shift(12)
    return df
