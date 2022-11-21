# Average of daily (absolute return / RMB volume) in month t
# para['Ahvaltrd_D'] = '日盘后成交总额' # 元
# ['Dnvaltrd'] = '日个股交易金额' # 单位： 元
# https://doi.org/10.1016/S1386-4181(01)00024-6
#
import numpy as np
def equation(x):
    x1 = x.copy()
    x1.dropna(subset=['dret', 'Dnvaltrd'], inplace=True)
    if len(x1) > 0:
        return (x1['dret'] / x1['Dnvaltrd']).mean()
    else:
        return np.nan
#
def calculation(df_input):
    df_output = df_input['daily'][['stkcd', 'day','month', 'dret', 'Dnvaltrd']]
    df_output = df_output.copy()
    #df_output['Dnvaltrd'][df_output['Dnvaltrd'] < 0.1] = np.nan # 将 0 值替换为空值
    #df_output = df_output.groupby(['stkcd', 'month']).apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby(['stkcd', 'month']).apply(lambda x: equation(x)).reset_index()
    df_output.rename(columns={list(df_output.columns)[-1] : 'ill'}, inplace=True)
    df_output = df_output[['stkcd', 'month', 'ill']]
    return df_output