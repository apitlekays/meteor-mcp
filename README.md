# Meteor.js MCP Server

A Model Context Protocol (MCP) server that provides complete **Meteor.js v3.4.0** API documentation, code examples, and architectural guides to AI coding assistants like Claude, Cursor, Windsurf, and any MCP-compatible client.

212 API entries across 20 modules — all embedded as static data, no external network calls required.

## Why

Meteor.js is a powerful full-stack JavaScript framework, but AI coding assistants often lack up-to-date knowledge of its APIs, especially the v3 async-first changes. This MCP server gives any AI assistant instant access to accurate, audited Meteor documentation so it can:

- Look up any Meteor API method with full signatures, parameters, and return types
- Get working code examples for common patterns (pub/sub, methods, auth, etc.)
- Understand Meteor v3's async-first architecture and migration from Fibers
- Follow best practices for security, reactivity, and project structure

## Tools

The server exposes 5 MCP tools:

| Tool | Description |
|------|-------------|
| `meteor_search` | Full-text search across all 212 API entries with score-based ranking |
| `meteor_api_reference` | Get complete reference for an API module (e.g. `collections`, `accounts`) |
| `meteor_method_lookup` | Look up a specific method by name (e.g. `Meteor.publish`, `Mongo.Collection.find`) |
| `meteor_code_examples` | Get annotated code examples for 15 topics |
| `meteor_guide` | Get conceptual guidance on 10 architectural topics |

## API Coverage

| Module | Entries | Description |
|--------|---------|-------------|
| `accounts` | 35 | User accounts, login, OAuth, password management |
| `collections` | 27 | Mongo.Collection, Cursor, CRUD operations |
| `tracker` | 21 | Tracker.autorun, Computation, Dependency, reactivity |
| `meteor_core` | 17 | Meteor.startup, settings, environment flags, promisify |
| `pubsub` | 15 | Meteor.publish, subscribe, publication lifecycle |
| `package_js` | 14 | Package.describe, api.use, Npm.depends |
| `methods` | 11 | Meteor.methods, callAsync, applyAsync, Error |
| `check` | 10 | check(), Match patterns and validators |
| `ejson` | 9 | EJSON serialization, custom types |
| `reactive_dict` | 9 | ReactiveDict get/set/equals/all |
| `webapp` | 7 | WebApp HTTP handlers, runtime config |
| `connections` | 5 | DDP.connect, Meteor.status, reconnect |
| `app_config` | 5 | App.info, accessRule, mobile config |
| `assets` | 5 | Assets.getText/getBinary (sync + async) |
| `ddp_rate_limiter` | 4 | DDPRateLimiter rules and configuration |
| `environment` | 4 | EnvironmentVariable, bindEnvironment |
| `timers` | 4 | Meteor.setTimeout/setInterval with env binding |
| `session` | 4 | Session get/set/equals |
| `reactive_var` | 3 | ReactiveVar get/set |
| `email_pkg` | 3 | Email.send, sendAsync, hookSend |

Plus **15 code example topics** and **10 architectural guides**.

## Quick Start

### Remote server (Docker)

```bash
git clone https://github.com/apitlekays/meteor-mcp.git
cd meteor-mcp
docker compose up -d --build
```

The server runs on port `8080` at `/mcp`.

### Local server (stdio)

```bash
pip install fastmcp==3.0.2
python local_server.py
```

## Client Configuration

### Claude Desktop / Claude Code

Add to your MCP settings:

```json
{
  "mcpServers": {
    "meteor": {
      "url": "http://YOUR_SERVER_IP:8080/mcp"
    }
  }
}
```

For local stdio mode:

```json
{
  "mcpServers": {
    "meteor": {
      "command": "python",
      "args": ["/path/to/meteor-mcp/local_server.py"]
    }
  }
}
```

### Cursor

Go to **Settings > MCP Servers > Add Server** and enter the URL:

```
http://YOUR_SERVER_IP:8080/mcp
```

## Project Structure

```
meteor-mcp/
├── server.py              # Remote MCP server (streamable-http, port 8080)
├── local_server.py        # Local MCP server (stdio, for dev/testing)
├── tools.py               # MCP tool definitions (5 tools)
├── search.py              # Score-based search engine
├── data/
│   ├── __init__.py        # Aggregates all modules into API_REGISTRY
│   ├── meteor_core.py     # Meteor.startup, settings, isClient/isServer, promisify
│   ├── methods.py         # Meteor.methods, call, callAsync, apply, Error
│   ├── pubsub.py          # Meteor.publish, subscribe, publication lifecycle
│   ├── collections.py     # Mongo.Collection, Cursor, ObjectID
│   ├── accounts.py        # Accounts, login, user management, OAuth
│   ├── connections.py     # DDP.connect, Meteor.status, reconnect
│   ├── check.py           # check(), Match patterns
│   ├── ejson.py           # EJSON serialization
│   ├── tracker.py         # Tracker.autorun, Computation, Dependency
│   ├── session.py         # Session get/set/equals
│   ├── reactive_var.py    # ReactiveVar
│   ├── reactive_dict.py   # ReactiveDict
│   ├── email_pkg.py       # Email.send, sendAsync, hooks
│   ├── assets.py          # Assets.getText/getBinary (sync + async)
│   ├── ddp_rate_limiter.py # DDPRateLimiter rules
│   ├── webapp.py          # WebApp HTTP handlers, runtime config
│   ├── app_config.py      # App.info, mobile configuration
│   ├── package_js.py      # Package.describe, onUse, Npm.depends
│   ├── timers.py          # Meteor.setTimeout/setInterval
│   ├── environment.py     # EnvironmentVariable, bindEnvironment
│   ├── examples.py        # 15 topics of annotated code examples
│   └── guides.py          # 10 conceptual architecture guides
├── Dockerfile
├── docker-compose.yml
└── requirements.txt       # fastmcp==3.0.2
```

## How It Works

All Meteor.js API documentation is embedded as Python dictionaries — no database, no network calls, no API keys. Each API entry contains:

- **name** and **signature** — the method name and call signature
- **description** — detailed explanation of behavior, parameters, and edge cases
- **params** — typed parameter list with optional flags
- **returns** — return type and description
- **environment** — `client`, `server`, or `anywhere`
- **is_reactive** — whether the API is a reactive data source
- **deprecated** — migration guidance for deprecated APIs
- **examples** — annotated code snippets showing real usage
- **tags** — keywords for search ranking

The search engine uses score-based ranking: exact name match (100pts) > partial name (50pts) > tag match (30pts) > description match (10pts).

## Deployment

### Docker on a VPS

```bash
ssh root@your-vps-ip
git clone https://github.com/apitlekays/meteor-mcp.git
cd meteor-mcp
docker compose up -d --build
```

Ensure port `8080` is open:

```bash
ufw allow 8080
```

### Health Check

The Docker container includes a health check. Verify it's running:

```bash
docker compose ps
```

### Behind a Reverse Proxy (nginx)

If you want HTTPS, put nginx in front:

```nginx
location /mcp {
    proxy_pass http://localhost:8080/mcp;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

## Tech Stack

- **Python 3.11** — runtime
- **FastMCP 3.0.2** — MCP server framework
- **Streamable HTTP** — transport protocol (port 8080)
- **Docker** — containerized deployment

## License

MIT
