import io
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


# Setting config load
class Settings(BaseSettings):
    SERVER_SECRET_KEY: Optional[str] = None
    KAKAO_CLIENT_ID: Optional[str] = None
    KAKAO_RESTAPI_KEY: Optional[str] = None
    NAVER_CLIENT_ID: Optional[str] = None
    NAVER_SECRET_KEY: Optional[str] = None
    DATABASE_HOST: Optional[str] = None
    DATABASE_USER: Optional[str] = None
    DATABASE_PWD: Optional[str] = None
    DATABASE_NAME: Optional[str] = None
    BUSSINESS_SERVICE_KEY: Optional[str] = None
    AWS_ACCESS_KEY_ID_: Optional[str] = None
    AWS_SECRET_ACCESS_KEY_: Optional[str] = None
    REGION_NAME: Optional[str] = None
    BUCKET_NAME: Optional[str] = None

    class Config:
        env_file = ".env"


# 데이터베이스 테이블 연결하는 클래스
class conn_db:
    def __init__(self, engine_url):
        self.engine = create_async_engine(engine_url, echo=False)
        try:
            self.engine.connect()
            print("db 연결됨")
        except:
            print("연결 안됨...")

    def sessionmaker(self):
        Session = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )
        session = Session()
        return session


# s3에 연결하는 클래스
class conn_S3:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, bucket_name):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.bucket_name = bucket_name

    # s3에 폴더 생성
    def create_folder(self, bucket, folder_name: str):
        print("폴더를 생성합니다.")
        try:
            self.s3.put_object(Bucket=bucket, Key=(folder_name + "/"))
            print("폴더를 생성했습니다.")
            return True
        except ClientError as e:
            return False

    # 이미지를 청크화 해서 업로드
    def upload_file_in_chunks(
        self,
        photo: io.BytesIO,
        bucket_name: str,
        object_name: str,
        content_type="image/JPEG",
        chunk_size=5 * 1024 * 1024,
    ):
        response = self.s3.create_multipart_upload(
            Bucket=bucket_name, Key=object_name, ContentType=content_type
        )
        parts = []

        with photo as file:
            file.seek(0)
            file_size = len(file.getbuffer())
            part_number = 1
            offset = 0

            while offset < file_size:
                chunk = file.read(chunk_size)
                response_upload = self.s3.upload_part(
                    Bucket=bucket_name,
                    Key=object_name,
                    PartNumber=part_number,
                    UploadId=response["UploadId"],
                    Body=chunk,
                )
                parts.append({"PartNumber": part_number, "ETag": response_upload["ETag"]})
                offset += len(chunk)
                part_number += 1

        try:
            self.s3.complete_multipart_upload(
                Bucket=bucket_name,
                Key=object_name,
                UploadId=response["UploadId"],
                MultipartUpload={"Parts": parts},
            )
            print("이미지 업로드 성공")
        except KeyError:
            print("이미지 업로드 실패")
            # print(
            #     "Error: 'UploadId' not found in response. Multipart upload may not have been initiated."
            # )
