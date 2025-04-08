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

    # 지수 변화에 대한 색상과 상태를 확인하는 함수
    def check_trend(index_element):
        if index_element:
            trend = index_element.find_next("span", class_="fluctuate")  # 'fluctuate' 클래스를 가진 span
            if trend:
                if "up" in trend["class"]:  # 상승
                    return "상향"
                elif "down" in trend["class"]:  # 하락
                    return "하향"
        return "변화 없음"

    # 코스피 지수 정보 추출
    kospi_index = soup.select_one("span#KOSPI_now")
    kospi_trend = check_trend(kospi_index)
    if kospi_index:
        print(f"현재 코스피 지수: {kospi_index.text} ({kospi_trend})")
    else:
        print("코스피 지수 정보를 찾을 수 없습니다.")

    # # 코스피200 지수 정보 추출
    # kospi200_index = soup.select_one("span#KOSPI200_now")
    # kospi200_trend = check_trend(kospi200_index)
    # if kospi200_index:
    #     print(f"현재 코스피200 지수: {kospi200_index.text} ({kospi200_trend})")
    # else:
    #     print("코스피200 지수 정보를 찾을 수 없습니다.")

    # 코스닥 지수 정보 추출
    kosdaq_index = soup.select_one("span#KOSDAQ_now")
    kosdaq_trend = check_trend(kosdaq_index)
    if kosdaq_index:
        print(f"현재 코스닥 지수: {kosdaq_index.text} ({kosdaq_trend})")
    else:
        print("코스닥 지수 정보를 찾을 수 없습니다.")

else:
    print("웹페이지를 가져올 수 없습니다. 상태 코드:", response.status_code)
