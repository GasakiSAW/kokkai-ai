import json

from analysis.metric_finder import find_metric_stats_id

metric = "消費者物価指数"

result = find_metric_stats_id(metric)

with open(
    "data/candidates.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )

print("保存完了")
