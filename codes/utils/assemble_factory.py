import time
import pandas as pd
from codes.utils.csmar_update import assemble_predictors, get_assemble_parameters
from codes.utils import csmar_process
from codes.utils import data_expert_module as data_expert
from codes.utils import parameters_module as param
#
def update_predictor_parameters(predictors):
    # 在 para_construct_portfolio.csv 中 添加 成功生成的 predictors
    para_anomaly = pd.read_csv('../data/para_file/para_construct_portfolio.csv')
    para_anomaly = param.anomaly().dataframe_to_dict(df_para=para_anomaly)
    para_anomaly['anomaly_list'] = predictors
    df_para = param.anomaly().dict_to_dataframe(para_anomaly)
    df_para.to_csv('../data/para_file/para_construct_portfolio.csv')
    return
#
def calculate_predictors(predictor_file_path,para_flag_path):
    """Description:

    Running this module is the step 2 for the whole algorithm.

    This module is used to calculate predictors according to file './data/basic/basic_data.parquet',
    and output the predictors in file './output/predictors/predictors.csv' .

    Args:
        predictor_file_path (str): the file path './codes/predictors/'
        para_flag_path (str): the file path + file name of the input file i.e. './data/para_file/para_flag.csv'
    Returns:
        None
    """
    print('begin to calculate predictors and output file "basic_data.parquet" along folder ../data/basic/ ')
    df_flag = pd.read_csv(para_flag_path)
    flag_class = param.flag()
    dict_flag = flag_class.dataframe_to_dict(df_para=df_flag)
    if dict_flag['Is_calculate_predictors'] == 'yes':
        print('begin to calculate predictors and output the file along: ../output/predictors/')
        t0 = time.time()
        # 根据 ../codes/predictors/ 路径下 xxx.py 文件的个数和给出的 predictor 中的参数信息
        # 来 update ../data/csmar/basic/ 路径下的 csmar_basic.parquet 文件和 csmar_basic_columns.csv 文件
        assemble = assemble_predictors(path=predictor_file_path)
        module_dict = assemble.predictors_info()
        para_predictor = get_assemble_parameters(module_dict=module_dict)
        #
        csmar_basic = pd.read_parquet('../data/basic/basic_data.parquet')
        add_predictor = csmar_process.csmar_basic_add_predictor(df=csmar_basic, para=para_predictor)
        df_all, predictors_list = add_predictor.add_predictor()
        #
        csmar_trade = csmar_process.csmar_trading()
        basic_columns = list(csmar_trade.columns_rename.values())
        df = df_all[basic_columns + predictors_list]  # select the columns include trade info and predictor info
        df.to_csv('../output/predictors/predictors.csv')
        # 同时将'../data/para_file/para_anomaly.csv' 中的参数进行更新。
        update_predictor_parameters(predictors=predictors_list)
        print('Done! of calculating predictors with the time cost:', time.time() - t0)
        return
    elif dict_flag['Is_calculate_predictors'] == 'no':
        print('you do NOT need to calculate predictors')
        print('predictors.csv has been build along folder ../output/predictors/')
        return
    else:
        raise Exception(' you input wrong parameters of "Is_calculate_predictors" in '
                        'file ../data/para_file/para_flag.csv')

#
#
def load_trading_scheme(para_path,df_path):
    """Description:

    Running this module is the step 3 for the whole algorithm.

    This module is used to wash file './output/predictors/predictors.csv'
    according to parameter file './data/para_file/para_trading_scheme.csv'.

    Args:
        para_path (str): the file path './data/para_file/para_trading_scheme.csv'
        df_path (str): the file path + file name of the input file i.e. './output/predictors/predictors.csv'
    Returns:
        df (pandas.DataFrame)
    """
    print('load trading scheme to wash file : ../output/predictors/predictors.csv')
    t0 = time.time()
    # 根据 '../../data/para_file/para_csmar_basic.csv' 中的参数, 对 csmar_bsic 进行清洗
    para_washing = pd.read_csv(para_path)
    para_washing = param.csmar_basic().dataframe_to_dict(df_para=para_washing)
    para_washing = param.csmar_basic().para_dict_retype(para_dict=para_washing)
    #
    df = pd.read_csv(df_path)
    #
    df_class = data_expert.expert_handle_df(para=para_washing, df=df)
    df = df_class.handle_df()
    print('Done! of washing with file the time cost', time.time() - t0)
    return df
