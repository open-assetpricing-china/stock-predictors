'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# pctacc: Same as acc except that the numerator is divided by the absolute value
# of net income if net income = 0 then net income set to 0.01 for
# denominator.
# CA:   'A001100000', current assets
# CASH: 'A001101000', cash / cash equivalents
# CL:   'A002100000', current liabilities
# STD:  'A002126000', debt included in current liabilities
# TP:   'B002100000', income tax payable
# Dep:  'D000103000', depreciation expense 折旧费用
# Dep:  'D000104000', amortization expense 摊销费用
# TA:   'A001000000', Total Assets
# acc = [(ΔCA - ΔCASH) - (ΔCL - ΔSTD -ΔTP) - Dep] / Total Assets
#
def equation(df):
    df = df.copy()
    df['pctacc'] =(( (df['A001100000'].diff(periods=3) - df['A001101000'].diff(periods=3)) - (
        df['A002100000'].diff(periods=3) - df['A002126000'].diff(periods=3) -
        df['B002100000'].diff(periods=3)) - (df['D000103000']
                                             + df['D000104000']) ).abs() / df['A001000000']).pct_change(periods=3)
    return df
#
def lag_one_month(x):
    x = x.copy()
    x['pctacc'] = x['pctacc'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001100000','A001101000','A002100000',
                                     'A002126000', 'B002100000','D000103000',
                                     'D000104000','A001000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pctacc']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output
