import numpy as np
import pandas as pd
import statsmodels.api as sm
import time
#==========================================================================
def get_rsquared_xy_dict(df, var_y_dict, var_x_dict, period=36):
    # 将要进行回归计算的全部 x 和 y 写成 dict 形式传进来
    length = len(df)
    for it in range(len(var_x_dict)):
        name = 'r_' + list(var_y_dict.keys())[0] + '_' + list(var_x_dict.keys())[it]
        df[name] = None
    for it in range(period, length): # 这里之所以用for循环是因为rolling 滚动计算只能返回 scaler 不能返回 list
        y = df[list(var_y_dict.values())[0]].iloc[it-36:it]
        for it1 in range(len(var_x_dict)):
            x = df[list(var_x_dict.values())[it1]].iloc[it-36:it]
            column_name = 'r_' + list(var_y_dict.keys())[0] + '_' + list(var_x_dict.keys())[it1]
            df[column_name].iloc[it] = sm.OLS(y,sm.add_constant(x)).fit().rsquared
    return df
#
def get_rsquared_xy(df, var_y, var_x, column_name,period=36):
    # var_y 和 var_x 分别对应某一个 column
    length = len(df)
    df[column_name] = None
    for it in range(period, length):# 这里之所以用for循环是因为rolling 滚动计算只能返回 scaler 不能返回 list
        y = df[var_y].iloc[it-period:it]
        x = df[var_x].iloc[it-period:it]
        df[column_name].iloc[it] = sm.OLS(y,sm.add_constant(x)).fit().rsquared
    return df
#
def get_rolling_list_xy(df, var_y, var_x,column_name_y,column_name_x,period=36):
    # var_y 和 var_x 分别对应某一个 column
    length = len(df)
    df[column_name_y] = None
    df[column_name_x] = None
    for it in range(period, length):
        df[column_name_y].iloc[it] = np.array(df[var_y].iloc[it-period:it])
        df[column_name_x].iloc[it] = np.array(df[var_x].iloc[it-period:it])
    return df
#
def get_rolling_list_xy_dict(df,var_y_dict, var_x_dict,period=36):
    # 将要进行回归计算的全部 x 和 y 写成 dict 形式传进来
    # y 一般对应某一列， x 可以对应多列
    length = len(df)
    name_y = list(var_y_dict.keys())[0] + '_' + 'list'
    df[name_y] = None
    for it in range(len(var_x_dict)):
        name_x =  list(var_x_dict.keys())[it] + '_' + 'list'
        df[name_x] = None
    for it in range(period, length): # 这里之所以用for循环是因为rolling 滚动计算只能返回 scaler 不能返回 list
        df[name_y].iloc[it] = np.array(df[list(var_y_dict.values())[0]].iloc[it-period:it])
        for it1 in range(len(var_x_dict)):
            column_name = list(var_x_dict.keys())[it1] + '_' + 'list'
            df[column_name].iloc[it] = np.array(df[list(var_x_dict.values())[it1]].iloc[it-period:it])
    return df
#===================================================================
def get_factor_rolling_list_ch3(panel,mret,mkt,smb,vmg,index,para):
    panel = panel.copy()
    para_panel = para
    mret_list = mret
    mkt_list = mkt
    smb_list = smb
    vmg_list = vmg
    index_list = index
    def get_df_list_by_rolling(x, df, period):
        if x >= period:
            mret = df['mret'].iloc[x - period: x]
            mkt = df['mkt'].iloc[x - period: x]
            smb = df['smb'].iloc[x - period: x]
            vmg = df['vmg'].iloc[x - period: x]
            mret_list.append(list(mret))
            mkt_list.append(list(mkt))
            smb_list.append(list(smb))
            vmg_list.append(list(vmg))
            index_list.append(df.index[x - 1])
        return 1
    def get_df_by_groupby(df, period=36):
        # print(df)
        df0 = pd.DataFrame({0: list(range(len(df)))})
        df0[0].rolling(1).apply(lambda x: get_df_list_by_rolling(int(x[0]), df, period=period), raw=True)
        return
    panel.groupby('stkcd').apply(
        lambda x: get_df_by_groupby(x, period=para_panel['exclude_count_trade_mnt'])).reset_index(drop=True)
    return mret_list,mkt_list,smb_list,vmg_list,index_list
