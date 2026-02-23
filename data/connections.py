"""Meteor.js v3.4.0 DDP connection and server connection management APIs."""

CONNECTIONS = [
    {
        "name": "DDP.connect",
        "module": "connections",
        "signature": "DDP.connect(url, [options])",
        "description": (
            "Connect to the DDP server of a different Meteor application to "
            "subscribe to its publications and invoke its methods. Returns a "
            "connection object that provides the same API surface as the Meteor "
            "object itself, including methods like `subscribe`, `call`, `callAsync`, "
            "`apply`, `applyAsync`, `status`, `reconnect`, and `disconnect`. "
            "The connection is established asynchronously and will automatically "
            "retry on failure with increasing backoff. On the server, the DDP "
            "connection runs in its own async context and does not share the "
            "same login state as the client."
        ),
        "params": [
            {
                "name": "url",
                "type": "String",
                "description": (
                    "The URL of another Meteor application's DDP server, "
                    "for example 'https://other-app.example.com'."
                ),
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Optional connection settings. Supports `headers` (Object) "
                    "to specify custom HTTP headers sent with the initial "
                    "connection request."
                ),
                "optional": True,
            },
        ],
        "returns": (
            "Object -- A DDP connection object with methods: subscribe, call, "
            "callAsync, apply, applyAsync, status, reconnect, disconnect, and userId."
        ),
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Connect to a remote Meteor server",
                "code": (
                    "const remote = DDP.connect('https://other-app.example.com');\n"
                    "\n"
                    "// Subscribe to a publication on the remote server\n"
                    "remote.subscribe('posts');\n"
                    "\n"
                    "// Call a method on the remote server\n"
                    "const result = await remote.callAsync('getPost', postId);"
                ),
                "description": (
                    "Creates a DDP connection to another Meteor app and uses it "
                    "to subscribe to data and call remote methods."
                ),
            },
            {
                "title": "Use a remote connection with a Mongo collection",
                "code": (
                    "const remote = DDP.connect('https://analytics.example.com');\n"
                    "\n"
                    "// Bind a local collection to the remote connection\n"
                    "const AnalyticsEvents = new Mongo.Collection('events', {\n"
                    "  connection: remote,\n"
                    "});\n"
                    "\n"
                    "// Subscribe through the remote connection\n"
                    "remote.subscribe('recentEvents');\n"
                    "\n"
                    "// Query the collection locally (populated via the remote subscription)\n"
                    "const recent = await AnalyticsEvents.find({}, { sort: { createdAt: -1 } }).fetchAsync();"
                ),
                "description": (
                    "Binds a Mongo.Collection to a remote DDP connection so that "
                    "documents published by the remote server are stored locally "
                    "in that collection."
                ),
            },
        ],
        "tags": ["ddp", "connection", "remote", "subscribe", "methods"],
    },
    {
        "name": "Meteor.status",
        "module": "connections",
        "signature": "Meteor.status()",
        "description": (
            "Returns the current connection status of the client to its Meteor "
            "server. This method is reactive: when used inside a Tracker.autorun "
            "or a reactive computation, it will re-run when the connection status "
            "changes. The returned object contains the following fields: "
            "`connected` (Boolean) -- whether the client is currently connected; "
            "`status` (String) -- one of 'connected', 'connecting', 'failed', "
            "'waiting', or 'offline'; "
            "`retryCount` (Number) -- the number of reconnection attempts since "
            "the last successful connection; "
            "`retryTime` (Number or undefined) -- if status is 'waiting', the "
            "estimated timestamp (milliseconds since epoch) of the next "
            "reconnection attempt; "
            "`reason` (String or undefined) -- if status is 'failed', the reason "
            "for the failure."
        ),
        "params": [],
        "returns": (
            "Object -- { connected: Boolean, status: String, retryCount: Number, "
            "retryTime: Number | undefined, reason: String | undefined }"
        ),
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Display connection status reactively",
                "code": (
                    "Tracker.autorun(() => {\n"
                    "  const status = Meteor.status();\n"
                    "  console.log('Connection status:', status.status);\n"
                    "  console.log('Connected:', status.connected);\n"
                    "\n"
                    "  if (status.status === 'waiting') {\n"
                    "    const retryIn = Math.round((status.retryTime - Date.now()) / 1000);\n"
                    "    console.log(`Reconnecting in ${retryIn} seconds...`);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Uses a reactive computation to log connection status changes "
                    "and display the time until the next reconnection attempt."
                ),
            },
            {
                "title": "React component showing connection status",
                "code": (
                    "import { useTracker } from 'meteor/react-meteor-data';\n"
                    "\n"
                    "function ConnectionBanner() {\n"
                    "  const status = useTracker(() => Meteor.status());\n"
                    "\n"
                    "  if (status.connected) {\n"
                    "    return null;\n"
                    "  }\n"
                    "\n"
                    "  return (\n"
                    "    <div className=\"connection-banner\">\n"
                    "      {status.status === 'connecting' && <p>Connecting to server...</p>}\n"
                    "      {status.status === 'waiting' && (\n"
                    "        <p>\n"
                    "          Disconnected. Retrying shortly...\n"
                    "          <button onClick={() => Meteor.reconnect()}>Reconnect now</button>\n"
                    "        </p>\n"
                    "      )}\n"
                    "      {status.status === 'failed' && <p>Connection failed: {status.reason}</p>}\n"
                    "      {status.status === 'offline' && (\n"
                    "        <p>\n"
                    "          Offline.\n"
                    "          <button onClick={() => Meteor.reconnect()}>Go online</button>\n"
                    "        </p>\n"
                    "      )}\n"
                    "    </div>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "A React component that uses useTracker to reactively display "
                    "a banner when the client is not connected to the server."
                ),
            },
        ],
        "tags": ["connection", "status", "reactive", "client", "ddp"],
    },
    {
        "name": "Meteor.reconnect",
        "module": "connections",
        "signature": "Meteor.reconnect()",
        "description": (
            "Forces the client to attempt to reconnect to the server immediately. "
            "If the client is already connected, this method has no effect. If the "
            "client is in the 'waiting' state (waiting for a scheduled reconnection "
            "attempt), calling this method cancels the wait and tries to connect "
            "right away. If the client was previously disconnected by calling "
            "Meteor.disconnect(), calling Meteor.reconnect() will re-establish "
            "the connection. This method is commonly used in UI elements that "
            "allow users to manually trigger reconnection."
        ),
        "params": [],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Manual reconnect button",
                "code": (
                    "function ReconnectButton() {\n"
                    "  const { connected, status } = useTracker(() => Meteor.status());\n"
                    "\n"
                    "  if (connected) {\n"
                    "    return null;\n"
                    "  }\n"
                    "\n"
                    "  return (\n"
                    "    <button\n"
                    "      onClick={() => Meteor.reconnect()}\n"
                    "      disabled={status === 'connecting'}\n"
                    "    >\n"
                    "      {status === 'connecting' ? 'Connecting...' : 'Reconnect'}\n"
                    "    </button>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "A React component that renders a reconnect button only when "
                    "the client is disconnected. The button is disabled while a "
                    "connection attempt is in progress."
                ),
            },
            {
                "title": "Reconnect after going back online",
                "code": (
                    "// Listen for the browser coming back online\n"
                    "window.addEventListener('online', () => {\n"
                    "  console.log('Network restored, reconnecting...');\n"
                    "  Meteor.reconnect();\n"
                    "});"
                ),
                "description": (
                    "Automatically reconnects to the Meteor server when the "
                    "browser detects that the network connection has been restored."
                ),
            },
        ],
        "tags": ["connection", "reconnect", "client", "ddp", "network"],
    },
    {
        "name": "Meteor.disconnect",
        "module": "connections",
        "signature": "Meteor.disconnect()",
        "description": (
            "Disconnects the client from the server. While disconnected, no "
            "DDP messages are sent or received, subscriptions are not maintained, "
            "and method calls will be queued until the connection is re-established. "
            "Call Meteor.reconnect() to restore the connection. This is useful for "
            "applications that need to operate in an offline mode or want to "
            "conserve resources when the user is not actively using the app. "
            "After calling disconnect, Meteor.status().status will be 'offline'."
        ),
        "params": [],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Toggle online/offline mode",
                "code": (
                    "function ConnectionToggle() {\n"
                    "  const { connected, status } = useTracker(() => Meteor.status());\n"
                    "\n"
                    "  function toggleConnection() {\n"
                    "    if (connected) {\n"
                    "      Meteor.disconnect();\n"
                    "    } else {\n"
                    "      Meteor.reconnect();\n"
                    "    }\n"
                    "  }\n"
                    "\n"
                    "  return (\n"
                    "    <button onClick={toggleConnection}>\n"
                    "      {connected ? 'Go Offline' : 'Go Online'}\n"
                    "    </button>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "A React component that lets users toggle between online and "
                    "offline mode by connecting and disconnecting from the server."
                ),
            },
            {
                "title": "Disconnect on page visibility change",
                "code": (
                    "document.addEventListener('visibilitychange', () => {\n"
                    "  if (document.hidden) {\n"
                    "    // Disconnect when the tab is hidden to save resources\n"
                    "    Meteor.disconnect();\n"
                    "  } else {\n"
                    "    // Reconnect when the tab becomes visible again\n"
                    "    Meteor.reconnect();\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Automatically disconnects from the server when the browser "
                    "tab is hidden and reconnects when it becomes visible again, "
                    "reducing resource usage for background tabs."
                ),
            },
        ],
        "tags": ["connection", "disconnect", "offline", "client", "ddp"],
    },
    {
        "name": "Meteor.onConnection",
        "module": "connections",
        "signature": "Meteor.onConnection(callback)",
        "description": (
            "Registers a callback that is invoked each time a new DDP connection "
            "is established to the server. The callback receives a single argument: "
            "a connection object with the following fields: "
            "`id` (String) -- a globally unique identifier for this connection; "
            "`close` (Function) -- call this to close the DDP connection; "
            "`onClose` (Function) -- register a callback to be called when the "
            "connection is closed; "
            "`clientAddress` (String) -- the IP address of the connected client; "
            "`httpHeaders` (Object) -- the HTTP headers from the initial DDP "
            "WebSocket connection request. "
            "This is useful for logging, rate limiting, or associating metadata "
            "with specific client connections. The onClose callback can be used "
            "to clean up resources when the client disconnects."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "A function called with a connection object whenever a new "
                    "DDP client connects. The connection object has fields: id, "
                    "close, onClose, and clientAddress."
                ),
                "optional": False,
            },
        ],
        "returns": (
            "Object -- { stop: Function }. Call stop() to unregister the "
            "callback so it is no longer invoked for new connections."
        ),
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log client connections and disconnections",
                "code": (
                    "Meteor.onConnection((connection) => {\n"
                    "  console.log(`Client connected: ${connection.id} from ${connection.clientAddress}`);\n"
                    "\n"
                    "  connection.onClose(() => {\n"
                    "    console.log(`Client disconnected: ${connection.id}`);\n"
                    "  });\n"
                    "});"
                ),
                "description": (
                    "Logs a message each time a client connects to the server "
                    "and another message when the client disconnects."
                ),
            },
            {
                "title": "Track active connections",
                "code": (
                    "const activeConnections = new Map();\n"
                    "\n"
                    "Meteor.onConnection((connection) => {\n"
                    "  activeConnections.set(connection.id, {\n"
                    "    id: connection.id,\n"
                    "    address: connection.clientAddress,\n"
                    "    connectedAt: new Date(),\n"
                    "  });\n"
                    "\n"
                    "  connection.onClose(() => {\n"
                    "    activeConnections.delete(connection.id);\n"
                    "  });\n"
                    "});\n"
                    "\n"
                    "// Expose active connection count via a method\n"
                    "Meteor.methods({\n"
                    "  async getActiveConnectionCount() {\n"
                    "    return activeConnections.size;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Maintains a Map of active DDP connections on the server and "
                    "exposes the count through a Meteor method."
                ),
            },
            {
                "title": "Simple rate limiting by IP address",
                "code": (
                    "const connectionsByIp = new Map();\n"
                    "const MAX_CONNECTIONS_PER_IP = 10;\n"
                    "\n"
                    "Meteor.onConnection((connection) => {\n"
                    "  const ip = connection.clientAddress;\n"
                    "  const count = connectionsByIp.get(ip) || 0;\n"
                    "\n"
                    "  if (count >= MAX_CONNECTIONS_PER_IP) {\n"
                    "    console.warn(`Too many connections from ${ip}, closing.`);\n"
                    "    connection.close();\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  connectionsByIp.set(ip, count + 1);\n"
                    "\n"
                    "  connection.onClose(() => {\n"
                    "    const current = connectionsByIp.get(ip) || 1;\n"
                    "    if (current <= 1) {\n"
                    "      connectionsByIp.delete(ip);\n"
                    "    } else {\n"
                    "      connectionsByIp.set(ip, current - 1);\n"
                    "    }\n"
                    "  });\n"
                    "});"
                ),
                "description": (
                    "Limits the number of simultaneous DDP connections from a "
                    "single IP address and closes excess connections."
                ),
            },
        ],
        "tags": ["connection", "server", "ddp", "callback", "onConnection"],
    },
]
