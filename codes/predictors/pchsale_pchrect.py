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
def parameter():
    para = {}
    para['predictor'] = 'pchsale_pchrect'
    para['relate_finance_index'] = ['C001001000', 'A001110000', 'A001111000','A0I1113000',
                                    'A0I1114000', 'A0I1115000','A0I1116000','A0I1116101',
                                    'A0I1116201', 'A0I1116301','A0I1116401','A001119000',
                                    'A001120000', 'A001121000' ]
    return para
#
def equation(df):
    df = df.copy()
    df['pchsale_pchrect'] = df['C001001000'].pct_change(periods=3) - (
        df['A001110000'] + df['A001111000'] + df['A0I1113000']
        + df['A0I1114000'] + df['A0I1115000'] + df['A0I1116000']
        + df['A0I1116101'] + df['A0I1116201'] + df['A0I1116301']
        + df['A0I1116401'] + df['A001119000'] + df['A001120000']
        + df['A001121000']).pct_change(periods=3)
    return df