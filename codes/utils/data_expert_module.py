import codes.utils.data_preprocess as data_pre
import codes.utils.data_factor_process as data_factor
import codes.utils.data_anomalies_process as data_anomaly
import codes.utils.data_postporcess as data_post
import codes.utils.data_anomalies_performance_process as data_anomaly_performance
#
import pandas as pd
def df_process_add_filter(para, df):
    df_class = data_pre.df_preprocessing(df=df,para=para) #
    df_process = data_pre.df_process_size_and_ret()  # 调用处理 size 和 ret 的类
    df_filter_size = data_pre.df_process_filter_size() # 调用过滤 size 的类
    df_filter_trdday = data_pre.df_process_filter_trddays() # 调用 过滤 trddays 的类
    #
    df1 = df_class.df_year_and_mnt_trddays() # 得到滚动的年度交易日和月度交易日
    #df1 = df_process.df_adopt_last_size_and_last_ret_mntly(df=df1,para=para_df1)
    df1 = df_process.df_adopt_default_size_and_ret_mntly(df=df1, para=para)
    df1 = df_filter_size.df_exclude_bottom_size_stocks(df=df1,para=para) # 排除市值<30% 的股票
    # # Exclude stocks with trade days of last month/year less than 15/120 days
    df1 = df_filter_trdday.df_exclude_trddays_last_year_and_mnt(df=df1, para=para) #
    df1 = df_filter_trdday.df_exclude_begin_trddays(df=df1,para=para) # 开始交易日 大于 ‘1999-12’
    return  df1
#
def factor_model_process(df,para):
    df1 = df
    para_factor = para
    rf = pd.read_excel(para['rf_path'])

    factor_group_class = data_factor.factor_ret_group_by_factor_quantile()  # 进行分类,
    factor_portfolio_class = data_factor.factor_ret_group_portfolio_ret()  # 得到分组投资组合收益
    #
    factor_ret =  factor_group_class.ep_and_size(df=df1,para=para_factor) # 根据 ep 和 size 进行分类
    factor_ret = factor_portfolio_class.portfolio_ret(df=factor_ret)
    factor_ret = factor_portfolio_class.portfolio_ret_to_ep_and_size(port_ret=factor_ret) # 得到 SMB, VMG
    factor_ret = factor_portfolio_class.portfolio_ret_to_market(df=df1,factor_ret=factor_ret,rf=rf) # 得到 MKT
    factor_ret_reform = data_factor.factor_ret_canonical_form(factor_ret=factor_ret,para=para_factor)
    factor_ret = factor_ret_reform.canonicalize()
    return factor_ret
#===============================================================================================
#
def predictor_to_portfolio(df, para,predictor):
    para_ = {}
    para_['Is_neutral'] = para['Is_neutral']
    para_['neutral_var'] = 'size'
    para_['way_weight'] = para['way_weight']
    #
    para_['anomaly'] = predictor #
    para_['std_columns'] = ['month'] + [para_['anomaly']]
    para_['columns'] = ['month'] + [para_['anomaly']]
    #
    anomaly_group_class = data_anomaly.anomalies_group_quantile()
    anomaly_ret_class = data_anomaly.anomalies_ret_group()
    #df_anomaly = anomaly_group_class.anomaly_split(df=df, para=para_) # get the decile groups
    df_anomaly = anomaly_group_class.anomaly_split_sort_method(df=df, para = para_)
    if para_['way_weight'] == 'size':
        port_ret = anomaly_ret_class.portfolio_ret(df=df_anomaly, para=para_)
    elif para_['way_weight'] == 'ew':
        port_ret = anomaly_ret_class.portfolio_ret_ew(df=df_anomaly, para = para_)
    else:
        raise Exception('input wrong para[way_weight]')
    anomaly_ret = anomaly_ret_class.anomaly_ret_long_short_(port_ret=port_ret, para=para_)
    return anomaly_ret
#=========================================================================================================
def panel_process_ch3(df,factor,para):
    df1 = df
    factor_ret = factor
    para_panel = para
    panel_class = data_post.panel_preprocessing(df=df1,factor_ret=factor_ret,para=para_panel,)
    panel_process = data_post.panel_process_filter_tradays()

    panel = panel_class.get_panel()
    panel = panel_process.panel_exclude_trddays_mnt(panel=panel,para=para_panel) # 排除总共交易月数小于36个月的股票
    panel_reform = data_post.panel_canonical_form(panel=panel,para=para_panel)
    panel = panel_reform.canonicalize()
    return panel
#================================================================================
def portfolio_regression_ch3(df_portfolio, df_factor, para):
    index_list = ['alpha','beta_mkt','beta_smb','beta_vmg','t_alpha','r_squared', 'r_squared_adj']
    column_list = ['OLS']
    df_performance = pd.DataFrame(index=index_list, columns=column_list)
    table_merge_class = data_anomaly_performance.anomaly_performance_preprocessing(
        df_anomaly=df_portfolio, df_factor= df_factor, para=para)
    table_remove_nan = data_anomaly_performance.anomaly_performance_remove_NaN()
    table_filter_trddays = data_anomaly_performance.anomaly_performance_filter_trddays()
    table_regression = data_anomaly_performance.anomaly_performance_regression()
    #
    table = table_merge_class.table_merge()
    table = table_remove_nan.remove_nan(df=table)  # 去除 NAN 值 #
    table = table_filter_trddays.df_fix_trddays_range(df=table, para=para)
    table_ols_model = table_regression.ch3_OLS(table=table, para=para)  #
    #
    alpha = table_ols_model.params[0]
    beta_mkt = table_ols_model.params[1]
    beta_smb = table_ols_model.params[2]
    beta_vmg = table_ols_model.params[3]
    t_alpha = table_ols_model.tvalues[0]
    r_squared = table_ols_model.rsquared
    r_squared_adj = table_ols_model.rsquared_adj
    #
    p_list = [alpha, beta_mkt, beta_smb, beta_vmg, t_alpha, r_squared, r_squared_adj]
    df_performance['OLS'] = p_list
    return df_performance
