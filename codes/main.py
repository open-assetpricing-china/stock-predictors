import sys
from os.path import dirname, abspath
path = dirname(dirname(abspath(__file__))) # back to folder 'OSAP' need back two steps
sys.path.append(path)
#print('sys.path:', str(sys.path))
from codes.utils.assemble_factory import read_parameters, download_data, build_data
from codes.utils.assemble_factory import calculate_predictors, predictors_wash, factors_model
from codes.utils.assemble_factory import predictors_to_portfolios
from codes.utils.assemble_factory import portfolios_risk_adjust
from codes.utils.assemble_factory import portfolios_risk_adjust_rolling
#
if __name__ == '__main__':
    #
    parameter = read_parameters() # reading input parameters
    download_data(parameter=parameter) # downloading raw data
    build_data(parameter=parameter) # raw data -> monthly data, weekly data, daily data
    calculate_predictors(parameter=parameter) # calculate predictors
    predictors_wash(parameter=parameter) # wash predictors
    predictors_to_portfolios(parameter=parameter) # obtain portfolio raw return
    factors_model(parameter=parameter) # construct factors model
    portfolios_risk_adjust(parameter=parameter) # get the regression performance of portfolio raw return
    portfolios_risk_adjust_rolling(parameter=parameter) # get the rolling regression performance of portfolio raw return

