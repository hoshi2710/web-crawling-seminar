import json

import requests
from bs4 import BeautifulSoup


def get_query_strings(event):
    queries = event["rawQueryString"].split("&")
    return dict(map(lambda q: q.split("="), queries))


def lambda_handler(event, context):
    queries = get_query_strings(event)
    url = queries["url"]
    if url is None:
        return {"statusCode": 400, "body": json.dumps("No url provided")}
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    data = {
        "title": soup.find("title").text.split("|")[0].strip(),
        "description": soup.select_one("header > p.mt-4").text.strip(),
        "tags": [tag.text.strip() for tag in soup.select("header > div.mt-5 > a")],
    }
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps(data, ensure_ascii=False),
    }
