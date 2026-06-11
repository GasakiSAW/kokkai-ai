from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

route = '''

@app.route("/timeline")
def timeline_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    grouped = {}

    for r in results:
        key = f"{r.get('date', '')}｜{r.get('meeting', '不明')}"
        grouped.setdefault(key, [])
        grouped[key].append(r)

    timeline = []

    for key, rows in grouped.items():
        date_part = key.split("｜")[0]
        meeting_part = key.split("｜")[1]

        timeline.append({
            "key": key,
            "date": date_part,
            "meeting": meeting_part,
            "count": len(rows),
            "themes": list(set([x.get("theme", "") for x in rows])),
            "speakers": list(set([x.get("speaker", "") for x in rows]))[:10],
            "rows": rows[:5]
        })

    timeline.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return render_template(
        "timeline.html",
        timeline=timeline,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )


@app.route("/news")
def news_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    cache_key = f"news_{from_date}_{until_date}_{keyword}"

    cache = load_json("data/news_cache.json")

    if cache_key in cache:
        news = cache[cache_key]
    else:
        news = create_kokkai_news(results)
        cache[cache_key] = news
        save_json("data/news_cache.json", cache)

    return render_template(
        "news.html",
        news=news,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

'''

if '@app.route("/timeline")' not in text:
    text = text.replace(
        '\nif __name__ == "__main__":\n    app.run(debug=True)\n',
        route + '\nif __name__ == "__main__":\n    app.run(debug=True)\n'
    )

path.write_text(text, encoding="utf-8")
