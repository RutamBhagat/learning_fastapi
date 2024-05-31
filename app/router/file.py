import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse


router = APIRouter(prefix="/file", tags=["file"])


@router.post("/file")
async def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines": lines}


@router.post("/upload-file")
async def upload_file(upload_file: UploadFile = File(...)):
    path = f"app/files/{upload_file.filename}"
    with open(path, "wb") as buffer:
        contents = await upload_file.read()  # Wait for the coroutine to complete
        buffer.write(contents)  # Write the contents to the buffer
    return {
        "filename": upload_file.filename,
        "type": upload_file.content_type,
    }


@router.get("/download/{name}", response_class=FileResponse)
async def download_file(name: str):
    path = f"app/files/{name}"
    return path
