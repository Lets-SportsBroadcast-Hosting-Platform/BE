import calendar
import json
from datetime import datetime, timedelta

import httpx
from fastapi import HTTPException

datedict = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}


# date에 해당하는 요일을 반환하는 함수
def weekDay(date):
    datetime_date = datetime.strptime(date, "%Y-%m-%d")
    result = datedict[datetime_date.weekday()]
    return result

# esports startdate값이 milliseconds값으로 오기때문에 변환하는 함수 271115456500->2015-05-03 18:30
def change_date(timestamp_ms):
    # milliseconds -> seconds
    timestamp_s = timestamp_ms / 1000
    # timestamp 생성
    date_time = datetime.utcfromtimestamp(timestamp_s)
    # 2024-05-03 12:30으로 변환
    kst_date_time = date_time + timedelta(hours=9)
    formatted_date_time = kst_date_time.strftime("%Y-%m-%d %H:%M")
    return formatted_date_time


# 크롤링정보 URL로 부터 get 요청
async def tt(url):
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise HTTPException(status_code=200, detail=400)


def make_url(upperCategoryId, categoryId):
    year = datetime.now().year
    month = datetime.now().month + 1

    days_in_month = calendar.monthrange(year, month)[1]
    url = f"https://api-gw.sports.naver.com/schedule/games?fields=basic%2CsuperCategoryId%2CcategoryName%2Cstadium%2CstatusNum%2CgameOnAir%2ChasVideo%2Ctitle%2CspecialMatchInfo%2CroundCode%2CseriesOutcome%2CseriesGameNo%2ChomeStarterName%2CawayStarterName%2CwinPitcherName%2ClosePitcherName%2ChomeCurrentPitcherName%2CawayCurrentPitcherName%2CbroadChannel&upperCategoryId={upperCategoryId}&categoryId={categoryId}&fromDate=2024-{month:02}-01&toDate=2024-{month:02}-{days_in_month}&roundCodes&size=500"
    return url


def make_url_esports(esportsId):
    year = datetime.now().year
    month = datetime.now().month + 1
    url = f"https://esports-api.game.naver.com/service/v2/schedule/month?month={year}-{month:02}&topLeagueId={esportsId}&relay=false"
    return url