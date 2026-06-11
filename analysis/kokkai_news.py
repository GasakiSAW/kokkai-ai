import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_kokkai_news(results):

    texts = []

    for r in results[:40]:
        texts.append(
            f"日付: {r['date']}\n"
            f"会議: {r['meeting']}\n"
            f"発言者: {r['speaker']}\n"
            f"テーマ: {r['theme']}\n"
            f"要約: {r['summary']}\n"
        )

    joined = "\n---\n".join(texts)

    prompt = f"""
以下の国会発言一覧をもとに、国民向けのニュース記事を作成してください。

必ずJSONのみで返してください。

形式:
{{
  "headline": "",
  "lead": "",
  "main_topics": [],
  "supporting_views": [],
  "opposing_views": [],
  "article": "",
  "metrics_to_watch": []
}}

条件:
- headlineはニュース見出し
- leadは80字以内
- articleは300〜500字程度
- 政策論点、賛成意見、反対意見、今後見るべき統計を含める

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

        return json.loads(content)

    except Exception as e:
        return {
            "headline": "国会ニュース生成に失敗しました",
            "lead": str(e),
            "main_topics": [],
            "supporting_views": [],
            "opposing_views": [],
            "article": "",
            "metrics_to_watch": []
        }
