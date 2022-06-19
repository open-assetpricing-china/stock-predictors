#
import importlib
import os
from codes.utils import csmar_process
#
class assemble_predictors(object):
    # 将 ../codes/predictors/ 路径下 xxx.py 文件信息进行组装,
    def __init__(self,path):
        self.path = path
    def path_files_name(self):
        a = os.listdir(self.path)
        try:
            a.remove('__pycache__')
        except:
            a = a
        a = [x[:-3] for x in a]
        return a
    def predictors_info(self):
        a = self.path_files_name()
        module_list = []
        for it in a:
            predictor_file_name = it
            fun_str = 'codes.predictors' + '.' + predictor_file_name
            module = importlib.import_module(fun_str)  # 通过 importlib.import_module 的方式导入函数
            # module = eval(fun_str) # 通过 字符串变为变量的方式导入函数, 这个方法不知为何失败
            module_list.append(module)
        module_dict = dict(zip(a, module_list))
        return module_dict
#
class csmar_columns_process(object):
    # 将 ../data/csmar/basic/csmar_basic.parquet 的 columns 进行简化
    # 只包含 csmar_trading 中的 columns 和 predictors
    def __init__(self):
        csmar_trade = csmar_process.csmar_trading()
        self.basic_columns = list(csmar_trade.columns_rename.values())
    def get_predictors(self,module_dict):
        predictor = list(module_dict.keys())
        return predictor
    def update_basic_columns(self,module_dict):
        self.basic_columns = self.basic_columns + self.get_predictors(module_dict)
#
def get_finance_index(module_dict):
    # 通过 module_dict 得到非冗余的 finance index
    fin = []
    for it in range(len(module_dict)):
        fin = fin + list(module_dict.values())[it].parameter()['relate_finance_index']
    fin = list(set(fin)) # 得到非冗余的 finance index
    return fin
def get_assemble_parameters(module_dict):
    module_list = list(module_dict.values())
    para = {}
    para['predictor'] = list(module_dict.keys())
    para['relate_finance_index'] = {}
    para['equation'] = {}
    for it in range(len(module_dict)):
        para['relate_finance_index'][list(module_dict.keys())[it]] = \
            list(module_dict.values())[it].parameter()['relate_finance_index']
        para['equation'][list(module_dict.keys())[it]] = module_list[it].equation
    return para



#=
