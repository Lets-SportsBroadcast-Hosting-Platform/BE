from fastapi.routing import APIRoute

from routes.mainpage.route import crawling_schdule, espots_crawling_schdule


sports_schdule_route = APIRoute(
    path="/sports_schdule", endpoint=crawling_schdule, methods=["POST"]
)

esports_schdule_route = APIRoute(
    path = "/e-sports_schdule", endpoint = espots_crawling_schdule, methods=["POST"]
)