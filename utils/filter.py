def is_noise(text):

    noise_words = [
        "議事日程",
        "本日の会議に付した案件",
        "――――――",
        "午後",
        "開議",
        "散会",
        "休憩",
        "会議録情報"
    ]

    if not text:
        return True

    if len(text) < 20:
        return True

    for word in noise_words:
        if word in text:
            return True

    return False


def is_noise_speaker(speaker):

    noise_speakers = [
        "会議録情報",
        "議長",
        "委員長"
    ]

    if not speaker:
        return True

    return speaker in noise_speakers