#
def portfolio_regression_capm(df_portfolio, df_factor, para):
    index_list = ['alpha','beta','t_alpha','r_squared', 'r_squared_adj']
    column_list = ['OLS']
    df_performance = pd.DataFrame(index=index_list, columns=column_list)
    table_merge_class = data_anomaly_performance.anomaly_performance_preprocessing(
        df_anomaly=df_portfolio, df_factor=df_factor, para=para)
    table_remove_nan = data_anomaly_performance.anomaly_performance_remove_NaN()
    table_filter_trddays = data_anomaly_performance.anomaly_performance_filter_trddays()
    table_regression = data_anomaly_performance.anomaly_performance_regression()
    #
    table = table_merge_class.table_merge()
    #
    table = table_remove_nan.remove_nan(df=table)  # 去除 NAN 值
    table = table_filter_trddays.df_fix_trddays_range(df=table, para=para)
    table_ols_model = table_regression.capm_OLS(table=table, para=para)
    #
    alpha = table_ols_model.params[0]
    beta = table_ols_model.params[1]
    t_alpha = table_ols_model.tvalues[0]
    r_squared = table_ols_model.rsquared
    r_squared_adj = table_ols_model.rsquared_adj
    p_list = [alpha, beta, t_alpha, r_squared, r_squared_adj]
    df_performance['OLS'] = p_list
    return df_performance
#
def portfolio_regression_ch3_rolling(df_portfolio, df_factor, para):
    #
    table_merge_class = data_anomaly_performance.anomaly_performance_preprocessing(
        df_anomaly=df_portfolio, df_factor=df_factor, para=para)
    table_remove_nan = data_anomaly_performance.anomaly_performance_remove_NaN()
    table_filter_trddays = data_anomaly_performance.anomaly_performance_filter_trddays()
    table_regression = data_anomaly_performance.anomaly_performance_regression_rolling()
    table = table_merge_class.table_merge()
    table = table_remove_nan.remove_nan(df=table)
    table = table_filter_trddays.df_fix_trddays_range(df=table, para=para)
    performance = table_regression.ch3_OLS_rolling(table=table, para=para)
    return performance
#
def portfolio_regression_capm_rolling(df_portfolio, df_factor, para):
    table_merge_class = data_anomaly_performance.anomaly_performance_preprocessing(df_anomaly=df_portfolio,
                                                                                   df_factor=df_factor,
                                                                                   para=para)
    table_remove_nan = data_anomaly_performance.anomaly_performance_remove_NaN()
    table_filter_trddays = data_anomaly_performance.anomaly_performance_filter_trddays()
    table_regression = data_anomaly_performance.anomaly_performance_regression_rolling()
    table = table_merge_class.table_merge()
    table = table_remove_nan.remove_nan(df=table)
    table = table_filter_trddays.df_fix_trddays_range(df=table, para=para)
    performance = table_regression.capm_OLS_rolling(table=table, para=para)
    return performance
#
#================================================================================
#
class expert_wash_df():
    def __init__(self, para, df):
        self.para = para
        self.df = df
    def wash_df_by_filter(self):
        df = df_process_add_filter(para = self.para, df = self.df)
        return df
#
class expert_construct_factor_model():
    def __init__(self,df,para):
        self.factor = df
        self.para = para
    def factor_model(self):
        factor = factor_model_process(df= self.factor, para=self.para)
        return factor
#
class expert_construct_portfolio():
    def __init__(self, df, para, predictor):
        self.df = df
        self.para = para
        self.predictor = predictor
    def construct_portfolio(self):
        raw_return = predictor_to_portfolio(df = self.df, para = self.para,
                                            predictor = self.predictor)
        return raw_return
#
class expert_handle_panel():
    def __init__(self,df,factor,model_name,para):
        self.df = df
        self.factor = factor
        self.para = para
        self.model_name = model_name
    def handle_panel(self):
        if self.model_name == 'ch3':
            panel = panel_process_ch3(df=self.df,factor=self.factor,
                                      para=self.para)
        else:
            raise Exception("input wrong model name")
        return panel
#======================================================================================
class expert_handle_portfolio_regression(object):
    def __init__(self, df_portfolio, df_factor, para):
        self.df_portfolio = df_portfolio
        self.df_factor = df_factor
        self.para = para
    def handle_portfolio_regression(self):
        if self.para['reg_model'] == 'capm':
            performance = portfolio_regression_capm(df_portfolio = self.df_portfolio,
                                                   df_factor = self.df_factor,
                                                   para = self.para)
            #
        elif self.para['reg_model'] == 'ch3':
            performance = portfolio_regression_ch3(df_portfolio = self.df_portfolio,
                                                   df_factor = self.df_factor,
                                                   para = self.para)
        else:
            raise Exception( "input wrong model for regression to get alpha and t-stats " )
        return performance
    def handle_portfolio_regression_rolling(self):
        if self.para['reg_model'] == 'capm':
            performance = portfolio_regression_capm_rolling(df_portfolio = self.df_portfolio,
                                                           df_factor = self.df_factor,
                                                           para = self.para)
        elif self.para['reg_model'] == 'ch3':

            performance = portfolio_regression_ch3_rolling(df_portfolio = self.df_portfolio,
                                                           df_factor = self.df_factor,
                                                           para = self.para)
        else:
            raise Exception('input wrong model for regression to get rolling alpha and t-stats')
        return performance