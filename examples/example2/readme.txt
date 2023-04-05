For example1, users just want to calculate value of predictors and
get raw return of portfoliosfor all stocks, then users try to calculate the risk-adjusted
return by using the CAPM model

Before running the project, there is a data preparation:
Users should download csmar_master.sas7bdat (financial statements data) from WRDS to the local path './data/download_data/',
Users should download csmar_t_mnth.sas7bdat (monthly trading data) from WRDS to the local path './data/download_data/'
Users should download csmar_t_week.sas7bdat (weekly trading data) from WRDS to the local path './data/download_data/'.
Users should download csmar_t_dalyr.sas7bdat (daily trading data) from WRDS to the local path './data/download_data/'.
Users should download csmar_t_co.sas7bdat (industry classification information) from WRDS to the local path './data/download_data/'.

After data preparation, to running project example1,
parameters in file './codes/parameter.xml' could be set as:
<Is_download_data> 'no' </Is_download_data> # in the version of project, this parameter is always set as 'no'
<Is_build_monthly_data> 'yes' </Is_build_monthly_data> # build montly data by merging monthly trading data, financial statement data, and industry classification information data
<Is_build_weekly_data> 'yes' </Is_build_weekly_data> # build weekly data by weekly trading data
<Is_build_daily_data> 'yes' </Is_build_daily_data> # build daily data by daily trading data
<Is_build_standard> 'yes' </Is_data_standard> #  standardizing the value of predictors
<Is_add_filters> 'no' </Is_add_filters> # not add filters to clean predictors
<Is_neutral> 'no' <Is_neutral> # not construct market value neutralized portfolio
<Is_construct_model> 'yes' </Is_construct_model> # not construct factor model
<Is_portfolio_regression> 'yes' </Is_portfolio_regression> # calculate the regression of portfolio raw return on factor model
<reg_model> 'capm' </reg_model> # factor model is CAPM
<Is_portfolio_regression_rolling> 'no' </Is_portfolio_regression_rolling> # not calculate the rolling regression of portfolio raw return on factor model

Users can modify the file './codes/parameter.xml' according the above description,
or users can just replace file './codes/parameter.xml' by the file  './examples/example2/parameter.xml'.

