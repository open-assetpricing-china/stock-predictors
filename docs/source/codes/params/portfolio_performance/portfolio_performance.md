### para_portfolio_performance
```python
#
from codes.utils import parameters_module as parameters
#
if __name__ == '__main__':
    para = {}
    para_anomaly_performance = parameters.anomaly_performance()
    para = para_anomaly_performance.default_para(para)
    #  这些参数是用来计算 回归表现的
    para['anomaly_list'] = ['ep', 'market_cap', 'pe'] # 用来计算回归表现的 predictors
    para['model'] = 'ch3'  # 设置回归模型 说 ch3 模型 还是 capm 模型
    para['start_date'] = '2000-07'  # start date for regression
    para['end_date'] = '2016-12'  # end date for regression
    #
    para['rolling_period'] = 10  # 滚动计算的窗口宽度
    #
    df_para = para_anomaly_performance.dict_to_dataframe(para)
    df_para.to_csv('../../data/para_file/para_portfolio_performance.csv')
```