from typing import Literal

def imp_level(imp) -> Literal["陌生", "初识", "熟悉", "亲密", "喜欢", "恋人"]:
    if imp >= 500:
        return "恋人"
    elif imp >= 300:
        return "喜欢"
    elif imp >= 100:
        return "亲密"
    elif imp >= 50:
        return "熟悉"
    elif imp >= 10:
        return "初识"
    else:
        return "陌生"
    