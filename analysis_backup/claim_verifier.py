import os
import json
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(
    Path(__file__).resolve().parent.parent / ".env",
    override=True
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def verify_claim(ai_result, policy_evaluation):

    claim = ai_result.get("claim", "")
    reason = ai_result.get("reason", "")

    evidence_text = ""

    for item in policy_evaluation:
        metric = item.get("metric", "")
        evaluation = item.get("evaluation", "不明")
        change = item.get("change", "")
        rule = item.get("rule", "")

        evidence_text += f"""
指標: {metric}
評価: {evaluation}
変化量: {change}
評価ルール: {rule}
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

supporting_evidence と contradicting_evidence は、
必ず文字列の配列にしてください。
例:
["完全失業率は改善傾向であり、雇用環境の改善を示している"]

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
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        result = json.loads(content)

        result["supporting_evidence"] = [
            str(x) for x in result.get("supporting_evidence", [])
        ]

        result["contradicting_evidence"] = [
            str(x) for x in result.get("contradicting_evidence", [])
        ]

        return result

    except Exception as e:
        return {
            "verdict": "統計だけでは判断できない",
            "confidence": "低",
            "summary": f"検証に失敗しました: {e}",
            "supporting_evidence": [],
            "contradicting_evidence": [],
            "caution": "APIキー、利用上限、またはJSON形式を確認してください。"
        }
