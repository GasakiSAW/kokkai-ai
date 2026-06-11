import os
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


def create_party_report(
    party_name,
    party_results
):

    text = ""

    for item in party_results:

        score = item["score"]

        text += f"""
テーマ: {item['theme']}
公約: {item['promise']}
評価: {score['grade']}
点数: {score['score']}
改善: {score['improve']}
悪化: {score['worse']}
不明: {score['unknown']}
---
"""

    prompt = f"""
あなたは政治アナリストです。

政党の公約達成状況を
国民向けに評価してください。

100〜200文字程度。

政党:
{party_name}

評価データ:
{text}
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"評価生成失敗: {e}"
