from typing import Optional

from pydantic import BaseModel


class KBO_TokenResponse(BaseModel):
    leId: Optional[int]
    srIdList: Optional[str]
    seasonId: Optional[int]
    gameMonth: Optional[str]
    teamId: Optional[str]
