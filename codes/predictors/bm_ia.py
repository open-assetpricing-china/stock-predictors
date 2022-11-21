#
# 'Msmvttl' : size
def mean_value(x):
    x['bm_ind_mean'] = x['bm'].mean()
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'A001000000','ind_cd']]
    df_output = df_output.copy()
    df_output['bm'] = df_output['A001000000'] / df_output['Msmvttl']  # df['A001000000'] -> Total Asset
    df_output = df_output.groupby(['month','ind_cd']).apply(lambda x: mean_value(x)).reset_index(drop=True)
    df_output['bm_ia'] = df_output['bm'] - df_output['bm_ind_mean']
    df_output = df_output[['stkcd', 'month', 'bm_ia']]
    return df_output