def create_ranking(results):

    ranking = {}

    for r in results:

        speaker = r["speaker"]
        score = r["score"]

        if speaker not in ranking:
            ranking[speaker] = {
                "speaker": speaker,
                "total_score": 0,
                "count": 0
            }

        ranking[speaker]["total_score"] += score
        ranking[speaker]["count"] += 1

    return sorted(
        ranking.values(),
        key=lambda x: x["total_score"],
        reverse=True
    )