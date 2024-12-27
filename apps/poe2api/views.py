from flask import Blueprint, request, jsonify
import requests

bp = Blueprint('poe2api', __name__, url_prefix='/poe2api')

headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

KORURL = 'https://poe.game.daum.net/api/trade2/search/poe2'
ENGURL = 'https://www.pathofexile.com/api/trade2/search/poe2'

"""
거래소 검색할 아이템 정보를 받아서
poe2 api를 이용해 거래소 주소에 들어가는 코드를 응답
"""
@bp.route('/trade', methods=['POST'])
def get_trade_code():
  request_data = request.get_json()
  type = request_data.get('type') # 카카오/공홈 선택
  selected_league = request_data.get('selectedLeague') # 리그 종류
  selected_item = request_data.get('selectedItem') # 선택한 아이템
  selected_filters = request_data.get('filters') # 선택한 아이템
  selected_stats = request_data.get('stats') # 선택한 아이템 옵션들

  print(selected_stats)

  url = f'{ENGURL}/{selected_league}' # 코드 발급용 요청 주소

  if type == 'kor':
    url = f'{KORURL}/{selected_league}'

  payload = make_trade_search_payload(selected_item)

  if selected_filters is not None:
    payload['query']['filters'] = selected_filters

  if selected_stats is not None:
    payload['query']['stats'] = selected_stats

  # return jsonify(payload) # 아이템, 필터요청까지는 잘되는거 확인

  # POST 요청 보내기
  response = requests.post(url, json=payload, headers=headers)

  # 응답 확인
  if response.status_code == 200:
    # 응답 데이터를 JSON으로 파싱
    response_data = response.json()
    search_id = response_data.get("id")

  return jsonify(search_id)

def make_trade_search_payload(selected_item):
  payload = {
    "query": {
      "status": {
        "option": "online"
      },
      "stats": [
        {
          "type": "and",
          "filters": []
        }
      ]
    },
    "sort": {
      "price": "asc"
    }
  }

  # selected_item이 None인 경우 기본 payload 반환
  if selected_item is None:
      return payload

  # 'type' 키가 있는 경우 payload에 추가
  if 'type' in selected_item:
    payload['query']['type'] = selected_item['type']

  # 'name' 키가 있는 경우 payload에 추가
  if 'name' in selected_item:
    payload['query']['name'] = selected_item['name']

  return payload

