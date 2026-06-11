from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

insert = '''

@app.route("/meeting-summaries")
def meeting_summaries_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    cache_key = f"meeting_summaries_{from_date}_{until_date}_{keyword}"

    cache = load_json("data/meeting_summaries_cache.json")

    if cache_key in cache:
        summaries = cache[cache_key]
    else:
        summaries = summarize_by_meeting(results)
        cache[cache_key] = summaries
        save_json("data/meeting_summaries_cache.json", cache)

    return render_template(
        "meeting_summaries.html",
        summaries=summaries,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

'''

text = text.replace(
    '\nif __name__ == "__main__":\n    app.run(debug=True)\n',
    insert + '\nif __name__ == "__main__":\n    app.run(debug=True)\n'
)

path.write_text(text, encoding="utf-8")
