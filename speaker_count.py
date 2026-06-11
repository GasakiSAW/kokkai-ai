from collections import Counter
from api.kokkai import fetch_speeches

data = fetch_speeches()

counter = Counter()

for row in data:
    speaker = row.get("speaker","")
    counter[speaker] += 1

for speaker, count in counter.most_common(20):
    print(f"{speaker}: {count}回")
