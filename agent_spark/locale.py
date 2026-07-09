"""
Agent Spark · Locale Detection
================================
Unified bilingual support: auto-detect EN/ZH from user input.

Usage:
    from agent_spark.locale import detect, _
    lang = detect(["cat food", "宠物用品"])   # "zh"
    print(_("Hello", "你好", lang))           # 你好
"""

from __future__ import annotations

import re

_CN = re.compile(r'[\u4e00-\u9fff]')


def detect(*texts: str) -> str:
    """Detect locale from one or more text strings.
    
    Returns "zh" if any text contains Chinese characters, else "en".
    """
    for t in texts:
        if _CN.search(t):
            return "zh"
    return "en"


def _(en: str, zh: str, locale: str | None = None) -> str:
    """Return the localized string.
    
    Args:
        en: English text.
        zh: Chinese text.
        locale: "zh", "en", or None for auto-detect from the strings themselves.
    """
    if locale is None:
        locale = detect(en, zh)
    return zh if locale == "zh" else en
