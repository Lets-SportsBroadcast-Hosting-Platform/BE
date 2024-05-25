from pydantic import BaseModel
from datetime import datetime

class HostinginsertModel(BaseModel):
    hosting_name: str = None
    business_no: int = None
    introduce: str = None
    current_personnel: int = None
    max_personnel: int = None
    age_group_start: int = None
    age_group_end: int = None
    hosting_data: datetime = None
    screen_size: int