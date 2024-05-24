from fastapi.routing import APIRoute
from routes.crawl.api import crawling_schedule, esports_crawling_schedule

sports_schedule_route = APIRoute(path="/sports", endpoint=crawling_schedule, methods=["GET"])

esports_schedule_route = APIRoute(
    path="/e_sports", endpoint=esports_crawling_schedule, methods=["GET"]
)
