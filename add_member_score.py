from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

old = '''    return render_template(
        "member.html",
        speaker_name=speaker_name,
        results=member_results,
        total_score=total_score,
        theme_counts=theme_counts,
        member_summary=member_summary,
        from_date=from_date,
        until_date=until_date
    )'''

new = '''    member_score = create_member_score(
        member_results
    )

    return render_template(
        "member.html",
        speaker_name=speaker_name,
        results=member_results,
        total_score=total_score,
        theme_counts=theme_counts,
        member_summary=member_summary,
        member_score=member_score,
        from_date=from_date,
        until_date=until_date
    )'''

text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
