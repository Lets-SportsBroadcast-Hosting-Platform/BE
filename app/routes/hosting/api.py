from database import get_db
import io
from fastapi import Depends, HTTPException, File, UploadFile
from typing import List
from database import _s3, settings
from PIL import Image
from models.hosting_table import HostingData
from routes.hosting.api_helper import (
    insert_hosting_table, 
    read_hosting_table, 
    read_hosting_tables, 
    update_hosting_table, 
    delete_hosting_table)
from routes.host.api_helper import make_store_data
from sqlalchemy.ext.asyncio import AsyncSession

# 클라이언트에서 호스팅 정보를 받아 db에 등록하는 api 함수
async def make_hosting(hostingdata: HostingData,  photos: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    store_table = make_store_data(len(photos))
    print(hostingdata.game_start_date)
    if await insert_hosting_table(hostingdata, db):
        return "호스팅 되었습니다."
    else:
        raise HTTPException(status_code=200, detail=400)


# 클라이언트에서 호스팅 id를 받아 응답하는 함수
async def read_hostings(business_no: int, db: AsyncSession = Depends(get_db)):
    result = await read_hosting_tables(business_no, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)

async def read_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await read_hosting_table(hosting_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def update_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await update_hosting_table(hosting_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)
    
async def delete_hosting(hosting_id: int, db: AsyncSession = Depends(get_db)):
    result = await delete_hosting_table(hosting_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=200, detail=400)
    

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