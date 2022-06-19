'''::parameter::'''
import pandas as pd
#
class predictor(object):
    # 关于 predictor 参数的类
    def default_common_parameters(self, para):
        para['neutral_var'] = 'size'  # 市值中性化 # 采用哪种 neutralize 的方式
        para['way_weight'] = 'size'  # 市值加权 # 控制计算ret 时加权的方式 {'size', 'ew'}
        para['Is_neutral'] = 'yes'  # 是否进行中性化 {'yes', 'no'}
        para['model'] = 'ch3'  # 设置回归模型 说 ch3 模型 还是 capm 模型
        para['start_date'] = '2000-07'  # start date for regression
        para['end_date'] = '2016-12'  # end date for regression
        return para
    #
    def make_consistent_parameters(self,para):
        return para
    #
    def dict_to_dataframe(self,para):
        df_para = pd.DataFrame(pd.Series(para))
        df_para.rename(columns={0: 'value'}, inplace=True)
        df_para.index.set_names('key', inplace=True)
        return df_para
    #
    def dataframe_to_dict(self, df_para):
        df_para.set_index('key', inplace=True)
        para_dict = {x: df_para.T.to_dict()[x]['value'] for x in df_para.T.to_dict().keys()}
        para_dict['rolling_period'] = eval(para_dict['rolling_period'])
        return para_dict
    #

#
class csmar_basic(object):
    def default_para(self, para):
        #para['data_format'] = 'parquet'
        #para['csmar_basic_path'] = '../data/csmar/basic/csmar_basic.parquet'
        return para
    def dict_to_dataframe(self,para):
        df_para = pd.DataFrame(pd.Series(para))
        df_para.rename(columns={0: 'value'}, inplace=True)
        df_para.index.set_names('key', inplace=True)
        return df_para
    def dataframe_to_dict(self, df_para):
        df_para.set_index('key', inplace=True)
        para_dict = {x: df_para.T.to_dict()[x]['value'] for x in df_para.T.to_dict().keys()}
        return para_dict
    def para_dict_retype(self,para_dict):
        para_dict['yearly_mnt_period'] = eval(para_dict['yearly_mnt_period'])
        para_dict['mnt_comm_trdday'] = eval(para_dict['mnt_comm_trdday'])
        para_dict['exclude_bottom_size'] = eval(para_dict['exclude_bottom_size'])
        para_dict['exclude_trdday_lsyr'] = eval(para_dict['exclude_trdday_lsyr'])
        para_dict['exclude_trdday_lsmnt'] = eval(para_dict['exclude_trdday_lsmnt'])
        return para_dict
#
class factor_model(object):
    def default_para(self,para):
        return para
    def dict_to_dataframe(self,para):
        df_para = pd.DataFrame(pd.Series(para))
        df_para.rename(columns={0: 'value'}, inplace=True)
        df_para.index.set_names('key', inplace=True)
        return df_para
    def dataframe_to_dict(self, df_para):
        df_para.set_index('key', inplace=True)
        para_dict = {x: df_para.T.to_dict()[x]['value'] for x in df_para.T.to_dict().keys()}
        return para_dict
    def para_dict_retype(self, para_dict):
        para_dict['std_columns'] = eval(para_dict['std_columns'])
        para_dict['yearly_mnt_period'] = eval(para_dict['yearly_mnt_period'])  # 股票一年交易的月份数量，用来计算一年中真实的累积交易天数
        para_dict['mnt_comm_trdday'] = eval(para_dict['mnt_comm_trdday'])   # 如果股票月度交易日数量缺失的话，用 21天来填充
        para_dict['exclude_bottom_size'] = eval(para_dict['exclude_bottom_size'])   # excluding the percentage of smallest stocks
        para_dict['exclude_trdday_lsyr'] = eval(para_dict['exclude_trdday_lsyr'])  # 除掉股票年度交易日累积小于126天的交易记录
        para_dict['exclude_trdday_lsmnt'] = eval(para_dict['exclude_trdday_lsmnt'])  # 除掉股票月度交易日小于15天的记录
        return para_dict
#
class anomaly(object):
    def default_para(self, para):
        return para
    def dict_to_dataframe(self, para):
        df_para = pd.DataFrame(pd.Series(para))
        df_para.rename(columns={0:'value'}, inplace=True)
        df_para.index.set_names('key', inplace=True)
        return df_para
    def dataframe_to_dict(self, df_para):
        df_para.set_index('key', inplace=True)
        para_dict = {x: df_para.T.to_dict()[x]['value'] for x in df_para.T.to_dict().keys()}
        return para_dict
    def para_dict_retype(self, para_dict):
        para_dict['anomaly_list'] = eval(para_dict['anomaly_list'])
        return para_dict
#
class anomaly_performance(object):
    def default_para(self, para):
        return para
    def dict_to_dataframe(self, para):
        df_para = pd.DataFrame(pd.Series(para))
        df_para.rename(columns={0:'value'}, inplace=True)
        df_para.index.set_names('key', inplace=True)
        return df_para
    def dataframe_to_dict(self, df_para):
        df_para.set_index('key', inplace=True)
        para_dict = {x: df_para.T.to_dict()[x]['value'] for x in df_para.T.to_dict().keys()}
        return para_dict
    def para_dict_retype(self, para_dict):
        para_dict['rolling_period'] = eval(para_dict['rolling_period'])  # 滚动计算的窗口宽度
        para_dict['anomaly_list'] = eval(para_dict['anomaly_list'])
        return para_dict
#
class flag(object):
    def default_para(self, para):
        return para
    def dict_to_dataframe(self, para):
        df_para = pd.DataFrame(pd.Series(para))
        df_para.rename(columns={0: 'value'}, inplace=True)
        df_para.index.set_names('key', inplace=True)
        return df_para
    def dataframe_to_dict(self, df_para):
        df_para.set_index('key', inplace=True)
        para_dict = {x: df_para.T.to_dict()[x]['value'] for x in df_para.T.to_dict().keys()}
        return para_dict
    def para_dict_retype(self, para_dict):
        return para_dict
#
def transform_dict_to_dataframe(dict):
    df = pd.DataFrame(pd.Series(dict))
    df.rename(columns={0: 'value'}, inplace=True)
    df.index.set_names('key', inplace=True)
    return df
#

