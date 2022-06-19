#
import pandas as pd
import statsmodels.api as sm
#
# 统计每个股票交易月的个数
def trade_mnt_count(x, var,):
    x['count_' + var] = len(x[var])
    return x
#===================================================
class panel_preprocessing(object):
    def __init__(self, df, factor_ret, para):
        self.df = df
        self.factor_ret = factor_ret
        self.para = para
    def get_panel(self):
        panel = pd.merge(self.df, self.factor_ret, left_on='month', right_on='month')
        return panel
class panel_process_filter_tradays(object):
    def panel_exclude_trddays_mnt(self,panel, para):
        panel = panel.groupby('stkcd').apply(trade_mnt_count, var='month').reset_index(drop=True) # 总共交易月数
        panel = panel[panel['count_month'] > para['exclude_count_trade_mnt']]
        panel = panel.drop(columns='count_month')
        panel = panel.dropna().sort_values(by=['stkcd', 'month'])
        return panel
class panel_canonical_form(object): # 将 panel 的形式规整化
    def __init__(self,panel,para):
        self.panel = panel
        self.para = para
    def canonicalize(self):
        self.panel = self.panel.sort_values(by=['stkcd','month'])
        self.panel = self.panel[self.para['std_columns']]
        return self.panel
#====================================
def OLS_ff3(df,ff3):
    ff3['month'] = pd.to_datetime(ff3['month'], format='%Y-%m-%d')
    ff3.rename(columns={'mkt':'ffmkt'},inplace=True)
    ff3.month = ff3.month.dt.strftime('%Y-%m')
    df_ff3_ch3 = pd.merge(ff3, df, left_on='month', right_on='month')
    df_ff3_ch3 = df_ff3_ch3.dropna()
    y_ff3_smb = df_ff3_ch3.ffsmb
    y_ff3_hml = df_ff3_ch3.ffhml
    y_ch3_smb = df_ff3_ch3.smb
    y_ch3_vmg = df_ff3_ch3.vmg
    x_ff3 = df_ff3_ch3[['ffmkt', 'ffsmb', 'ffhml']]
    x_ch3 = df_ff3_ch3[['mkt', 'smb', 'vmg']]
    '''mod1 & mod2 adopt ff3 factor as dependent var check significant level of alpha
    mod3 & mod4 adopt ch3 factor as dependent var check significant level of alpha '''
    table = pd.DataFrame(columns=['para', 'tvalues'])
    mod1 = sm.OLS(y_ff3_smb, sm.add_constant(x_ch3)).fit()
    mod2 = sm.OLS(y_ff3_hml, sm.add_constant(x_ch3)).fit()
    mod3 = sm.OLS(y_ch3_smb, sm.add_constant(x_ff3)).fit()
    mod4 = sm.OLS(y_ch3_vmg, sm.add_constant(x_ff3)).fit()
    table.para = [mod1.params[0], mod2.params[0], mod3.params[0], mod4.params[0]]
    table.tvalues = [mod1.tvalues[0], mod2.tvalues[0], mod3.tvalues[0], mod4.tvalues[0]]
    return table