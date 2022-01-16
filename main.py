#  -*-  coding:utf-8 -*-
from fastapi import FastAPI
from utils.excel import ExcelUtils
from service import employess
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lottery/{id}/{nums}")
async def lottery(nums):
    lists = ExcelUtils().excel_read()
    employees_list = employess.random_employees(lists, int(nums))
    # 删除已中奖的员工
    employess.del_employees(employees_list)
    return employees_list


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
