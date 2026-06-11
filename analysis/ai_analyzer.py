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


def analyze_policy(text):

    # 長すぎる発言は短くする
    text = text[:3000]

    prompt = f"""
あなたは国会発言を分析する政策分析AIです。

必ずJSONのみで返してください。
説明文、コードブロック、```json は不要です。

出力形式:
{{
  "claim": "",
  "reason": "",
  "theme": "",
  "target": "",
  "expected_effect": "",
  "metrics": [],
  "counter_argument": "",
  "evaluation_method": ""
}}

metricsには、政府統計で検証しやすい指標を3つ入れてください。
例:
消費者物価指数、完全失業率、実質賃金、出生数、合計特殊出生率、有効求人倍率

発言:
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
            "claim": f"AI分析エラー: {e}",
            "reason": "",
            "theme": "",
            "target": "",
            "expected_effect": "",
            "metrics": [],
            "counter_argument": "",
            "evaluation_method": ""
        }
