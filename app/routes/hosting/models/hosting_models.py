from pydantic import BaseModel

from datetime import datetime

class HostinginsertModel(BaseModel):
    hosting_name: str = None
    business_no: int = None
    introduce: str = None
    current_personnel: int = None
    max_personnel: int = None
    age_group_min: int = None
    age_group_max: int = None
    hosting_date: datetime = None