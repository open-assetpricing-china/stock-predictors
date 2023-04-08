'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Sum of 9 indicator variables that are defined similarly as in Piotroski (2000)
# F_SCORE = F_ROA + F_ΔROA + F_CFO + F_ACCRUAL +
#           F_ΔMARGIN + F_ΔTURN + F_ΔLEVER + F_ΔLIQUID + EQ_OFFER
# =====================================================================
# ROA = Net Income / Total Assets  (也可以用 Net Profit / Total Asset 来代替)
# Net income (NI), also called net earnings,
# is calculated as sales minus cost of goods sold, selling, general
# and administrative expenses, operating expenses, depreciation, interest,
# taxes, and other expenses.
# 'A001000000' : Total Assets
# 'B001100000' : Total Operating Revenue
# 'B001209000' : Selling Expenses
# 'B001500000' : Non-operating Expenses
# 'A001219000' : Research & Development Expenses
# 'A001221000' : Long-term Deferred Expenses
# 'B0D1104501' : Fees and Commissions Expenses
# 'B0I1203101' : Claim Expenses
# 'B0F1208000' : Business and Management Expenses
# 'B001209000' : Selling Expenses
# 'B001210000' : Administrative Expenses
# 'B001211000' : Financial Expenses
# 'B0F1213000' : Cost of Other Operations
# 'B001500000' : Non-operating Expenses
# *********************************************
# 值得注意的是 在财报columns 中没有找到这几列：'B0D1104501', 'B0I1203101', 'B0F1208000', 'B0F1213000',
# (也可以用 Net Profit / Total Asset 来代替)
# Net Profit: 'B002000000 : Net profit ==> 净利润
# ROA > 0  F_ROA = 1   ROA < 0  F_ROA = 0
# 'A001000000' : Total Assets
#=========================================================
# CFO : cash flow from operation / beginning of the year total assets
# 'D000100000' : Net Cash Flow from Operating Activities
# CFO > 1  F_CFO = 1   CFO < 1  F_CFO =0
#==============================================================
# ACCRUAL : Define the variable ACCRUAL as the current year's net income before
# extraordinary items less cash flow from operations, scaled by beginning-of-the-year total assets.
# CFO > ROA  F_ACCRUAL = 1 ;  CFO < ROA  F_ACCRUAL = 0
#================================================================
# MARGIN : the firm's current gross margin ratio (gross margin scaled by total sales)
# MARGIN  =  gross margin / total sales;  gross margin ratio : 毛利率
# ΔMARGIN > 0  F_ΔMARGIN = 1;
# ΔMARGIN < 0  F_ΔMARGIN = 0;
# 'B001000000' : Total Profit
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# ===========================================================================
# ΔTURN : firm's current year asset turnover ratio (total sales scaled by beginning-of-the-year
# total assets) less the prior year's asset turnover ratio.
# TURN = total sales / total assets
# ΔTURN > 0  F_ΔTURN = 1
# ΔTURN < 0  F_ΔTURN = 0
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'A001000000' : Total Assets
# ====================================================================
# LEVER : captures changes in the firm's long-term debt levels.
# LEVER = total long-term debt / average total assets
# ΔLEVER < 0  F_ΔLEVER = 1
# ΔLEVER > 0  F_ΔLEVER = 0
# 'A001206000' : Net Long-term Debt Investments
# =====================================================================
# Liquidity:
# ΔLIQUID: measures the historical change in the firm's current ratio
# between the current and prior year, where define the current ratio as the ratio
# as the ratio of current assets to current liabilities at fiscal year end
# ΔLIQUID > 0  F_ΔLEVER = 1
# ΔLIQUID < 0  F_ΔLEVER = 0
# 'A002100000' : Total Current Liabilities
# 'A001100000' : Total Current Assets
#================================================================================
# EQ_OFFER
#
#================================================================================
def parameter():
    para = {}
    para['predictor'] = 'ps'
    list_ROA = [ 'A001000000', 'B001100000','B001209000','B001500000',
                 'B0D1104501', 'B0I1203101','B0F1208000','B001210000',
                 'B001211000', 'B0F1213000', 'B001500000']
    list_CFO = ['D000100000']
    list_MARGIN = ['B001000000', 'C001001000']
    list_LEVER = ['A001206000']
    list_LIQUID = ['A002100000', 'A001100000']
    para['relate_finance_index'] = list_ROA + list_CFO + list_MARGIN + list_LEVER + list_LIQUID
    return para
