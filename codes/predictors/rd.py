'''
@Author: Yi Tian
@Email: 12232985@mail.sustech.edu.cn
'''
# rd: An indicator variable equal to 1 if R&D expense as a percentage of total assets has an
# increase greater than 5%.
# R&D expenses: 'A001219000'
# Total asset:  'A001000000'
# R&D expenses/Total asset increase > 0.05则rd=1,否则为0
#
def equation(x):
    x['rd'] = (x['A001219000']/x['A001000000'])/(x['A001219000'].shift(3)/x['A001000000'].shift(3))
    x['rd'][x['rd'] <= 1.05] = 0
    x['rd'][x['rd'] > 1.05] = 1
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['rd'] = x['rd'].shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001000000', 'A001219000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'rd']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output