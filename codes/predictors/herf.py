'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# herf: Sum of squared percent sales in industry for each company.
# 'B001100000' : Total operating revenue, ==> sales
def equation_s_p_sale(x):
    x['p_sale'] = x['B001100000' ] / x['B001100000' ].sum()
    return x
#
def equation(x):
    x['herf'] = x['s_p_sale'].sum()
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['herf'] = x['herf'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'ind_cd','B001100000' ]]
    df_output = df_output.groupby(['month','ind_cd']).apply(equation_s_p_sale).reset_index(drop=True)
    df_output['s_p_sale'] = df_output['p_sale'] * df_output['p_sale']
    df_output = df_output.groupby(['month', 'ind_cd']).apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'herf']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output