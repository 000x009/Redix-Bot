import boto3
import os
import io

from aiogram.types import File

class YandexStorageClient:
    def __init__(self, token: str, secret: str, bucket_name: str) -> None:
        self.session = boto3.session.Session()
        self.s3 = self.session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=token,
            aws_secret_access_key=secret
        )
        self.bucket_name = bucket_name

    async def upload_file(self, file: bytes, object_name: str) -> str:
        try:
            self.s3.upload_fileobj(file, self.bucket_name, object_name)
            url = f"https://storage.yandexcloud.net/{self.bucket_name}/{object_name}"
            return url
        except Exception as e:
            print(f"Error uploading file to Yandex Cloud S3: {e}")

    def get_file(self, object_url: str) -> bytes:
        try:
            object_key = object_url.split('https://storage.yandexcloud.net/paradox/', 1)[-1]
            print(object_key)
            response = self.s3.get_object(Bucket=self.bucket_name, Key=object_key)
            file_content = response['Body'].read()
            return file_content
        except Exception as e:
            print(f"Error getting file from Yandex Cloud S3: {e}")
