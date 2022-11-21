import time
import pandas as pd
from codes.utils.csmar_update import assemble_predictors, assemble_output_predictors
from codes.utils.csmar_update import assemble_standard_predictors, assemble_csv_file_info
from codes.utils import csmar_process
from codes.utils import csmar_consolidation
from codes.utils import data_expert_module as data_expert
from codes.utils import parameters_module as param
from codes.utils.basic_data import DataForPredictors
import codes.utils.make_model as make_model
import wrds
#
def read_parameters():
    para_class = param.parameters()
    return para_class
#
def download_data(parameter):
    para = parameter.data_download()
    #
    if para['Is_download_data'] == 'yes':
        print('begin to download monthly trading data from wrds')
        conn = wrds.Connection()
        t0 = time.time()
        csmar_t_mnth = conn.raw_sql(""" select a.* from csmar.csmar_t_mnth as a where a.Opndt >= '01/01/1959' """)
        print('download <csmar_t_mnth> take time cost:', time.time() - t0)
        csmar_t_mnth.to_parquet('../data/download_data/csmar_t_mnth.parquet')
        #
        print('begin to download weekly trading data from wrds')
        t0 = time.time()
        csmar_t_week = conn.raw_sql(""" select a.* from csmar.csmar_t_week as a where a.Opndt >= '01/01/1959' """)
        print('download <csmar_t_week> take time cost:', time.time() - t0)
        csmar_t_week.to_parquet('../data/download_data/csmar_t_week.parquet')
        #
        print('begin to download daily trading data from wrds')
        t0 = time.time()
        csmar_t_dalyr = conn.raw_sql(""" select a.* from csmar.csmar_t_dalyr as a where a.Trddt >= '01/01/1959' """)
        print('download <csmar_t_dalyr> take time cost:', time.time() - t0)
        csmar_t_dalyr.to_parquet('../data/download_data/csmar_t_dalyr.parquet')
        #
        print('begin to download industry data from wrds')
        t0 = time.time()
        csmar_t_co = conn.raw_sql(""" select a.* from csmar.csmar_t_co as a where a.Listdt >= '01/01/1959' """)
        print('download <csmar_t_co> take time cost:', time.time() - t0)
        csmar_t_co.to_parquet('../data/download_data/csmar_t_co.parquet')
        #
        print('begin to download firm financial statement data from wrds')
        t0 = time.time()
        csmar_master = conn.raw_sql(""" select a.* from csmar.csmar_master as a where a.Accper >= '01/01/1959' """)
        print('download <csmar_master> take time cost:', time.time() - t0)
        csmar_master.to_parquet('../data/download_data/csmar_master.parquet')
    elif para['Is_download_data'] == 'no':
        print('Not need to download data from wrds')
    else:
        raise Exception('you input wrong parameters of "Is_download_data" in '
                        'file <./parameter.xml>')
    return
#
def build_data(parameter):
    para = parameter.data_build()
    #
    if para['Is_build_monthly_data'] == 'yes':
        print('begin to build data and output files along folder ../data/build_data/ ')
        df_mnt_fin = csmar_consolidation.monthly_add_finance_data() # merge the finance accounting data
        df_mnt_fin_ind = csmar_consolidation.monthly_add_industry_data(df=df_mnt_fin) # merge the industry date
        df_mnt_fin_ind.to_parquet('../data/build_data/basic_monthly_data.parquet') # form the basic monthly data
    elif para['Is_build_monthly_data'] == 'no':
        print('NOT need to build monthly data through merging trade data and finance data')
    else:
        raise Exception(' you input wrong parameters of "Is_build_monthly_data" in '
                        'file  <./parameter.xml>')
    if para['Is_build_weekly_data'] == 'yes':
        print('begin to build data and output file "basic_weekly_data.parquet" along folder ../data/build_data/ ')
        df_week = csmar_consolidation.weekly_data()
        df_week.to_parquet('../data/build_data/basic_weekly_data.parquet')
    elif para['Is_build_weekly_data'] == 'no':
        print('NOT need to build weekly data')
    else:
        raise Exception(' you input wrong parameters of "Is_build_weekly_data" in '
                        'file  <./parameter.xml>')
    if para['Is_build_daily_data'] == 'yes':
        print('begin to build data and output file "basic_daily_data.parquet" along folder ../data/build_data/ ')
        df_daily = csmar_consolidation.daily_data()
        df_daily.to_parquet('../data/build_data/basic_daily_data.parquet')
    elif para['Is_build_daily_data'] == 'no':
        print('NOT need to build daily data')
    else:
        raise Exception(' you input wrong parameters of "Is_build_daily_data" in '
                        'file <./parameter.xml>')
    return
