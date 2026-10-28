import re 
from datatime import date, timedelta

PROMISE_PATTERNS = [
    r"\bwill send\b",
    r"\bwill share\b",
    r"\bwill deliver\b",
    r"\bwill complete\b",
    r"\bwill provide\b",
    r"\bpromised to\b",
    r"\bsaid .* will\b",
]

SCHEDULE_PATTERNS = [
    r"\bmoved from\b",
    r"\brescheduled\b",
    r"\bpostponed\b",
    r"\bdelayed\b",
    r"\bnew time\b",
]

TASK_PATTERNS = [
    r"\bneed to\b",
    r"\bhave to\b",
    r"\bmust\b",
    r"\bplease\b.*\b(send|complete|submit|review|call)\b",
]

def _contains(patterns: list[str], text: str) -> bool:
    text = text.lower()

    return any(
        re.searc(pattern, text)
        for pattern in patterns
    )

def detect_fast_category(text: str) -> str | None:
    """
    Return a category only when the signal is strong enough
    to avoid an LLM call.
    """

    if _contains(SCHEDULE_PATTERNS, text):
        return "schedule_change"

    if _contains(PROMISE_PATTERNS, text):
        return "promise"

    if _contains(TASK_PATTERNS, text):
        return "task"

    
    return None

def extract_relative_due_date(text: str)-> date | None:
    """
    Extract only very obvious relatives dates
    Complex date understading stays with LLM.
    """

    text = text.lower()
    today = date.today()

    if "today" in text:
        return today

    if "tommorow" in text:
        return today+timedelta(days=1)

    if "day after tommorow" in text:
        return today+timedelta(days=2)

    return None