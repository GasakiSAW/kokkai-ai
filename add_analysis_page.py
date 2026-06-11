from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

route = '''

@app.route("/analyze/<int:speech_id>")
def analyze_page(speech_id):

    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    data = fetch_speeches(
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

    if speech_id < 0 or speech_id >= len(data):
        return "発言が見つかりません", 404

    speech = data[speech_id]

    ai_result = analyze_policy(
        speech["speech"]
    )

    metrics = ai_result.get("metrics", [])

    policy_score = create_policy_score(
        metrics
    )

    metrics_data = get_metrics_data(
        metrics
    )

    claim_verification = verify_claim(
        ai_result,
        policy_score.get("details", [])
    )

    return render_template(
        "analysis.html",
        speech=speech,
        ai_result=ai_result,
        policy_score=policy_score,
        metrics_data=metrics_data,
        claim_verification=claim_verification
    )

'''

if '@app.route("/analyze/<int:speech_id>")' not in text:
    text = text.replace(
        '\nif __name__ == "__main__":\n    app.run(debug=True)\n',
        route + '\nif __name__ == "__main__":\n    app.run(debug=True)\n'
    )

path.write_text(text, encoding="utf-8")
