"""Score-based search engine for Meteor.js API entries."""


def search_api(query: str, registry: list[dict]) -> list[dict]:
    """Search API registry with score-based ranking.

    Scoring: exact name match (100) > partial name (50) > tag match (30) > description (10).
    """
    query_lower = query.lower()
    tokens = query_lower.split()
    scored = []

    for entry in registry:
        score = 0
        name_lower = entry["name"].lower()

        if name_lower == query_lower:
            score += 100
        if query_lower in name_lower:
            score += 50
        for token in tokens:
            if token in name_lower:
                score += 25

        # Tag match
        for tag in entry.get("tags", []):
            tag_lower = tag.lower()
            if query_lower == tag_lower:
                score += 30
            elif query_lower in tag_lower or tag_lower in query_lower:
                score += 15
            else:
                for token in tokens:
                    if token in tag_lower:
                        score += 10

        # Description match
        desc_lower = entry.get("description", "").lower()
        if query_lower in desc_lower:
            score += 10
        else:
            for token in tokens:
                if token in desc_lower:
                    score += 5

        # Signature match
        sig_lower = entry.get("signature", "").lower()
        if query_lower in sig_lower:
            score += 15

        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored]
