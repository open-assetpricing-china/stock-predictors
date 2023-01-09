import pandas as pd
import numpy as np
import pyarrow.feather as feather
from tqdm import tqdm
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import ParameterGrid
from sklearn.linear_model import ElasticNet
from sklearn.cross_decomposition import PLSRegression
from sklearn.neural_network import MLPRegressor

'''You might need to change your parameter here'''
input_path = 'monthly_predictors.parquet'
output_path = 'Change Path'
train_start_year = 1991
train_year_number = 12
val_year_number = 8
test_year_number = 11
model = 'RF'  # Choose Your Model from ['PLS', 'ENet', 'RF', 'GBRT', 'NN1', 'NN3', 'NN5']

def model_choose(m):
    if m == 'PLS':
        param_grid = {
            'n_components': np.arange(1, 15, 1).tolist(),
            'scale': [False]
        }
    if m == 'ENet':
        param_grid = {
            'alpha': [0.0001, 0.00025, 0.0005, 0.00075, 0.001, 0.0025,
                      0.005, 0.0075, 0.01, 0.025, 0.05, 0.075, 0.1],
            'random_state': [55]
        }
    if m == 'RF':
        param_grid = {
            'max_depth': [1, 2, 3, 4, 5],
            'max_features': [3, 5, 10, 20, 30],
            'n_estimators': [100],
            'min_samples_split': [0.01],
            'min_samples_leaf': [0.01],
            'random_state': [55],
            'bootstrap': [True],
            'n_jobs': [-1]
        }
    if m == 'GBRT':
        param_grid = {
            'max_depth': [1, 3, 5],
            'max_features': [10, 30, 50],
            'n_estimators': [300],
            'random_state': [55],
            'loss': ['huber'],
            'criterion': ['squared_error'],
            'n_iter_no_change': [10],
            'tol': [0.01],
            'learning_rate': [0.1, 0.01]
        }
    if m == 'NN1':
        param_grid = {
            'hidden_layer_sizes': [(32,)],
            'activation': ['relu'],
            'solver': ['adam'],
            'random_state': [66],
            'alpha': [0.001, 0.00001],
            'batch_size': [10000],
            'learning_rate_init': [0.001, 0.01],
            'early_stopping': [True],
            'n_iter_no_change': [10],
            'max_iter': [500],
            'tol': [0.0001]
        }
    if m == 'NN3':
        param_grid = {
            'hidden_layer_sizes': [(32, 16, 8)],
            'activation': ['relu'],
            'solver': ['adam'],
            'random_state': [5, 15, 25, 35, 45],
            'alpha': [0.001, 0.00001],
            'batch_size': [10000],
            'learning_rate_init': [0.001, 0.01],
            'n_iter_no_change': [10],
            'early_stopping': [True],
            'max_iter': [500],
            'tol': [0.01]
        }
    if m == 'NN5':
        param_grid = {
            'hidden_layer_sizes': [(32, 16, 8, 4, 2)],
            'activation': ['relu'],
            'solver': ['adam'],
            'random_state': [5, 15, 25, 35, 45],
            'alpha': [0.001, 0.00001],
            'batch_size': [10000],
            'learning_rate_init': [0.001, 0.01],
            'n_iter_no_change': [10],
            'early_stopping': [True],
            'max_iter': [500],
            'tol': [0.01]
        }
    param_space = list(ParameterGrid(param_grid))
    return param_space, param_grid

