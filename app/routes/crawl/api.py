from fastapi import HTTPException
from routes.crawl.api_helper import change_date, make_url, make_url_esports, get_crawling_info, weekDay, sorted_schedule

# 축구, 야구 crawling
async def crawling_schedule(upperCategoryId: str, categoryId: str, count: int):
    first_num = (count) * 10
    last_num = (count+1) * 10

    game_schdule = {"games": []}
    if upperCategoryId != 'esports':

        # crawling url
        url = await make_url(upperCategoryId, categoryId)

        # 해당 url로 부터 데이터 받아오기
        data = await get_crawling_info(url)
        # data에 포함된 games값 저장
        if data:
            games = data.get("result").get("games")
            game_schdule["total_count"] = len(games)
            # 각각의 game sports dic에 저장
            for i in range(first_num, last_num):
                if i >= game_schdule["total_count"]:
                    break
                game = games[i]
                date, time = game.get("gameDateTime").split(
                    "T"
                )  # 2024-05-31T18:30:00 -> date = '2024-05-31' / time = '18:30:00'
                weekname = await weekDay(date)  # 2024-05-31 -> 금
                date = date.replace("-", "")  # 2024-05-31 -> date = 20240531
                hour, minute, _ = time.split(":")  # 18:30:00 -> hour = 18 / minute = 30

                game_schdule["games"].append(
                    {
                        "date": date,
                        "time": f"{hour}{minute}",
                        "weekDay": weekname,
                        "awayTeamName": game.get("awayTeamName"),
                        "awayTeamEmblemUrl": game.get("awayTeamEmblemUrl"),
                        "homeTeamName": game.get("homeTeamName"),
                        "homeTeamEmblemUrl": game.get("homeTeamEmblemUrl"),
                    }
                )
            game_schdule = await sorted_schedule(game_schdule)
            return game_schdule
        else:
            raise HTTPException(status_code=200, detail=400)
    else:
        # crawling esports url
        url = await make_url_esports(categoryId)
        print(url)
        # 해당 url로 부터 데이터 받아오기
        data = await get_crawling_info(url)
        # data에 포함된 games값 저장
        if data:
            games = data.get("content").get("matches")
            game_schdule["total_count"] = len(games)
            print(len(games))
            # 각각의 game esports dic에 저장
            for i in range(first_num, last_num):
                if i >= game_schdule["total_count"]:
                    break
                game = games[i]
                date_time = await change_date(game.get("startDate"))
                date, time = date_time.split(" ")  # 2024-05-31 18:30 -> date = '2024-05-31' / time = '18:30:00'
                weekname = await weekDay(date)  # 2024-05-31 -> 금
                date = date.replace("-", "")  # 2024-05-31 -> date = 20240531
                hour, minute = time.split(":")  # 18:30:00 -> hour = 18 / minute = 30

                game_schdule["games"].append(
                    {
                        "date": date,
                        "time": f"{hour}{minute}",
                        "weekDay": weekname,
                        "homeTeamName": game.get("homeTeam").get("nameAcronym"),
                        "homeTeamEmblemUrl": game.get("homeTeam").get("imageUrl"),
                        "awayTeamName": game.get("awayTeam").get("nameAcronym"),
                        "awayTeamEmblemUrl": game.get("awayTeam").get("imageUrl"),
                    }
                )
            game_schdule = await sorted_schedule(game_schdule)
            return game_schdule
        else:
            raise HTTPException(status_code=200, detail=400)


# esports crawling
'''async def esports_crawling_schedule(esportsId: str, count: int):

    first_num = (count) * 10
    last_num = (count+1) * 10

    game_schdule = {"games": []}
    # crawling esports url
    url = await make_url_esports(esportsId)
    print(url)
    # 해당 url로 부터 데이터 받아오기
    data = await get_crawling_info(url)
    # data에 포함된 games값 저장
    if data:
        games = data.get("content").get("matches")
        game_schdule["total_count"] = len(games)
        print(len(games))
        # 각각의 game esports dic에 저장
        for i in range(first_num, last_num):
            if i >= game_schdule["total_count"]:
                break
            game = games[i]
            date_time = await change_date(game.get("startDate"))
            date, time = date_time.split(" ")  # 2024-05-31 18:30 -> date = '2024-05-31' / time = '18:30:00'
            weekname = await weekDay(date)  # 2024-05-31 -> 금
            date = date.replace("-", "")  # 2024-05-31 -> date = 20240531
            hour, minute = time.split(":")  # 18:30:00 -> hour = 18 / minute = 30

            game_schdule["games"].append(
                {
                    "date": date,
                    "time": f"{hour}{minute}",
                    "weekDay": weekname,
                    "homeTeamName": game.get("homeTeam").get("nameAcronym"),
                    "homeTeamEmblemUrl": game.get("homeTeam").get("imageUrl"),
                    "awayTeamName": game.get("awayTeam").get("nameAcronym"),
                    "awayTeamEmblemUrl": game.get("awayTeam").get("imageUrl"),
                }
            )
        game_schdule = await sorted_schedule(game_schdule)
        return game_schdule
    else:
        raise HTTPException(status_code=200, detail=400)
'''