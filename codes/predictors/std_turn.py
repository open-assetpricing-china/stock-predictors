# std_turn : Monthly standard deviation of daily share turnover
# ['Ahshrtrd_D'] = '日盘后成交总量'
# ['Dnshrtrd'] = '日个股交易股数'
# ['Dnvaltrd'] = '日个股交易金额' # 单位： 元
# ['Dsmvosd'] = '日个股流通市值' # 单位： 千元
# turn = 成交量 / 流通股本
#
def equation(x):
    return x['turn'].std()

def daily_to_monthly(x):
    x.drop_duplicates(subset=['month'], keep='last', inplace=True, ignore_index=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['std_turn'] =x['std_turn'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['daily'][['stkcd', 'month', 'day', 'Dnvaltrd', 'Dsmvosd']]
    df_output = df_output.copy()
    df_output['turn'] = df_output['Dnvaltrd'] / df_output['Dsmvosd']
    #df_output = df_output.groupby(['stkcd','month']).apply(equation).reset_index(drop=True)
    #df_output = df_output.groupby('stkcd').apply(daily_to_monthly).reset_index(drop=True)
    df_output = df_output.groupby(['stkcd', 'month']).apply(equation).reset_index()
    df_output.rename(columns={list(df_output.columns)[-1]:'std_turn'}, inplace=True)
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True) # lag one month
    return df_output[['stkcd', 'month', 'std_turn']]