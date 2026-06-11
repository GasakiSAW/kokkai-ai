from analysis.ai_analyzer import analyze_policy

text = """
物価高によって国民生活が厳しくなっている。
政府は減税を含めた対策を検討すべきである。
"""

result = analyze_policy(text)

print(result)
