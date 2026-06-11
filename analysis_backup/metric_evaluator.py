import json
import os

from analysis.estat import get_time_series


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
    "待機児童数": "lower_is_better",
    "自殺者数": "lower_is_better",
    "貧困率": "lower_is_better",
    "消費者物価指数": "depends"
}


def get_rule(metric):

    for key, rule in RULES.items():
        if key in metric:
            return rule

    return "higher_is_better"


def evaluate(metric, series):

    if not series:
        return {
            "evaluation": "データなし",
            "change": 0,
            "rule": get_rule(metric)
        }

    numeric_values = []

    for row in series:

        try:
            value = float(row["value"])
            numeric_values.append(value)

        except:
            continue

    if len(numeric_values) < 2:
        return {
            "evaluation": "データ不足",
            "change": 0,
            "rule": get_rule(metric)
        }

    first = numeric_values[0]
    last = numeric_values[-1]

    change = last - first
    rule = get_rule(metric)

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
        "evaluation": evaluation,
        "change": round(change, 2),
        "rule": rule
    }


def evaluate_metric(metric, stats_data_id):

    series = get_time_series(stats_data_id)

    result = evaluate(
        metric,
        series
    )

    return {
        "metric": metric,
        "stats_data_id": stats_data_id,
        "series": series,
        "rule": result["rule"],
        "change": result["change"],
        "evaluation": result["evaluation"]
    }


def save_metric_evaluation(metric, stats_data_id):

    result = evaluate_metric(
        metric,
        stats_data_id
    )

    os.makedirs("data", exist_ok=True)

    with open(
        "data/metric_evaluation.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2
        )

    return result
