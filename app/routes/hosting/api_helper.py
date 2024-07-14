import io
from datetime import datetime
from typing import List

from database import _s3, settings
from database.search_query import query_response, update_response, delete_response
from fastapi import HTTPException, UploadFile
from models.hosting_table import HostingModel
from models.store_table import StoreModel
from PIL import Image
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def s3_upload_issue(folder: str, photos: List[UploadFile]):
    print(photos)
    index = 0
    if _s3.create_folder(_s3.bucket_name, folder):
        for photo in photos:
            image_data = await photo.read()
            image = Image.open(io.BytesIO(image_data))
            print(image.mode)
            rgb_image = image
            if image.mode in ("RGBA", "RGBX", "LA", "P", "PA"):
                rgb_image = image.convert("RGB")
                
            # 리사이즈와 품질 조정을 통한 이미지 크기 조정
            max_size = (1024, 1024)
            rgb_image.thumbnail(max_size)
            output = io.BytesIO()
            quality = 80

            while True:
                output.seek(0)
                rgb_image.save(output, format="JPEG", quality=quality, optimize=True)
                size = output.tell()
                if size <= 1_000_000:  # 1MB 이하인지 확인
                    break
                quality -= 5  # 품질을 낮추어 재시도
                if quality < 10:
                    break  # 너무 낮은 품질을 피하기 위해 중단

            output.seek(0)
            _s3.upload_file_in_chunks(
                photo=output,
                bucket_name=_s3.bucket_name,
                object_name=f"{folder}/{index}",
            )
            print(f"https://s3.ap-northeast-2.amazonaws.com/letsapp.store/{folder}/{index}")
            index += 1
        return True
    else:
        return False


# s3 사업자 번호를 기준으로 폴더를 만들고 이미지를 청크화해서 업로드하는 함수
async def s3_upload(folder: str, photos: List[UploadFile]):
    print(photos)
    try:
        if _s3.create_folder(_s3.bucket_name, folder):
            for file_no in range(len(photos)):
                image_data = await photos[file_no].read()
                image = Image.open(io.BytesIO(image_data))
                print(image.mode)
                rgb_image = image
                if image.mode in ("RGBA", "RGBX", "LA", "P", "PA"):
                    rgb_image = image.convert("RGB")
                output = io.BytesIO()
                rgb_image.save(output, format="JPEG", quality=80, optimize=True)
                output.seek(0)
                _s3.upload_file_in_chunks(
                    photo=output,
                    bucket_name=_s3.bucket_name,
                    object_name=f"{folder}/{file_no}",
                )
            return True
        else:
            return False
    except Exception as e:
        error = f"An error occurred: {e}"
        return error

# Hosting 테이블에 insert 하는 함수 CQRS : Create
"""async def insert_hosting_table(hostingModel: HostinginsertModel, db: AsyncSession) -> bool:
    try:
        hostings = HostingModel(
            hosting_name=hostingModel.hosting_name,
            business_no=hostingModel.business_no,
            introduce=hostingModel.introduce,
            current_personnel=hostingModel.current_personnel,
            max_personnel=hostingModel.max_personnel,
            age_group_start=hostingModel.age_group_start,
            hosting_date=hostingModel.hosting_date
        )
        return True
    except:
        raise HTTPException(status_code=200, detail=400)"""


# Hosting 테이블에서 사업자번호로 Read 하는 함수 CQRS : Read
async def read_hosting_tables(business_no: int, status: bool, db: AsyncSession) -> HostingModel:
    diff_status = not status
    _query = select(HostingModel).where(
        HostingModel.business_no == business_no,
        HostingModel.active_state == status,
        HostingModel.delete_state == diff_status,
        HostingModel.current_personnel < HostingModel.max_personnel,
    ).order_by(HostingModel.update_time.desc())
    responses = await query_response(_query, db)
    if responses:
        hosting_list = []
        # 객체의 컬럼 값을 가져오기
        for response in responses:
            # response = response[0]
            hosting_list.append(
                {
                    "hosting_id": response.hosting_id,
                    "hosting_name": response.hosting_name,
                    "introduce": response.introduce,
                    "current_personnel": response.current_personnel,
                    "max_personnel": response.max_personnel,
                    "age_group_min": response.age_group_min,
                    "age_group_max": response.age_group_max,
                    "hosting_date": response.hosting_date,
                }
            )
        return hosting_list
    else:
        return False


