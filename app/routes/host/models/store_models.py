from pydantic import BaseModel

class StoreUpdateModel(BaseModel):
    store_address: str
    store_address_road: str
    store_name: str

class StoreinsertModel(BaseModel):
    business_no: int
    token: str
    store_name: str
    store_address: str
    store_address_road: str
    store_category: str
    store_contact_number: str