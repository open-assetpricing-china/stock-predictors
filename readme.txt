open source asset pricing in china's stock market
#========================================================================================================
# 通过 predictors 路径下的 xxx.py 文件个数 确定 predictors 的个数
# 通过 /predictos/ 中 xxx.py 文件中对 predictor 的定义来确定所需要的财务指标 也就是 financial_index
#
#========================================================================================================
# 如果从 wrds 下载了最新的 csmar_trade data 和 csmar_finance data
# run ./codes/main.py 中的 build_data() 函数来更新 ./data/basic/basic_data.parquet
#
#=======================================================================================================
# update factor_model
# run ./codes/factor_model/make.py to update the file in ./output/factor_model/factor_model.csv
#
#==================================================================================================

