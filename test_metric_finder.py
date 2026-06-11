from analysis.metric_finder import save_metric_candidates

metrics = [
    "完全失業率",
    "実質賃金",
    "消費者物価指数"
]

result = save_metric_candidates(metrics)

print(result)
