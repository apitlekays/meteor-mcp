"""Shared MCP tool definitions for Meteor.js documentation server."""

from data import API_REGISTRY, EXAMPLES, GUIDES, MODULE_NAMES
from search import search_api


def register_tools(mcp):
    """Register all Meteor.js documentation tools on the given MCP instance."""

    @mcp.tool()
    def meteor_search(query: str) -> str:
        """Full-text search across all Meteor.js APIs. Returns matching methods with names, signatures, and descriptions."""
        if not query or not query.strip():
            return "Please provide a search query."

        query = query.strip()
        if len(query) > 200:
            return "Search query is too long. Please use fewer than 200 characters."

        results = search_api(query, API_REGISTRY)

        if not results:
            return f"No results found for '{query}'. Try broader terms like 'publish', 'collection', 'accounts', or 'methods'."

        lines = [f"## Search results for '{query}'\n"]
        for entry in results[:10]:
            env = f" *({entry['environment']})*" if entry.get("environment") else ""
            lines.append(f"### `{entry['name']}`{env}")
            lines.append(f"```\n{entry['signature']}\n```")
            desc = entry["description"]
            lines.append(desc[:200] + "..." if len(desc) > 200 else desc)
            if entry.get("deprecated"):
                lines.append("**DEPRECATED**")
            lines.append("")

        if len(results) > 10:
            lines.append(f"*... and {len(results) - 10} more results. Narrow your search for more specific results.*")

        return "\n".join(lines)

    @mcp.tool()
    def meteor_api_reference(module: str) -> str:
        """Get complete API reference for a Meteor.js module. Use module names like 'collections', 'accounts', 'pubsub', 'methods', etc."""
        module = module.strip().lower()

        if module not in MODULE_NAMES:
            available = ", ".join(sorted(MODULE_NAMES))
            return f"Unknown module '{module}'. Available modules: {available}"

        entries = [e for e in API_REGISTRY if e["module"] == module]

        if not entries:
            return f"No entries found for module '{module}'."

        lines = [f"## Meteor.js API Reference: `{module}`\n"]
        for entry in entries:
            env = f" *({entry['environment']})*" if entry.get("environment") else ""
            lines.append(f"### `{entry['name']}`{env}")
            lines.append(f"```\n{entry['signature']}\n```")
            lines.append(entry["description"])
            if entry.get("params"):
                lines.append("\n**Parameters:**")
                for p in entry["params"]:
                    opt = " *(optional)*" if p.get("optional") else ""
                    lines.append(f"- `{p['name']}` ({p['type']}){opt}: {p['description']}")
            if entry.get("returns"):
                lines.append(f"\n**Returns:** {entry['returns']}")
            if entry.get("deprecated"):
                lines.append("\n**DEPRECATED**")
            if entry.get("examples"):
                lines.append("\n**Examples:**")
                for ex in entry["examples"]:
                    lines.append(f"\n*{ex['title']}*")
                    lines.append(f"```javascript\n{ex['code']}\n```")
                    if ex.get("description"):
                        lines.append(ex["description"])
            lines.append("\n---\n")

        return "\n".join(lines)

    @mcp.tool()
    def meteor_method_lookup(method_name: str) -> str:
        """Look up a specific Meteor.js method by name. Examples: 'Meteor.publish', 'Mongo.Collection', 'Accounts.createUser'."""
        method_name = method_name.strip()

        exact = [e for e in API_REGISTRY if e["name"].lower() == method_name.lower()]
        if not exact:
            partial = [e for e in API_REGISTRY if method_name.lower() in e["name"].lower()]
            if partial:
                names = ", ".join(f"`{e['name']}`" for e in partial[:10])
                suffix = f" (and {len(partial) - 10} more)" if len(partial) > 10 else ""
                return f"No exact match for '{method_name}'. Did you mean: {names}{suffix}"
            return f"No method found for '{method_name}'. Use `meteor_search` to find methods."

        entry = exact[0]
        lines = [f"## `{entry['name']}`\n"]
        lines.append(f"**Module:** {entry['module']}")
        lines.append(f"**Environment:** {entry.get('environment', 'anywhere')}")
        if entry.get("is_reactive"):
            lines.append("**Reactive:** Yes")
        if entry.get("deprecated"):
            lines.append("**DEPRECATED**")
        lines.append(f"\n```\n{entry['signature']}\n```")
        lines.append(f"\n{entry['description']}")

        if entry.get("params"):
            lines.append("\n### Parameters")
            for p in entry["params"]:
                opt = " *(optional)*" if p.get("optional") else ""
                lines.append(f"- `{p['name']}` ({p['type']}){opt}: {p['description']}")

        if entry.get("returns"):
            lines.append(f"\n### Returns\n{entry['returns']}")

        if entry.get("examples"):
            lines.append("\n### Examples")
            for ex in entry["examples"]:
                lines.append(f"\n**{ex['title']}**")
                lines.append(f"```javascript\n{ex['code']}\n```")
                if ex.get("description"):
                    lines.append(ex["description"])

        return "\n".join(lines)

    @mcp.tool()
    def meteor_code_examples(topic: str) -> str:
        """Get working code examples for common Meteor.js patterns. Topics: methods, publications, collections, accounts, reactive, security, testing, routing, deployment, etc."""
        topic = topic.strip().lower()

        if topic in EXAMPLES:
            ex = EXAMPLES[topic]
            lines = [f"## Code Examples: {ex['title']}\n"]
            lines.append(ex.get("intro", ""))
            for snippet in ex["snippets"]:
                lines.append(f"\n### {snippet['title']}")
                lines.append(f"```javascript\n{snippet['code']}\n```")
                if snippet.get("description"):
                    lines.append(snippet["description"])
            return "\n".join(lines)

        available = ", ".join(sorted(EXAMPLES.keys()))
        return f"No examples found for topic '{topic}'. Available topics: {available}"

    @mcp.tool()
    def meteor_guide(topic: str) -> str:
        """Get conceptual guidance on Meteor.js architecture and patterns. Topics: reactivity, data-flow, security, project-structure, methods, publications, accounts, deployment, testing, packages."""
        topic = topic.strip().lower()

        if topic in GUIDES:
            guide = GUIDES[topic]
            lines = [f"## {guide['title']}\n"]
            lines.append(guide["content"])
            return "\n".join(lines)

        available = ", ".join(sorted(GUIDES.keys()))
        return f"No guide found for topic '{topic}'. Available topics: {available}"