#
def update_portfolio_ret(para_path,df):
    """Description:

    Running this module is the step 4 for the whole algorithm.

    This module is used to calculate the portfolio monthly long-short return, and output the
    results in the file './output/portfolio_ret/para_trading_scheme.csv'.

    Args:
        para_path (str): the file path './data/para_file/para_construct_portfolio.csv'
        df (pandas.DataFrame): df is the return of load_trading_scheme(para_path,df_path)
    Returns:
        portfolio_ret (pandas.DataFrame)
    """
    print('begin to update the file: ../output/portfolio_ret/portfolio_ret.csv')
    t0 = time.time()
    para = pd.read_csv(para_path)
    para = param.anomaly().dataframe_to_dict(df_para=para)
    para = param.anomaly().para_dict_retype(para_dict=para)
    # 对 df 的 columns 进行简化
    csmar_trade = csmar_process.csmar_trading()
    basic_columns = list(csmar_trade.columns_rename.values())

    df1 = df[basic_columns+para['anomaly_list']+['ret']] # 挑选出对计算 portfolio_ret 有用的 columns
    anomaly_class = data_expert.expert_handle_anomalies(df=df1, para=para)
    portfolio_ret = anomaly_class.handle_anomalies()
    #
    portfolio_ret.to_csv('../output/portfolio_ret/portfolio_ret.csv')
    print('Done! of updating with the time cost:', time.time() - t0)
    return portfolio_ret
#
#
#
def update_portfolio_performance(path_anomaly,path_factor,path_para):
    """Description:

    Running this module is the step 5 for the whole algorithm.

    This module is used to calculate the regression results of portfolio long-short return.
    In the process of regression, y is the portfolio long-short return calculated according to
    the predictors, which is saved in the file './output/portfolio_ret/portfolio_ret.csv'.
    Correspondingly, x in regression is the factor model, which is saved in the file
    './output/factor_model/factor_model.csv'.

    Args:
        path_anomaly (str): the file path './output/portfolio_ret/portfolio_ret.csv'
        path_factor (str): the file path './output/factor_model/factor_model.csv'
        path_para (str): the file path './data/para_file/para_portfolio_performance.csv'
    Returns:
        anomaly_performance (pandas.DataFrame): the regression results of portfolio long-short return, which
        is saved in the file './output/portfolio_performance/portfolio_performance.csv'.
    """
    print('begin to update the file: ../output/portfolio_performance/portfolio_performance.csv')
    t0 = time.time()
    anomaly_ret = pd.read_csv(path_anomaly)
    factor_ret = pd.read_csv(path_factor)
    para_anomaly = pd.read_csv(path_para)
    para_anomaly = param.anomaly_performance().dataframe_to_dict(df_para=para_anomaly)
    para_anomaly = param.anomaly_performance().para_dict_retype(para_dict=para_anomaly)
    anomaly_performance_class = data_expert.expert_handle_anomaly_performance(df_anomaly=anomaly_ret,
                                                                              df_factor=factor_ret,
                                                                              para=para_anomaly)
    anomaly_performance_class.anomaly_precanonicalize()
    anomaly_performance_class.factor_precanonicalize()
    anomaly_performance = anomaly_performance_class.handle_anomaly_performance() # 得出异象表现。
    anomaly_performance.to_csv('../output/portfolio_performance/portfolio_performance.csv')
    print('Done! of updating with the time cost:', time.time() - t0)
    return anomaly_performance
