from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

route = '''

@app.route("/party-compare")
def party_compare_page():

    party_ranking = create_party_ranking()

    return render_template(
        "party_compare.html",
        party_ranking=party_ranking
    )

'''

if '@app.route("/party-compare")' not in text:
    text = text.replace(
        '\nif __name__ == "__main__":\n    app.run(debug=True)\n',
        route + '\nif __name__ == "__main__":\n    app.run(debug=True)\n'
    )

path.write_text(text, encoding="utf-8")
