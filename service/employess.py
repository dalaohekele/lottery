import random
from utils.excel import ExcelUtils


# 随机选取员工
def random_employees(lists, nums):
    employees_list = random.sample(lists, nums)
    return employees_list


# 已获奖的员工不能再抽奖
def del_employees(list_employees):
    utils = ExcelUtils()
    list_had_lottery = utils.get_cell_row(list_employees)
    try:
        utils.delete_row(list_had_lottery)
    except Exception as e:
        print("删除数据失败 :{}".format(e))
