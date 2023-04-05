'''::parameter::'''
import pandas as pd
import xml.etree.ElementTree as ET
import os
#
class parameters(object):
    def __init__(self):
        self.para_input = ET.XML(open('./parameter.xml', 'r').read())
    def run_id(self):
        for it in self.para_input:
            para = {}
            if it.tag == 'run_id':
                para['run_id'] = eval(it.text)
                return para
    def data_download(self):
        for it in self.para_input:
            if it.tag == 'data_download':
                para_data_download = {}
                for it1 in it:
                    para_data_download[it1.tag] = eval(it1.text)
                return para_data_download
    def calculate_predictors(self):
        for it in self.para_input:
            if it.tag == 'calculate_predictors':
                para_calculate_predictors = {}
                for it1 in it:
                    para_calculate_predictors[it1.tag] = eval(it1.text)
                return para_calculate_predictors
    def data_build(self):
        for it in self.para_input:
            if it.tag == 'data_build':
                para_data_build = {}
                for it1 in it:
                    para_data_build[it1.tag] = eval(it1.text)
                return para_data_build
    def data_clean(self):
        for it in self.para_input:
            if it.tag == 'data_clean':
                para_data_clean = {}
                for it1 in it:
                    para_data_clean[it1.tag] = eval(it1.text)
                return para_data_clean
    def portfolio_construct(self):
        for it in self.para_input:
            if it.tag == 'portfolio_construct':
                para_portfolio_construct = {}
                for it1 in it:
                    para_portfolio_construct[it1.tag] = eval(it1.text)
                return para_portfolio_construct
    def factor_model(self):
        for it in self.para_input:
            if it.tag == 'factor_model':
                para_factor_model = {}
                for it1 in it:
                    para_factor_model[it1.tag] = eval(it1.text)
                return para_factor_model
    def portfolio_regression(self):
        for it in self.para_input:
            if it.tag == 'portfolio_regression':
                para_p_r = {}
                for it1 in it:
                    para_p_r[it1.tag] = eval(it1.text)
                return para_p_r
    def output(self):
        para = {}
        para['run_id'] = self.run_id()['run_id']
        para['data_download'] = self.data_download()
        para['data_build'] = self.data_build()
        para['data_clean'] = self.data_clean()
        para['portfolio_construct'] = self.portfolio_construct()
        para['factor_model'] = self.factor_model()
        para['portfolio_regression'] = self.portfolio_regression()
        return para
#
def mkdir(path):
    """
       Create a folder at your path
       :param path: the path of the folder you wish to create
       :return: the path of folder being created
       Notes: if the folder already exist, it will not create a new one.
    """
    path = path.strip()
    path = path.rstrip("\\")
    path_flag = os.path.exists(path)
    if not path_flag:
        os.makedirs(path)
    return path_flag
#
#
#
#
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
        print('para_dict:',para_dict)
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

class anomaly_regression(object):
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

