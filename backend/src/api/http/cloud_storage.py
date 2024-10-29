import io
from typing import List

from fastapi import APIRouter, File, UploadFile, Depends

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.services import YandexStorageClient

router = APIRouter(
    prefix="/cloud-storage",
    tags=["Cloud Storage"],
)


@router.post("/upload-files")
@inject
async def upload_files(
    yandex_storage_client: YandexStorageClient = Depends(Provide[Container.yandex_storage_client]),
    files: List[UploadFile] = File(...),
) -> List[str]:
    file_urls = []
    for file in files:
        content = await file.read()
        file_like_object = io.BytesIO(content)
        file_urls.append(await yandex_storage_client.upload_file(file_like_object, file.filename))

    return file_urls
