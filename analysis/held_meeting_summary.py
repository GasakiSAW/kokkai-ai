import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_held_meetings(results):

    grouped = {}

    for r in results:
        key = f"{r.get('date', '')}｜{r.get('meeting', '不明')}"
        grouped.setdefault(key, [])
        grouped[key].append(r)

    summaries = {}

    for key, rows in grouped.items():

        texts = []

        for r in rows[:20]:
            texts.append(
                f"発言者: {r['speaker']}\n"
                f"テーマ: {r['theme']}\n"
                f"要約: {r['summary']}\n"
            )

        joined = "\n---\n".join(texts)

        prompt = f"""
以下は「{key}」に行われた会議の発言一覧です。

この会議で何が話し合われたかを、国民向けに80～120文字で要約してください。
重要な政策論点、賛成意見、反対意見、結論を含めてください。

必ずJSONのみで返してください。

形式:
{{
  "meeting_key": "{key}",
  "summary": "",
  "main_topics": [],
  "important_points": []
}}

発言一覧:
{joined}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            content = response.choices[0].message.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()

            summaries[key] = json.loads(content)

        except Exception as e:
            summaries[key] = {
                "meeting_key": key,
                "summary": f"要約に失敗しました: {e}",
                "main_topics": [],
                "important_points": []
            }

    return summaries
