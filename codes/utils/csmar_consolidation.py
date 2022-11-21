# process the daily data, weekly data, and monthly data
#
from codes.utils import csmar_process
import time
#
def monthly_add_finance_data():
    # merge monthly data with finance data
    print('begin the merging of <monthly trade data> and <finance data> to form a large panel data')
    t0 = time.time()
    # 将 raw csmar_trade 和 raw csmar_finance 并起来，形成一个大的panel data.
    csmar_trade = csmar_process.csmar_trading()
    df_trade = csmar_trade.output_trading_data()

    # 得到 csmar_finance data
    csmar_finance = csmar_process.csmar_finance_raw()
    df_finance = csmar_finance.output_finance_data()
    # 对 csmar_finance data 进行处理
    t1 = time.time()
    fin_post = csmar_process.csmar_finance_postprocess_raw(df=df_finance)
    df_fin = fin_post.output_finance_data()
    print('Done! of postprocessing csmar_finance with time cost:', time.time() - t1)
    # 通过 merge 的方法来 merge df_csmar_basic 和 df_fin 来更新 csmar_basic
    data_merge = csmar_process.merge_csmar_basic_and_finance_data(df_basic=df_trade, df_fin=df_fin)
    df_all = data_merge.merge()
    print('Done! of merging with time cost:', time.time() - t0)
    return df_all
#
def monthly_add_industry_data(df):
    # merge monthly data with industry data
    print('begin the merging of <monthly data> and <industry data> to form a large panel data')
    t0 = time.time()
    csmar_indutry = csmar_process.csmar_basic_add_industry(df)
    df1 = csmar_indutry.add_industry()
    print('Done! of merging with time cost:', time.time() - t0)
    return df1
#=======================================================================
def weekly_data():
    print('begin the initial process of weekly data')
    t0 = time.time()
    csmar_week = csmar_process.csmar_t_week()
    df = csmar_week.output_trading_data()
    print('Done! of initial processing of weekly data with time cost:', time.time()-t0)
    return df
#
def weekly_add_finance_data():
    # merge weekly data with finance data
    return
#
def weekly_add_industry_data():
    # merge weekly data with industry data
    return
#======================================================================
def daily_data():
    print('begin the initial process of daily data')
    t0 = time.time()
    csmar_daily = csmar_process.csmar_t_daily()
    df = csmar_daily.output_trading_data()
    print('Done! of initial processing of daily data with time cost:', time.time() - t0)
    return df
#
def daily_add_finance_data():
    # merge daily data with finance data
    return
#
def daily_add_industry_data():
    # merge daily data with industry data
    return



