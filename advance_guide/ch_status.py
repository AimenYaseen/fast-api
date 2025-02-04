"""
Set Custom Header, Cookies and Status Code
"""
from fastapi import FastAPI, Response, status

app = FastAPI()

tasks = {"foo": "Listen to the Bar Fighters"}


@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
        response.headers["X-Cat-Dog"] = "alone in the world"
        response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return tasks[task_id]
