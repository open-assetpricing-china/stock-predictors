'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# bm: Book-to-market ratio, which equals the book value of equity divided by market capitalization
# book value of equity: 'A001000000'(total asset)
# 'Msmvttl': 'size'
#
def lag_one_month(x):
    x = x.copy()
    x['bm'] = x['bm'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'A001000000']]
    df_output = df_output.copy()
    df_output['bm'] = (df_output['A001000000'] / df_output['Msmvttl']) # df['A001000000'] -> Total Asset
    df_output = df_output[['stkcd', 'month', 'bm']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output