#
def calculate_predictors(parameter):
    print('begin to calculate predictors and output the file along: ../output/predictors/')
    # 根据 ../codes/predictors/ 路径下 xxx.py 文件的个数和给出的 predictor 中的参数信息
    # 将 predictor 的结果输出到 '../output/predictors/' 路径下
    para_class = parameter
    para = para_class.run_id()
    path = '../output/' + para['run_id'] + '/predictors/'
    param.mkdir(path=path)
    #
    para_calculate = parameter.calculate_predictors()
    predictor_file_path = para_calculate['predictor_file_path']
    #
    assemble = assemble_predictors(path=predictor_file_path)
    module_dict = assemble.predictors_info()
    print('total predictors:', list(module_dict.keys()))
    assemble_output = assemble_output_predictors(para = para) #
    exist_predictors = assemble_output.path_files_name()  #
    print('successful realized predictors: \n', exist_predictors)
    total_predictors = list(module_dict.keys())
    predictors_list = list(set(total_predictors) - set(exist_predictors))
    print('predictors need to calculate: \n', predictors_list)
    if len(predictors_list) > 0:
        df_input = {}
        df_input['monthly'] = DataForPredictors().monthly()
        df_input['weekly'] = DataForPredictors().weekly()
        df_input['daily'] = DataForPredictors().daily()
        for it in range(len(predictors_list)):
            print('begin to calculate predictor:', predictors_list[it])
            t0 = time.time()
            print(module_dict[predictors_list[it]])
            try:
                dp = module_dict[predictors_list[it]].calculation(df_input)
                print('Done! with time cost:', time.time() - t0)
                p_name = predictors_list[it] + '.csv'
                path = '../output/' + para['run_id'] + '/predictors/'
                dp.to_csv(path + p_name)
            except KeyError as e:
                print('key error', e)
                print('get predictor ' + predictors_list[it] + ' failed may due to wrong definition of predictors')
    else:
        print('Done! Not need to calculate predictors')
    return
