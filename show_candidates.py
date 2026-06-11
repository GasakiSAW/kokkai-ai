from analysis.metric_finder import find_metric_stats_id

metric = "消費者物価指数"

candidates = find_metric_stats_id(metric)

for i, c in enumerate(candidates):

    print()
    print("候補", i + 1)
    print("タイトル:", c["title"])
    print("統計名:", c["stat_name"])
    print("統計ID:", c["stats_data_id"])
