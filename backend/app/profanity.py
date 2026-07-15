"""아주 단순한 금칙어(욕설/심한 비방) 필터.

부분 문자열 매칭 방식이라 띄어쓰기·특수문자를 섞은 우회는 걸러내지 못한다.
공공 게시판에서 가장 흔히 올라오는 표현 위주의 최소 목록이며, 운영 시에는
팀에서 목록을 계속 보강하면 된다.
"""

BANNED_WORDS = [
    "씨발",
    "시발",
    "씨팔",
    "ㅅㅂ",
    "개새끼",
    "개새키",
    "새끼야",
    "병신",
    "ㅂㅅ",
    "지랄",
    "좆",
    "좃",
    "미친놈",
    "미친년",
    "닥쳐",
    "꺼져",
    "걸레",
    "창녀",
    "fuck",
    "asshole",
    "bitch",
]


def contains_banned_word(*texts: str) -> bool:
    for text in texts:
        if not text:
            continue
        lowered = text.lower()
        if any(word in lowered for word in BANNED_WORDS):
            return True
    return False
