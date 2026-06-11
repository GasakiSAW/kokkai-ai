import json
from datetime import date, timedelta

from flask import Flask, render_template, request

from api.kokkai import fetch_speeches
from analysis.summary import summarize
from analysis.classify import classify
from analysis.score import score
from analysis.ranking import create_ranking
from analysis.topic_ranking import create_topic_ranking
from analysis.ai_analyzer import analyze_policy
from analysis.metrics import get_metrics_data
from analysis.claim_verifier import verify_claim
from analysis.policy_score import create_policy_score
from analysis.cache import load_json, save_json
from analysis.meeting_summary import summarize_meeting
from analysis.member_summary import summarize_member
from analysis.member_score import create_member_score
from analysis.meeting_group_summary import summarize_by_meeting
from analysis.held_meeting_summary import summarize_held_meetings
from analysis.kokkai_news import create_kokkai_news
from analysis.party_analysis import analyze_party, calc_party_achievement
from analysis.party_report import create_party_report
from analysis.cached_party_ranking import get_cached_party_ranking
from analysis.party_report import create_party_report
from analysis.cached_party_ranking import get_cached_party_ranking
from utils.filter import is_noise, is_noise_speaker

app = Flask(__name__)


TOPIC_KEYWORDS = {
    "物価・賃上げ": ["物価", "賃上げ", "インフレ", "所得", "減税"],
    "防衛・安全保障": ["防衛", "自衛隊", "安全保障", "ミサイル"],
    "年金・介護": ["年金", "介護", "高齢者", "社会保障"],
    "少子化・子育て": ["少子化", "子育て", "保育", "児童"],
    "教育": ["教育", "学校", "大学", "教師", "生徒"],
    "農業・食料": ["農業", "農地", "食料", "米"],
    "医療": ["医療", "病院", "看護", "診療"],
    "災害・防災": ["災害", "地震", "防災", "復興"],
    "外交": ["外交", "国際", "中国", "アメリカ", "韓国"],
    "デジタル": ["AI", "DX", "デジタル", "マイナンバー"]
}


def get_default_dates():
    return "2024-01-01", "2024-12-31"


def build_results(keyword="", from_date=None, until_date=None):
    default_from, default_until = get_default_dates()

    if from_date is None:
        from_date = default_from

    if until_date is None:
        until_date = default_until

    data = fetch_speeches(
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

    results = []

    for i, d in enumerate(data[:50]):
        speech = d["speech"]

        if is_noise(speech):
            continue

        theme = classify(speech)

        results.append({
            "id": i,
            "speaker": d["speaker"],
            "speech": speech,
            "summary": speech[:100] + "..." if len(speech) > 100 else speech,
            "theme": theme,
            "score": score(speech),
            "date": d.get("date", ""),
            "meeting": d.get("meeting", "")
        })

    return results


@app.route("/")
def index():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    ranking = create_ranking(results)
    topic_ranking = create_topic_ranking(results)
    party_ranking = get_cached_party_ranking()

    theme_counts = {}
    meeting_counts = {}
    speaker_counts = {}

    for r in results:
        theme = r["theme"]
        meeting = r["meeting"]

        theme_counts[theme] = theme_counts.get(theme, 0) + 1
        meeting_counts[meeting] = meeting_counts.get(meeting, 0) + 1

        speaker = r["speaker"]
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1

    with open("data/result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return render_template(
        "index.html",
        results=results,
        ranking=ranking,
        topic_ranking=topic_ranking,
        party_ranking=party_ranking,
        keyword=keyword,
        from_date=from_date,
        until_date=until_date,
        theme_counts=theme_counts,
        meeting_counts=meeting_counts,
        speaker_counts=speaker_counts
    )


@app.route("/topic/<topic_name>")
def topic_page(topic_name):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        from_date=from_date,
        until_date=until_date
    )

    keywords = TOPIC_KEYWORDS.get(topic_name, [])

    topic_results = []

    for r in results:
        for word in keywords:
            if word in r["speech"]:
                topic_results.append(r)
                break

    ranking = create_ranking(topic_results)

    return render_template(
        "topic.html",
        topic_name=topic_name,
        results=topic_results,
        ranking=ranking,
        from_date=from_date,
        until_date=until_date
    )


