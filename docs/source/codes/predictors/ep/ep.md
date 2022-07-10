### ep 

The definition of predictor ep:
```python
def parameter():
    para = {}
    para['predictor'] = 'ep'
    para['relate_finance_index'] = ['clsprc', 'B003000000']
    return para
def equation(df):
    df = df.copy()
    df['ep'] = df['B003000000'] / df['clsprc'] # df['B00300000'] -> eps
    return df
```
This definition is written in file <font color=green>'./codes/predictors/ep.py'</font>.
Here, <font color=blue>'clsprc'</font> represent the close price, 
and <font color=blue>'B003000000'</font>  represents 
the  Earnings Per Share (eps) which from the 
CSMAR <font color=red>csmar_master.sas7bdat</font> dataset.
 
>Tips:
 * Like <font color=green>'ep.py'</font> file, people can add new predictor file 
   <font color=green>'ep.py'</font> in the path <font color=green>'./codes/predictors/'</font>. 
 * <font color=blue>'predictor_name'</font> should keep 
   consist with <font color=blue>para['predictor']</font>

