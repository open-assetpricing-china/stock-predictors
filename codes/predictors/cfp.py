# 'D000100000' : Net Cash Flow from Operating Activities
# 'Msmvttl' : size
def calculation(df_input):
     df = df_input['monthly']
     df_output = df[['stkcd', 'month', 'Msmvttl', 'D000100000']]
     df_output['cfp'] = (df['D000100000'] / df['Msmvttl']).shift()
     df_output = df_output[['stkcd', 'month', 'cfp']]
     return df_output