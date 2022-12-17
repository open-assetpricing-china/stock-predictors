'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# pchcapx_ia : Industry adjusted percentage change in capital expenditure
#===========================================================================
# 在企业的经营活动中，供长期使用的、其经济寿命将经历许多会计期间的资产如：
# 固定资产、无形资产、递延资产等都要作为资本性支出。
# 即先将其资本化，形成固定资产、无形资产、递延资产等。
# 而后随着他们为企业提供的效益，在各个会计期间转销为费用。
# 固定资产: A001212000 ： Net Fixed Assets 固定资产净额
# 无形资产：A001218000 ： Net Intangible Assets 无形资产净额
# 延递资产：A001222000 ： Deferred Income Tax Assets 递延所得税资产
def mean_value(x):
    x['pchcapx_ind'] = x['pchcapx'].mean()
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchcapx_ia'] = x['pchcapx_ia'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001212000', 'A001218000',
                                     'A001222000','ind_cd']]
    df_output = df_output.copy()
    df_output['pchcapx'] = df_output['A001212000'] + df_output['A001218000'] + df_output['A001222000']
    df_output = df_output.groupby(['month', 'ind_cd']).apply(mean_value).reset_index(drop=True)
    df_output['pchcapx_ia'] = df_output['pchcapx'] - df_output['pchcapx_ind']
    df_output = df_output[['stkcd', 'month', 'pchcapx_ia']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output