def rolling(df, method, x_col, param_space, train_start, train_year, val_year, test_year):
    aggregate_r = []
    aggregate_mse = []
    best_parameters = pd.DataFrame()
    best_scores = []
    pred_test = []
    group_result = pd.DataFrame(columns=['r1', 'r2', 'r3', 'mse1', 'mse2', 'mse3', 'c1', 'c2', 'c3'])

    for i in tqdm(range(test_year)):

        # Define Timing Variables
        val_start = train_start + train_year + i
        train_end = val_start - 1
        val_end = val_start + val_year - 1
        test_year = val_end + 1

        # Split Data
        x_train, y_train = df.loc[(df['year'] >= train_start) & (df['year'] <= train_end), x_col].values, \
            df.loc[(df['year'] >= train_start) & (df['year'] <= train_end), 'ret'].values
        x_val, y_val = df.loc[(df['year'] >= val_start) & (df['year'] <= val_end), x_col].values, \
            df.loc[(df['year'] >= val_start) & (df['year'] <= val_end), 'ret'].values
        x_test, y_test = df.loc[df['year'] == test_year, x_col].values, \
            df.loc[df['year'] == test_year, 'ret'].values

        # Grid Search for Best Model

        best_score = -10000
        best_para = {}
        best_model = np.NAN

        if method == 'ENet':
            for regress_para in param_space:
                regressor = ElasticNet(**regress_para).fit(x_train, y_train)
                r2_up = (y_val - regressor.predict(x_val)) ** 2
                r2_down = (y_val) ** 2
                score = 1 - (r2_up.sum() / r2_down.sum())
                if score > best_score:
                    best_score = score
                    best_para = regress_para
                    best_model = regressor

            y_test_pred = best_model.predict(x_test)
            aggregate_r.append(r2_score(y_test, y_test_pred))
            aggregate_mse.append(mean_squared_error(y_test, y_test_pred))
            best_parameters = pd.concat([best_parameters, pd.DataFrame([best_para])])
            best_scores.append(best_score)
            pred_test.extend(y_test_pred)

        if method == 'PLS':
            for regress_para in param_space:
                regressor = PLSRegression(**regress_para).fit(x_train, y_train)
                r2_up = (y_val - regressor.predict(x_val)) ** 2
                r2_down = (y_val) ** 2
                score = 1 - (r2_up.sum() / r2_down.sum())
                if score > best_score:
                    best_score = score
                    best_para = regress_para
                    best_model = regressor

            y_test_pred = best_model.predict(x_test)
            aggregate_r.append(r2_score(y_test, y_test_pred))
            aggregate_mse.append(mean_squared_error(y_test, y_test_pred))
            best_parameters = pd.concat([best_parameters, pd.DataFrame([best_para])])
            best_scores.append(best_score)
            pred_test.extend(y_test_pred)

        if method == 'RF':
            for regress_para in param_space:
                regressor = RandomForestRegressor(**regress_para).fit(x_train, y_train)
                r2_up = (y_val - regressor.predict(x_val)) ** 2
                r2_down = (y_val) ** 2
                score = 1 - (r2_up.sum() / r2_down.sum())
                if score > best_score:
                    best_score = score
                    best_para = regress_para
                    best_model = regressor

            y_test_pred = best_model.predict(x_test)
            aggregate_r.append(r2_score(y_test, y_test_pred))
            aggregate_mse.append(mean_squared_error(y_test, y_test_pred))
            best_parameters = pd.concat([best_parameters, pd.DataFrame([best_para])])
            best_scores.append(best_score)
            pred_test.extend(y_test_pred)

        if method == 'GBRT':
            for regress_para in param_space:
                regressor = GradientBoostingRegressor(**regress_para).fit(x_train, y_train)
                r2_up = (y_val - regressor.predict(x_val)) ** 2
                r2_down = (y_val) ** 2
                score = 1 - (r2_up.sum() / r2_down.sum())
                if score > best_score:
                    best_score = score
                    best_para = regress_para
                    best_model = regressor

            y_test_pred = best_model.predict(x_test)
            aggregate_r.append(r2_score(y_test, y_test_pred))
            aggregate_mse.append(mean_squared_error(y_test, y_test_pred))
            best_parameters = pd.concat([best_parameters, pd.DataFrame([best_para])])
            best_scores.append(best_score)
            pred_test.extend(y_test_pred)

        if method == 'NN1':
            for regress_para in param_space:
                regressor = MLPRegressor(**regress_para).fit(x_train, y_train)
                r2_up = (y_val - regressor.predict(x_val)) ** 2
                r2_down = (y_val) ** 2
                score = 1 - (r2_up.sum() / r2_down.sum())
                if score > best_score:
                    best_score = score
                    best_para = regress_para
                    best_model = regressor

            y_test_pred = best_model.predict(x_test)
            aggregate_r.append(r2_score(y_test, y_test_pred))
            aggregate_mse.append(mean_squared_error(y_test, y_test_pred))
            best_parameters = pd.concat([best_parameters, pd.DataFrame([best_para])])
            best_scores.append(best_score)
            pred_test.extend(y_test_pred)

        if method == 'NN3':
            for regress_para in param_space:
                regressor = MLPRegressor(**regress_para).fit(x_train, y_train)
                r2_up = (y_val - regressor.predict(x_val)) ** 2
                r2_down = (y_val) ** 2
                score = 1 - (r2_up.sum() / r2_down.sum())
                if score > best_score:
                    best_score = score
                    best_para = regress_para
                    best_model = regressor

            y_test_pred = best_model.predict(x_test)
            aggregate_r.append(r2_score(y_test, y_test_pred))
            aggregate_mse.append(mean_squared_error(y_test, y_test_pred))
            best_parameters = pd.concat([best_parameters, pd.DataFrame([best_para])])
            best_scores.append(best_score)
            pred_test.extend(y_test_pred)

        if method == 'NN5':
            for regress_para in param_space:
                regressor = MLPRegressor(**regress_para).fit(x_train, y_train)
                r2_up = (y_val - regressor.predict(x_val)) ** 2
                r2_down = (y_val) ** 2
                score = 1 - (r2_up.sum() / r2_down.sum())
                if score > best_score:
                    best_score = score
                    best_para = regress_para
                    best_model = regressor

            y_test_pred = best_model.predict(x_test)
            aggregate_r.append(r2_score(y_test, y_test_pred))
            aggregate_mse.append(mean_squared_error(y_test, y_test_pred))
            best_parameters = pd.concat([best_parameters, pd.DataFrame([best_para])])
            best_scores.append(best_score)
            pred_test.extend(y_test_pred)

        print(best_para)
        print(best_score)

        # Record Model Prediction (Group)

        group = pd.DataFrame(columns=['y_test', 'y_test_pred'])
        group['y_test'] = y_test
        group['y_test_pred'] = y_test_pred

        temp = group[group['y_test'] < group['y_test'].quantile(0.1)]
        group_result.loc[i, 'r1'] = r2_score(temp['y_test'], temp['y_test_pred'])
        group_result.loc[i, 'mse1'] = mean_squared_error(temp['y_test'], temp['y_test_pred'])
        group_result.loc[i, 'c1'] = temp['y_test'].count()

        temp = group[
            (group['y_test'] <= group['y_test'].quantile(0.9)) & (group['y_test'] >= group['y_test'].quantile(0.1))]
        group_result.loc[i, 'r2'] = r2_score(temp['y_test'], temp['y_test_pred'])
        group_result.loc[i, 'mse2'] = mean_squared_error(temp['y_test'], temp['y_test_pred'])
        group_result.loc[i, 'c2'] = temp['y_test'].count()

        temp = group[group['y_test'] > group['y_test'].quantile(0.9)]
        group_result.loc[i, 'r3'] = r2_score(temp['y_test'], temp['y_test_pred'])
        group_result.loc[i, 'mse3'] = mean_squared_error(temp['y_test'], temp['y_test_pred'])
        group_result.loc[i, 'c3'] = temp['y_test'].count()

    result = pd.concat([group_result, pd.DataFrame(aggregate_r, columns=['outsample_r'])], axis=1)
    result = pd.concat([result, pd.DataFrame(best_scores, columns=['insample_mse'])], axis=1)
    result = pd.concat([result, pd.DataFrame(aggregate_mse, columns=['outsample_mse'])], axis=1)
    result = pd.concat([result, best_parameters.reset_index(drop=True)], axis=1)

    # 更改test年份
    df_sr = pd.concat([df.loc[(df['year'] >= (train_start + train_year + val_year)) &
                              (df['year'] <= (train_start + train_year + val_year + test_year - 1)),
                              ['month', 'stkcd', 'ret']].reset_index(drop=True),
                       pd.DataFrame(pred_test, columns=['pred_ret'])], axis=1)

    return result, df_sr

