'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# acc = [(ΔCA - ΔCASH) - (ΔCL - ΔSTD - ΔTP) - Dep] / Total Assets
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
def equation(x):
    x = x.copy()
    x['acc'] =( (x['A001100000'].diff() - x['A001101000'].diff()) - (
            x['A002100000'].diff() - x['A002125000'].diff() - x['B002100000'].diff()) - (
            x['D000103000'] + x['D000104000']) ) / x['A001000000']
    return x
def lag_one_month(x):
    x= x.copy()
    x['acc'] = x['acc'].shift()
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001100000','A001101000','A002100000','A002125000',
                    'B002100000','D000103000','D000104000','A001000000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'acc']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True) # lag one month
    return df_output
