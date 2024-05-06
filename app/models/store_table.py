import re
from typing import Optional

from database import settings
from pydantic import BaseModel


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


# 지도에 없는 가게 정보 추가 클래스
class Add_New_StoreInfo(BaseModel):
    place_name: str = None
    address_name: str = None
    road_address_name: str = None
    category_group_name: str = None
    phone: str = None

    def __init__(
        self,
        place_name: str,
        address_name: str,
        road_address_name: str,
        category_group_name: str,
        phone: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.place_name = place_name
        self.address_name = address_name
        self.road_address_name = road_address_name
        self.category_group_name = category_group_name
        self.phone = phone


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
