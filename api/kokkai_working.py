import requests
import xml.etree.ElementTree as ET


def fetch_speeches(from_date="2024-01-01", until_date="2024-01-31", keyword=""):

    speeches = []
    start = 1

    while True:

        params = {
            "from": from_date,
            "until": until_date,
            "maximumRecords": 100,
            "startRecord": start
        }

        if keyword:
            params["any"] = keyword

        r = requests.get(
            "https://kokkai.ndl.go.jp/api/speech",
            params=params
        )

        if r.status_code != 200:
            print("取得失敗", r.status_code)
            break

        root = ET.fromstring(r.content)

        records = root.findall(".//speechRecord")

        if len(records) == 0:
            break

        for record in records:
            speeches.append({
                "speaker": record.findtext("speaker", ""),
                "speech": record.findtext("speech", ""),
                "date": record.findtext("date", ""),
                "meeting": record.findtext("nameOfMeeting", "")
            })

        next_pos = root.findtext(".//nextRecordPosition")

        if not next_pos:
            break

        start = int(next_pos)

        if len(speeches) >= 500:
            break

    return speeches
