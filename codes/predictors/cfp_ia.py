'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# cfp_ia: industry-adjusted operating cash flows.
# 'D000100000' : Net Cash Flow from Operating Activities
# 'Msmvttl' : 'size'
def mean_value(x):
    x['cfp_ind_mean'] = x['cfp'].mean()
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['cfp_ia'] = x['cfp_ia'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'D000100000', 'ind_cd']]
    df_output = df_output.copy()
    df_output['cfp'] = df['D000100000'] / df['Msmvttl']
    df_output = df_output.groupby(['month', 'ind_cd']).apply(lambda x: mean_value(x)).reset_index(drop=True)
    df_output['cfp_ia'] = (df_output['cfp'] - df_output['cfp_ind_mean'])
    df_output = df_output[['stkcd', 'month', 'cfp_ia']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output