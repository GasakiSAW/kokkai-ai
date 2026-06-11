def score(text):
    score = 0

    important_words = [
        "予算",
        "物価",
        "法案",
        "支援",
        "重要",
        "課題",
        "対応"
    ]

    for word in important_words:
        if word in text:
            score += 3

    score += min(len(text) // 200, 2)

    return int(score)
