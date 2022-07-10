### para_flag
```python
#
from codes.utils import parameters_module as parameters
if __name__ == '__main__':
    para = {}
    para_flag = parameters.flag()
    para = para_flag.default_para(para=para)
    para['Is_build_data'] = 'no'     # yes or no
    para['Is_calculate_predictors'] = 'no'       # yes or no
    #
    df_para = para_flag.dict_to_dataframe(para=para)
    df_para.to_csv('../../data/para_file/para_flag.csv')
```