def predictors_wash(parameter):
    print('washing predictors files:')
    para = parameter.run_id()
    path = '../output/' + para['run_id'] + '/predictors_wash/'
    param.mkdir(path=path)
    predictors_file_path = '../output/' + para['run_id'] + '/predictors/'
    file_info_1 = assemble_csv_file_info(path=predictors_file_path)
    predictors_total = file_info_1.path_files_name()
    predictors_list = list(predictors_total)
    para_wash = parameter.data_wash()
    if para_wash['Is_data_standard'] == 'yes':
        t0 = time.time()
        df_cell = {}
        for it in range(len(predictors_list)):
            print('begin to standardizing predictor:', predictors_list[it])
            file_name = predictors_file_path + predictors_list[it] + '.csv'
            df = pd.read_csv(file_name)
            predictor = predictors_list[it]
            predictors_postprocess = csmar_process.csmar_single_predictor_postprocess(df=df, predictor=predictor)
            df_s = predictors_postprocess.output_predictor_()
            df_cell[predictors_list[it]] = df_s
        print('Done! of standardizing predictors with time cost:', time.time() - t0)
    elif para_wash['Is_data_standard'] == 'no':
        df_cell = {}
        for it in range(len(predictors_list)):
            file_name = predictors_file_path + predictors_list[it] + '.csv'
            df = pd.read_csv(file_name)
            df_cell[predictors_list[it]] = df
    else:
        raise Exception(' you input wrong parameters of "Is_data_standard" in '
                        'file <./parameter.xml>')
    #
    if para_wash['Is_add_filters'] == 'yes':
        t0 = time.time()
        df0 = pd.read_parquet('../data/build_data/basic_monthly_data.parquet')
        df0 = df0[['stkcd', 'month', 'mret', 'Msmvttl', 'Ndaytrd']]  #
        df0.rename(columns={'Msmvttl': 'size', 'Ndaytrd': 'trdday'}, inplace=True)
        df_class = data_expert.expert_wash_df(para=para_wash, df=df0)
        df = df_class.wash_df_by_filter()
        df.sort_values(by=['stkcd', 'month'], inplace=True)
        df = df.copy()
        df['stkcd'] = df['stkcd'].apply(lambda x: str(x))
        for it in range(len(list(df_cell.keys()))):
            predictor_name =  list(df_cell.keys())[it]
            print('wash predictor using filters:', predictor_name)
            file_name = predictors_file_path + predictor_name + '.csv'
            df1 = pd.read_csv(file_name)
            df1.sort_values(by=['stkcd', 'month'], inplace=True)
            df1['stkcd'] = df1['stkcd'].apply(lambda x: str(x))
            #df1['stkcd'] = df1['stkcd'].apply(lambda x: str(x).zfill(6))
            df_f = pd.merge(df, df1, on=['stkcd', 'month'], how='left')
            save_name = path + predictor_name + '.csv'
            df_f.to_csv(save_name)
        print('Done! of washing predictors files with the time cost', time.time() - t0)
    elif para_wash['Is_add_filters'] == 'no':
        t0 = time.time()
        df0 = pd.read_parquet('../data/build_data/basic_monthly_data.parquet')
        df0 = df0[['stkcd', 'month', 'mret', 'Msmvttl', 'Ndaytrd']]  #
        df0.rename(columns={'Msmvttl': 'size', 'Ndaytrd': 'trdday'}, inplace=True)
        df0.sort_values(by=['stkcd', 'month'], inplace=True)
        df0 = df0.copy()
        df0['stkcd'] = df0['stkcd'].apply(lambda x: str(x))
        #
        for it in range(len(list(df_cell.keys()))):
            predictor_name =  list(df_cell.keys())[it]
            print('wash predictor without filters:', predictor_name)
            df1 = df_cell[predictor_name]
            df1 = df1[['stkcd', 'month', predictor_name]]
            df1.sort_values(by=['stkcd', 'month'], inplace=True)
            df1 = df1.copy()
            df1['stkcd'] = df1['stkcd'].apply(lambda x: str(x))
            # df1['stkcd'] = df1['stkcd'].apply(lambda x: str(x).zfill(6))
            df_merge = pd.merge(df0, df1, on=['stkcd', 'month'], how='left')
            save_name = path + predictor_name + '.csv'
            df_merge.to_csv(save_name)
        print('Done! of washing predictors files with the time cost', time.time() - t0)
    else:
        raise Exception(' you input wrong parameters of "Is_add_filters" in '
                        'file <./parameter.xml>')
    return
