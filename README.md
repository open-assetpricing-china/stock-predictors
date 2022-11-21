
###  Open-assetpricing-china

#### Stock-predictors

* Get the codes:
 
> $ git clone https://github.com/open-assetpricing-china/stock-predictors.git

<!--* View docs:

> documentation is now at [Read The Docs](https://stock-predictors.readthedocs.io/en/latest/) 
> or just click https://stock-predictors.readthedocs.io/en/latest/ -->

* Directory tree:

> ├─codes    
> │  ├─main.py  
> │  ├─parammeter.xml  
> │  ├─predictors  
> │  ├─utils  
> ├─data    
> │  ├─download_data       
> │  ├─build_data   
> │  └─risk_free_return  
> └─output  
>　├─test_1  
>　　    ├─factor_model  
>　　    ├─portfolio_regression  
>　　    ├─portfolio_regression_rolling  
>　　    ├─portfolio_ret 　　    
>　　├─predictors_wash    
>　　    └─predictors  

* Usage:
> 1. Running the codes:
>> $ python [./codes/main.py](./codes/main.py)
>> [./codes/parameter.xml](./codes/parameter.xml) contains the control parameters.    
> 2. Input files:
>> all input files are in the path ./data/  
>>>   ├─data      
>>>　　　├─download_data      
>>>　　　├─build_data      
>>>　　　└─risk_free_return     
>>> (a) Download csmar_master.sas7bdat from [WRDS](https://wrds-www.wharton.upenn.edu/) to the local path ['./data/download_data/'](./data/download_data/). 
>>>   
>>> (b) Download csmar_t_mnth.sas7bdat from [WRDS](https://wrds-www.wharton.upenn.edu/) to the local path ['./data/download_data/'](./data/download_data/).    
>>>
>>> (c) Download csmar_t_week.sas7bdat from [WRDS](https://wrds-www.wharton.upenn.edu/) to the local path ['./data/download_data/'](./data/download_data/). 
>>>
>>> (d) Download csmar_t_dalyr.sas7bdat from [WRDS](https://wrds-www.wharton.upenn.edu/) to the local path ['./data/download_data/'](./data/download_data/). 
>>>
>>> (e) Download csmar_t_co.sas7bdat from [WRDS](https://wrds-www.wharton.upenn.edu/) to the local path ['./data/download_data/'](./data/download_data/). 
>>>
>>> (f) ['./data/build_data/'](./data/build_data/) includes a panel data 'basic_monthly_data.parquet', which is the merging result of
>>>   csmar_master.sas7bdat, csmar_t_mnth.sas7bdat, and csmar_t_co when running " $ python [./codes/main.py](./codes/main.py)".
>>>
>>> (g) ['./data/build_data/'](./data/build_data/) includes a panel data 'basic_weekly_data.parquet', which is generated
>>> through function <build_data(parameter=parameter)> when running " $ python [./codes/main.py](./codes/main.py)" .
>>>
>>> (h) ['./data/build_data/'](./data/build_data/) includes a panel data 'basic_daily_data.parquet', which is generated
>>> through function <build_data(parameter=parameter)> when running " $ python [./codes/main.py](./codes/main.py)" .
>>>
>>> (i) [rf.xlsx](./data/risk_free_return/rf.xlsx) in path './data/risk_free_return/' is the market risk free return.
>>>
> 3. Output files:      
>> all the results are in the path [./output/](./output/),
<!-- >> see more details in [Read The Docs](https://stock-predictors.readthedocs.io/en/latest/). -->

* Tips: 

> 1. How to add predictors 
>
>> ├─codes      
>>　　　├─predictors   
>>　　　　　├─ ass.py  
>>　　　　　└─ absacc.py 
>>
>> create a predictor_name.py follow the writing styles of examples
>> i.e. [ass.py](./codes/predictors/ass.py) and [absacc.py](./codes/predictors/absacc.py) 
<!-- >> see more details in [Read The Docs](https://stock-predictors.readthedocs.io/en/latest/) --> 
> 2. How to set control parameters:
>> ├─codes      
>>　　　├─parameter.xml           
>> Just modify the parameters according the comments in file ['parameter.xml'](./codes/parameter.xml) 

* Notes:  

> The frequency of predictors: monthly.
>
> Portfolio is constructed by buying the highest expected
return stocks (decile 10) and selling the lowest (decile 1).
>
> Predictors are scaled to range (-1, 1) by 
>function [<predictors_wash(parameter=parameter)>](./codes/main.py) .  