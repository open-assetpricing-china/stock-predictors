### para_construct_portfolio
```python
from codes.utils import parameters_module as parameters
if __name__ == '__main__':
    para = {}
    para_anomaly = parameters.anomaly()
    print('para_anomaly:', para_anomaly)
    para = para_anomaly.default_para(para)
    para['neutral_var'] = 'size'  # 市值中性化 # 采用哪种 neutralize 的方式
    para['way_weight'] = 'size'  # 市值加权 # 控制计算 ret 时加权的方式 {'size', 'ew'}
    para['Is_neutral'] = 'yes'  # 是否进行中性化 {'yes', 'no'}
    #
    df_para = para_anomaly.dict_to_dataframe(para)
    df_para.to_csv('../../data/para_file/para_construct_portfolio.csv')
```
