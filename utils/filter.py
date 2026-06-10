def is_noise(text):

    keywords = [
        "これより会議を開きます",
        "本日の会議に付した案件",
        "議事日程",
        "散会",
        "開会",
        "登壇",
        "拍手"
    ]

    for k in keywords:
        if k in text:
            return True

    return False
