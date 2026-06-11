from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

if "from analysis.party_analysis import analyze_party" not in text:
    text = text.replace(
        "from analysis.meeting_group_summary import summarize_by_meeting",
        "from analysis.meeting_group_summary import summarize_by_meeting\nfrom analysis.party_analysis import analyze_party"
    )

route = '''

@app.route("/party/<party_name>")
def party_page(party_name):

    import json

    with open("data/member_party.json", encoding="utf-8") as f:
        member_party = json.load(f)

    members = [
        name
        for name, party in member_party.items()
        if party == party_name
    ]

    party_results = analyze_party(party_name)

    return render_template(
        "party.html",
        party_name=party_name,
        members=members,
        party_results=party_results
    )

'''

if '@app.route("/party/<party_name>")' not in text:
    text = text.replace(
        '\nif __name__ == "__main__":\n    app.run(debug=True)\n',
        route + '\nif __name__ == "__main__":\n    app.run(debug=True)\n'
    )

path.write_text(text, encoding="utf-8")
