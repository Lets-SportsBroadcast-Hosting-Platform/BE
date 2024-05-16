import httpx
import json
from datetime import datetime
import calendar
from fastapi import HTTPException
datedict = {0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'}

KBO_game_schdule = {
    'games':[
    ]
}

#date에 해당하는 요일을 반환하는 함수
def weekDay(date):
    datetime_date = datetime.strptime(date, '%Y-%m-%d')
    result = datedict[datetime_date.weekday()]
    return result

#크롤링정보 URL로 부터 get 요청
async def tt(url):
    async with httpx.AsyncClient(http2=True) as client:      
        response = await client.get(url)
        if response.status_code == 200:
            return json.loads(response.text)

async def make_url(upperCategoryId, categoryId):
    year = datetime.now().year
    month = datetime.now().month
    
    days_in_month = calendar.monthrange(year, month)[1]
    url =f"https://api-gw.sports.naver.com/schedule/games?fields=basic%2CsuperCategoryId%2CcategoryName%2Cstadium%2CstatusNum%2CgameOnAir%2ChasVideo%2Ctitle%2CspecialMatchInfo%2CroundCode%2CseriesOutcome%2CseriesGameNo%2ChomeStarterName%2CawayStarterName%2CwinPitcherName%2ClosePitcherName%2ChomeCurrentPitcherName%2CawayCurrentPitcherName%2CbroadChannel&upperCategoryId={upperCategoryId}&categoryId={categoryId}&fromDate=2024-{month:02}-01&toDate=2024-{month:02}-{days_in_month}&roundCodes&size=500"
    return url

async def crawling_schdule(upperCategoryId: str, categoryId: str):
    #crawling url
    url = await make_url(upperCategoryId, categoryId)

    #해당 url로 부터 데이터 받아오기
    data = await tt(url)
    #data에 포함된 games값 저장
    if data:
        games = data.get('result').get('games')

        #각각의 game KBO_game_schdule dic에 저장
        for game in games:

            date, time = game.get('gameDateTime').split('T') #2024-05-31T18:30:00 -> date = '2024-05-31' / time = '18:30:00'
            weekname = weekDay(date) # 2024-05-31 -> 금
            date = date.replace('-', '')# 2024-05-31 -> date = 20240531
            hour, minute, _ = time.split(':') # 18:30:00 -> hour = 18 / minute = 30


            KBO_game_schdule['games'].append(
                {
                'date':date,
                'time':f'{hour}{minute}',
                'weekDay': weekname,
                'awayTeamName':game.get('awayTeamName'),
                'awayTeamEmblemUrl':game.get('awayTeamEmblemUrl'),
                'homeTeamName':game.get('homeTeamName'),
                'homeTeamEmblemUrl':game.get('homeTeamEmblemUrl')
                }
            )
        return KBO_game_schdule
    else:
        raise HTTPException(status_code=200, detail=400)
        