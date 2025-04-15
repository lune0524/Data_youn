# API 키 설정 (공공데이터포털에서 발급받은 키)
api_key = 'api_key'

# 필요한 라이브러리 임포트
import requests  # HTTP 요청을 보낼 때 사용
import json      # JSON 데이터 처리
import pandas as pd  # 데이터프레임 형태로 데이터를 처리하기 위한 라이브러리

# 결과 데이터를 저장할 리스트 초기화
lst_rows = []

# 시작 페이지 번호와 한 페이지당 데이터 수 설정
page_no = 1
page_size = 20

# 기상청 날씨 데이터 API의 기본 URL
my_url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'

# API 요청에 필요한 파라미터 설정
params = {
    'ServiceKey' : api_key,        # 인증 키
    'numOfRows' : page_size,       # 한 페이지에 가져올 데이터 수
    'pageNo' : page_no,            # 요청할 페이지 번호
    'dataType' : 'JSON',           # 응답 데이터 타입 (JSON)
    'dataCd' : 'ASOS',             # 데이터 코드 (기상관측)
    'dateCd' : 'DAY',              # 날짜 코드 (일별 데이터)
    'startDt' : '20230101',        # 조회 시작 날짜 (YYYYMMDD)
    'endDt' : '20230601',          # 조회 종료 날짜 (YYYYMMDD)
    'stnIds' : '146'               # 측정소 ID (108은 서울) , 146은 전주
}

# 페이지를 반복적으로 요청해서 모든 데이터를 가져옴
for i in range(1, 1000000):
    params['pageNo'] = i  # 현재 페이지 번호 설정
    response = requests.get(my_url, params=params, verify=False)  # API 요청 (SSL 인증 무시)
    html = json.loads(response.text)  # 응답 데이터를 JSON 형태로 파싱

    resultCode = html['response']['header']['resultCode']  # 응답 코드 확인
    if resultCode != '00':  # 정상 응답이 아니면 반복 종료
        break

    items = html['response']['body']['items']['item']  # 데이터 항목 추출
    for item in items:
        lst_rows.append(pd.Series(item))  # 각 항목을 Series로 변환하여 리스트에 추가

# 리스트에 저장된 Series들을 데이터프레임으로 결합
df = pd.concat(lst_rows, axis=1)
df = df.T  # 행/열 전환

# 결과를 CSV 파일로 저장
df.to_csv('result.csv')

# 데이터프레임 출력
print(df)
