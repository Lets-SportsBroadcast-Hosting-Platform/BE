from datetime import datetime
from database import _s3, settings
from typing import List
from PIL import Image
import io
from database.search_query import query_response, update_response
from fastapi import HTTPException, UploadFile
from models.hosting_table import HostingModel
from models.store_table import StoreModel
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from .models.hosting_models import HostinginsertModel
 

# s3 사업자 번호를 기준으로 폴더를 만들고 이미지를 청크화해서 업로드하는 함수
async def s3_upload(folder: str, photos: List[UploadFile]):
    if _s3.create_folder(_s3.bucket_name, folder):
        for file_no in range(len(photos)):
            image_data = await photos[file_no].read()
            image = Image.open(io.BytesIO(image_data))
            print(image.mode)
            if image.mode in ("RGBA", "RGBX", "LA", "P", "PA"):
                rgb_image = image.convert("RGB")
            output = io.BytesIO()
            rgb_image.save(output, format="JPEG", quality=80, optimize=True)
            _s3.upload_file_in_chunks(
                photo=output,
                bucket_name=_s3.bucket_name,
                object_name=f"{folder}/{file_no}",
            )
        return True
    else:
        return False

# Hosting 테이블에 insert 하는 함수 CQRS : Create
'''async def insert_hosting_table(hostingModel: HostinginsertModel, db: AsyncSession) -> bool:
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
        raise HTTPException(status_code=200, detail=400)'''


# Hosting 테이블에서 사업자번호로 Read 하는 함수 CQRS : Read
async def read_hosting_tables(hosting_name: str, db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.business_no == hosting_name,
        HostingModel.active_state == True,
        HostingModel.delete_state == False,
    )
    responses = (await query_response(_query, db))
    if responses:
        hosting_list =[]
        # 객체의 컬럼 값을 가져오기
        for response in responses:
            #response = response[0]
            hosting_list.append({
                "hosting_id" : response.hosting_id,
                "hosting_name": response.hosting_name,
                "business_no": response.business_no,
                "introduce": response.introduce,
                "current_personnel": response.current_personnel,
                "max_personnel": response.max_personnel,
                "age_group_min": response.age_group_min,
                "age_group_max": response.age_group_max,
                "hosting_date": response.hosting_date,
            })
        return hosting_list
    else:
        raise HTTPException(status_code=200, detail=400)
    
def make_hosting_data(data: HostinginsertModel):
    hosting_data = HostingModel(
        hosting_name=data.hosting_name,
        business_no=data.business_no,
        introduce=data.introduce,
        current_personnel=data.current_personnel,
        max_personnel=data.max_personnel,
        age_group_min=data.age_group_min,
        age_group_max=data.age_group_max,
        hosting_date=data.hosting_date,
    )
    return hosting_data

# Hosting 테이블에서 hosting_id로 Read 하는 함수 CQRS : Read
async def read_hosting_table(hosting_id: str, db: AsyncSession) -> HostingModel:
    _query = select(HostingModel).where(
        HostingModel.hosting_id == hosting_id,
        HostingModel.active_state == True,
        HostingModel.delete_state == False,
    )
    response = (await query_response(_query, db))
    if response:
        response = response[0]
        _query_store = select(StoreModel).where(
            StoreModel.business_no == response.business_no
        )
        response_store = (await query_response(_query_store, db))
        if response_store:
            response_store = response_store[0]
            hosting_list={
                "hosting_id" : response.hosting_id,
                "hosting_name": response.hosting_name,
                "business_no": response.business_no,
                "introduce": response.introduce,
                "current_personnel": response.current_personnel,
                "max_personnel": response.max_personnel,
                "age_group_min": response.age_group_min,
                "age_group_max": response.age_group_max,
                "hosting_date": response.hosting_date,
                "store_image_url" : response_store.store_image_url,
                "store_image_count" : response_store.store_image_count,
                "screen_size" : response_store.screen_size
            }
            return hosting_list
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def delete_hosting_table(hosting_id: int, db: AsyncSession):
    value = {
        HostingModel.active_state : False,
        HostingModel.delete_state : True
    }
    _query = update(HostingModel).where(HostingModel.hosting_id == hosting_id).values(value)
    return await update_response(_query,db)

async def update_hosting_table(hosting_id: int, db: AsyncSession):
    value = {
        HostingModel.active_state : False,
        HostingModel.delete_state : True
    }
    _query = update(HostingModel).where(HostingModel.hosting_id == hosting_id).values(value)
    return await update_response(_query,db)

async def update_storeimage(business_no: int, image_count: int, screen_size: int, db: AsyncSession):
    value = {
        StoreModel.store_image_count : image_count,
        StoreModel.store_image_url : f"https://s3.ap-northeast-2.amazonaws.com/letsapp.store/{business_no}/",
        StoreModel.screen_size: screen_size
    }
    _query = update(StoreModel).where(StoreModel.business_no == business_no).values(value)
    return await update_response(_query,db)