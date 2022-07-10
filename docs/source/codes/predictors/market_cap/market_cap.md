### market_cap

The definition of predictor market_cap:

```python
def parameter():
    para = {}
    para['predictor'] = 'market_cap'
    para['relate_finance_index'] = ['size']
    return para
def equation(df):
    df = df.copy()
    df['market_cap'] = df['size']
    return df
```

This definition is written in file <font color=green>'./codes/predictors/market_cap.py'</font>.
Here, <font color=blue>'size'</font> represents the market value.


>Tips:
 * Like <font color=green>'market_cap.py'</font>, people can add new predictor file 
   <font color=green>'predictor_name.py'</font> in the path 
   <font color=green>'./codes/predictors/'</font>. 
 * <font color=blue>'predictor_name'</font> should keep consist with <font color=blue>para['predictor']</font>