def make_hosting_data(data: dict, business_no:int, update: bool):
    print(data)
    if not update:
        hosting_data = HostingModel(
            hosting_name=data.get("hosting_name"),
            business_no = business_no,
            introduce=data.get("introduce"),
            max_personnel=data.get("max_personnel"),
            age_group_min=data.get("age_group_min"),
            age_group_max=data.get("age_group_max"),
            hosting_date=data.get("hosting_date"),
            create_time=datetime.now(),
        )
    else:
        hosting_data = HostingModel(
            hosting_name=data.get("hosting_name"),
            business_no = business_no,
            introduce=data.get("introduce"),
            max_personnel=data.get("max_personnel"),
            age_group_min=data.get("age_group_min"),
            age_group_max=data.get("age_group_max"),
        )
    return hosting_data


# Hosting 테이블에서 hosting_id로 Read 하는 함수 CQRS : Read
async def read_hosting_table(hosting_id: str, db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.hosting_id == hosting_id,
        HostingModel.active_state == True,
        HostingModel.delete_state == False,
    )
    response = await query_response(_query, db)
    print(response)
    if response:
        response = response[0]
        print(response.business_no)
        _query_store = select(StoreModel).where(StoreModel.business_no == response.business_no)
        response_store = await query_response(_query_store, db)
        if response_store:
            response_store = response_store[0]
            hosting_list = {
                "hosting_id": response.hosting_id,
                "hosting_name": response.hosting_name,
                "business_no": response.business_no,
                "introduce": response.introduce,
                "current_personnel": response.current_personnel,
                "max_personnel": response.max_personnel,
                "age_group_min": response.age_group_min,
                "age_group_max": response.age_group_max,
                "hosting_date": response.hosting_date,
                "store_image_url": response_store.store_image_url,
                "store_image_count": response_store.store_image_count,
                "screen_size": response_store.screen_size,
                "store_number": response_store.store_number,
                "store_name": response_store.store_name,
                "store_address": response_store.store_address,
                "store_road_address": response_store.store_road_address,
            }
            return hosting_list
    else:
        raise HTTPException(status_code=200, detail=400)


async def delete_hosting_table(hosting_id: int, db: AsyncSession):
    _query = delete(HostingModel).where(HostingModel.hosting_id == hosting_id)
    return await delete_response(_query, db)


async def update_hosting_table(hosting_id: int, hostingdata: HostingModel, db: AsyncSession):
    value = {
        HostingModel.hosting_name: hostingdata.hosting_name,
        HostingModel.introduce: hostingdata.introduce,
        HostingModel.max_personnel: hostingdata.max_personnel,
        HostingModel.age_group_min: hostingdata.age_group_min,
        HostingModel.age_group_max: hostingdata.age_group_max,
    }
    _query = update(HostingModel).where(HostingModel.hosting_id == hosting_id).values(value)
    return await update_response(_query, db)


async def update_storeimage(business_no: int, image_count: int, screen_size: int, db: AsyncSession):
    value = {
        StoreModel.store_image_count: image_count,
        StoreModel.store_image_url: f"https://s3.ap-northeast-2.amazonaws.com/letsapp.store/{business_no}/",
        StoreModel.screen_size: screen_size,
    }
    _query = update(StoreModel).where(StoreModel.business_no == business_no).values(value)

    return await update_response(_query, db)

async def insert_certification_number(certification_number:str, db: AsyncSession)
    query = insert()