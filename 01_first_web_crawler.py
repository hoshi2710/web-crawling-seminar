import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://hoshi2710.github.io/blog/2026-03-24-sqs-lambda-valkey-sse-crawling-workflow/"
response = requests.get(TARGET_URL)
response.raise_for_status()
raw_html = response.text

soup = BeautifulSoup(raw_html, "html.parser")

title = (soup.find("title").text).split("|")[0]
description = soup.select_one("header > p.mt-4").text
tags = [tag.text for tag in soup.select("header>div.mt-5 > a")]
data = {"title": title, "description": description, "tags": tags}
print(data)
