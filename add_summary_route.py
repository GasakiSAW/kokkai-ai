from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

insert = '''

@app.route("/summary")
def summary_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    cache_key = f"summary_{from_date}_{until_date}_{keyword}"

    summary_cache = load_json("data/summary_cache.json")

    if cache_key in summary_cache:
        summary = summary_cache[cache_key]
    else:
        summary = summarize_meeting(results)
        summary_cache[cache_key] = summary
        save_json("data/summary_cache.json", summary_cache)

    return render_template(
        "summary.html",
        summary=summary,
        results=results,
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

'''

text = text.replace(
    '\nif __name__ == "__main__":\n    app.run(debug=True)\n',
    insert + '\nif __name__ == "__main__":\n    app.run(debug=True)\n'
)

path.write_text(text, encoding="utf-8")
