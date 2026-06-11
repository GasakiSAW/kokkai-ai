import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def search_stats(keyword):

    app_id = os.getenv("ESTAT_APP_ID")

    url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"

    params = {
        "appId": app_id,
        "searchWord": keyword,
        "limit": 5
    }

    response = requests.get(url, params=params)
    response.encoding = "utf-8"

    return response.json()


def get_stats_data(stats_data_id):

    app_id = os.getenv("ESTAT_APP_ID")

    url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

    params = {
        "appId": app_id,
        "statsDataId": stats_data_id,
        "limit": 5000
    }

    response = requests.get(url, params=params)
    response.encoding = "utf-8"

    return response.json()


def is_number(value):

    try:
        float(value)
        return True
    except:
        return False


def get_latest_value(stats_data_id):

    series = get_time_series(stats_data_id)

    if not series:
        return None

    latest = series[-1]

    return {
        "year": latest.get("year", ""),
        "value": latest.get("value", ""),
        "unit": latest.get("unit", "")
    }


def get_series_key(v):

    return (
        v.get("@tab", ""),
        v.get("@cat01", ""),
        v.get("@cat02", ""),
        v.get("@cat03", ""),
        v.get("@area", "")
    )


def format_year(raw):

    if not raw:
        return ""

    return raw[:4]


def get_time_series(stats_data_id):

    data = get_stats_data(stats_data_id)

    values = (
        data
        .get("GET_STATS_DATA", {})
        .get("STATISTICAL_DATA", {})
        .get("DATA_INF", {})
        .get("VALUE", [])
    )

    target_key = None
    result = []

    for v in values:

        value = v.get("$", "")

        if not is_number(value):
            continue

        current_key = get_series_key(v)

        if target_key is None:
            target_key = current_key

        if current_key != target_key:
            continue

        result.append({
            "year": format_year(v.get("@time", "")),
            "value": value,
            "unit": v.get("@unit", "")
        })

    result = sorted(
        result,
        key=lambda x: x["year"]
    )

    return result[-10:]
