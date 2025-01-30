from typing import Annotated

from fastapi import FastAPI, File, UploadFile, Form
from starlette.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_file(
        file: Annotated[bytes, File(description="A file read as bytes")]
):
    return {
        "file_size": len(file),
    }


@app.post("/upload-file/")
async def create_upload_file(
        file: UploadFile,
        files: Annotated[  # Multiple File Uploads
            list[UploadFile], File(description="Multiple files as UploadFile")
        ],
):
    return {
        "filename": file.filename,
        "filenames": [file.filename for file in files]
    }


# FILE AND FORM PARAMETERS

@app.post("/form-files/")
async def create_file(
        file: Annotated[bytes, File()],
        file_b: Annotated[UploadFile, File()],
        token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": file_b.content_type,
    }


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/upload-file/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)
