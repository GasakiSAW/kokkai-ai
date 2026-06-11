import json
import os

from analysis.estat import search_stats


def safe_text(value):

    if isinstance(value, dict):
        return value.get("$", "")

    if isinstance(value, str):
        return value

    return ""


def find_metric_stats_id(metric):

    data = search_stats(metric)

    stats_list = (
        data
        .get("GET_STATS_LIST", {})
        .get("DATALIST_INF", {})
        .get("TABLE_INF", [])
    )

    if isinstance(stats_list, dict):
        stats_list = [stats_list]

    candidates = []

    if isinstance(stats_list, list):
        for item in stats_list[:5]:

            if not isinstance(item, dict):
                continue

            candidates.append({
                "metric": metric,
                "title": safe_text(item.get("TITLE", "")),
                "stat_name": safe_text(item.get("STAT_NAME", "")),
                "stats_data_id": item.get("@id", "")
            })

    return candidates


def save_metric_candidates(metrics):

    result = {}

    for metric in metrics:
        result[metric] = find_metric_stats_id(metric)

    os.makedirs("data", exist_ok=True)

    with open("data/metric_candidates.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result
