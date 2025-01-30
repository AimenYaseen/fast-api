from typing import Annotated

from fastapi import FastAPI, BackgroundTasks, Depends

app = FastAPI()


def write_notification(message: str):
    with open("log.txt", mode="a") as file:
        file.write(message)


# Multiple Background Task
def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if not q:
        return q
    message = f"Found Query : {q}\n"
    background_tasks.add_task(write_notification, message)


@app.post("/send-notification/{email}")
async def send_notification(
        email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    content = f"Notification for {email}\n"
    background_tasks.add_task(write_notification, content)
    return {
        "message": "Notification sent in the Background!"
    }
