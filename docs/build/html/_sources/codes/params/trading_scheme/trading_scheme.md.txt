### para_trading_scheme
```python
#
from codes.utils import parameters_module as parameters
#
if __name__ == '__main__':
    para = {}
    para_csmar_basic = parameters.csmar_basic()
    para = para_csmar_basic.default_para(para=para)
    para['yearly_mnt_period'] = 12     # 股票一年交易的月份数量，用来计算一年中真实的累积交易天数
    para['mnt_comm_trdday'] = 21       # 如果股票月度交易日数量缺失的话，用 21天来填充
    para['exclude_bottom_size'] = 0.3  #  excluding the percentage of smallest stocks
    para['exclude_trdday_lsyr'] = 126  # 除掉股票年度交易日累积小于126天的交易记录
    para['exclude_trdday_lsmnt'] = 15  # 除掉股票月度交易日小于15天的记录
    para['exclude_begin_trdday'] = '1999-12' # 除掉股票在 '1992-12' 月之前有交易的股票记录
    #
    df_para = para_csmar_basic.dict_to_dataframe(para=para)
    df_para.to_csv('../../data/para_file/para_trading_scheme.csv')
```