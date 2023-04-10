'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# zerotrade:
# LM-1 = [Number of zero daily volumes in prior 1 months + (1/(1-month turnover))/Deflator] * (21)/NoTD
# turnover: the sum of daily turnover over the prior 1 month, where daily turnover is the ratio of the
#           number of shares traded on a day to the number of shares outstanding at the end of the day
# NoTD: total number of trading days in the market over the prior 1 months
# Deflator is chosen such that 0 < [(1/(1-month turnover)) / Deflator] < 1 for all stocks
#==============================================================================================
# 'Dnshrtrd', number of daily trading stocks
# 'Dsmvtll', total market value (千元)
# 'Clsprc', close price
# 'Ndaytrd': number of trading days one month
#=============================================================================================
import pandas as pd
def deflator(x):
    x = x.copy()
    deflator = (1 / x['turnover']).max() + 0.1
    x['deflator'] = deflator
    return x
def get_0traddays(df):
    df.loc[(df['Dnshrtrd'] == 0.0), 'num_0trade'] = 1
    df.loc[(df['Dnshrtrd'] > 0.), 'num_0trade' ] = 0
    df_0trade= df.groupby(['stkcd', 'month']).apply(lambda x: x['num_0trade'].sum())
    df_0trade = df_0trade.reset_index()
    df_0trade.rename(columns={df_0trade.columns[-1]: '0trade_days'}, inplace=True)
    return df_0trade
def get_turnover(df):
    df['turnover_daily'] = df['Dnshrtrd'] / (df['Dsmvtll'] * 1000 / df['Clsprc'])
    df_turnover = df.groupby(['stkcd', 'month']).apply(lambda x: x['turnover_daily'].sum())
    df_turnover = df_turnover.reset_index()
    df_turnover.rename(columns={df_turnover.columns[-1]: 'turnover'}, inplace=True)
    return df_turnover
def get_Deflator(df):
    df1 = df.groupby(['month']).apply(lambda x: deflator(x))
    df1 = df1.set_index(['stkcd', 'month']).reset_index()
    df1.sort_values(['stkcd', 'month'], inplace=True)
    return df1
#
def lag_one_month(x):
    x = x.copy()
    x['zerotrade'] = x['zerotrade'].shift()
    return x
#
def calculation(df_input):
    df_output_1 = df_input['daily'][['stkcd', 'month', 'Dnshrtrd', 'Dsmvtll', 'Clsprc']]
    df_output_1_0trade = get_0traddays(df=df_output_1)
    df_output_1_turnover = get_turnover(df=df_output_1)
    df_output_1_deflator = get_Deflator(df=df_output_1_turnover)
    df_output_by_daily = pd.merge(df_output_1_0trade,df_output_1_deflator, on=['stkcd', 'month'])
    #
    df_output_by_monthly = df_input['monthly'][['stkcd', 'month', 'Ndaytrd']]
    #
    df_output = pd.merge(df_output_by_daily,df_output_by_monthly, on = ['stkcd', 'month'])
    #
    df_output['zerotrade'] = (df_output['0trade_days'] + ((1 / df_output['turnover']) / df_output['deflator'])) * \
                            (21 / df_output['Ndaytrd'])
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output[['stkcd', 'month', 'zerotrade']]