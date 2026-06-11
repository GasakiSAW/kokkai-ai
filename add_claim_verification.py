from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

if "from analysis.claim_verifier import verify_claim" not in text:
    text = text.replace(
        "from analysis.policy_score import create_policy_score",
        "from analysis.policy_score import create_policy_score\nfrom analysis.claim_verifier import verify_claim"
    )

if "claim_verification = verify_claim" not in text:
    text = text.replace(
        '    return render_template(\n        "speech.html",',
        '    claim_verification = verify_claim(\n        ai_result,\n        policy_score.get("details", [])\n    )\n\n    return render_template(\n        "speech.html",'
    )

if "claim_verification=claim_verification" not in text:
    text = text.replace(
        "        chart_data=chart_data\n    )",
        "        chart_data=chart_data,\n        claim_verification=claim_verification\n    )"
    )

path.write_text(text, encoding="utf-8")
