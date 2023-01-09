# OpenChinaAssetPricing with Machine Learning

This is the example code for the OpenChinaAssetPricing project:
We follow the details of Gu Kelly and Xiu (2020)

### Inputs

Using the monthly_predictors.parquet (factor and return data matrix) getting from our data part

### Parameters

You might need to change default path and the model you wanna apply
You could also use a different train/validation/test splitting 
You might change the parameters of ML models in model_choose function

### Outputs

The output contains:
  A dataframe with yearly pricing results (test_result)
  A monthly pricing results for each stock (test_sr)

We print Parameters and out-of-sample equal-weighted portfolio results

### Functions

model_choose:
  Change ML model parameters

rolling:
  main function for model training

standardize:
  standardize factor data month by month (To be specific, we cross-sectionally rank all stock characteristics period-by-period and map these ranks into the [-1,1] interval following Kelly, Pruitt, and Su (2019) and Freyberger, Neuhierl, and Weber (2020))

cal_sr:
  calculate out-of-sample equal-weighted portfolio results (Sharpe ratio)


## Preparation

Python 3.9
numpy
pandas
sklearn
pyarrow


### Contact

If you have any questions or want to use the code, please contact zhaosuwu@outlook.com
