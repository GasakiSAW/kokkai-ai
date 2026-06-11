import os
import json
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(
    Path(__file__).resolve().parent.parent / ".env",
    override=True
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def summarize_meeting(results):

    texts = []

    for r in results[:30]:
        texts.append(
            f"発言者: {r['speaker']}\n"
            f"テーマ: {r['theme']}\n"
            f"要約: {r['summary']}\n"
        )

    joined_text = "\n---\n".join(texts)

    prompt = f"""
以下は国会会議録から取得した発言一覧です。

議会全体の内容を、国民に分かりやすく100字程度で詳しく要約してください。重要な政策論点、議論の内容、結論を含めてください。

出力形式:
{{
  "overall_summary": "",
  "main_topics": [],
  "important_points": [],
  "conflicts": [],
  "metrics_to_check": [],
  "one_line_summary": ""
}}

必ずJSONのみで返してください。

発言一覧:
{joined_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        return json.loads(content)

    except Exception as e:
        return {
            "overall_summary": f"要約に失敗しました: {e}",
            "main_topics": [],
            "important_points": [],
            "conflicts": [],
            "metrics_to_check": [],
            "one_line_summary": ""
        }


