from pathlib import Path
import re

path = Path("app.py")
text = path.read_text(encoding="utf-8")

new_block = r'''
@app.route("/speech/<int:speech_id>")
def speech_detail(speech_id):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)
    keyword = request.args.get("keyword", "")

    data = fetch_speeches(
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

    if speech_id < 0 or speech_id >= len(data):
        return "発言が見つかりません", 404

    speech = data[speech_id]

    return render_template(
        "speech.html",
        speech=speech,
        speech_id=speech_id,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )


@app.route("/analyze/<int:speech_id>")
def analyze_page(speech_id):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)
    keyword = request.args.get("keyword", "")

    data = fetch_speeches(
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

    if speech_id < 0 or speech_id >= len(data):
        return "発言が見つかりません", 404

    speech = data[speech_id]
    cache_key = f"{from_date}_{until_date}_{keyword}_{speech_id}"

    ai_cache = load_json("data/ai_cache.json")
    score_cache = load_json("data/policy_score_cache.json")

    if cache_key in ai_cache:
        ai_result = ai_cache[cache_key]
    else:
        ai_result = analyze_policy(speech["speech"])
        ai_cache[cache_key] = ai_result
        save_json("data/ai_cache.json", ai_cache)

    metrics = ai_result.get("metrics", [])

    if cache_key in score_cache:
        policy_score = score_cache[cache_key]
    else:
        policy_score = create_policy_score(metrics)
        score_cache[cache_key] = policy_score
        save_json("data/policy_score_cache.json", score_cache)

    metrics_data = get_metrics_data(metrics)

    chart_data = []

    for item in policy_score.get("details", []):
        chart_data.append({
            "metric": item.get("metric", ""),
            "series": item.get("series", [])
        })

    claim_verification = verify_claim(
        ai_result,
        policy_score.get("details", [])
    )

    return render_template(
        "analysis.html",
        speech=speech,
        speech_id=speech_id,
        ai_result=ai_result,
        metrics_data=metrics_data,
        policy_score=policy_score,
        chart_data=chart_data,
        claim_verification=claim_verification,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )
'''

pattern = r'@app\.route\("/speech/<int:speech_id>"\)\ndef speech_detail\(speech_id\):.*?(?=\n@app\.route\("/summary"\)|\n@app\.route\("/held-meeting-summaries"\)|\n@app\.route\("/party/<party_name>"\)|\nif __name__ == "__main__":)'

text = re.sub(pattern, new_block.strip() + "\n\n", text, flags=re.S)

path.write_text(text, encoding="utf-8")
