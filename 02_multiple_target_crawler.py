import time

import requests
from bs4 import BeautifulSoup

# 실행 시간 측정
start = time.perf_counter()

# 크롤링을 진행할 대상 페이지 URL들
urls = [
    "https://hoshi2710.github.io/blog/2026-03-24-sqs-lambda-valkey-sse-crawling-workflow/",
    "https://hoshi2710.github.io/blog/2025-10-06-umc-9th-nodejs-week03/",
    "https://hoshi2710.github.io/blog/2025-09-24-umc-9th-nodejs-week02/",
    "https://hoshi2710.github.io/blog/2025-09-18-umc-9th-nodejs-week01/",
]


# url 객체로부터 soup객체 생성
def get_soup_object_from_url(url):
    # GET 요청 보내기
    response = requests.get(url)
    # HTTP Status결과에서 오류 발생시 에러 Raise
    response.raise_for_status()
    # 응답으로 나온 HTML 문서 코드 변수에 저장
    raw_html = response.text
    # HTML 코드 값을 파서로 읽고 soup 객체를 반환
    return BeautifulSoup(raw_html, "html.parser")


# 객체로부터 제목 추출
def get_title_from_soup(soup):
    # <title>태그에서 게시글 제목 값 추출하기
    return (soup.find("title").text).split("|")[0]


# 객체로 부터 설명 추출
def get_description_from_soup(soup):
    # CSS Selector를 이용하여 글 한줄 요약 값 추출하기
    return soup.select_one("header > p.mt-4").text


# 객체로부터 태그들 추출
def get_tags_from_soup(soup):
    # CSS Selector를 이용하여 어러개의 태그 값을 찾은 다음 텍스트 값만 추출하기
    return [tag.text for tag in soup.select("header>div.mt-5 > a")]


# 결과값을 누적시킬 리스트 변수
results = []
# 모든 url들에 대해서 반복
for url in urls:
    # url로 soup객체 생성하기
    soup = get_soup_object_from_url(url)
    # 결과를 results 사전에 누적
    results.append(
        {
            "title": get_title_from_soup(soup),
            "description": get_description_from_soup(soup),
            "tags": get_tags_from_soup(soup),
        }
    )
# 수집한 데이터를 출력
print(results)
# 실행시간 결과 출력
end = time.perf_counter()
print(f"실행 시간: {end - start:.2f}초")
