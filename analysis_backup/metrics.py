import json
import os

from analysis.estat import search_stats
from analysis.estat import get_latest_value

CACHE_PATH = "data/metrics_cache.json"


def safe_text(value):

    if isinstance(value, dict):
        return value.get("$", "")

    if isinstance(value, str):
        return value

    return ""


def load_cache():

    if not os.path.exists(CACHE_PATH):
        return {}

    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache):

    os.makedirs("data", exist_ok=True)

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_metrics_data(metrics):

    cache = load_cache()
    result = {}

    for metric in metrics:

        if metric in cache:
            result[metric] = cache[metric]
            continue

        try:
            data = search_stats(metric)

            stats_list = (
                data
                .get("GET_STATS_LIST", {})
                .get("DATALIST_INF", {})
                .get("TABLE_INF", [])
            )

            if isinstance(stats_list, dict):
                stats_list = [stats_list]

            rows = []

            if isinstance(stats_list, list):
                for item in stats_list[:3]:

                    if not isinstance(item, dict):
                        continue

                    stats_data_id = item.get("@id", "")

                    latest = None

                    if stats_data_id:
                        try:
                            latest = get_latest_value(stats_data_id)
                        except:
                            latest = None

                    rows.append({
                        "title": safe_text(item.get("TITLE", "")),
                        "stat_name": safe_text(item.get("STAT_NAME", "")),
                        "stats_data_id": stats_data_id,
                        "latest": latest
                    })

            if not rows:
                rows = [{
                    "title": "該当する統計が見つかりません",
                    "stat_name": "",
                    "stats_data_id": "",
                    "latest": None
                }]

            cache[metric] = rows
            result[metric] = rows

        except Exception as e:
            result[metric] = [{
                "title": f"取得エラー: {e}",
                "stat_name": "",
                "stats_data_id": "",
                "latest": None
            }]

    save_cache(cache)

    return result
