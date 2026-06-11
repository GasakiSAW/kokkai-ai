from pathlib import Path

path = Path("app.py")
lines = path.read_text(encoding="utf-8").splitlines()

seen = set()
new_lines = []

for line in lines:
    if line.startswith("from analysis.meeting_summary import summarize_meeting"):
        if line in seen:
            continue
        seen.add(line)

    if line.startswith("from analysis.member_summary import summarize_member"):
        if line in seen:
            continue
        seen.add(line)

    if line.startswith("from analysis.meeting_group_summary import summarize_by_meeting"):
        if line in seen:
            continue
        seen.add(line)

    new_lines.append(line)

path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
