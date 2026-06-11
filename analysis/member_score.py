from collections import Counter

from analysis.ai_analyzer import analyze_policy
from analysis.policy_score import create_policy_score
from analysis.claim_verifier import verify_claim


def create_member_score(member_results):

    total_policy_score = 0
    scored_count = 0

    supported = 0
    contradicted = 0
    unclear = 0

    theme_counter = Counter()

    details = []

    for r in member_results[:5]:

        theme_counter[r.get("theme", "不明")] += 1

        ai_result = analyze_policy(r["speech"])
        metrics = ai_result.get("metrics", [])

        policy_score = create_policy_score(metrics)

        claim_result = verify_claim(
            ai_result,
            policy_score.get("details", [])
        )

        score = policy_score.get("score", 0)

        total_policy_score += score
        scored_count += 1

        verdict = claim_result.get("verdict", "")

        if "支持" in verdict:
            supported += 1
        elif "反" in verdict:
            contradicted += 1
        else:
            unclear += 1

        details.append({
            "date": r.get("date", ""),
            "meeting": r.get("meeting", ""),
            "theme": r.get("theme", ""),
            "summary": r.get("summary", ""),
            "policy_score": score,
            "grade": policy_score.get("grade", ""),
            "verdict": verdict
        })

    if scored_count:
        average_score = round(total_policy_score / scored_count, 1)
    else:
        average_score = 0

    if average_score >= 80:
        grade = "A"
    elif average_score >= 60:
        grade = "B"
    elif average_score >= 40:
        grade = "C"
    else:
        grade = "D"

    return {
        "average_score": average_score,
        "grade": grade,
        "supported": supported,
        "contradicted": contradicted,
        "unclear": unclear,
        "main_themes": theme_counter.most_common(5),
        "details": details
    }

