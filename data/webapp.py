"""WebApp API entries for Meteor.js v3.4.0."""

WEBAPP = [
    {
        "name": "WebApp.connectHandlers",
        "module": "webapp",
        "signature": "WebApp.connectHandlers",
        "description": (
            "The main connect middleware stack used by Meteor's HTTP server to "
            "handle incoming requests. WebApp.connectHandlers is the canonical "
            "name documented in the official Meteor API. WebApp.handlers is "
            "available as an alias for backward compatibility. This is a "
            "standard connect-compatible middleware stack that runs after "
            "Meteor's built-in middleware (such as static file serving and "
            "the DDP WebSocket handler). Use WebApp.connectHandlers to add "
            "custom routes, REST API endpoints, or any HTTP middleware to "
            "your Meteor application. Middleware added here has access to "
            "parsed request bodies and cookies. In Meteor v3, handler "
            "functions can be async."
        ),
        "params": [],
        "returns": "connect.Server",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Add a REST API endpoint",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.handlers.use('/api/health', (req, res) => {\n"
                    "  res.writeHead(200, { 'Content-Type': 'application/json' });\n"
                    "  res.end(JSON.stringify({ status: 'ok', timestamp: Date.now() }));\n"
                    "});"
                ),
                "description": (
                    "Add a simple health-check endpoint. Middleware added via "
                    "WebApp.handlers runs after Meteor's own middleware, so "
                    "static assets and DDP are already handled."
                ),
            },
            {
                "title": "Add Express-style middleware for JSON parsing",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "import express from 'express';\n"
                    "\n"
                    "const app = express();\n"
                    "app.use(express.json());\n"
                    "\n"
                    "app.post('/api/webhooks/stripe', async (req, res) => {\n"
                    "  const event = req.body;\n"
                    "  console.log('Received Stripe event:', event.type);\n"
                    "\n"
                    "  // Process the webhook event\n"
                    "  await processStripeEvent(event);\n"
                    "\n"
                    "  res.status(200).json({ received: true });\n"
                    "});\n"
                    "\n"
                    "WebApp.handlers.use(app);"
                ),
                "description": (
                    "Mount a full Express app onto Meteor's connect stack. "
                    "This is a common pattern for building REST APIs alongside "
                    "Meteor's DDP-based data layer."
                ),
            },
        ],
        "tags": ["http", "middleware", "connect", "connectHandlers", "rest", "api", "server", "handlers"],
    },
    {
        "name": "WebApp.rawConnectHandlers",
        "module": "webapp",
        "signature": "WebApp.rawConnectHandlers",
        "description": (
            "A connect middleware stack that runs before all of Meteor's "
            "built-in middleware. Unlike connectHandlers, middleware added "
            "here executes before static file serving, DDP WebSocket "
            "handling, and cookie parsing. Use rawConnectHandlers when you "
            "need to intercept requests at the earliest possible stage, "
            "such as adding CORS headers, implementing rate limiting, "
            "or handling custom authentication before Meteor processes "
            "the request."
        ),
        "params": [],
        "returns": "connect.Server",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Add CORS headers to all requests",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.rawConnectHandlers.use((req, res, next) => {\n"
                    "  res.setHeader('Access-Control-Allow-Origin', '*');\n"
                    "  res.setHeader(\n"
                    "    'Access-Control-Allow-Headers',\n"
                    "    'Origin, X-Requested-With, Content-Type, Accept'\n"
                    "  );\n"
                    "  res.setHeader(\n"
                    "    'Access-Control-Allow-Methods',\n"
                    "    'GET, POST, PUT, DELETE, OPTIONS'\n"
                    "  );\n"
                    "\n"
                    "  if (req.method === 'OPTIONS') {\n"
                    "    res.writeHead(204);\n"
                    "    res.end();\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  next();\n"
                    "});"
                ),
                "description": (
                    "CORS headers must be set before Meteor's middleware "
                    "processes the request, so rawConnectHandlers is the "
                    "appropriate place for this."
                ),
            },
            {
                "title": "Simple rate limiting middleware",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "const requestCounts = new Map();\n"
                    "\n"
                    "WebApp.rawConnectHandlers.use((req, res, next) => {\n"
                    "  const ip = req.socket.remoteAddress;\n"
                    "  const count = requestCounts.get(ip) || 0;\n"
                    "\n"
                    "  if (count > 100) {\n"
                    "    res.writeHead(429, { 'Content-Type': 'text/plain' });\n"
                    "    res.end('Too Many Requests');\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  requestCounts.set(ip, count + 1);\n"
                    "  setTimeout(() => requestCounts.delete(ip), 60000);\n"
                    "\n"
                    "  next();\n"
                    "});"
                ),
                "description": (
                    "Rate limiting is best applied via rawConnectHandlers "
                    "to reject excessive requests before Meteor expends "
                    "resources processing them."
                ),
            },
        ],
        "tags": ["http", "middleware", "connect", "cors", "raw", "server"],
    },
    {
        "name": "WebApp.httpServer",
        "module": "webapp",
        "signature": "WebApp.httpServer",
        "description": (
            "The underlying Node.js http.Server instance used by Meteor. "
            "This gives direct access to the HTTP server object, which is "
            "useful for attaching WebSocket servers (such as ws or "
            "socket.io), listening for low-level server events like "
            "'upgrade' or 'connection', or integrating with libraries that "
            "require a raw Node.js HTTP server reference. The server is "
            "already listening on the port specified by the PORT environment "
            "variable when accessed in Meteor.startup."
        ),
        "params": [],
        "returns": "http.Server",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Attach a WebSocket server using the ws library",
                "code": (
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { WebApp } from 'meteor/webapp';\n"
                    "import { WebSocketServer } from 'ws';\n"
                    "\n"
                    "Meteor.startup(() => {\n"
                    "  const wss = new WebSocketServer({\n"
                    "    server: WebApp.httpServer,\n"
                    "    path: '/ws/live',\n"
                    "  });\n"
                    "\n"
                    "  wss.on('connection', (ws) => {\n"
                    "    console.log('New WebSocket connection');\n"
                    "\n"
                    "    ws.on('message', (message) => {\n"
                    "      console.log('Received:', message.toString());\n"
                    "      ws.send(JSON.stringify({ echo: message.toString() }));\n"
                    "    });\n"
                    "\n"
                    "    ws.on('close', () => {\n"
                    "      console.log('WebSocket connection closed');\n"
                    "    });\n"
                    "  });\n"
                    "});"
                ),
                "description": (
                    "Mount a separate WebSocket server on a custom path "
                    "alongside Meteor's DDP WebSocket. This is useful for "
                    "real-time features that do not need Meteor's pub/sub."
                ),
            },
            {
                "title": "Log active connections",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.httpServer.on('connection', (socket) => {\n"
                    "  console.log('New TCP connection from', socket.remoteAddress);\n"
                    "});"
                ),
                "description": (
                    "Listen for low-level TCP connection events on the "
                    "underlying HTTP server for monitoring or debugging."
                ),
            },
        ],
        "tags": ["http", "server", "websocket", "node", "low-level"],
    },
    {
        "name": "WebApp.onListening",
        "module": "webapp",
        "signature": "WebApp.onListening(callback)",
        "description": (
            "Register a callback to be invoked when Meteor's HTTP server "
            "begins listening for connections. The callback receives no "
            "arguments. Use this to perform initialization that depends on "
            "the server being ready to accept requests, such as logging "
            "the bound address and port, registering with a service "
            "discovery system, or notifying a process manager that the "
            "application is ready. If the server is already listening when "
            "the callback is registered, it fires immediately."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "A function invoked once the HTTP server is listening. "
                    "Receives no arguments."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log the server address on startup",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.onListening(() => {\n"
                    "  const address = WebApp.httpServer.address();\n"
                    "  console.log(\n"
                    "    `Meteor server listening on ${address.address}:${address.port}`\n"
                    "  );\n"
                    "});"
                ),
                "description": (
                    "Use onListening to log the exact address and port "
                    "Meteor is bound to, which is especially useful when "
                    "the port is dynamically assigned."
                ),
            },
            {
                "title": "Notify a process manager that the app is ready",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.onListening(() => {\n"
                    "  if (process.send) {\n"
                    "    process.send('ready');\n"
                    "  }\n"
                    "  console.log('Application is ready to accept connections');\n"
                    "});"
                ),
                "description": (
                    "When running under a process manager like PM2 in cluster "
                    "mode, send a 'ready' signal once the server is listening."
                ),
            },
        ],
        "tags": ["http", "server", "startup", "lifecycle", "listening"],
    },
    {
        "name": "WebApp.addRuntimeConfigHook",
        "module": "webapp",
        "signature": "WebApp.addRuntimeConfigHook(hook)",
        "description": (
            "Add a hook function that can modify the __meteor_runtime_config__ "
            "object before it is sent to the client. The runtime config is a "
            "JSON-encoded string embedded in the initial HTML page that "
            "provides configuration to the client, including "
            "Meteor.settings.public, the ROOT_URL, and DDP connection "
            "information. The hook function receives an object with 'arch' "
            "(the client architecture, e.g., 'web.browser'), 'request' (the "
            "incoming HTTP request), 'encodedCurrentConfig' (the current "
            "JSON-encoded config string), and 'updated' (a callback to call "
            "with the new JSON-encoded config string). To modify the config, "
            "parse encodedCurrentConfig, apply changes, then call "
            "updated(newEncodedConfig). This is useful for injecting "
            "per-request or per-architecture configuration values into "
            "the client bundle."
        ),
        "params": [
            {
                "name": "hook",
                "type": "Function",
                "description": (
                    "A function that receives "
                    "{ arch, request, encodedCurrentConfig, updated }. "
                    "The arch string identifies the client architecture "
                    "(e.g., 'web.browser', 'web.browser.legacy'). The "
                    "request is the incoming HTTP request object. "
                    "encodedCurrentConfig is the current JSON-encoded "
                    "runtime config string. Call updated(newEncodedConfig) "
                    "with the modified JSON-encoded config string to apply "
                    "changes."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Inject custom configuration per client architecture",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.addRuntimeConfigHook(\n"
                    "  ({ arch, request, encodedCurrentConfig, updated }) => {\n"
                    "    const config = JSON.parse(encodedCurrentConfig);\n"
                    "\n"
                    "    config.customFeatureFlags = {\n"
                    "      enableNewDashboard: true,\n"
                    "      maxUploadSize: 10485760,\n"
                    "    };\n"
                    "\n"
                    "    if (arch === 'web.browser.legacy') {\n"
                    "      config.customFeatureFlags.enableNewDashboard = false;\n"
                    "    }\n"
                    "\n"
                    "    updated(JSON.stringify(config));\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Parse the encoded config, add custom feature flags, and "
                    "call updated() with the new JSON string. On the client, "
                    "access them via "
                    "__meteor_runtime_config__.customFeatureFlags."
                ),
            },
            {
                "title": "Inject server timestamp into client config",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.addRuntimeConfigHook(\n"
                    "  ({ encodedCurrentConfig, updated }) => {\n"
                    "    const config = JSON.parse(encodedCurrentConfig);\n"
                    "    config.serverStartedAt = Date.now();\n"
                    "    updated(JSON.stringify(config));\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Embed a server-side value into the runtime config so "
                    "the client can access it immediately on load without "
                    "a round-trip."
                ),
            },
        ],
        "tags": ["http", "config", "runtime", "client", "hook", "server"],
    },
    {
        "name": "WebApp.addUpdatedNotifyHook",
        "module": "webapp",
        "signature": "WebApp.addUpdatedNotifyHook(hook)",
        "description": (
            "Register a hook function that is called when the client bundle "
            "has been updated (e.g., during hot code push in development or "
            "after a new deployment). The hook receives an object with "
            "'arch' (the client architecture string), 'manifest' (the new "
            "client asset manifest), and 'runtimeConfig' (the current "
            "runtime configuration object). The hook should return true if "
            "the update notification should proceed to connected clients, "
            "or false to suppress the notification. This is useful for "
            "controlling when clients are told to reload, such as delaying "
            "updates during peak usage or coordinating blue-green "
            "deployments."
        ),
        "params": [
            {
                "name": "hook",
                "type": "Function",
                "description": (
                    "A function that receives "
                    "{ arch, manifest, runtimeConfig } when a client bundle "
                    "update is detected. The arch string identifies the "
                    "client architecture (e.g., 'web.browser'). The manifest "
                    "is the new client asset manifest. The runtimeConfig is "
                    "the current runtime configuration object. Return true "
                    "to allow the update notification to propagate to "
                    "clients, or false to suppress it."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log client bundle updates",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.addUpdatedNotifyHook(({ arch, manifest }) => {\n"
                    "  console.log(\n"
                    "    `Client bundle for ${arch} updated at `\n"
                    "    + `${new Date().toISOString()} `\n"
                    "    + `with ${manifest.length} assets`\n"
                    "  );\n"
                    "  return true;\n"
                    "});"
                ),
                "description": (
                    "Log each time the server detects an updated client "
                    "bundle, including the architecture and asset count, "
                    "then allow the notification to proceed."
                ),
            },
            {
                "title": "Delay hot code push during peak hours",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.addUpdatedNotifyHook(({ arch }) => {\n"
                    "  const hour = new Date().getHours();\n"
                    "  const isPeakHour = hour >= 9 && hour <= 17;\n"
                    "\n"
                    "  if (isPeakHour) {\n"
                    "    console.log(\n"
                    "      `Suppressing hot code push for ${arch} during peak hours`\n"
                    "    );\n"
                    "    return false;\n"
                    "  }\n"
                    "\n"
                    "  return true;\n"
                    "});"
                ),
                "description": (
                    "Suppress automatic client reload notifications during "
                    "business hours to avoid disrupting active users."
                ),
            },
        ],
        "tags": ["http", "hot-code-push", "deployment", "update", "hook", "server"],
    },
    {
        "name": "WebApp.addHtmlAttributeHook",
        "module": "webapp",
        "signature": "WebApp.addHtmlAttributeHook(hook)",
        "description": (
            "Register a hook function that can add or modify attributes on "
            "the <html> tag of the initial HTML page served to the client. "
            "The hook receives a 'request' object (the Node.js "
            "IncomingMessage) and should return an object whose keys are "
            "attribute names and values are attribute values. Multiple hooks "
            "are merged, with later hooks overriding earlier ones for the "
            "same attribute. This is commonly used to set the 'lang' "
            "attribute based on the user's locale, add 'dir' for "
            "right-to-left languages, or inject data attributes."
        ),
        "params": [
            {
                "name": "hook",
                "type": "Function",
                "description": (
                    "A function that receives the HTTP request object and "
                    "returns an object of HTML attribute key-value pairs "
                    "to apply to the <html> tag."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Set the lang attribute based on Accept-Language header",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.addHtmlAttributeHook((request) => {\n"
                    "  const acceptLang = request.headers['accept-language'] || '';\n"
                    "  const primaryLang = acceptLang.split(',')[0].split('-')[0] || 'en';\n"
                    "\n"
                    "  return { lang: primaryLang };\n"
                    "});"
                ),
                "description": (
                    "Parse the Accept-Language header to determine the "
                    "user's preferred language and set it on the <html> tag "
                    "for accessibility and SEO."
                ),
            },
            {
                "title": "Add right-to-left support for Arabic and Hebrew",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "const RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur'];\n"
                    "\n"
                    "WebApp.addHtmlAttributeHook((request) => {\n"
                    "  const acceptLang = request.headers['accept-language'] || '';\n"
                    "  const primaryLang = acceptLang.split(',')[0].split('-')[0];\n"
                    "  const attrs = { lang: primaryLang || 'en' };\n"
                    "\n"
                    "  if (RTL_LANGUAGES.includes(primaryLang)) {\n"
                    "    attrs.dir = 'rtl';\n"
                    "  }\n"
                    "\n"
                    "  return attrs;\n"
                    "});"
                ),
                "description": (
                    "Set both the lang and dir attributes on the <html> "
                    "tag to properly support right-to-left languages."
                ),
            },
        ],
        "tags": ["http", "html", "i18n", "locale", "hook", "server", "accessibility"],
    },
]
