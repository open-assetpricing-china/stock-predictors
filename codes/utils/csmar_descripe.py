# descripe the variables in csmar database
#=========================================
def csmar_t_mnth():
    para = dict()
    para['Stkcd'] = 'Stock code'
    para['Trdmnt'] = 'Trade month'
    para['Opndt'] = 'Day of Opening Price of Month (OPNDT)'
    para['Mopnprc'] = 'Monthly Opening Price (MOPNPRC)'
    para['Clsdt'] = 'Day of Closing Price of Month (CLSDT)'
    para['Mclsprc'] = 'Monthly Closing Price (MCLSPRC)'
    para['Mnshrtrd'] = 'Number of Shares Traded in Month (MNSHRTRD)'  # 当月交易的股票数量（MNSHRTRD）
    para['Mnvaltrd'] = 'Value of Shares Traded in Month (MNVALTRD)'  # 当月交易的股票价值（MNVALTRD）
    para['Mnvaltrd'] = 'Market Value of Tradable Shares (MSMVOSD)'  # 可交易股份的市场价值（MSMVOSD）
    para['Msmvosd'] = 'Market Value of Tradable Shares (MSMVOSD)'  # 可交易股份的市场价值（MSMVOSD）
    para['Msmvttl'] = 'Total Market Value (MSMVTTL)'  # 总市值（MSMVTTL）
    para['Ndaytrd'] = 'Number of Days of Monthly Trading (NDAYTRD)'  # 月度交易日数量
    para['Mretwd'] = 'Monthly Return with Cash Dividend Reinvested (MRETWD)'  # 现金红利再投资的月度回报（MRETWD）
    para['Mretnd'] = 'Monthly Return without Cash Dividend Reinvested (MRETND)'  # 不含现金红利再投资的月度回报（MRETND）
    para['Markettype'] = 'Market Type (MARKETTYPE)'  # 市场类型
    para['Capchgdt'] = 'Share Outstanding Change Date (CAPCHGDT)'  # 未偿股份变更日期（CAPCHGDT）
    para['Ahshrtrd_M'] = 'Monthly After-hours Trading Volume (AHSHRTRD_M)'  # 月度盘后交易量（AHSHRTRD_M）
    para['Ahvaltrd_M'] = 'Monthly After-hours Trading Turnover (AHVALTRD_M)'  # 月度盘后交易额（AHVALTRD_M）
    para['CAPCHGDT_o'] = 'Share Outstanding Change Date (added by WRDS) (CAPCHGDT_O)'  # 未偿股份变更日期（由WRDS添加）（CAPCHGDT_O）
    return para
