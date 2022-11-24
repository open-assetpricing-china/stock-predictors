# zerotrade Turnover weighted number of zero trading days in month t - 1.
# ['Mnshrtrd'] = 'Number of Shares Traded in Month (MNSHRTRD)'  # 当月交易的股票数量（MNSHRTRD）
# ['Mnvaltrd'] = 'Value of Shares Traded in Month (MNVALTRD)'  # 当月交易的股票价值（MNVALTRD）
# ['Msmvosd'] = 'Market Value of Tradable Shares (MSMVOSD)'  # 可交易股份的市场价值（MSMVOSD）
# 'Ndaytrd': 'trdday'
# 'Mnvaltrd': 'mtrdvalue'
def month_days(x):
    if x[-2:] in ['01', '03', '05', '07', '08', '10', '12']:
       return 31
    elif x[-2:] in ['04', '06', '09', '11']:
        return 30
    else:
        return 28
#
def lag_one_month(x):
    x = x.copy()
    x['zerotrade'] = x['zerotrade'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'Mnvaltrd', 'Msmvosd', 'Ndaytrd']]
    df_output = df_output.copy()
    df_output['mnt_days'] = df_output['month'].apply(month_days)
    df_output['z_trd_day'] = df_output['mnt_days'] - df_output['Ndaytrd']
    df_output['turnover'] = df_output['Mnvaltrd'] / df_output['Msmvosd']
    df_output['zerotrade'] = (df_output['turnover'] * df_output['z_trd_day'])
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output[['stkcd', 'month', 'zerotrade']]