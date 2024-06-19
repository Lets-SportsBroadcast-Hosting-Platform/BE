import re
from typing import List, Optional
from datetime import datetime
from database import settings
from models import Base
from pydantic import BaseModel
from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


# store 테이블
class StoreModel(Base):
    __tablename__ = "stores"
 
    business_no: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    id : Mapped[str] = mapped_column(nullable=False)
    store_name: Mapped[str] = mapped_column(nullable=False)
    store_address: Mapped[str] = mapped_column(nullable=False)
    store_road_address: Mapped[str] = mapped_column(nullable=False)
    store_category: Mapped[str] = mapped_column(nullable=True)
    store_number: Mapped[str] = mapped_column(nullable=True)
    store_image_url: Mapped[str] = mapped_column(nullable=True)
    store_image_count: Mapped[int] = mapped_column(nullable=True)
    screen_size: Mapped[int] = mapped_column(nullable=True)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    delete_state: Mapped[bool] = mapped_column(nullable=False, default=False)


# 사업자 인증번호 클래스
class Auth_Business_Registration_Number(BaseModel):
    b_no: list[str] = None
    params: dict = None

    def __init__(self, b_no: str, **kwargs):
        super().__init__(**kwargs)
        self.b_no = [b_no.replace("-", "")]

    def __json__(self):
        return self.model_dump_json()

    def __params__(self):
        self.params = {"serviceKey": settings.BUSSINESS_SERVICE_KEY, "return_type": "JSON"}
        return self.params


# api에서 받아온 가게 정보 클래스
class storeData(BaseModel):
    stores: Optional[list] = None

    def __init__(self, stores: list, provider: str, **kwargs):
        super().__init__(**kwargs)
        if provider.lower() == "kakao":
            self.stores = [
                {
                    "place_name": data.get("place_name"),
                    "address_name": data.get("address_name"),
                    "road_address_name": data.get("road_address_name"),
                    "category_group_name": data.get("category_group_name"),
                    "phone": data.get("phone"),
                }
                for data in stores
            ]
        elif provider.lower() == "naver":
            self.stores = [
                {
                    "place_name": re.sub(r"<.*?>", "", data.get("title")),
                    "address_name": data.get("address"),
                    "road_address_name": data.get("roadAddress"),
                    "category_group_name": re.sub(r".*?>([^>]+)$", r"\1", data.get("category")),
                    "phone": data.get("telephone"),
                }
                for data in stores
            ]
        else:
            self.stores = [
                {
                    "address_name": data.get("address").get("address_name"),
                    "road_address_name": data.get("road_address").get("address_name"),
                }
                for data in stores
            ]
    
