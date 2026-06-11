import json

from analysis.party_analysis import analyze_party, calc_party_achievement


def create_party_ranking():

    with open("data/party_manifesto.json", encoding="utf-8-sig") as f:
        manifestos = json.load(f)

    ranking = []

    for party_name in manifestos.keys():

        results = analyze_party(party_name)

        achievement = calc_party_achievement(results)

        ranking.append({
            "party_name": party_name,
            "achievement_rate": achievement["achievement_rate"],
            "grade": achievement["grade"],
            "promise_count": len(results)
        })

    ranking.sort(
        key=lambda x: x["achievement_rate"],
        reverse=True
    )

    return ranking
