import requests
from bs4 import BeautifulSoup

# 네이버 증권 페이지 URL
url = "https://finance.naver.com/sise/"

# 헤더 추가하여 실제 브라우저 요청처럼 위장
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# requests를 이용해 웹페이지 가져오기
response = requests.get(url, headers=headers)  # 헤더를 포함하여 요청

# HTTP 상태 코드 확인
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # 코스피 지수 정보 추출
    kospi_index = soup.select_one("span#KOSPI_now")
    if kospi_index:
        print("현재 코스피 지수:", kospi_index.text)
    else:
        print("코스피 지수 정보를 찾을 수 없습니다.")

    # 코스피200 지수 정보 추출
    kospi200_index = soup.select_one("span#KOSPI200_now")  # 정확한 셀렉터로 수정
    if kospi200_index:
        print("현재 코스피200 지수:", kospi200_index.text)
    else:
        print("코스피200 지수 정보를 찾을 수 없습니다.")

    # 코스닥 지수 정보 추출
    kosdaq_index = soup.select_one("span#KOSDAQ_now")
    if kosdaq_index:
        print("현재 코스닥 지수:", kosdaq_index.text)
    else:
        print("코스닥 지수 정보를 찾을 수 없습니다.")
        

else:
    print("웹페이지를 가져올 수 없습니다. 상태 코드:", response.status_code)
