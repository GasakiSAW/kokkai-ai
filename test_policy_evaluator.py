from analysis.policy_evaluator import evaluate_metrics

metrics = [
    "完全失業率",
    "実質賃金",
    "消費者物価指数"
]

result = evaluate_metrics(metrics)

for r in result:
    print(r)