def cal_sr(df):
    long_port = df.groupby('month').pred_ret.quantile(0.9).reset_index()
    short_port = df.groupby('month').pred_ret.quantile(0.1).reset_index()
    long_port = long_port.rename(columns={'pred_ret': 'long'})
    short_port = short_port.rename(columns={'pred_ret': 'short'})

    df1 = pd.merge(df, long_port, on='month')
    df1 = pd.merge(df1, short_port, on='month')

    df_long = df1[df1['pred_ret'] >= df1['long']].reset_index(drop=True)
    df_long_pred = df_long.groupby('month').pred_ret.mean().reset_index()
    df_long_pred = df_long_pred.rename(columns={'pred_ret': 'pred_long'})
    df_long_avg = df_long.groupby('month').ret.mean().reset_index()
    df_long_avg = df_long_avg.rename(columns={'ret': 'ret_long'})

    df_short = df1[df1['pred_ret'] <= df1['short']].reset_index(drop=True)
    df_short_pred = df_short.groupby('month').pred_ret.mean().reset_index()
    df_short_pred = df_short_pred.rename(columns={'pred_ret': 'pred_short'})
    df_short_avg = df_short.groupby('month').ret.mean().reset_index()
    df_short_avg = df_short_avg.rename(columns={'ret': 'ret_short'})

    df_avg = pd.merge(df_long_avg, df_short_avg, on='month')
    df_pred = pd.merge(df_long_pred, df_short_pred, on='month')
    df_avg['hedge_ret'] = df_avg['ret_long'] - df_avg['ret_short']
    df_pred['hedge_ret'] = df_pred['pred_long'] - df_pred['pred_short']

    avg_mean = df_avg['hedge_ret'].mean()
    pred_mean = df_pred['hedge_ret'].mean()
    avg_std = df_avg['hedge_ret'].std()
    avg_sr = avg_mean * 12 / (avg_std ** 2 * 12) ** 0.5

    df['up'] = (df['ret'] - df['pred_ret']) ** 2
    df['down'] = (df['ret']) ** 2
    r2 = 1 - (df['up'].sum() / df['down'].sum())

    return pred_mean, avg_mean, avg_std, avg_sr, r2

