from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

old = '''    total_score = sum(r["score"] for r in member_results)

    theme_counts = {}

    for r in member_results:
        theme = r["theme"]
        theme_counts[theme] = theme_counts.get(theme, 0) + 1

    return render_template(
        "member.html",
        speaker_name=speaker_name,
        results=member_results,
        total_score=total_score,
        theme_counts=theme_counts,
        from_date=from_date,
        until_date=until_date
    )'''

new = '''    total_score = sum(r["score"] for r in member_results)

    theme_counts = {}

    for r in member_results:
        theme = r["theme"]
        theme_counts[theme] = theme_counts.get(theme, 0) + 1

    cache_key = f"member_summary_{speaker_name}_{from_date}_{until_date}"

    member_cache = load_json("data/member_summary_cache.json")

    if cache_key in member_cache:
        member_summary = member_cache[cache_key]
    else:
        member_summary = summarize_member(member_results)
        member_cache[cache_key] = member_summary
        save_json("data/member_summary_cache.json", member_cache)

    return render_template(
        "member.html",
        speaker_name=speaker_name,
        results=member_results,
        total_score=total_score,
        theme_counts=theme_counts,
        member_summary=member_summary,
        from_date=from_date,
        until_date=until_date
    )'''

text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
