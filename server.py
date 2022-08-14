from datetime import datetime, timezone
from email.policy import HTTP
from time import timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import  List,Dict
import json
import os.path

class Task(BaseModel):
    name: str
    description: str | None = ""
    status: str | None = "incomplete"
    creation_time : datetime = datetime.now()
    username : str
    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: str
        }
    def dict(self,**kwargs):
        standard_dict =  super().dict(**kwargs)
        standard_dict["creation_time"] = str(standard_dict["creation_time"])
        return standard_dict

class Users(BaseModel):
    login: str
    password: str
    def dict(self,**kwargs):
        standard_dict =  super().dict(**kwargs)
        return standard_dict

config = json.load(open("config.json", "r"))

app = FastAPI()


@app.on_event("startup")
async def app_init():
    # user file initialization
    if not os.path.isfile("users.json"):
        with open("users.json", "w") as users_file:
            json.dump([], users_file)



@app.get("/tasks")
async def get_tasks(username: str):
    json_tasks = json.load(open("tasks.json"))
    return json_tasks

@app.post("/registration")
async def create_new_user(user: Users):
    ex_users = json.load(open("users.json", "r"))
    for existed_user in ex_users:
        if user.login == existed_user["login"]:
            raise HTTPException(409,f"Username already exists. Choose another one.")
    ex_users.append(user.dict())
    json.dump(ex_users, open("users.json", "w"))
    return "OK"
                
@app.post("/task")
async def post_task(task: Task, user: Users):
    pass
    # tasks.append(task)
    # dict_tasks = [task.dict() for task in tasks]
    # with open("tasks.json","w") as tasks_file:
    #     tasks_file.write(json.dumps(dict_tasks))
    # return dict_tasks

@app.put("/task")
async def update_task(task: Task):
    pass

# @app.delete("/task")
# async def delete_task(task: Task):
#     tasks.remove(task)
#     dict_tasks = [task.dict() for task in tasks]
#     with open("tasks.json","w") as tasks_file:
#         tasks_file.write(json.dumps(dict_tasks))
#     return dict_tasks
    
    
    