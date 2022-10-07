# orgcap: Capitalized management expenses.
# This characteristic uses expense data acquired from CSMAR and is constructed
# according to the definition in Eisfeldt and Papanikolaou (2013)
#
def parameter():
    para = {}
    para['predictor'] = 'orgcap'
    para['relate_finance_index'] = ['A003000000','B001300000']
    return para
#
def equation(df):
    df = df.copy()
    df['orgcap'] = df['B001300000'] / df['A003000000'].shift(3)
    return df