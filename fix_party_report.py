from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

old = '''    party_results = analyze_party(party_name)

    return render_template(
        "party.html",
        party_name=party_name,
        members=members,
        party_results=party_results
    )'''

new = '''    party_results = analyze_party(party_name)

    party_report = create_party_report(
        party_name,
        party_results
    )

    return render_template(
        "party.html",
        party_name=party_name,
        members=members,
        party_results=party_results,
        party_report=party_report
    )'''

text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
