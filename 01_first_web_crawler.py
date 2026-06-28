import requests
from bs4 import BeautifulSoup

# 크롤링 대상 URL
TARGET_URL = "https://hoshi2710.github.io/blog/2026-03-24-sqs-lambda-valkey-sse-crawling-workflow/"
# GET 요청 보내기
response = requests.get(TARGET_URL)
# HTTP Status결과에서 오류 발생시 에러 Raise
response.raise_for_status()
# 응답으로 나온 HTML 문서 코드 변수에 저장
raw_html = response.text
# HTML 코드 값을 파서로 읽기
soup = BeautifulSoup(raw_html, "html.parser")
# <title>태그에서 게시글 제목 값 추출하기
title = (soup.find("title").text).split("|")[0]
# CSS Selector를 이용하여 글 한줄 요약 값 추출하기
description = soup.select_one("header > p.mt-4").text
# CSS Selector를 이용하여 어러개의 태그 값을 찾은 다음 텍스트 값만 추출하기
tags = [tag.text for tag in soup.select("header>div.mt-5 > a")]
# 사전 변수에 보기 좋게 수집한 데이터를 대입
data = {"title": title, "description": description, "tags": tags}
# 수집한 데이터를 출력
print(data)