#
def predictors_to_portfolios(parameter):
    print('begin to construct portfolios')
    para = parameter.run_id()
    para_portfolio = parameter.portfolio_construct()
    path = '../output/' + para['run_id'] + '/portfolio_ret/'
    param.mkdir(path=path)
    predictors_file_path = '../output/' + para['run_id'] + '/predictors_wash/'
    #
    file_info_1 = assemble_csv_file_info(path=predictors_file_path)
    predictor_total = file_info_1.path_files_name()
    file_info_2 = assemble_csv_file_info(path=path)
    portfolio_exist = file_info_2.path_files_name()
    #
    predictor_list = list( set(predictor_total) - set(portfolio_exist) )
    t0 = time.time()
    if len(predictor_list) > 0:
        for it in range(len(predictor_list)):
            print('predictor_to_portfolio:', predictor_list[it])
            file_name = predictors_file_path + predictor_list[it] + '.csv'
            df1 = pd.read_csv(file_name)
            df1['stkcd'] = df1['stkcd'].apply(lambda x: str(x).zfill(6))
            df1['ret'] = df1['mret']
            portfolio_class = data_expert.expert_construct_portfolio(df=df1, para=para_portfolio,
                                                                     predictor=predictor_list[it])
            raw_return = portfolio_class.construct_portfolio()
            save_name = path + predictor_list[it] + '.csv'
            raw_return.to_csv(save_name)
        print('Done! of getting portfolio raw return with the time cost:', time.time() - t0)
    else:
        print('Done! All portfolios are already exist. Not need to calculate portfolio raw return ')
    return
#
def factors_model(parameter):
    print('begin to construct factors models')
    para = parameter.run_id()
    para_factor_model = parameter.factor_model()
    path = '../output/' + para['run_id'] + '/factor_model/'
    param.mkdir(path=path)
    if para_factor_model['Is_construct_model'] == 'yes':
        t0 = time.time()
        df = pd.read_parquet('../data/build_data/basic_monthly_data.parquet')
        para_factor_model['rf_path'] = '../data/risk_free_return/rf.xlsx'
        para_factor_model['std_columns'] = ['month', 'mkt', 'smb', 'vmg']
        para_factor_model['filter_exclude_bottom_size'] = 0.3  # excluding the percentage of smallest stocks
        para_factor_model['filter_exclude_trdday_lsyr'] = 126  # 除掉股票年度交易日累积小于126天的交易记录
        para_factor_model['filter_exclude_trdday_lsmnt'] = 15  # 除掉股票月度交易日小于15天的记录
        para_factor_model['filter_exclude_begin_trdday'] = '1990-12'  # 除掉股票在 '1990-12' 月之前有交易的股票记录
        df = make_model.washing_data(para=para_factor_model, df=df)
        factor_ret = make_model.update_factor_model(para=para_factor_model, df=df)
        filename = path + 'factor_model.csv'
        factor_ret.to_csv(filename)
        print('Done! of making factors model with time cost:', time.time() - t0)
    elif para_factor_model['Is_construct_model'] == 'no':
        print('Done! Not need to construct factor model')
    else:
        raise Exception(' you input wrong parameters of "Is_construct_model" in '
                        'file <./parameter.xml>')
    return
