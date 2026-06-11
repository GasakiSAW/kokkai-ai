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


def verify_claim(ai_result, policy_evaluation):

    claim = ai_result.get("claim", "")
    reason = ai_result.get("reason", "")

    evidence_text = ""

    for item in policy_evaluation:

        metric = item.get("metric", "")
        evaluation = item.get("evaluation", "不明")
        change = item.get("change", "")
        rule = item.get("rule", "")
        series = item.get("series", [])

        values = []

        for row in series:
            values.append(
                f'{row.get("year", "")}: {row.get("value", "")}{row.get("unit", "")}'
            )

        evidence_text += f"""
指標: {metric}
評価: {evaluation}
変化量: {change}
評価ルール: {rule}
時系列:
{values}
---
"""

    prompt = f"""
あなたは政策ファクトチェックAIです。

以下の議員発言の主張が、統計データによって支持されるか検証してください。

必ずJSONのみで返してください。

形式:
{{
  "verdict": "",
  "confidence": "",
  "summary": "",
  "supporting_evidence": [],
  "contradicting_evidence": [],
  "caution": ""
}}

判定基準:
verdict は次のどれか:
- "統計は主張を支持している"
- "統計は主張に反している"
- "統計だけでは判断できない"

confidence は次のどれか:
- "高"
- "中"
- "低"

議員の主張:
{claim}

主張の理由:
{reason}

統計データ:
{evidence_text}
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
            "verdict": "統計だけでは判断できない",
            "confidence": "低",
            "summary": f"検証に失敗しました: {e}",
            "supporting_evidence": [],
            "contradicting_evidence": [],
            "caution": "APIキー、利用上限、またはJSON形式を確認してください。"
        }
