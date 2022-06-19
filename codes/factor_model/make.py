# 用于 更新 factor_model
import pandas as pd
import time
import codes.utils.parameters_module as param
from codes.utils import data_expert_module as data_expert
from codes.utils import csmar_process
#
def ep(df):
    df = df.copy()
    df['ep'] = df['B003000000'] / df['clsprc']
    return  df
#
def add_ep(df):
    df = df.copy()
    df = df.groupby('stkcd').apply(ep).reset_index(drop=True)
    return df
#
def washing_data(para_path,df):
    print('begin to washing the file: ../../data/csmar/basic/csmar_basic.parquet')
    t0 = time.time()
    df = df.copy()
    df = add_ep(df=df)
    csmar_trade = csmar_process.csmar_trading()
    basic_columns = list(csmar_trade.columns_rename.values())
    df = df[basic_columns + ['ep'] ]  # 挑选出对计算 factor_model 有用的 columns
    #
    para = pd.read_csv(para_path)
    para_factor_model = param.factor_model().dataframe_to_dict(df_para=para)
    para_factor_model = param.factor_model().para_dict_retype(para_dict=para_factor_model)
    #
    df_class = data_expert.expert_handle_df(para=para_factor_model, df=df)
    df = df_class.handle_df()
    print('Done! of washing with the time cost', time.time() - t0)
    return df
#
def update_factor_model(para_path,df):
    print('begin to update the file: ../../data/result_file/factor_ret.csv')
    t0 = time.time()
    # df: 清洗完之后的 csmar_basic.parquet
    # 根据 '../../data/para_file/para_factor_model.csv' 中的参数，更新 factor_model
    para_factor_model = pd.read_csv(para_path)
    para_factor_model = param.factor_model().dataframe_to_dict(df_para=para_factor_model)
    para_factor_model = param.factor_model().para_dict_retype(para_dict=para_factor_model)
    factor_class = data_expert.expert_handle_factor(df=df,para=para_factor_model)
    factor_ret = factor_class.handle_factor()
    factor_ret.to_csv('../../output/factor_model/factor_model.csv')
    print('Done! of updating with the time cost:', time.time() - t0)
    return factor_ret
#
if __name__ == '__main__':
    # 用来更新 factor model
    df = pd.read_parquet('../../data/csmar/basic/csmar_basic.parquet')
    df = washing_data(para_path='../../data/para_file/para_factor_model.csv',
                      df=df)
    update_factor_model(para_path='../../data/para_file/para_factor_model.csv',
                        df=df)