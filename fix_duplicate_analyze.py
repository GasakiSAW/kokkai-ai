from pathlib import Path
import re

path = Path("app.py")
text = path.read_text(encoding="utf-8")

pattern = r'@app\.route\("/analyze/<int:speech_id>"\)\ndef analyze_page\(speech_id\):.*?(?=\n@app\.route|\nif __name__ == "__main__":)'

matches = list(re.finditer(pattern, text, flags=re.S))

if len(matches) > 1:
    # 最初の analyze_page だけ残して、2個目以降を削除
    keep = matches[0].group(0)
    text = re.sub(pattern, "", text, flags=re.S)
    insert_pos = text.find('\nif __name__ == "__main__":')
    text = text[:insert_pos] + "\n\n" + keep + "\n" + text[insert_pos:]

path.write_text(text, encoding="utf-8")
