'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# pctacc: Same as acc except that the numerator is divided by the absolute value
# of net income if net income = 0 then net income set to 0.01 for
# denominator.
# CA:   'A001100000', current assets
# CASH: 'A001101000', cash / cash equivalents
# CL:   'A002100000', current liabilities
# STD:  'A002125000', Non-current Liabilities Due within One Year
# TP:   'B002100000', income tax payable
# Dep:  'D000103000', depreciation expense 折旧费用
# Dep:  'D000104000', amortization expense 摊销费用
# TA:   'A001000000', Total Assets
# acc = [(ΔCA - ΔCASH) - (ΔCL - ΔSTD -ΔTP) - Dep] / Total Assets
#
import numpy as np
def equation(df):
    df = df.copy()
    df['pctacc'] =(( (df['A001100000'].diff(periods=3) - df['A001101000'].diff(periods=3)) - (
        df['A002100000'].diff(periods=3) - df['A002125000'].diff(periods=3) -
        df['B002100000'].diff(periods=3)) - (df['D000103000']
                                             + df['D000104000']) ).abs() / df['A001000000']).pct_change(periods=3)
    return df
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001000000']==0),'A001000000'] = np.nan
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pctacc'] = x['pctacc'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001100000','A001101000','A002100000',
                                     'A002125000', 'B002100000','D000103000',
                                     'D000104000','A001000000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pctacc']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output