#==============================================================================================================
def calculate_rsquared_ch3(df,index,mret,mkt,smb,vmg):
    dff = pd.DataFrame()
    dff.index = index
    dff['mret'] = mret
    dff['mkt'] = mkt
    dff['smb'] = smb
    dff['vmg'] = vmg
    dff['mkt_smb'] = dff.apply( lambda x: [x['mkt'], x['smb']],axis=1)
    dff['mkt_vmg'] = dff.apply( lambda x: [x['mkt'], x['vmg']],axis=1)
    dff['mkt_smb_vmg'] = dff.apply( lambda x: [x['mkt'], x['smb'], x['vmg']], axis=1)
    #
    dff['merged_mret_mkt'] = dff.apply(lambda x: (x['mret'], x['mkt']), axis=1) # 形成元组列
    dff['r_mret_mkt'] = dff['merged_mret_mkt'].apply(lambda x: sm.OLS(np.array(x[0]),
                                                                          sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    #
    dff['merged_mret_mkt_smb'] = dff.apply(lambda x: (x['mret'], x['mkt_smb']), axis=1) # 形成元组列
    dff['r_mret_mkt_smb'] = dff['merged_mret_mkt_smb'].apply(lambda x: sm.OLS(np.array(x[0]),
                                                                        sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    dff['merged_mret_mkt_vmg'] = dff.apply(lambda x: (x['mret'], x['mkt_vmg']), axis=1) # 形成元组列
    dff['r_mret_mkt_vmg'] = dff['merged_mret_mkt_vmg'].apply(lambda x: sm.OLS(np.array(x[0]),
                                                                          sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    dff['merged_mret_mkt_smb_vmg'] = dff.apply(lambda x: (x['mret'], x['mkt_smb_vmg']), axis=1) # 形成元组列
    dff['r_mret_mkt_smb_vmg'] = dff['merged_mret_mkt_smb_vmg'].apply(lambda x: sm.OLS(np.array(x[0]),
                                                                          sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    df = pd.concat([df,dff],axis=1)
    return df
def calculate_OLS_all_ch3(df,index,mret,mkt,smb,vmg):
    # 将OLS 能输出的结果全部返回出来
    dff = pd.DataFrame()
    dff.index = index
    dff['mret'] = mret
    dff['mkt'] = mkt
    dff['smb'] = smb
    dff['vmg'] = vmg
    dff['mkt_smb'] = dff.apply( lambda x: [x['mkt'], x['smb']],axis=1)
    dff['mkt_vmg'] = dff.apply( lambda x: [x['mkt'], x['vmg']],axis=1)
    dff['mkt_smb_vmg'] = dff.apply( lambda x: [x['mkt'], x['smb'], x['vmg']], axis=1)
    #
    dff['merged_mret_mkt'] = dff.apply(lambda x: (x['mret'], x['mkt']), axis=1) # 形成元组列
    dff['r_mret_mkt'] = dff['merged_mret_mkt'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    dff['alpha_mret_mkt'] = dff['merged_mret_mkt'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().params[0])
    dff['ta_mret_mkt'] = dff['merged_mret_mkt'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().tvalues[0])# 关于 alpha 的 t 值
    #
    dff['merged_mret_mkt_smb'] = dff.apply(lambda x: (x['mret'], x['mkt_smb']), axis=1) # 形成元组列
    dff['r_mret_mkt_smb'] = dff['merged_mret_mkt_smb'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    dff['alpha_mret_mkt_smb'] = dff['merged_mret_mkt_smb'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().params[0])
    dff['ta_mret_mkt_smb'] = dff['merged_mret_mkt_smb'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().tvalues[0])
    #
    dff['merged_mret_mkt_vmg'] = dff.apply(lambda x: (x['mret'], x['mkt_vmg']), axis=1) # 形成元组列
    dff['r_mret_mkt_vmg'] = dff['merged_mret_mkt_vmg'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    dff['alpha_mret_mkt_vmg'] = dff['merged_mret_mkt_vmg'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().params[0])
    dff['ta_mret_mkt_vmg'] = dff['merged_mret_mkt_vmg'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().tvalues[0])
    #
    dff['merged_mret_mkt_smb_vmg'] = dff.apply(lambda x: (x['mret'], x['mkt_smb_vmg']), axis=1) # 形成元组列
    dff['r_mret_mkt_smb_vmg'] = dff['merged_mret_mkt_smb_vmg'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().rsquared)
    dff['alpha_mret_mkt_smb_vmg'] = dff['merged_mret_mkt_smb_vmg'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().params[0])
    dff['ta_mret_mkt_smb_vmg'] = dff['merged_mret_mkt_smb_vmg'].apply(
        lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().tvalues[0])
    df = pd.concat([df,dff],axis=1)
    return df
#===============================================================================================
class regression_OLS():
    def __init__(self,panel,para,model_name):
        self.model_name = model_name
        self.panel = panel
        self.para = para
    def rsquared(self):
        t1 = time.time()
        if self.model_name == 'ch3':
            mret_roll = []
            mkt_roll = []
            smb_roll = []
            vmg_roll = []
            index_roll = []
            panel_ = self.panel.copy()
            mret_list, mkt_list, smb_list, vmg_list, index_list = \
                get_factor_rolling_list_ch3(panel=panel_,
                                            mret=mret_roll,mkt=mkt_roll,smb=smb_roll,vmg=vmg_roll,
                                            index=index_roll,para=self.para)
            panel = calculate_rsquared_ch3(df=panel_, index=index_list, mret=mret_list, mkt=mkt_list, smb=smb_list,
                                       vmg=vmg_list)
        else:
            raise Exception('input wrong model name')
        print('spending time of using rolling methods to calculate rsquared \n',
              time.time() - t1)  # 216.6257779598236
        return panel
    def OLS_all(self):
        t1 = time.time()
        if self.model_name == 'ch3':
            mret_roll = []
            mkt_roll = []
            smb_roll = []
            vmg_roll = []
            index_roll = []
            panel_ = self.panel.copy()
            mret_list, mkt_list, smb_list, vmg_list, index_list = \
                get_factor_rolling_list_ch3(panel=panel_,
                                            mret=mret_roll,mkt=mkt_roll,smb=smb_roll,vmg=vmg_roll,
                                            index=index_roll,para=self.para)
            panel = calculate_OLS_all_ch3(df=panel_, index=index_list, mret=mret_list, mkt=mkt_list, smb=smb_list,
                                       vmg=vmg_list)
        else:
            raise Exception('input wrong model name')
        print('spending time of using rolling methods to calculate OLS_all \n',
              time.time() - t1)
        return panel