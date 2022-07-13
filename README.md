
###  Open-assetpricing-china

#### Stock-predictors

* Get the codes:
 
> $ git clone https://github.com/open-assetpricing-china/stock-predictors.git

* View docs:

> documentation is now at [Read The Docs](https://stock-predictors.readthedocs.io/en/latest/) 
> or just click https://stock-predictors.readthedocs.io/en/latest/

* Directory tree:

> ├─codes    
> │  ├─factor_model  
> │  ├─params  
> │  ├─predictors  
> │  ├─utils  
> ├─data  
> │  ├─basic  
> │  ├─csmar  
> │  │  ├─csmar_finance  
> │  │  └─csmar_trade    
> │  ├─para_file   
> │  └─rf  
> └─output  
>　　├─factor_model  
>　　├─portfolio_performance  
>　　├─portfolio_ret  
>　　└─predictors  

* Usage:
> 1. Running the codes:
>> $ python [./codes/main.py](./codes/main.py)   
> 2. Input files:
>> all input files are in the path ./data/  
>>>   ├─data      
>>>　　　├─basic      
>>>　　　├─csmar    
>>>　　　│  ├─csmar_finance    
>>>　　　│  └─csmar_trade      
>>>　　　├─para_file     
>>>　　　└─rf     
>>> (a) Download csmar_master.sas7bdat from [WRDS](https://wrds-www.wharton.upenn.edu/) to the local path ['./data/csmar/csmar_finance/'](./data/csmar/csmar_finance/). 
>>>   
>>> (b) Download csmar_t_mnth.sas7bdat from [WRDS](https://wrds-www.wharton.upenn.edu/) to the local path ['./data/csmar/csmar_trade/'](./data/csmar/csmar_trade/).    
>>>
>>> (c) ['./data/basic/'](./data/basic/) includes a panel data 'basic_data.parquet', which is the merging result of
>>>   csmar_master.sas7bdat and csmar_t_mnth.sas7bdat when running " $ python [./codes/main.py](./codes/main.py)".
>>>
>>> (d) [rf.xlsx](./data/rf/rf.xlsx) in path './data/rf/' is the market risk free return.
>>>
>>> (e) ['./data/para_file/'](./data/para_file/) includes the corresponding parameters files, which can be created by 
>>> running orders: $ python codes.params.XXX.py, where XXX.py are in the path ['./codes/params/'](./codes/params/).  
>>>  * For example, running: $ python [./codes/params/para_construct_portfolio.py](./codes/params/para_construct_portfolio.py) to update the file 
      ['para_construct_portfolio.csv'](./data/para_file/para_construct_portfolio.csv) in path ['./data/para_file/'](./data/para_file/).    
> 3. Output files:      
>> all the results are in the path [./output/](./output/),
>> see more details in [Read The Docs](https://stock-predictors.readthedocs.io/en/latest/).

* Tips: 

> 1. How to add predictors 
>
>> ├─codes      
>>　　　├─predictors   
>>　　　　　├─ ep.py  
>>　　　　　└─ market_cap.py 
>>
>> create a predictor_name.py follow the writing styles of examples
>> i.e. [ep.py](./codes/predictors/ep.py) and [market_cap.py](./codes/predictors/market_cap.py) 
>> see more details in [Read The Docs](https://stock-predictors.readthedocs.io/en/latest/) 
> 2. How to set control parameters:
>> ├─codes      
>>　　　├─params         
>>　　　　　└─ para_construct_portfolio.py   
>> ├─data          
>>　　　├─para_file     
>>　　　　　└─ para_construct_portfolio.csv   
>> Take the parameter file ['para_construct_portfolio.csv'](./data/para_file/para_construct_portfolio.csv)
>> as an example, there are two ways to reset parameters:
>>  * (a) open csv file ['para_construct_portfolio.csv'](./data/para_file/para_construct_portfolio.csv), 
 change the corresponding parameters, then save the modifies.    
>> * (b) reset the variables in python file [para_construct_portfolio.py](./codes/params/para_construct_portfolio.py),
 then running $ python [./codes/params/para_construct_portfolio.py](./codes/params/para_construct_portfolio.py).

* Notes:  
> The frequency of data: monthly.