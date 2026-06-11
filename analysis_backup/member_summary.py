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


def summarize_member(results):

    texts = []

    for r in results[:30]:

        texts.append(
            f"""
テーマ:{r["theme"]}
要約:{r["summary"]}
"""
        )

    joined = "\n".join(texts)

    prompt = f"""
以下は同じ議員の発言一覧です。

JSONのみで返してください。

{{
  "main_topics": [],
  "policy_positions": [],
  "strengths": [],
  "weaknesses": [],
  "overall_comment": ""
}}

発言一覧:

{joined}
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

        content = response.choices[0].message.content

        content = content.replace("```json", "")
        content = content.replace("```", "")

        return json.loads(content)

    except Exception as e:

        return {
            "main_topics": [],
            "policy_positions": [],
            "strengths": [],
            "weaknesses": [],
            "overall_comment": str(e)
        }