@app.route("/meeting/<meeting_name>")
def meeting_page(meeting_name):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        from_date=from_date,
        until_date=until_date
    )

    meeting_results = [
        r for r in results
        if r["meeting"] == meeting_name
    ]

    ranking = create_ranking(meeting_results)

    return render_template(
        "meeting.html",
        meeting_name=meeting_name,
        results=meeting_results,
        ranking=ranking,
        from_date=from_date,
        until_date=until_date
    )


@app.route("/member/<speaker_name>")
def member_page(speaker_name):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        from_date=from_date,
        until_date=until_date
    )

    member_results = [
        r for r in results
        if r["speaker"] == speaker_name
    ]

    total_score = sum(r["score"] for r in member_results)

    theme_counts = {}

    for r in member_results:
        theme = r["theme"]
        theme_counts[theme] = theme_counts.get(theme, 0) + 1

    cache_key = f"member_summary_{speaker_name}_{from_date}_{until_date}"

    member_cache = load_json("data/member_summary_cache.json")

    if cache_key in member_cache:
        member_summary = member_cache[cache_key]
    else:
        member_summary = summarize_member(member_results)
        member_cache[cache_key] = member_summary
        save_json("data/member_summary_cache.json", member_cache)

    member_score = create_member_score(
        member_results
    )

    return render_template(
        "member.html",
        speaker_name=speaker_name,
        results=member_results,
        total_score=total_score,
        theme_counts=theme_counts,
        member_summary=member_summary,
        member_score=member_score,
        from_date=from_date,
        until_date=until_date
    )


@app.route("/theme/<theme_name>")
def theme_page(theme_name):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        from_date=from_date,
        until_date=until_date
    )

    theme_results = [
        r for r in results
        if r["theme"] == theme_name
    ]

    ranking = create_ranking(theme_results)

    return render_template(
        "theme.html",
        theme_name=theme_name,
        results=theme_results,
        ranking=ranking,
        from_date=from_date,
        until_date=until_date
    )


