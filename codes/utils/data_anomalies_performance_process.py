import pandas as pd
import numpy as np
import statsmodels.api as sm
class anomaly_performance_preprocessing(object):
    def __init__(self, df_anomaly, df_factor, para):
        self.df_anomaly = df_anomaly
        self.df_factor = df_factor
        self.para = para
    def date_cross_select(self): # 取 df_anomaly 和 df_factor 的日期的交集
        date_cross = list(set(list(self.df_factor['month'])) & set(list(self.df_anomaly['month'])))
        date_cross.sort()
        self.df_factor = self.df_factor.copy()
        self.df_factor['date_select'] = self.df_factor['month'].apply(
            lambda x: 'keep' if x in date_cross else 'remove').reset_index(drop=True)
        self.df_anomaly = self.df_anomaly.copy()
        self.df_anomaly['date_select'] = self.df_anomaly['month'].apply(
            lambda x: 'keep' if x in date_cross else 'remove').reset_index(drop=True)
        #
        self.df_factor = self.df_factor.loc[self.df_factor['date_select'] == 'keep']
        self.df_factor.drop('date_select', axis = 1, inplace=True)
        #
        self.df_anomaly = self.df_anomaly.loc[self.df_anomaly['date_select'] == 'keep']
        self.df_anomaly.drop('date_select', axis = 1, inplace=True)
        #
        return
    def table_merge(self):
        self.date_cross_select()
        table = pd.merge(self.df_anomaly,self.df_factor,on='month')
        return table
#
class anomaly_performance_remove_NaN(object):
    def remove_nan(self, df):
        df = df.copy()
        df.dropna(inplace = True)
        return df
#
class anomaly_performance_filter_trddays(object):
    def df_fix_trddays_range(self, df, para):
        df1 = df.copy()
        date_max = df1['month'].max()
        date_min = df1['month'].min()
        if para['start_date'] > date_max or para['end_date'] < date_min:
            raise Exception('please reset the date range for regression ')
        else:
            df1 = df1[(df1['month'] >= para['start_date']) &
                      (df1['month'] <= para['end_date'])].reset_index(drop=True)
        return df1
class anomaly_performance_regression(object):
    def capm_OLS(self, table, para):
        y = table[para['anomaly']]
        x = table['mkt']
        ols_model = sm.OLS(y, sm.add_constant(x)).fit()
        return ols_model
    def ch3_OLS(self,table, para):
        y = table[para['anomaly']]
        x = table[['mkt','smb','vmg']]
        ols_model = sm.OLS(y, sm.add_constant(x)).fit()
        return ols_model
#====================================================================
# 形成元组列，通过 rolling 的方式得到滚动的 list
def get_rolling_list(table,anomaly,mkt,smb,vmg,index,para):
    table = table.copy()
    table['group'] = 'aaa' # 正加一列辅助列，用于下面的 table.groupby('group') 操作
    para_table = para
    anomaly_list = anomaly
    mkt_list = mkt
    smb_list = smb
    vmg_list = vmg
    index_list = index
    def get_df_list_by_rolling(x, df, period):
        if x >= period:
            anomaly = df[para_table['anomaly']].iloc[x - period: x]
            mkt = df['mkt'].iloc[x - period: x]
            smb = df['smb'].iloc[x - period: x]
            vmg = df['vmg'].iloc[x - period: x]
            anomaly_list.append(list(anomaly))
            mkt_list.append(list(mkt))
            smb_list.append(list(smb))
            vmg_list.append(list(vmg))
            index_list.append(df.index[x - 1])
        return 1
    def get_df_by_groupby(df, period):
        # print(df)
        df0 = pd.DataFrame({0: list(range(len(df)))})
        df0[0].rolling(1).apply(lambda x: get_df_list_by_rolling(int(x[0]), df, period=period), raw=True)
        return
    table.groupby('group').apply(
        lambda x: get_df_by_groupby(x, period=para_table['rolling_period'])).reset_index(drop=True)
    return anomaly_list,mkt_list,smb_list,vmg_list,index_list
#=====================================================================
class anomaly_performance_regression_rolling(object):
    def rolling_list(self,table,para):
        anomaly_roll = []
        mkt_roll = []
        smb_roll = []
        vmg_roll = []
        index_roll = []
        table = table.copy()
        anomaly_list ,mkt_list, smb_list, vmg_list, index_list = \
            get_rolling_list(table=table,anomaly=anomaly_roll,mkt=mkt_roll, smb=smb_roll, vmg=vmg_roll,
                             index=index_roll, para=para)
        dff = pd.DataFrame()
        dff.index = index_list
        dff[para['anomaly']] = anomaly_list
        dff['mkt'] = mkt_list
        dff['smb'] = smb_list
        dff['vmg'] = vmg_list
        month = table.loc[dff.index]['month']
        dff['month'] = month
        return dff
    def capm_OLS_rolling(self,table,para):
        table_rolling = self.rolling_list(table=table,para=para)
        table_rolling['merged_anomaly_mkt'] = table_rolling.apply(lambda x: (x[para['anomaly']], x['mkt']), axis=1)  # 形成元组列

        table_rolling['r_squared'] = table_rolling['merged_anomaly_mkt'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().rsquared)

        table_rolling['r_squared_adj'] = table_rolling['merged_anomaly_mkt'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().rsquared_adj)

        table_rolling['alpha'] = table_rolling['merged_anomaly_mkt'].apply(
            lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().params[0])

        table_rolling['beta_mkt'] = table_rolling['merged_anomaly_mkt'].apply(
            lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().params[1])

        table_rolling['t_alpha'] = table_rolling['merged_anomaly_mkt'].apply(
            lambda x: sm.OLS(np.array(x[0]), sm.add_constant(np.array(x[1]).T)).fit().tvalues[0])

        return  table_rolling[['month',para['anomaly'],'mkt','alpha',
                               'beta_mkt','r_squared','r_squared_adj','t_alpha',]]

    def ch3_OLS_rolling(self,table,para):
        table_rolling = self.rolling_list(table=table, para=para)
        table_rolling['mkt_smb_vmg'] = table_rolling.apply(lambda x: [x['mkt'], x['smb'], x['vmg']], axis=1)
        table_rolling['merged_anomaly_mkt_smb_vmg'] = table_rolling.apply(
            lambda x: (x[para['anomaly']], x['mkt_smb_vmg']), axis=1)  # 形成元组列
        table_rolling['r_squared'] = table_rolling['merged_anomaly_mkt_smb_vmg'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().rsquared)
        table_rolling['r_squared_adj'] = table_rolling['merged_anomaly_mkt_smb_vmg'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().rsquared_adj)
        table_rolling['alpha'] = table_rolling['merged_anomaly_mkt_smb_vmg'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().params[0])
        table_rolling['beta_mkt'] = table_rolling['merged_anomaly_mkt_smb_vmg'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().params[1])
        table_rolling['beta_smb'] = table_rolling['merged_anomaly_mkt_smb_vmg'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().params[2])
        table_rolling['beta_vmg'] = table_rolling['merged_anomaly_mkt_smb_vmg'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().params[3])
        table_rolling['t_alpha'] = table_rolling['merged_anomaly_mkt_smb_vmg'].apply(
            lambda x: sm.OLS(np.array(x[0]),sm.add_constant(np.array(x[1]).T)).fit().tvalues[0])

        return table_rolling[['month',para['anomaly'],'mkt','smb','vmg',
                              'alpha','beta_mkt','beta_smb','beta_vmg','r_squared','r_squared_adj','t_alpha']]