def equation(x):
    #df['ROA'] = (df['B001100000'] - df['B001209000'] - df['B001500000']
    #             - df['B0D1104501'] - df['B0I1203101'] - df['B0F1208000']
    #             - df['B001210000'] - df['B001211000'] - df['B0F1213000']
    #             - df['B001500000']) / df['A001000000']
    x['ROA'] = x['B002000000'] / x['A001000000']
    x['F_ROA'] = x['ROA'].apply(lambda x: 1 if x>0 else 0)
    #
    x['Delta_ROA'] = x['ROA'].diff(periods=3)
    x['F_Delta_ROA'] = x['Delta_ROA'].apply(lambda x: 1 if x>0 else 0)
    #
    x['CFO'] = x['D000100000'] / x['A001000000'].shift(12)
    x['F_CFO'] = x['CFO'].apply(lambda x: 1 if x>0 else 0)
    #
    x['Diff_CFO_ROA'] = x['CFO'] - x['ROA']
    x['F_ACCRUAL'] =  x['Diff_CFO_ROA'].apply(lambda x: 1 if x>0 else 0)
    #
    x['MARGIN'] = x['B001000000'] / x['C001001000']
    x['Delta_MARGIN'] = x['MARGIN'].diff(periods=3)
    x['F_Delta_MARGIN'] = x['Delta_MARGIN'].apply(lambda x: 1 if x>0 else 0)
    #
    x['TURN'] = x['C001001000'] / x['A001000000'].shift(12)
    x['Delta_TURN'] = x['TURN'].diff(periods=3)
    x['F_Delta_TURN'] = x['Delta_TURN'].apply(lambda x : 1 if x>0 else 0)
    #
    x['LEVER'] = x['A001206000'] / x['A001000000']
    x['Delta_LEVER'] = x['LEVER'].diff(periods=3)
    x['F_Delta_LEVER'] = x['Delta_LEVER'].apply(lambda x: 1 if x<0 else 0)
    #
    x['LIQUID'] = x['A002100000'] / x['A001100000']
    x['Delta_LIQUID'] = x['LIQUID'].diff(periods=3)
    x['F_Delta_LIQUID'] = x['Delta_LIQUID'].apply(lambda x:1 if x>0 else 0)
    #
    x['ps'] = x['F_ROA'] + x['F_Delta_ROA'] + x['F_CFO'] + x['F_ACCRUAL'] + \
               x['F_Delta_MARGIN'] + x['F_Delta_TURN'] + x['F_Delta_LEVER'] + \
               x['F_Delta_LIQUID']

    #drop_columns = ['ROA', 'F_ROA', 'Delta_ROA', 'F_Delta_ROA', 'CFO', 'F_CFO',
    #                'Diff_CFO_ROA', 'F_ACCRUAL', 'MARGIN', 'Delta_MARGIN',
    #                'F_Delta_MARGIN', 'TURN', 'Delta_TURN', 'F_Delta_TURN',
    #                'LEVER','Delta_LEVER','F_Delta_LEVER','LIQUID','Delta_LIQUID''F_Delta_LIQUID']
    #df.drop(columns=drop_columns, inplace=True)
    return x

def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month','A001000000', 'B001100000','B001209000',
                                     'B001500000', 'B002000000',
                                     'B001210000', 'B001211000', 'B001500000',
                                     'D000100000', 'B001000000', 'C001001000',
                                     'A001206000', 'A002100000', 'A001100000',]]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'ps']]
    return df_output