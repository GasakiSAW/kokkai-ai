from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

old = '''    party_results = analyze_party(party_name)

    party_report = create_party_report(
        party_name,
        party_results
    )'''

new = '''    party_results = analyze_party(party_name)

    party_achievement = calc_party_achievement(
        party_results
    )

    party_report = create_party_report(
        party_name,
        party_results
    )'''

text = text.replace(old, new)

old2 = '''        party_results=party_results,
        party_report=party_report'''

new2 = '''        party_results=party_results,
        party_achievement=party_achievement,
        party_report=party_report'''

text = text.replace(old2, new2)

path.write_text(text, encoding="utf-8")
