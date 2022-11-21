# 'D000100000' : Net Cash Flow from Operating Activities
#
# 'Msmvttl' : 'size'
def mean_value(x):
    x['cfp_ind_mean'] = x['cfp'].mean()
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'D000100000', 'ind_cd']]
    df_output = df_output.copy()
    df_output['cfp'] = df['D000100000'] / df['Msmvttl']
    df_output = df_output.groupby(['month', 'ind_cd']).apply(lambda x: mean_value(x)).reset_index(drop=True)
    df_output['cfp_ia'] = (df_output['cfp'] - df_output['cfp_ind_mean']).shift()
    df_output = df_output[['stkcd', 'month', 'cfp_ia']]
    return df_output