#
def csmar_financial_income_statement():
    para = {}
    para['Stkcd'] = 'Stock Code'
    para['Accper'] = 'Accounting Period'
    para['Typrep'] = 'Type of statement'
    para['B001100000'] = 'Total Operating Revenue (b001100000)' #营业总收入
    para['B001101000'] = 'Operating Revenue (b001101000)' #营业收入
    para['Bbd1102000'] = 'Net Interest Income (bbd1102000)' # 净利息收入
    para['Bbd1102101'] = 'Interest Income (bbd1102101)' #利息收入
    para['Bbd1102203'] ='Interest Expenses (bbd1102203)' #利息支出
    para['B0i1103000'] = 'Net Earned Premiums (b0i1103000)'#净赚取保费
    para['B0i1103101'] = 'Insurance Underwriting Income (b0i1103101)' #保险承保收入
    para['B0i1103111'] = 'Including: Reinsurance Premium Income (b0i1103111)' #其中：再保险保费收入
    para['B0i1103203'] = 'Less: Premium Ceded To Reinsurers (b0i1103203)' #减：分出给再保险人的保费
    para['B0i1103303'] = 'Less: Provision For Unearned Premium Reserves (b0i1103303)' #减：未到期保费准备金
    para['B0d1104000'] = 'Net Fees And Commissions Income (b0d1104000)' #手续费和佣金净收入（b0d1104000）
    para['B0d1104101'] = 'Including: Net Income From Securities Broker (b0d1104101)'#其中：证券经纪商净收入（b0d1104101）
    para['B0d1104201'] = 'Including: Net Income From Securities Underwriting (b0d1104201)'#其中：证券承销净收入（b0d1104201）
    para['B0d1104301'] = 'Including: Net Income From Asset Management For Customers (b0d1104301)' #其中：客户资产管理净收入（b0d1104301）
    para['B0d1104401'] = 'Fees And Commissions Income (b0d1104401)' #费用和佣金收入（b0d1104401）
    para['B0d1104501'] = 'Fees And Commissions Expenses (b0d1104501)' #费用和佣金支出（b0d1104501）
    para['B0f1105000'] = 'Other Operating Revenue (b0f1105000)' #其他营业收入（b0f1105000）
    para['B001200000'] = 'Total Operating Expenses (b001200000)' #营业费用总额（b001200000）
    para['B001201000'] = 'Operating Expenses (b001201000)'#营业费用（b001201000）
    para['B0i1202000'] = 'Payments On Surrenders (b0i1202000)'#退保付款（b0i1202000）
    para['B0i1203000'] = 'Net Claim Expenses (b0i1203000)' #净索赔费用（b0i1203000）
    para['B0i1203101'] = 'Claim Expenses (b0i1203101)' #索赔费用（b0i1203101）
    para['B0i1203203'] = 'Less: Claims Recoverable From Reinsurers (b0i1203203)' #减：可从再保险人处收回的索赔
    para['B0i1204000'] = 'Net Provision For Insurance Reserves (b0i1204000)' #保险准备金准备金净额（b0i1204000）
    para['B0i1204101'] = 'Provision For Insurance Reserves (b0i1204101)' #保险准备金准备金
    para['B0i1204203'] = 'Less: Insurance Reserves Recoverable From Reinsurers (b0i1204203)' # 减：可从再保险人处收回的保险准备金
    para['B0i1205000'] = 'Policyholder Dividends (b0i1205000)' #投保人股息（b0i1205000）
    para['B0i1206000'] = 'Expenses For Reinsurance Accepted (b0i1206000)' #接受再保险的费用（b0i1206000）
    para['B001207000'] = 'Tax And Additional Fees Of Operations (b001207000)' #营业税及附加费
    para['B0f1208000'] = 'Business And Management Expenses (b0f1208000)' #业务和管理费用（b0f1208000）
    para['B0i1208103'] = 'Less: Expenses Recoverable From Reinsurers (b0i1208103)' #减：可从再保险人处收回的费用
    para['B001209000'] = 'Selling Expenses (b001209000)' #销售费用
    para['B001210000'] = 'General And Administrative Expenses (b001210000)' # 一般和管理费用
    para['B001211000'] = 'Finance Expenses (b001211000)' #财务费用（b001211000）
    para['B001212000'] = 'Impairment Losses (b001212000)' # 减值损失（b001212000）
    para['B0f1213000'] = 'Other Operating Expenses (b0f1213000)' #其他营业费用（b0f1213000）
    para['B001301000'] = 'Gains/Losses From Fair Value Change (b001301000)' #公允价值变动损益
    para['B001302000'] = 'Investment Gains (b001302000)' #投资收益（b001302000）
    para['B001302101'] = 'Including: Investment Gains From Associates And Joint Venture (b001302101)' # 其中：联营企业和合营企业的投资收益（b001302101）
    para['B001303000'] = 'Foreign Exchange Gains (b001303000) ' #外汇收益（b001303000）
    para['B001304000'] = 'Profit From Other Operations (b001304000)' #其他业务利润（b001304000）
    para['B001300000'] = 'Operating Profit (b001300000)' #营业利润（b001300000）
    para['B001400000'] = 'Non-Operating Income (b001400000)' #  营业外收入（B00140000）
    para['B001400101'] = 'Including:Gains from Disposal of Non-current Assets (b001400101)' #其中：非流动资产处置收益（B00140011）
    para['B001500000'] = 'Non-Operating Expenses (b001500000)' #营业外支出（b001500000）
    para['B001500101'] = 'Including: Net Loss From Disposal Of Non-Current Assets (b001500101)' #其中：处置非流动资产净损失（b001500101）
    para['B001500201'] = 'Including:Losses from Disposal of Non-current Assets (b001500201)' #其中：非流动资产处置损失（b001500201）
    para['B001000000'] = 'Total Profit (b001000000)' #利润总额（b001000000）
    para['B002100000'] = 'Income Tax Expenses (b002100000)' #所得税费用（b002100000）
    para['B002200000'] = 'Unrealized Investment Loss (b002200000)' #未实现投资损失（b002200000）
    para['B002300000'] = 'Other Items Affect Net Profit (b002300000)' #其他影响净利润的项目（b002300000）
    para['B002000000'] = 'Net Profit (b002000000)' #净利润（b002000000）
    para['B002000101'] = 'Net Profit Attributable To Owners Of The Parent Company (b002000101)' #归属于母公司所有者的净利润（B0020000101）
    para['B002000201'] = 'Minority Interests (b002000201)' #少数股东权益（b002000201）
    para['B003000000'] = 'Basic Earnings Per Share (b003000000)' #基本每股收益（b003000000）
    para['B004000000'] = 'Diluted Earnings Per Share (b004000000)' #稀释每股收益（b004000000）
    para['B005000000'] = 'Other Consolidated Income (Loss) (b005000000)' #其他综合收益（损失）（b005000000）
    para['B006000000'] = 'Total Consolidated Income (b006000000)' #合并收益总额（b006000000）
    para['B006000101'] = 'Consolidated Income Attributable to Owners of the Parent Company (b006000101)'
    #归属于母公司所有者的合并收益（b006000101）
    para['B006000102'] = 'Consolidated Income Attributable to Minority Shareholders (b006000102)'#归属于少数股东的合并收益（b006000102）
    para['B001216000'] = 'R&D Expenses (b001216000)' #研发费用（b001216000）
    para['B001211101'] = 'Including: Interest Expenses (Financial Expenses) (b001211101)' #其中：利息费用（财务费用）（b001211101）
    para['B001211203'] = 'Including: Interest Income (Financial Expenses) (b001211203)' #其中：利息收入（财务费用）（b001211203）
    para['B001305000'] = 'Other Income (b001305000)' # 其他收入（b001305000）
    para['B001302201'] = 'Including: Derecognition of Financial Assets Measured at Amortized Cost (b001302201)' #
    # 其中：终止确认以摊余成本计量的金融资产（B00130201）
    para['B001306000'] = 'Net Open Hedge Income (b001306000)' #未结对冲净收入（b001306000）
    para['B001307000'] = 'Credit Impairment Loss (b001307000)' # 信用减值损失（b001307000）
    para['B001308000'] = 'Income from Assets Disposal (b001308000)' #资产处置收入（b001308000）
    para['B002000301'] = 'Net Profit Attributable to holders of Other Equity Instruments of the Parent Company (b002000301)'
    #归属于母公司权益工具持有人的净利润
    return para
#===========================================================================
def financial_index_dict():
    para = {}
    para['eps'] = 'B003000000'  # csmar 的financial 数据提供的是 2007 年以后的，2007年以前的 eps 找不到。
    return  para
