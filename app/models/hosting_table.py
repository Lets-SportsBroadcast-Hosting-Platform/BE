from datetime import datetime

from models import Base
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


# store 테이블
class HostingModel(Base):
    __tablename__ = "Hosting"

    hosting_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    hosting_name: Mapped[str] = mapped_column(nullable=False)
    business_no: Mapped[int] = mapped_column(nullable=False)
    introduce: Mapped[str] = mapped_column(nullable=False)
    cur_personnel: Mapped[int] = mapped_column(nullable=False, default=0)
    max_personnel: Mapped[int] = mapped_column(nullable=False)
    age_group_start: Mapped[int] = mapped_column(nullable=False, default=0)
    age_group_end: Mapped[int] = mapped_column(nullable=False)
    game_start_date: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    active_state: Mapped[bool] = mapped_column(nullable=False, default=True)
    delete_state: Mapped[bool] = mapped_column(nullable=False, default=False)


# 클라이언트에서 요청받은 데이터
class HostingData(BaseModel):
    hosting_name: str = None
    business_no: int = None
    introduce: str = None
    cur_personnel: int = None
    max_personnel: int = None
    age_group_start: int = None
    age_group_end: int = None
    game_start_date: datetime = None

    def to_HostingModel(self):
        return HostingModel(
            hosting_name=self.hosting_name,
            business_no=self.business_no,
            introduce=self.introduce,
            cur_personnel=self.cur_personnel,
            max_personnel=self.max_personnel,
            age_group_start=self.age_group_start,
            age_group_end=self.age_group_end,
            game_start_date=self.game_start_date,
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
