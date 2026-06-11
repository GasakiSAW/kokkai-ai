from analysis.policy_evaluator import evaluate_metrics


def create_policy_score(metrics):

    results = evaluate_metrics(metrics)

    improve = 0
    worse = 0
    unknown = 0

    for r in results:

        evaluation = r.get("evaluation")

        if evaluation == "改善傾向":
            improve += 1

        elif evaluation == "悪化傾向":
            worse += 1

        else:
            unknown += 1

    if improve >= 3 and worse == 0:
        grade = "A"

    elif improve > worse:
        grade = "B"

    elif improve == worse:
        grade = "C"

    else:
        grade = "D"

    return {
        "grade": grade,
        "improve": improve,
        "worse": worse,
        "unknown": unknown,
        "details": results
    }
