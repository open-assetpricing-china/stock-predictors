'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# ms: Sum of 8 indicator variables for fundamental performance
# following the corresponding definitions in Mohanram (2005).
# G1: ROA >= ind.median; ROA = Net Income / average assets
# G2: CFROA >= ind.median; CFROA = cash form operations / average assets
# G3: CFROA >= ROA;
# G4: VARROA <= ind.median; VARROA = variance of ROA over past four years
# G5: VARSGR <= ind.median; VARSGR = variance of SGR over past four years
# G6: RDINT > ind.median; RDINT = R & D / total asset.
# G7: CAPINT > ind.median; CAPINT = capital expenditure scaled by total assets
# G8: ADINT > ind.median; ADINT = advertising expenses / total assets.
#================================================
# SGR: Sustainable Growth Rate 可持续增长率
# SGR = 销售净利率 * 总资产周转率 * 权益乘数 * 留存收益率
# SGR = 权益资本收益率 * （1 - 股利支付比率）
# 销售净利率 = 净利润除以销售收入
# 'D000101000' : Net profit ==> 净利润
# 'B001100000' : Total Operating Revenue ==> represents the 销售收入总额
# 总资产周转率=销售收入总额/资产平均总额×100%
# 'B001100000' : Total Operating Revenue ==> represents the 销售收入总额
# 'A001000000' : Total asset , average asset = (total_asset_(t-1) + total_asset_(t)) / 2
#  权益乘数=资产总额/股东权益总额 =  1/(1-资产负债率);
# 'A002000000' :  Total Liabilities 负债合计
# 'A003200000' : Minority Interests 少数股东权益
# 'A003000000' : Total Shareholders’ Equity  所有者权益合计
# 留存收益率=留存的收益/净利润*100% =(净利润-分配给股东的利润)/净利润*100%
# 'B002000000 : Net profit ==> 净利润
# 'B002000101' : Net Profit Attributable to Owners of the Parent Company 归属于母公司所有者的净利润
# =======================================================
# ROA: 资产收益率=净利润/资产
# 'B002000000' : Net profit ==> 净利润
# 'A001000000' : Total asset
# ==============================================================
# CFROA >= ind.median; CFROA = cash form operations / average assets
# 'C001000000' :  Net Cash Flow from Operating Activities 经营活动产生的现金流量净额
# ====================================================================
# G6: RDINT > ind.median; RDINT = R & D / total asset.
# 'A001219000' : Research & Development Expenses
#===========================================================================
# G7: CAPINT > ind.median; CAPINT = capital expenditure scaled by total assets 资本支出
# 在企业的经营活动中，供长期使用的、其经济寿命将经历许多会计期间的资产如：
# 固定资产、无形资产、递延资产等都要作为资本性支出。
# 即先将其资本化，形成固定资产、无形资产、递延资产等。
# 而后随着他们为企业提供的效益，在各个会计期间转销为费用。
# 固定资产: A001212000 ： Net Fixed Assets 固定资产净额
# 无形资产：A001218000 ： Net Intangible Assets 无形资产净额
# 延递资产：A001222000 ： Deferred Income Tax Assets 递延所得税资产
# ===============================================================================
# G8: ADINT > ind.median; ADINT = advertising expenses / total assets.
# 'B001209000' : Selling Expenses => represents advertising expenses
# The expenses incurred by an enterprise in the sales of products, including expenses involved
# in transportation, loading and unloading, packaging, insurance, exhibition, advertising, etc
# 企业销售产品所发生的费用，包括运输、装卸、包装、保险、展览、广告等费用
#======================================================================================
def mean_value(x):
    x['ROA_ind'] = x['ROA'].mean()
    x['CFROA_ind'] = x['CFROA'].mean()
    x['VARROA_ind'] = x['VARROA'].mean()
    x['VARSGR_ind'] = x['VARSGR'].mean()
    x['RDINT_ind'] = x['RDINT'].mean()
    x['CAPINT_ind'] = x['CAPINT'].mean()
    x['ADINT_ind'] = x['ADINT'].mean()
    return x
#
def var(x):
    x['VARROA'] = x['ROA'].rolling(48).var()
    x['VARSGR'] = x['SGR'].rolling(48).var()
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['ms'] = x['ms'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month','B002000000', 'A001000000', 'C001000000',
                    'D000101000', 'B001100000','A003000000', 'B002000101',
                    'A001219000', 'A001212000', 'A001218000', 'A001222000',
                    'B001209000']]
    df_output = df_output.copy()
    df_output['ROA'] = df_output['B002000000'] / df_output['A001000000']
    df_output['CFROA'] = df_output['C001000000'] / df_output['A001000000']
    df_output['SGR_1'] = df_output['B002000000'] / df_output['B001100000']
    df_output['SGR_2'] = df_output['B001100000'] / df_output['A001000000']
    df_output['SGR_3'] = df_output['A001000000'] / df_output['A003000000']
    df_output['SGR_4'] = df_output['B002000101'] / df_output['B002000000']
    df_output['SGR'] = df_output['SGR_1'] * df_output['SGR_2'] * df_output['SGR_3'] * df_output['SGR_4']
    df_output = df_output.groupby('stkcd').apply(var).reset_index(drop=True)
    df_output['RDINT'] = df_output['A001219000'] / df_output['A001000000']
    df_output['CAPINT'] = (df_output['A001212000'] + df_output['A001218000']
                           + df_output['A001222000']) / df_output['A001000000']
    df_output['ADINT'] = df_output['B001209000'] / df_output['A001000000']
    #
    df_output = df_output.groupby(['month', 'stkcd']).apply(mean_value).reset_index(drop=True)
    df_output['G1'] = 0
    df_output.loc[(df_output['ROA'] >= df_output['ROA_ind']), 'G1'] = 1
    df_output['G2'] = 0
    df_output.loc[(df_output['CFROA'] >= df_output['CFROA_ind']),'G2'] = 1
    df_output['G3'] = 0
    df_output.loc[(df_output['CFROA'] >= df_output['ROA']), 'G3'] = 1
    df_output['G4'] = 0
    df_output.loc[(df_output['VARROA'] <= df_output['VARROA_ind']), 'G4'] = 1
    df_output['G5'] = 0
    df_output.loc[(df_output['VARSGR'] <= df_output['VARSGR_ind']), 'G5'] = 1
    df_output['G6'] = 0
    df_output.loc[(df_output['RDINT'] >= df_output['RDINT_ind']), 'G6'] = 1
    df_output['G7'] = 0
    df_output.loc[(df_output['CAPINT'] >= df_output['CAPINT_ind']), 'G7'] = 1
    df_output['G8'] = 0
    df_output.loc[(df_output['ADINT'] >= df_output['ADINT_ind']), 'G8'] = 1
    #
    df_output['ms'] = df_output['G1'] + df_output['G2'] + df_output['G3'] + df_output['G4'] + \
                      df_output['G5'] + df_output['G6'] + df_output['G7'] + df_output['G8']
    df_output = df_output[['stkcd', 'month', 'ms']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output