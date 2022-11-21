# pchsale_pchrect: Quarterly percentage change in sales minus quarterly percentage change
# in receivables
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'A001110000' : Net Notes Receivable
# 'A001111000' : Net Accounts Receivable
# 'A0I1113000' : Net Insurance Premium Receivable
# 'A0I1114000' : Net Reinsurance Receivable
# 'A0I1115000' : Net Subrogation Receivable
# 'A0I1116000' : Net Reinsurance Contract Reserve Receivable
# 'A0I1116101' : Including: Net Receivable from Ceded Unearned Premium Reserves
# 'A0I1116201' : Including: Net Receivable from Ceded Claim Reserves
# 'A0I1116301' : Including: Net Receivable from Ceded Life Insurance Reserves
# 'A0I1116401' : Including: Net Receivable Reserves for Reinsured Long-term Health Insurance Liabilities
# 'A001119000' : Net Interest Receivable
# 'A001120000' : Net Dividends Receivable
# 'A001121000' : Net Other Receivables
#
def equation(x):
    x['pchsale_pchrect'] = x['C001001000'].pct_change(periods=3) - (
        x['A001110000'] + x['A001111000'] + x['A0I1113000']
        + x['A0I1114000'] + x['A0I1115000'] + x['A0I1116000']
        + x['A0I1116101'] + x['A0I1116201'] + x['A0I1116301']
        + x['A0I1116401'] + x['A001119000'] + x['A001120000']
        + x['A001121000']).pct_change(periods=3)
    return x

#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'C001001000', 'A001110000', 'A001111000',
                                     'A0I1113000','A0I1114000', 'A0I1115000','A0I1116000',
                                     'A0I1116101','A0I1116201', 'A0I1116301','A0I1116401',
                                     'A001119000','A001120000', 'A001121000' ]]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchsale_pchrect' ]]
    return df_output