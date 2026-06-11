def create_topic_ranking(results):

    topics = {
        "物価・賃上げ": ["物価", "賃上げ", "インフレ"],
        "防衛・安全保障": ["防衛", "自衛隊", "安全保障"],
        "年金・介護": ["年金", "介護"],
        "少子化・子育て": ["少子化", "子育て"],
        "教育": ["教育", "学校"]
    }

    ranking = {}

    for topic in topics:
        ranking[topic] = 0

    for r in results:

        speech = r["speech"]

        for topic, words in topics.items():

            for word in words:

                if word in speech:
                    ranking[topic] += 1
                    break

    return sorted(
        ranking.items(),
        key=lambda x: x[1],
        reverse=True
    )
