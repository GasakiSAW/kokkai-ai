from analysis.metric_finder import find_metric_stats_id

targets = [
    "GDP",
    "出生数",
    "合計特殊出生率"
]

for target in targets:

    print()
    print("========")
    print(target)
    print("========")

    results = find_metric_stats_id(target)

    for i, r in enumerate(results):

        print()
        print("候補", i + 1)
        print("タイトル:", r["title"])
        print("統計名:", r["stat_name"])
        print("統計ID:", r["stats_data_id"])
