import calendar
import json
from datetime import datetime, timedelta

import httpx
from fastapi import HTTPException
from database import KST, now
datedict = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}


# date에 해당하는 요일을 반환하는 함수
async def weekDay(date):
    datetime_date = datetime.strptime(date, "%Y-%m-%d")
    result = datedict[datetime_date.weekday()]
    return result

# esports startdate값이 milliseconds값으로 오기때문에 변환하는 함수 271115456500->2015-05-03 18:30
async def change_date(timestamp_ms):
    # milliseconds -> seconds
    timestamp_s = timestamp_ms / 1000
    # timestamp 생성
    date_time = datetime.utcfromtimestamp(timestamp_s)
    # 2024-05-03 12:30으로 변환
    kst_date_time = date_time + timedelta(hours=9)
    formatted_date_time = kst_date_time.strftime("%Y-%m-%d %H:%M")
    return formatted_date_time


# 크롤링정보 URL로 부터 get 요청
async def get_crawling_info(url):
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise HTTPException(status_code=200, detail=400)


async def make_url(upperCategoryId, categoryId):
    today = KST.localize(now).today()
    today_plus_31 = (today + timedelta(days=31)).strftime("%Y-%m-%d")

    url = f"https://api-gw.sports.naver.com/schedule/games?fields=basic%2CsuperCategoryId%2CcategoryName%2Cstadium%2CstatusNum%2CgameOnAir%2ChasVideo%2Ctitle%2CspecialMatchInfo%2CroundCode%2CseriesOutcome%2CseriesGameNo%2ChomeStarterName%2CawayStarterName%2CwinPitcherName%2ClosePitcherName%2ChomeCurrentPitcherName%2CawayCurrentPitcherName%2CbroadChannel&upperCategoryId={upperCategoryId}&categoryId={categoryId}&fromDate={today.strftime('%Y-%m-%d')}&toDate={today_plus_31}&roundCodes&size=500"
    return url


async def make_url_esports(esportsId):
    year = KST.localize(now).year
    month = KST.localize(now).month + 1
    url = f"https://esports-api.game.naver.com/service/v2/schedule/month?month={year}-{month:02}&topLeagueId={esportsId}&relay=false"
    return url

async def sorted_schedule(game_schedule:dict):
    sorted_games = sorted(game_schedule.get("games"), key=lambda x: (x["date"], x["time"]))
    game_schedule["games"] = [game for game in sorted_games]
    return game_schedule