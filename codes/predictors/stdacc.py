# stdacc : Standard deviation of 16 quarters of accruals from month t - 16 to t - 1
#
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
    df['acc_'] = ((df['A001100000'].diff(periods=4) - df['A001101000'].diff(periods=3)) - (
            df['A002100000'].diff(periods=3) - df['A002126000'].diff(periods=3) -
            df['B002100000'].diff(periods=3)) - (
                         df['D000103000'].diff(periods=3) + df['D000104000'])) / df['A001000000']
    df['stdacc'] = df['acc_'].rolling(48).std()
    return df

def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001100000', 'A001101000', 'A002100000', 'A002126000',
                                    'B002100000', 'D000103000', 'D000104000', 'A001000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'stdacc']]
    return df_output