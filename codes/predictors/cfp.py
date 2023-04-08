'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# cfp: Operating cash flow divided by quarter-end market capitalization.
# 'D000100000' : Net Cash Flow from Operating Activities
# 'Msmvttl' : size
def lag_one_month(x):
     x = x.copy()
     x['cfp'] = x['cfp'].shift()
     return x
#
def calculation(df_input):
     df = df_input['monthly']
     df_output = df[['stkcd', 'month', 'Msmvttl', 'D000100000']]
     df_output['cfp'] = (df['D000100000'] / df['Msmvttl'])
     df_output = df_output[['stkcd', 'month', 'cfp']]
     df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
     return df_output