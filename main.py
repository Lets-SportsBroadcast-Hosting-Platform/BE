from fastapi import FastAPI, Request
import requests
import urllib.parse
import json
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용, 필요에 따라 변경 가능
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # 허용할 메서드 목록
    allow_headers=["*"],  # 모든 헤더 허용, 필요에 따라 변경 가능
)
KAKAO_REST_API = os.getenv("KAKAO_REST_API")
KAKAO_API_BASE_URL = 'https://dapi.kakao.com/v2/local/search/keyword.json'

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_API_BASE_URL = 'https://openapi.naver.com/v1/search/local.json'

BUSSINESS_SERVICE_KEY = os.getenv("BUSSINESS_SERVICE_KEY")
BUSSINESS_BASE_URL = f'http://api.odcloud.kr/api/nts-businessman/v1/status?'

class Storeinfo(BaseModel):
    place_name: str
    address_name: str
    road_address_name: str
    phone: str

@app.post('/host/status')
async def status(request: Request):
    data = await request.json()
    query = data.get('b_no', '')
    req_body = {
      "b_no": [
        query
      ]
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    Params = {
        'serviceKey': BUSSINESS_SERVICE_KEY,
        'return_type' : 'JSON'
    }
    result = {
        'b_status' : ''
    }
    req_body_json = json.dumps(req_body)
    response = requests.post(BUSSINESS_BASE_URL, data = req_body_json, headers = headers, params = urllib.parse.urlencode(Params))
    responseData = response.json()
    check = responseData['data'][0]['tax_type']
    if check == '국세청에 등록되지 않은 사업자등록번호입니다.':
        result['b_status'] = '0'
    else:
        result['b_status'] = '1'

    return JSONResponse(result)


@app.post('/host/detail/store/list')
async def kakao_searchlist(request:Request):
    data = await request.json()
    query = data.get('keyword', '')
    print(query)  
    header = {
        'Authorization': f'KakaoAK {KAKAO_REST_API}'
    }
    data = {
        'query': query,
        'sort': 'accuracy',
        'size' : 5
    }
    response = requests.get(url=KAKAO_API_BASE_URL, headers=header, params=urllib.parse.urlencode(data))
    response = response.json()
    store_detail = []
    for document in response['documents']:
        store_detail.append({
            'place_name':document['place_name'],
            'address_name':document['address_name'],
            'road_address_name':document['road_address_name'],
            'phone':document['phone']
        })
    return JSONResponse(store_detail)

@app.post('/host/kakao/store/list')
async def kakao_searchlist(request:Request):
    data = await request.json()
    query = data.get('keyword', '')
    print(query)  
    header = {
        'Authorization': f'KakaoAK {KAKAO_REST_API}'
    }
    data = {
        'query': query,
        'sort': 'accuracy',
        'size' : 5
    }
    response = requests.get(url=KAKAO_API_BASE_URL, headers=header, params=urllib.parse.urlencode(data))
    response = response.json()
    store_detail = []
    for document in response['documents']:
        store_detail.append({
            'place_name':document['place_name'],
            'address_name':document['address_name'],
            'road_address_name':document['road_address_name'],
            'phone':document['phone']
        })
    return JSONResponse(store_detail)

@app.post('/host/naver/store/list')
async def naver_searchlist(request:Request):
    data = await request.json()
    query = data.get('keyword', '')
    print(query)  
    header = {
        "X-Naver-Client-Id":NAVER_CLIENT_ID,
        "X-Naver-Client-Secret":NAVER_CLIENT_SECRET
    }
    data = {
        'query': query,
        'display' : 5
    }
    response = requests.get(url=NAVER_API_BASE_URL, headers=header, params=urllib.parse.urlencode(data))
    response = response.json()
    store_detail = [] 
    for item in response['items']:
        store_detail.append({
            'place_name':item['title'].replace('<b>', '').replace('</b>', ''),
            'address_name':item['address'],
            'road_address_name':item['roadAddress'],
            'phone':item['telephone']
        })
    return JSONResponse(store_detail)
    
@app.post('host/store/insert')
async def storeinsert(storeinfo: Storeinfo):
    if storeinfo:
        store = {
            'place_name':storeinfo.place_name,
            'address_name':storeinfo.address_name,
            'road_address_name':storeinfo.road_address_name,
            'phone':storeinfo.phone
        }
        print(store)
        result = {
                    'check_response':'ok'
                }
    else:
        result = {
                    'check_response': 'error'
                }
    print(result)
    return JSONResponse(result)


    

