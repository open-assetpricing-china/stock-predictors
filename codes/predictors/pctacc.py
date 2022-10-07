# Same as acc except that the numerator is divided by the absolute value
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
def parameter():
    para = {}
    para['predictor'] = 'pctacc'
    para['relate_finance_index'] = ['A001100000','A001101000','A002100000','A002126000',
                                    'B002100000','D000103000','D000104000','A001000000']
    return para
def equation(df):
    df = df.copy()
    df['pctacc'] =(( (df['A001100000'].diff() - df['A001101000'].diff()) - (
        df['A002100000'].diff() - df['A002126000'].diff() - df['B002100000'].diff()) - (
        df['D000103000'].diff() + df['D000104000']) ).abs() / df['A001000000']).pct_change()
    return df