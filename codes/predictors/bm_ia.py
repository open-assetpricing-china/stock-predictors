'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# bm: Book-to-market ratio, which equals the book value of equity divided by market capitalization
# 'Msmvttl' : size
#
def mean_value(x):
    x['bm_ind_mean'] = x['bm'].mean()
    return x
def lag_one_month(x):
    x = x.copy()
    x['bm_ia'] = x['bm_ia'].shift()
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'A001000000','ind_cd']]
    df_output = df_output.copy()
    df_output['bm'] = df_output['A001000000'] / df_output['Msmvttl']  # df['A001000000'] -> Total Asset
    df_output = df_output.groupby(['month','ind_cd']).apply(lambda x: mean_value(x)).reset_index(drop=True)
    df_output['bm_ia'] = df_output['bm'] - df_output['bm_ind_mean']
    df_output = df_output[['stkcd', 'month', 'bm_ia']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output