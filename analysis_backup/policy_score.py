from analysis.policy_evaluator import evaluate_metrics


def calc_point(item):

    evaluation = item.get("evaluation")
    change = item.get("change", 0)

    try:
        change = float(change)
    except:
        change = 0

    abs_change = abs(change)

    if evaluation == "改善傾向":
        if abs_change >= 10:
            return 20
        elif abs_change >= 3:
            return 15
        else:
            return 10

    elif evaluation == "悪化傾向":
        if abs_change >= 10:
            return -20
        elif abs_change >= 3:
            return -15
        else:
            return -10

    else:
        return 0


def create_policy_score(metrics):

    results = evaluate_metrics(metrics)

    improve = 0
    worse = 0
    unknown = 0
    raw_score = 0

    for r in results:

        evaluation = r.get("evaluation")

        if evaluation == "改善傾向":
            improve += 1

        elif evaluation == "悪化傾向":
            worse += 1

        else:
            unknown += 1

        point = calc_point(r)
        r["point"] = point
        raw_score += point

    score = 50 + raw_score

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    if score >= 80:
        grade = "A"

    elif score >= 60:
        grade = "B"

    elif score >= 40:
        grade = "C"

    else:
        grade = "D"

    return {
        "score": score,
        "grade": grade,
        "improve": improve,
        "worse": worse,
        "unknown": unknown,
        "raw_score": raw_score,
        "details": results
    }
