from app.intelligence.fast_path import(
    detect_fast_category,
    extract_relative_due_date,
)

def should_use_llm(content: str) -> bool:
    """
    Decide wheather the input requires semantic understanding.
    """

    category = detect_fast_category(content)

    if category is not None:
        return False

    return True

def fast_extract(content: str) -> dict:
    """
    Extract the small information we can determine
    determinstically
    """

    return {
        "category": detect_fast_category(content),
        "due_date": extract_relative_due_date(content)
    }