def standardize(df):
    # exclude the the information columns
    col_names = df.columns.values.tolist()
    list_to_remove = ['stkcd', 'month', 'ret']
    col_names = list(set(col_names).difference(set(list_to_remove)))
    for col_name in tqdm(col_names):
        # print('processing %s' % col_name)
        # count the non-missing number of factors, we only count non-missing values
        unique_count = df.dropna(subset=['%s' % col_name]).groupby(['month'])['%s' % col_name].unique().apply(len)
        unique_count = pd.DataFrame(unique_count).reset_index()
        unique_count.columns = ['month', 'count']
        df = pd.merge(df, unique_count, how='left', on=['month'])
        # ranking, and then standardize the data
        df['%s_rank' % col_name] = df.groupby(['month'])['%s' % col_name].rank(method='dense')
        df['rank_%s' % col_name] = (df['%s_rank' % col_name] - 1) / (df['count'] - 1) * 2 - 1
        df = df.drop(['%s_rank' % col_name, '%s' % col_name, 'count'], axis=1)
    df = df.fillna(0)
    return df

with open(input_path, 'rb') as f:
    df = pd.read_parquet(f)
df = df.rename(columns={'mret':'ret'})
# Fill NaN with Median then 0; Then standardize data
df = df.fillna(df.groupby('month').transform('median'))
df = df.fillna(0)
df = df.sort_values(by=['month', 'stkcd']).reset_index(drop=True)
df = standardize(df)

df.insert(0, 'year', pd.to_datetime(df['month'], format='%Y-%m').dt.year)
df = df[(df['year'] >= 1991)]
col_names = df.columns.values.tolist()
list_to_remove = ['stkcd', 'ret', 'year', 'month']
x_col_names = list(set(col_names).difference(set(list_to_remove)))

param_grid, param_collection = model_choose(model)
test_result, test_sr = rolling(df, method=model, x_col=x_col_names, param_space= param_grid,
                               train_start=train_start_year, train_year=train_year_number, val_year=val_year_number,
                               test_year=test_year_number)
print(f'{train_start_year}, {train_year_number+val_year_number+test_year_number} years result\n'
      'Model: ' + model)
print(param_collection)
a, b, c, d, e = cal_sr(test_sr)
print(f'Equal_Weight: r2_score:{e}, pred_mean:{a}\n'
      f'avg_mean:{b}, avg_std:{c}, avg_sr:{d}')

feather.write_feather(test_result, output_path + '%s_result_yearly.feather' % model)
feather.write_feather(test_sr, output_path + '/home/suyang/%s_result_stocks.feather' % model)
