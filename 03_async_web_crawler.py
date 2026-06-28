import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

# 크롤링을 진행할 대상 페이지 URL들
urls = [
    "https://hoshi2710.github.io/blog/2026-03-24-sqs-lambda-valkey-sse-crawling-workflow/",
    "https://hoshi2710.github.io/blog/2025-10-06-umc-9th-nodejs-week03/",
    "https://hoshi2710.github.io/blog/2025-09-24-umc-9th-nodejs-week02/",
    "https://hoshi2710.github.io/blog/2025-09-18-umc-9th-nodejs-week01/",
]


# url 객체로부터 soup객체 생성
async def get_soup(session, url):
    # URL에 GET보내고 받은 response 객체로 작업 진행
    async with session.get(url) as response:
        response.raise_for_status()  # 상태코드에서 오류 발생시 에러 Raise
        raw_html = await response.text()  # 응답값에서 웹페이지 HTML 코드 추출
        return BeautifulSoup(raw_html, "html.parser")  # soup객체를 생성하여 반환


# 객체로부터 제목 추출
def get_title(soup):
    # <title>태그에서 게시글 제목 값 추출하기
    return soup.find("title").text.split("|")[0].strip()


# 객체로 부터 설명 추출
def get_description(soup):
    # CSS Selector를 이용하여 글 한줄 요약 값 추출하기
    return soup.select_one("header > p.mt-4").text.strip()


# 객체로부터 태그들 추출
def get_tags(soup):
    # CSS Selector를 이용하여 어러개의 태그 값을 찾은 다음 텍스트 값만 추출하기
    return [tag.text.strip() for tag in soup.select("header > div.mt-5 > a")]


# 해당 URL로부터 데이터들을 크롤링하고 결과값을 반환
async def crawl_page(session, url):
    soup = await get_soup(session, url)  # soup객체 생성
    # 크롤링 결과 dict 자료 형태로 반환
    return {
        "url": url,
        "title": get_title(soup),
        "description": get_description(soup),
        "tags": get_tags(soup),
    }


async def main():
    start = time.perf_counter()  # 실행시간 카운터 시작
    # 세션 생성 및 Coroutine 객체 생성, 동시 실행, 결과값 반환
    async with aiohttp.ClientSession() as session:
        tasks = [crawl_page(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    print(results)  # 크롤링 결과 출력
    # 타이머를 중지하고 걸린 시간 출력
    end = time.perf_counter()
    print(f"실행 시간: {end - start:.2f}초")


# main 함수 실행
asyncio.run(main())
