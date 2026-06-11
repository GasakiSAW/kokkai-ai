import json

from analysis.policy_score import create_policy_score


def analyze_party(party_name):

    with open("data/party_manifesto.json", encoding="utf-8-sig") as f:
        manifestos = json.load(f)

    promises = manifestos.get(party_name, [])

    results = []

    for promise in promises:

        metrics = promise.get("metrics", [])

        score = create_policy_score(metrics)

        achievement_rate = score.get("score", 0)

        results.append({
            "theme": promise.get("theme", ""),
            "promise": promise.get("promise", ""),
            "achievement_rate": achievement_rate,
            "score": score
        })

    return results


def calc_party_achievement(party_results):

    if not party_results:
        return {
            "achievement_rate": 0,
            "grade": "D"
        }

    rates = [
        item.get("achievement_rate", 0)
        for item in party_results
    ]

    average = round(sum(rates) / len(rates), 1)

    if average >= 80:
        grade = "A"
    elif average >= 60:
        grade = "B"
    elif average >= 40:
        grade = "C"
    else:
        grade = "D"

    return {
        "achievement_rate": average,
        "grade": grade
    }
