# operprof : Quarterly operating profit divided by lagged commom shareholders' equity
# Total shareholders' equity: 'A003000000'
# Operating Profit : 'B001300000'
#
#
def parameter():
    para = {}
    para['predictor'] = 'operprof'
    para['relate_finance_index'] = ['A003000000','B001300000']
    return para
#
def equation(df):
    df = df.copy()
    df['operprof'] = df['B001300000'] / df['A003000000'].shift(3)
    return df
