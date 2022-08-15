from datetime import datetime, timezone
from email.policy import HTTP
from time import timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import  List, Dict
import json
import os
import uuid

class Task(BaseModel):
    name: str
    description: str | None = ""
    status: str | None = "incomplete"
    creation_time : datetime = datetime.now()
    username : str
    id : str = str(uuid.uuid4())
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

config: Dict = json.load(open("config.json", "r"))

app = FastAPI()

@app.on_event("startup")
async def app_init():
    # user file initialization
    if not os.path.isfile("users.json"):
        with open("users.json", "w") as users_file:
            json.dump([], users_file)

@app.get("/tasks")
async def get_tasks(username: str):
    json_tasks = json.load(open(f"users_tasks/{username}.json", "r"))
    return json_tasks

@app.post("/registration")
async def create_new_user(user: Users):
    ex_users = json.load(open(config.get("users_path", "users.json"), "r"))
    for existed_user in ex_users:
        if user.login == existed_user["login"]:
            raise HTTPException(409,f"Username already exists. Choose another one.")
    ex_users.append(user.dict())
    json.dump(ex_users, open("users.json", "w"))
    return "OK"
                
@app.post("/task")
async def post_task(task: Task, user: Users):
    task_id = task.id
    # creating path to user's tasks file
    os.makedirs(config.get("users_tasks_path", "users_tasks"),exist_ok=True)
    # checking if the user's tasks file exists if not creating it 
    if not os.path.isfile(f"users_tasks/{user.login}.json"):
        with open(f"users_tasks/{user.login}.json", "w") as user_tasks_file:
            json.dump([], user_tasks_file)
    tasks = json.load(open(f"users_tasks/{user.login}.json", "r"))
    if tasks != []:
        if task_id != task["id"]:
            raise HTTPException(409,f"You cannot change task id.")
    tasks.append(task.dict())
    json.dump(tasks, open(f"users_tasks/{user.login}.json", "w"))
    return task
    
@app.put("/task")
async def update_task(task: Task, user: Users):
    task_uuid = task.id
    tasks = json.load(open(f"users_tasks/{user.login}.json", "r"))
    for tsk in tasks:
        if tsk["id"] == task_uuid:
            tasks.remove(tsk)
    tasks.append(task.dict())
    json.dump(tasks, open(f"users_tasks/{user.login}.json", "w"))
    return task    
    
@app.delete("/task")
async def delete_task(task: Task, user: Users):
    tasks = json.load(open(f"users_tasks/{user.login}.json", "r"))
    for tsk in tasks:
        if tsk == task:
            tasks.remove(task)
        else:
            raise HTTPException(409,f"You don't have such task. Please, try to delete your task.")
    json.dump(tasks, open(f"users_tasks/{user.login}.json", "w"))
    return f"{task} successfully deleted"
#     tasks.remove(task)
#     dict_tasks = [task.dict() for task in tasks]
#     with open("tasks.json","w") as tasks_file:
#         tasks_file.write(json.dumps(dict_tasks))
#     return dict_tasks
    
    
    