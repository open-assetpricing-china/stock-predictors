# std_dolvol :
# Monthly standard deviation of daily RMB trading volume
# 'Ahshrtrd_D': 日盘后成交量
# ['Ahvaltrd_D'] = '日盘后成交总额' # 元
# 'Dnvaltrd' = '日个股交易金额' # 单位： 元
def equation(x):
    return x['Dnvaltrd'].std()
def daily_to_monthly(x):
    x.drop_duplicates(subset=['month'], keep='last', inplace=True, ignore_index=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['std_dolvol'] = x['std_dolvol'].shift()
    return x

def calculation(df_input):
    df_output = df_input['daily'][['stkcd', 'day','month', 'Dnvaltrd']]
    #df_output = df_output.groupby(['stkcd','month']).apply(equation).reset_index(drop=True)
    #df_output = df_output.groupby('stkcd').apply(daily_to_monthly).reset_index(drop=True)
    df_output = df_output.groupby(['stkcd', 'month']).apply(equation).reset_index()
    df_output.rename(columns={list(df_output.columns)[-1]:'std_dolvol'}, inplace=True)
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True) # lag one month
    return df_output[['stkcd', 'month', 'std_dolvol']]