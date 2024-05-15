from datetime import datetime

from models import Base
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


# store 테이블
class HostingModel(Base):
    __tablename__ = "Hosting"

    hosting_name: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    business_no: Mapped[int] = mapped_column(nullable=False)
    introduce: Mapped[str] = mapped_column(nullable=False)
    cur_personnel: Mapped[int] = mapped_column(nullable=False)
    max_personnel: Mapped[int] = mapped_column(nullable=False)
    age_group_start: Mapped[int] = mapped_column(nullable=False)
    age_group_end: Mapped[int] = mapped_column(nullable=False)
    screen_size: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())


class HostingData(BaseModel):
    hosting_name: str = None
    business_no: int = None
    introduce: str = None
    cur_personnel: int = None
    max_personnel: int = None
    age_group_start: int = None
    age_group_end: int = None
    screen_size: int = None
    start_time: datetime = None

    def to_HostingModel(self):
        return HostingModel(
            hosting_name=self.hosting_name,
            business_no=self.business_no,
            introduce=self.introduce,
            cur_personnel=self.cur_personnel,
            max_personnel=self.max_personnel,
            age_group_start=self.age_group_start,
            age_group_end=self.age_group_end,
            screen_size=self.screen_size,
            start_time=self.start_time,
        )

    # def __init__(self, instance: HostingModel = None, **kwargs):
    #     super().__init__(**kwargs)
    #     self.hosting_name = instance.hosting_name
    #     self.business_no = instance.business_no
    #     self.introduce = instance.introduce
    #     self.personnel = instance.personnel
    #     self.age_group_start = instance.age_group_start
    #     self.age_group_end = instance.age_group_end
    #     self.screen_size = instance.screen_size
    #     self.start_time = instance.start_time
