from codes.utils.assemble_factory import build_data
from codes.utils.assemble_factory import calculate_predictors, load_trading_scheme
from codes.utils.assemble_factory import update_portfolio_ret
from codes.utils.assemble_factory import update_portfolio_performance
from codes.utils.assemble_factory import update_portfolio_rolling_performance
#
if __name__ == '__main__':
    #
    build_data(para_flag_path = '../data/para_file/para_flag.csv') # merging csmar_trade data and csmar_finance data to form a large panel data
    #running build_csmar_basic() cost: 289s
    calculate_predictors(predictor_file_path = './predictors/',
                         para_flag_path = '../data/para_file/para_flag.csv')
    #
    df = load_trading_scheme(para_path='../data/para_file/para_trading_scheme.csv',
                             df_path='../output/predictors/predictors.csv')
    update_portfolio_ret(para_path='../data/para_file/para_construct_portfolio.csv', df=df) # long short raw return
    #
    # get the regression performance of portfolio_ret
    path_portfolio = '../output/portfolio_ret/portfolio_ret.csv'
    path_factor = '../output/factor_model/factor_model.csv'
    path_para_portfolio_performance = '../data/para_file/para_portfolio_performance.csv'
    #
    update_portfolio_performance(path_anomaly=path_portfolio, path_factor=path_factor,
                               path_para = path_para_portfolio_performance)
    #
    update_portfolio_rolling_performance(path_anomaly=path_portfolio,path_factor=path_factor,
                                       path_para = path_para_portfolio_performance)
