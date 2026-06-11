from analysis.policy_score import create_policy_score

result = create_policy_score([
    "完全失業率",
    "消費者物価指数",
    "出生数",
    "合計特殊出生率"
])

print(result)
