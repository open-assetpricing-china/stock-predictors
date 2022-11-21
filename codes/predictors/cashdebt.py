# 'B002000000' : Net Profit
# df['A002000000'] -> Total Liabilities
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B002000000','A002000000' ]]
    df_output = df_output.copy()
    df_output['cashdebt'] = (df_output['B002000000'] / df_output['A002000000']).shift()
    df_output = df_output[['stkcd', 'month', 'cashdebt']]
    return df_output