#
def portfolios_risk_adjust(parameter):
    para = parameter.run_id()
    para_portfolio_regression = parameter.portfolio_regression()
    if para_portfolio_regression['Is_portfolio_regression'] == 'yes':
        print('Calculate the regression performance of portfolios raw return using factor model')
        path = '../output/' + para['run_id'] + '/portfolio_regression/'
        param.mkdir(path=path)
        portfolios_file_path = '../output/' + para['run_id'] + '/portfolio_ret/'
        factor_model_file = '../output/' + para['run_id'] + '/factor_model/factor_model.csv'
        df_factor_model = pd.read_csv(factor_model_file)
        columns = list(df_factor_model.columns)
        if 'Unnamed: 0' in columns:
            df_factor_model.drop('Unnamed: 0', axis=1, inplace=True)
        else:
            df_factor_model = df_factor_model
        #
        files1 = assemble_csv_file_info(portfolios_file_path)
        portfolios_total = files1.path_files_name()
        files2 = assemble_csv_file_info(path=path)
        portfolios_reged = files2.path_files_name()
        #
        portfolios_list = list(set(portfolios_total) - set(portfolios_reged))
        t0 = time.time()
        if len(portfolios_list) > 0:
            for it in range(len(portfolios_list)):
                print('portfolio:', portfolios_list[it], '|', 'factor model:',
                      para_portfolio_regression['reg_model'])
                file_name = portfolios_file_path + portfolios_list[it] + '.csv'
                df_portfolio = pd.read_csv(file_name)
                df_portfolio = df_portfolio[['month', portfolios_list[it]]]
                para_portfolio_regression['anomaly'] = portfolios_list[it]
                portfolio_regression = data_expert.expert_handle_portfolio_regression(
                    df_portfolio=df_portfolio, df_factor=df_factor_model, para=para_portfolio_regression)
                portfolio_reg_result = portfolio_regression.handle_portfolio_regression()
                save_name = path + portfolios_list[it] + '.csv'
                portfolio_reg_result.to_csv(save_name)
            print('Done! of calculating regression of portfolio raw return '
                  'with the time cost:', time.time() - t0)
        else:
            print('Done! All regressions of portfolios are already exist. '
                  'Not need to calculate regression of portfolios ')
    elif para_portfolio_regression['Is_portfolio_regression'] == 'no':
        print('Not calculate regression of portfolios')
    else:
        raise Exception(' you input wrong parameters of "Is_portfolio_regression" in '
                        'file <./parameter.xml>')
    return
#
def portfolios_risk_adjust_rolling(parameter):
    para = parameter.run_id()
    para_portfolio_regression = parameter.portfolio_regression()
    if para_portfolio_regression['Is_portfolio_regression_rolling'] == 'yes':
        print('Calculate the  rolling regression performance of portfolios raw return using factor model')
        path = '../output/' + para['run_id'] + '/portfolio_regression_rolling/'
        param.mkdir(path=path)
        portfolios_file_path = '../output/' + para['run_id'] + '/portfolio_ret/'
        factor_model_file = '../output/' + para['run_id'] + '/factor_model/factor_model.csv'
        df_factor_model = pd.read_csv(factor_model_file)
        columns = list(df_factor_model.columns)
        if 'Unnamed: 0' in columns:
            df_factor_model.drop('Unnamed: 0', axis=1, inplace=True)
        else:
            df_factor_model = df_factor_model
        #
        files1 = assemble_csv_file_info(portfolios_file_path)
        portfolios_total = files1.path_files_name()
        files2 = assemble_csv_file_info(path=path)
        portfolios_reged = files2.path_files_name()
        portfolios_list = list(set(portfolios_total) - set(portfolios_reged))
        t0 = time.time()
        if len(portfolios_list) > 0:
            for it in range(len(portfolios_list)):
                print('portfolio:', portfolios_list[it], '|rolling|',
                      'factor model:', para_portfolio_regression['reg_model'])
                file_name = portfolios_file_path + portfolios_list[it] + '.csv'
                df_portfolio = pd.read_csv(file_name)
                df_portfolio = df_portfolio[['month', portfolios_list[it]]]
                para_portfolio_regression['anomaly'] = portfolios_list[it]
                #
                portfolio_regression = data_expert.expert_handle_portfolio_regression(
                    df_portfolio=df_portfolio, df_factor=df_factor_model, para=para_portfolio_regression)
                portfolio_reg_result = portfolio_regression.handle_portfolio_regression_rolling()
                save_name = path + portfolios_list[it] + '.csv'
                portfolio_reg_result.to_csv(save_name)
            print('Done! of calculating rolling regression of portfolio '
                  'raw return with the time cost:', time.time() - t0)
        else:
            print('Done! All rolling regressions of portfolios are already exist. '
                  'Not need to calculate rolling regression of portfolios ')
    elif para_portfolio_regression['Is_portfolio_regression_rolling'] == 'no':
        print('Not calculate rolling regression of portfolios')
    else:
        raise Exception(' you input wrong parameters of "Is_portfolio_regression_rolling" in '
                        'file <./parameter.xml>')
    return