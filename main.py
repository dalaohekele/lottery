import pymysql
from fastapi import FastAPI
from pydantic import BaseModel

from utils.excel import ExcelUtils
from service import employess
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lottery/employees")
async def get_all_employees():
    all_employees = ExcelUtils().excel_read()
    lists = []
    for member in all_employees:
        member_dict = {"name": member}
        lists.append(member_dict)
    return {"data": lists}


class Info(BaseModel):
    description: str
    name: str


@app.post("/push/lottery")
async def push_lottery(info: Info):
    db = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                         database='lottery', charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO user_info(name,description)values('%s','%s')" % (info.description, info.name.rstrip(','))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print("push error:" + e)
    db.close()
    return {"message": "push success"}


@app.get("/lottery/{id}/{nums}")
async def lottery(nums):
    all_employees = ExcelUtils().excel_read()
    employees_list = employess.random_employees(all_employees, int(nums))
    # 删除已中奖的员工
    employess.del_employees(employees_list)
    lists = []
    for member in employees_list:
        member_dict = {"name", member}
        lists.append(member_dict)
    return lists


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
