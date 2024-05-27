from datetime import datetime

from models import Base
from pydantic import BaseModel
from sqlalchemy import func, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


# store 테이블
class HostingModel(Base):
    __tablename__ = "Hosting"

    hosting_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    hosting_name: Mapped[str] = mapped_column(nullable=False)
    business_no: Mapped[int] = mapped_column(nullable=False)
    introduce: Mapped[str] = mapped_column(nullable=False)
    current_personnel: Mapped[int] = mapped_column(nullable=False, default=0)
    max_personnel: Mapped[int] = mapped_column(nullable=False)
    age_group_min: Mapped[int] = mapped_column(nullable=False, default=0)
    age_group_max: Mapped[int] = mapped_column(nullable=False)
    hosting_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    active_state: Mapped[bool] = mapped_column(nullable=False, default=True)
    delete_state: Mapped[bool] = mapped_column(nullable=False, default=False)


# 클라이언트에서 요청받은 데이터
class HostingData(BaseModel):
    hosting_name: str = None
    business_no: int = None
    introduce: str = None
    current_personnel: int = None
    max_personnel: int = None
    age_group_min: int = None
    age_group_max: int = None
    hosting_date: datetime = None
    #screen_size: int #store테이블에 넣어야하는 데이터

    def to_HostingModel(self):
        return HostingModel(
            hosting_name=self.hosting_name,
            business_no=self.business_no,
            introduce=self.introduce,
            current_personnel=self.current_personnel,
            max_personnel=self.max_personnel,
            age_group_min=self.age_group_min,
            age_group_max=self.age_group_max,
            hosting_date=self.hosting_date
            #screen_size=self.screen_size
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
