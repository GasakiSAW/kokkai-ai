from pathlib import Path

path = Path("app.py")
text = path.read_text(encoding="utf-8")

text = text.replace(
'''    theme_counts = {}
    meeting_counts = {}

    for r in results:''',
'''    theme_counts = {}
    meeting_counts = {}
    speaker_counts = {}

    for r in results:'''
)

path.write_text(text, encoding="utf-8")
