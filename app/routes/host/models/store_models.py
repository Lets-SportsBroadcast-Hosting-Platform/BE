from pydantic import BaseModel

class StoreUpdateModel(BaseModel):
    store_address: str
    store_road_address: str
    store_name: str

class StoreinsertModel(BaseModel):
    business_no: int
    id: str
    store_name: str
    store_address: str
    store_road_address: str
    store_category: str
    store_number: str