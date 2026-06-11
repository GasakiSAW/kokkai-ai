import json
import os

from analysis.estat import get_time_series


def save_time_series(stats_data_id, name):

    data = get_time_series(stats_data_id)

    os.makedirs("data", exist_ok=True)

    result = {
        "name": name,
        "stats_data_id": stats_data_id,
        "series": data
    }

    with open("data/timeseries.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


save_time_series(
    "0000010206",
    "労働関連統計"
)
