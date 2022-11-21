#
# 'Msmvttl': 'size'
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'A001000000']]
    df_output = df_output.copy()
    df_output['bm'] = (df_output['A001000000'] / df_output['Msmvttl']).shift() # df['A001000000'] -> Total Asset
    df_output = df_output[['stkcd', 'month', 'bm']]
    return df_output