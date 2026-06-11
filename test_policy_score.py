from analysis.policy_evaluator import evaluate_metrics

metrics = [
    "完全失業率",
    "消費者物価指数",
    "出生数",
    "合計特殊出生率"
]

results = evaluate_metrics(metrics)

improve = 0
worse = 0
unknown = 0

for r in results:

    if r.get("evaluation") == "改善傾向":
        improve += 1

    elif r.get("evaluation") == "悪化傾向":
        worse += 1

    else:
        unknown += 1

print()
print("改善:", improve)
print("悪化:", worse)
print("不明:", unknown)

if improve > worse:
    print("総合評価: 改善傾向")

elif worse > improve:
    print("総合評価: 悪化傾向")

else:
    print("総合評価: 横ばい")