#
#
def update_portfolio_rolling_performance(path_anomaly,path_factor,path_para):
    """Description:

    Running this module is the step 6 for the whole algorithm.

    This module is used to calculate the rolling performance of the regression results of
    portfolio long-short return. In the rolling process of regression, y is the portfolio long-short
    return calculated according to the predictors, which is saved in the file
    './output/portfolio_ret/portfolio_ret.csv'. Correspondingly, x in regression is the factor model,
    which is saved in the file './output/factor_model/factor_model.csv'.

    This module output the results of the rolling performance of the regression in the
    file './output/portfolio_performance/rolling_performance_predictor.csv'

    Args:
        path_anomaly (str): the file path './output/portfolio_ret/portfolio_ret.csv'
        path_factor (str): the file path './output/factor_model/factor_model.csv'
        path_para (str): the file path './data/para_file/para_portfolio_performance.csv'
    Returns:
        None
    """
    print('begin the updating the rolling performance of predictors')
    t0 = time.time()
    anomaly_ret = pd.read_csv(path_anomaly)
    factor_ret = pd.read_csv(path_factor)
    para_anomaly = pd.read_csv(path_para)
    para_anomaly = param.anomaly_performance().dataframe_to_dict(df_para=para_anomaly)
    para_anomaly = param.anomaly_performance().para_dict_retype(para_dict=para_anomaly)
    anomaly_performance_class = data_expert.expert_handle_anomaly_performance(df_anomaly=anomaly_ret,
                                                                              df_factor=factor_ret,
                                                                              para=para_anomaly)
    #
    anomaly_performance_class.anomaly_precanonicalize()
    anomaly_performance_class.factor_precanonicalize()
    anomaly_performance_rolling = anomaly_performance_class.handle_anomaly_performance_rolling()
    #
    for it in list(anomaly_performance_rolling.keys()):
        file_name = 'rolling_performance_' + it + '.csv'
        df = anomaly_performance_rolling[it]
        df.to_csv('../output/portfolio_performance/' + file_name )
    print('Done! of updating with the time cost:', time.time() - t0)
    return
#========================================================================
#
def build_data(para_flag_path):
    """Description:

    Running this module is the step 1 for the whole algorithm.

    This module is used to create a large panel data file i.e. 'basic_data.parquet' and along folder './data/basic/'.

    Args:
        para_flag_path (str): the file path + file name of the input file i.e. 'para_flag.csv' along folder './data/para_file/'
    Returns:
        None
    """
    print('begin to build data and output file "basic_data.parquet" along folder ../data/basic/ ')
    df_flag = pd.read_csv(para_flag_path)
    flag_class = param.flag()
    dict_flag = flag_class.dataframe_to_dict(df_para=df_flag)
    if dict_flag['Is_build_data'] == 'yes':
        print('begin the merging of trade data and finance data to form a large panel data')
        t0 = time.time()
        # 将 raw csmar_trade 和 raw csmar_finance 并起来，形成一个大的panel data.
        csmar_trade = csmar_process.csmar_trading()
        df_trade = csmar_trade.output_trading_data()
        # 得到 csmar_finance data
        csmar_finance = csmar_process.csmar_finance_raw()
        df_finance = csmar_finance.output_finance_data()
        # 对 csmar_finance data 进行处理
        t1 = time.time()
        fin_post = csmar_process.csmar_finance_postprocess_raw(df=df_finance)
        df_fin = fin_post.output_finance_data()
        print('Done! of postprocessing csmar_finance with time cost:', time.time() - t1)
        # 通过 merge 的方法来 merge df_csmar_basic 和 df_fin 来更新 csmar_basic
        data_merge = csmar_process.merge_csmar_basic_and_finance_data(df_basic=df_trade, df_fin=df_fin)
        df_all = data_merge.merge()
        df_all.to_parquet('../data/basic/basic_data.parquet')
        print('Done! of merging with time cost:', time.time() - t0)
        return
    elif dict_flag['Is_build_data'] == 'no':
        print('you do NOT need to build date through merging trade data and finance data')
        return
    else:
        raise Exception(' you input wrong parameters of "Is_build_data" in '
                        'file ../data/para_file/para_flag.csv')