@app.route("/speech/<int:speech_id>")
def speech_detail(speech_id):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)
    keyword = request.args.get("keyword", "")

    data = fetch_speeches(
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

    if speech_id < 0 or speech_id >= len(data):
        return "発言が見つかりません", 404

    speech = data[speech_id]

    return render_template(
        "speech.html",
        speech=speech,
        speech_id=speech_id,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )



@app.route("/summary")
def summary_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    cache_key = f"summary_{from_date}_{until_date}_{keyword}"

    summary_cache = load_json("data/summary_cache.json")

    if cache_key in summary_cache:
        summary = summary_cache[cache_key]
    else:
        summary = summarize_meeting(results)
        summary_cache[cache_key] = summary
        save_json("data/summary_cache.json", summary_cache)

    return render_template(
        "summary.html",
        summary=summary,
        results=results,
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )



@app.route("/meeting-summaries")
def meeting_summaries_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    cache_key = f"meeting_summaries_{from_date}_{until_date}_{keyword}"

    cache = load_json("data/meeting_summaries_cache.json")

    if cache_key in cache:
        summaries = cache[cache_key]
    else:
        summaries = summarize_by_meeting(results)
        cache[cache_key] = summaries
        save_json("data/meeting_summaries_cache.json", cache)

    return render_template(
        "meeting_summaries.html",
        summaries=summaries,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )



@app.route("/party/<party_name>")
def party_page(party_name):

    import json

    with open("data/member_party.json", encoding="utf-8-sig") as f:
        member_party = json.load(f)

    members = [
        name
        for name, party in member_party.items()
        if party == party_name
    ]

    party_results = analyze_party(party_name)

    party_achievement = calc_party_achievement(
        party_results
    )

    party_report = create_party_report(
        party_name,
        party_results
    )

    return render_template(
        "party.html",
        party_name=party_name,
        members=members,
        party_results=party_results,
        party_achievement=party_achievement,
        party_report=party_report
    )



@app.route("/held-meeting-summaries")
def held_meeting_summaries_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    cache_key = f"held_meeting_summaries_{from_date}_{until_date}_{keyword}"

    cache = load_json("data/held_meeting_summaries_cache.json")

    if cache_key in cache:
        summaries = cache[cache_key]
    else:
        summaries = summarize_held_meetings(results)
        cache[cache_key] = summaries
        save_json("data/held_meeting_summaries_cache.json", cache)

    return render_template(
        "held_meeting_summaries.html",
        summaries=summaries,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )



@app.route("/timeline")
def timeline_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    grouped = {}

    for r in results:
        key = f"{r.get('date', '')}｜{r.get('meeting', '不明')}"
        grouped.setdefault(key, [])
        grouped[key].append(r)

    timeline = []

    for key, rows in grouped.items():
        date_part = key.split("｜")[0]
        meeting_part = key.split("｜")[1]

        timeline.append({
            "key": key,
            "date": date_part,
            "meeting": meeting_part,
            "count": len(rows),
            "themes": list(set([x.get("theme", "") for x in rows])),
            "speakers": list(set([x.get("speaker", "") for x in rows]))[:10],
            "rows": rows[:5]
        })

    timeline.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return render_template(
        "timeline.html",
        timeline=timeline,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )


@app.route("/news")
def news_page():
    default_from, default_until = get_default_dates()

    keyword = request.args.get("keyword", "")
    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)

    results = build_results(
        keyword=keyword,
        from_date=from_date,
        until_date=until_date
    )

    cache_key = f"news_{from_date}_{until_date}_{keyword}"

    cache = load_json("data/news_cache.json")

    if cache_key in cache:
        news = cache[cache_key]
    else:
        news = create_kokkai_news(results)
        cache[cache_key] = news
        save_json("data/news_cache.json", cache)

    return render_template(
        "news.html",
        news=news,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )



@app.route("/party-compare")
def party_compare_page():

    party_ranking = get_cached_party_ranking()

    return render_template(
        "party_compare.html",
        party_ranking=party_ranking
    )





@app.route("/analyze/<int:speech_id>")
def analyze_page(speech_id):
    default_from, default_until = get_default_dates()

    from_date = request.args.get("from_date", default_from)
    until_date = request.args.get("until_date", default_until)
    keyword = request.args.get("keyword", "")

    data = fetch_speeches(
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )

    if speech_id < 0 or speech_id >= len(data):
        return "発言が見つかりません", 404

    speech = data[speech_id]
    cache_key = f"{from_date}_{until_date}_{keyword}_{speech_id}"

    ai_cache = load_json("data/ai_cache.json")
    score_cache = load_json("data/policy_score_cache.json")

    if cache_key in ai_cache:
        ai_result = ai_cache[cache_key]
    else:
        ai_result = analyze_policy(speech["speech"])
        ai_cache[cache_key] = ai_result
        save_json("data/ai_cache.json", ai_cache)

    metrics = ai_result.get("metrics", [])

    if cache_key in score_cache:
        policy_score = score_cache[cache_key]
    else:
        policy_score = create_policy_score(metrics)
        score_cache[cache_key] = policy_score
        save_json("data/policy_score_cache.json", score_cache)

    metrics_data = get_metrics_data(metrics)

    chart_data = []

    for item in policy_score.get("details", []):
        chart_data.append({
            "metric": item.get("metric", ""),
            "series": item.get("series", [])
        })

    claim_verification = verify_claim(
        ai_result,
        policy_score.get("details", [])
    )

    return render_template(
        "analysis.html",
        speech=speech,
        speech_id=speech_id,
        ai_result=ai_result,
        metrics_data=metrics_data,
        policy_score=policy_score,
        chart_data=chart_data,
        claim_verification=claim_verification,
        from_date=from_date,
        until_date=until_date,
        keyword=keyword
    )



if __name__ == "__main__":
    app.run(debug=True)
































