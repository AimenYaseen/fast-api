from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow All
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # upcoming headers
    expose_headers=["*"],  # return headers
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
