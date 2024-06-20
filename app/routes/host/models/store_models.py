from pydantic import BaseModel

class StoreUpdateModel(BaseModel):
    store_name: str
    store_address: str
    store_road_address: str
    store_number: str

class StoreinsertModel(BaseModel):
    business_no: int
    store_name: str
    store_address: str
    store_road_address: str
    store_category: str
    store_number: str
    alarm: bool