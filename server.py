from datetime import datetime, timezone
from time import timezone
from fastapi import FastAPI
from pydantic import BaseModel, validator
import json

tasks = []

def convert_datetime_to_string(creation_time: datetime) -> str:
    return creation_time.strftime("%Y-%m-%dT%H:%M:%SZ'")


class Task(BaseModel):
    name: str
    description: str | None = ""
    status: str | None = "incomplete"
    creation_time : datetime = datetime.now()
    holder : str
    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: str
        }

app = FastAPI()



@app.get("/tasks")
async def get_tasks(username: str):
    json_tasks = json.load(open("tasks.json"))
    return json_tasks

@app.post("/task")
async def post_task(task: Task):
    tasks.append(task)
    dict_tasks = [task.json() for task in tasks]
    with open("tasks.json","w") as tasks_file:
        tasks_file.write(json.dumps(dict_tasks))
    return json.dump(dict_tasks, open("tasks.json","w"))

@app.put("/task")
async def update_task(task:Task):
    #smth to edit task
    task.status = str
    pass
    
    