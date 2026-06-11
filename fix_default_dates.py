from pathlib import Path
import re

path = Path("app.py")
text = path.read_text(encoding="utf-8")

pattern = r'def get_default_dates\(\):.*?return str\(from_date\), str\(today\)'

replacement = '''def get_default_dates():
    return "2024-01-01", "2024-12-31"'''

text = re.sub(pattern, replacement, text, flags=re.S)

path.write_text(text, encoding="utf-8")
