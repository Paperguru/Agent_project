from datetime import date, datetime, timezone
from uuid import uuid4

from langchain_core.prompts import ChatPromptTemplate

from app.providers.llm import get_llm
from app.schemas.inbox import InboxItem, InboxAnalysis

SYSTEM_PROMPT = """
Analyze the input for a Life Inbox.

Fill every field in the schema.

Rules:
- summary: maximum 15 words
- category: information | task | deadline | promise | schedule_change | reminder | decision | other
- priority: low | medium | high
- requires_action: true only if the user must do something
- due_date: use a date only when explicitly stated or clearly implied by today/tomorrow
- people: names explicitly mentioned in the input
- status: always "new"
- never invent facts, names, or dates
- today is {today}

Return only the requested structured object.
"""

def analyze_inbox_item(
    content: str,
    source: str = "manual",
) -> InboxItem:

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Source: {source}\nInput: {content}",
            ),
        ]
    )

    structured_llm = llm.with_structured_output(
        InboxAnalysis,
        method="json_schema"
        )

    chain = prompt | structured_llm

    return chain.invoke(
        {
            "source": source,
            "content": content,
            "today": date.today().isoformat(),
        }
    )

def build_inbox_items(
    content: str,
    source: str,
    analysis: InboxAnalysis,
) -> InboxItem:

    return InboxItem(
        id= str(uuid4()),
        source=source,
        content=content,
        summary=analysis.summary,
        category=analysis.category,
        priority=analysis.priority,
        requires_action=analysis.requires_action,
        due_date=analysis.due_date,
        people=analysis.people,
        status=analysis.status,
        created_at=datetime.now(timezone.utc),
    )