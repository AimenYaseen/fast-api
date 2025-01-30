from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# add a static folder which will hold static data of application
app.mount("/static", StaticFiles(directory="static"), name="static")
