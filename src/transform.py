from bs4 import BeautifulSoup

def clean(text):
    if not text:
        return ""
    return BeautifulSoup(text, "html.parser").get_text("\n")

def transform_issue_to_jsonl(issue, client):
    key = issue.get("key")
    full = client.get_issue(key)

    fields = full.get("fields", {})
    comments_raw = fields.get("comment", {}).get("comments", [])
    comments = [
        {"author": c.get("author", {}).get("displayName"),
        "text": clean(c.get("body")),
        "created": c.get("created")}
        for c in comments_raw
    ]

    description = clean(fields.get("description"))

    combined = (
        f"Title: {fields.get('summary')}\n\n"
        f"Description:\n{description}\n\n"
        "Comments:\n" +
        "\n".join(f"- {c['author']}: {c['text']}" for c in comments)
    )

    return {
        "id": key,
        "project": fields.get("project", {}).get("key"),
        "title": fields.get("summary"),
        "status": fields.get("status", {}).get("name"),
        "priority": fields.get("priority", {}).get("name"),
        "description": description,
        "comments": comments,
        "combined_text": combined,
        "derived": {
            "summary": None,
            "classification": {"type": fields.get("issuetype", {}).get("name")},
            "qa_pairs": []
        }
    }
