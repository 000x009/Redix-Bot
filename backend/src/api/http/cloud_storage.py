import io
from typing import List

from fastapi import APIRouter, File, UploadFile

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.services import YandexStorageClient

router = APIRouter(
    prefix="/cloud-storage",
    tags=["Cloud Storage"],
    route_class=DishkaRoute,
)


@router.post("/upload-files")
async def upload_files(
    yandex_storage_client: FromDishka[YandexStorageClient],
    files: List[UploadFile] = File(...),
) -> List[str]:
    file_urls = []
    for file in files:
        content = await file.read()
        file_like_object = io.BytesIO(content)
        file_urls.append(await yandex_storage_client.upload_file(file_like_object, file.filename))

    return file_urls
