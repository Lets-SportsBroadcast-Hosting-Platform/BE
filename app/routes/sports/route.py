import json

import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException, status
from models.sports_response import KBO_TokenResponse


async def kbo_datacrawl(token: KBO_TokenResponse):
    print("토큰 옴", token.model_dump(), type(token.model_dump()))
    url = "https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList"
    date_index = (0, 1, 2, 5, 7)  # 날짜가 있는 인덱스
    non_date_index = (0, 1, 4, 6)
    game_list = {}
    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.post(url, data=token.model_dump())
            if response.status_code == 200:
                response = json.loads((response).text)
            else:
                raise ValueError("응답이 오지 않았습니다.")
            for game in response.get("rows"):
                game_contents = game.get("row")
                if not game_contents:
                    continue
                if len(game_contents) == 9:
                    day, schedule = kbo_soup_parsing(*[game_contents[v] for v in date_index])
                    game_list[day] = [schedule]
                else:
                    data = [None] + [game_contents[v] for v in non_date_index]
                    schedule = kbo_soup_parsing(*data)
                    game_list[day].append(schedule)
            return {"schedule": game_list}
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# kbo 크롤링 날짜 포맷 변경 함수
def kbo_date_formatting(words: str) -> str:
    return words.split("(")[0].replace(".", "-")


# kbo 크롤링 팀, 점수 추출 함수
def kbo_team_and_score_formmating(words: str) -> tuple:
    html_content = BeautifulSoup(words, "html.parser")
    # 팀 이름 추출
    team_names = [
        span.get_text()
        for span in html_content.find_all("span", attrs={"class": False})
        if span.get_text() != "vs"
    ]
    # 점수 추출
    scores = [span.get_text() for span in html_content.find_all("span", {"class": ["win", "lose"]})]
    return (team_names, scores)


def kbo_soup_parsing(_date: str, _time: str, _game: str, _tv: dict, _stadium: dict):
    time = BeautifulSoup(_time.get("Text"), "html.parser").find("b").get_text()
    game = kbo_team_and_score_formmating(_game.get("Text"))
    tv = _tv.get("Text")
    stadium = _stadium.get("Text")
    if _date:
        date = kbo_date_formatting(_date.get("Text"))
        return date, (time, game, tv, stadium)
    else:
        return (time, game, tv, stadium)
