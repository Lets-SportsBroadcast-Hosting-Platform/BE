from fastapi.routing import APIRoute
from routes.hosting.api import make_hosting, read_hosting, read_hostings,update_image_store

# 호스팅 등록 (Create)
hosting_create_route = APIRoute(path="/make_hosting", endpoint=make_hosting, methods=["POST"])

#호스팅 읽기 - 사업자번호로 비교 호스팅 리스트(Read)
hosting_read_tables_route = APIRoute(path="/read_hostings", endpoint=read_hostings, methods=["GET"])

#호스팅 읽기 - 호스팅id로 비교(Read)
hosting_read_table_route = APIRoute(path="/read_hosting", endpoint=read_hosting, methods=["GET"])

#이미지, 스크린 사이즈 삽입
store_input_image = APIRoute(path='/insert_images', endpoint=update_image_store, methods=['POST'])