import json


RULES = {
    "失業率": "lower_is_better",
    "完全失業率": "lower_is_better",
    "有効求人倍率": "higher_is_better",
    "実質賃金": "higher_is_better",
    "GDP": "higher_is_better",
    "国内総生産": "higher_is_better",
    "出生数": "higher_is_better",
    "合計特殊出生率": "higher_is_better",
    "婚姻数": "higher_is_better",
    "自殺者数": "lower_is_better",
    "待機児童数": "lower_is_better",
    "貧困率": "lower_is_better",
    "医療費": "depends",
    "消費者物価指数": "depends"
}


def judge_trend(name, first, last):

    rule = "higher_is_better"

    for key, value in RULES.items():
        if key in name:
            rule = value
            break

    change = last - first

    if rule == "higher_is_better":
        if change > 0:
            evaluation = "改善傾向"
        elif change < 0:
            evaluation = "悪化傾向"
        else:
            evaluation = "横ばい"

    elif rule == "lower_is_better":
        if change < 0:
            evaluation = "改善傾向"
        elif change > 0:
            evaluation = "悪化傾向"
        else:
            evaluation = "横ばい"

    else:
        evaluation = "要個別判断"

    return {
        "rule": rule,
        "change": round(change, 2),
        "evaluation": evaluation
    }


with open(
    "data/timeseries.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

series = data["series"]

first = float(series[0]["value"])
last = float(series[-1]["value"])

judgement = judge_trend(
    data["name"],
    first,
    last
)

result = {
    "name": data["name"],
    "first": first,
    "last": last,
    "rule": judgement["rule"],
    "change": judgement["change"],
    "evaluation": judgement["evaluation"]
}

print(result)
