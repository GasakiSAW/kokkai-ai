import json
import os

from analysis.metric_finder import find_metric_stats_id
from analysis.metric_evaluator import evaluate_metric
from analysis.metric_master import get_master_metric


def evaluate_metrics(metrics):

    results = []

    for metric in metrics:

        master = get_master_metric(metric)

        if master:

            evaluation = evaluate_metric(
                metric,
                master["stats_data_id"]
            )

            evaluation["title"] = master["title"]

            results.append(evaluation)

            continue

        candidates = find_metric_stats_id(metric)

        if not candidates:

            results.append({
                "metric": metric,
                "status": "統計候補なし"
            })

            continue

        first_candidate = candidates[0]

        stats_data_id = first_candidate["stats_data_id"]

        if not stats_data_id:

            results.append({
                "metric": metric,
                "status": "統計IDなし"
            })

            continue

        evaluation = evaluate_metric(
            metric,
            stats_data_id
        )

        evaluation["title"] = first_candidate["title"]
        evaluation["stat_name"] = first_candidate["stat_name"]

        results.append(evaluation)

    os.makedirs("data", exist_ok=True)

    with open(
        "data/policy_evaluation.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=2
        )

    return results
