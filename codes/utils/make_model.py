# 用于 更新 factor_model
#import sys
#from os.path import dirname, abspath
#path = dirname(dirname(dirname(abspath(__file__)))) # back to folder 'OSAP-v4' need back three steps
#sys.path.append(path)
import pandas as pd
import time
import codes.utils.parameters_module as param
from codes.utils import data_expert_module as data_expert
#
def factor_to_VMG(df):  # =
    df = df.copy()
    df['ep'] = (df['B003000000'] / df['Mclsprc']).shift() # lag one month
    return  df
#
def factor_to_SMB(df):
    df = df.copy()
    df['size_factor'] = df['size'].shift() # lag one month
    return df
#
def add_factors(df):
    df = df.copy()
    df = df.groupby('stkcd').apply(factor_to_VMG).reset_index(drop=True)
    df = df.groupby('stkcd').apply(factor_to_SMB).reset_index(drop=True)
    return df
#
def washing_data(para,df):
    print('according to conditions for constructing factor model to wash data')
    t0 = time.time()
    df1 = df[['stkcd', 'month', 'mret', 'Msmvttl', 'Ndaytrd', 'B003000000', 'Mclsprc']]  # 挑选出对计算 factor_model 有用的 columns
    df1.rename(columns={'Msmvttl': 'size', 'Ndaytrd' : 'trdday'}, inplace = True)
    df1 = add_factors(df=df1)
    #
    #para = pd.read_csv(para_path)
    #para_factor_model = param.factor_model().dataframe_to_dict(df_para=para)
    #para_factor_model = param.factor_model().para_dict_retype(para_dict=para_factor_model)
    #
    df_class = data_expert.expert_wash_df(para=para, df=df1)
    df_new = df_class.wash_df_by_filter()
    print('Done! of washing with the time cost', time.time() - t0)
    return df_new
#
def update_factor_model(para,df):
    print('after washing data, begin to making factor model ')
    t0 = time.time()
    # df: 清洗完之后的 csmar_basic.parquet
    # 根据 '../../data/para_file/para_factor_model.csv' 中的参数，更新 factor_model
    #para_factor_model = pd.read_csv(para_path)
    #para_factor_model = param.factor_model().dataframe_to_dict(df_para=para_factor_model)
    #para_factor_model = param.factor_model().para_dict_retype(para_dict=para_factor_model)
    factor_class = data_expert.expert_construct_factor_model(df=df,para=para)
    factor_ret = factor_class.factor_model()
    #factor_ret.to_csv('../../output/factor_model/factor_model.csv')
    #print('Done! of updating with the time cost:', time.time() - t0)
    return factor_ret
#
if __name__ == '__main__':
    # 用来更新 factor model
    df = pd.read_parquet('../../data/basic/basic_monthly_data.parquet')
    df = washing_data(para_path='../../data/para_file/para_factor_model.csv',
                      df=df)
    update_factor_model(para_path='../../data/para_file/para_factor_model.csv',
                        df=df)