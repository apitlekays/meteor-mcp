"""Meteor.js v3.4.0 Methods API data module.

Covers Meteor.methods, Meteor.call/callAsync, Meteor.apply/applyAsync,
Meteor.Error, and the method context properties (this.userId, this.isSimulation,
this.connection, this.unblock).
"""

METHODS = [
    {
        "name": "Meteor.methods",
        "module": "methods",
        "signature": "Meteor.methods(methods)",
        "description": (
            "Defines named functions that can be invoked over the network by clients "
            "using Meteor.callAsync. Each key in the methods object becomes a callable "
            "method name. Methods defined on the server execute on the server; methods "
            "defined on the client can act as stubs for optimistic UI. In Meteor v3, "
            "method functions can be async and should use await for any asynchronous work."
        ),
        "params": [
            {
                "name": "methods",
                "type": "Object",
                "description": (
                    "Dictionary whose keys are method names and values are functions. "
                    "Each function receives the arguments passed by the caller and can "
                    "access the method invocation context via 'this'."
                ),
                "optional": False,
            }
        ],
        "returns": "void",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Define async methods",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'tasks.insert'(text) {\n"
                    "    check(text, String);\n"
                    "\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized',\n"
                    "        'You must be logged in to create a task.');\n"
                    "    }\n"
                    "\n"
                    "    const taskId = await TasksCollection.insertAsync({\n"
                    "      text,\n"
                    "      createdAt: new Date(),\n"
                    "      owner: this.userId,\n"
                    "    });\n"
                    "\n"
                    "    return taskId;\n"
                    "  },\n"
                    "\n"
                    "  async 'tasks.remove'(taskId) {\n"
                    "    check(taskId, String);\n"
                    "\n"
                    "    const task = await TasksCollection.findOneAsync(taskId);\n"
                    "    if (!task) {\n"
                    "      throw new Meteor.Error('not-found', 'Task not found.');\n"
                    "    }\n"
                    "    if (task.owner !== this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized',\n"
                    "        'You can only remove your own tasks.');\n"
                    "    }\n"
                    "\n"
                    "    await TasksCollection.removeAsync(taskId);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Defines two async methods with authentication checks. In Meteor v3, "
                    "collection operations use their async variants (insertAsync, "
                    "findOneAsync, removeAsync)."
                ),
            },
            {
                "title": "Method with client-side stub for optimistic UI",
                "code": (
                    "// Shared code (runs on both client and server)\n"
                    "Meteor.methods({\n"
                    "  async 'messages.send'(conversationId, text) {\n"
                    "    check(conversationId, String);\n"
                    "    check(text, String);\n"
                    "\n"
                    "    const message = {\n"
                    "      conversationId,\n"
                    "      text,\n"
                    "      sender: this.userId,\n"
                    "      createdAt: new Date(),\n"
                    "    };\n"
                    "\n"
                    "    await MessagesCollection.insertAsync(message);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "When defined in shared code, the method runs as a stub on the client "
                    "for instant UI feedback, then the server re-runs it authoritatively. "
                    "The client stub result is replaced by the server result automatically."
                ),
            },
        ],
        "tags": ["methods", "rpc", "remote", "define", "server", "async"],
    },
    {
        "name": "Meteor.call",
        "module": "methods",
        "signature": "Meteor.call(name, ...args, asyncCallback)",
        "description": (
            "Invokes a method by name, passing any number of arguments. When called on "
            "the client, the method runs asynchronously and invokes asyncCallback with "
            "(error, result). When called on the server without a callback, it runs "
            "synchronously and returns the result or throws. This function does not "
            "return a Promise; use Meteor.callAsync for Promise-based usage. For methods "
            "with async stubs, prefer Meteor.callAsync."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": "Name of the method to invoke.",
                "optional": False,
            },
            {
                "name": "...args",
                "type": "any",
                "description": (
                    "Zero or more arguments to pass to the method. Arguments are "
                    "serialized with EJSON."
                ),
                "optional": True,
            },
            {
                "name": "asyncCallback",
                "type": "Function",
                "description": (
                    "Callback invoked with (error, result). If omitted on the server, "
                    "the call is synchronous. On the client, a callback is expected."
                ),
                "optional": True,
            },
        ],
        "returns": "any (when called synchronously on the server) or void",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Callback-style call",
                "code": (
                    "// Client-side usage\n"
                    "Meteor.call('tasks.insert', 'Buy groceries', (error, result) => {\n"
                    "  if (error) {\n"
                    "    console.error('Method failed:', error.reason);\n"
                    "  } else {\n"
                    "    console.log('Task created with id:', result);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "For methods with async stubs, prefer Meteor.callAsync which returns "
                    "a Promise and integrates with async/await."
                ),
            },
        ],
        "tags": ["methods", "rpc", "remote", "call", "callback"],
    },
    {
        "name": "Meteor.callAsync",
        "module": "methods",
        "signature": "Meteor.callAsync(name, ...args)",
        "description": (
            "Invokes a method by name and returns a Promise that resolves with the "
            "method's return value or rejects with a Meteor.Error. This is the "
            "recommended way to call methods in Meteor v3. On the client, the method "
            "stub (if defined) runs first for optimistic UI, then the server result "
            "replaces it. On the server, the call is awaited asynchronously."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": "Name of the method to invoke.",
                "optional": False,
            },
            {
                "name": "...args",
                "type": "any",
                "description": (
                    "Zero or more arguments to pass to the method. Arguments are "
                    "serialized with EJSON."
                ),
                "optional": True,
            },
        ],
        "returns": (
            "Promise<any> -- The returned Promise also exposes `stubPromise` "
            "(resolves when the client stub finishes) and `serverPromise` "
            "(resolves with the server result) properties on the client."
        ),
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Call a method with async/await",
                "code": (
                    "async function createTask(text) {\n"
                    "  try {\n"
                    "    const taskId = await Meteor.callAsync('tasks.insert', text);\n"
                    "    console.log('Task created:', taskId);\n"
                    "    return taskId;\n"
                    "  } catch (error) {\n"
                    "    console.error('Failed to create task:', error.reason);\n"
                    "  }\n"
                    "}"
                ),
                "description": (
                    "The recommended pattern in Meteor v3. Returns a Promise so it "
                    "works naturally with async/await."
                ),
            },
            {
                "title": "Call a method in a React event handler",
                "code": (
                    "const TaskForm = () => {\n"
                    "  const [text, setText] = useState('');\n"
                    "\n"
                    "  const handleSubmit = async (e) => {\n"
                    "    e.preventDefault();\n"
                    "    await Meteor.callAsync('tasks.insert', text);\n"
                    "    setText('');\n"
                    "  };\n"
                    "\n"
                    "  return (\n"
                    "    <form onSubmit={handleSubmit}>\n"
                    "      <input\n"
                    "        value={text}\n"
                    "        onChange={(e) => setText(e.target.value)}\n"
                    "        placeholder=\"Add a task\"\n"
                    "      />\n"
                    "      <button type=\"submit\">Add</button>\n"
                    "    </form>\n"
                    "  );\n"
                    "};"
                ),
                "description": (
                    "Using callAsync inside a React component's async event handler."
                ),
            },
        ],
        "tags": ["methods", "rpc", "remote", "call", "async", "promise"],
    },
    {
        "name": "Meteor.apply",
        "module": "methods",
        "signature": "Meteor.apply(name, args, options, asyncCallback)",
        "description": (
            "Like Meteor.call, but passes method arguments as an array and accepts an "
            "options object. The options parameter allows controlling behavior such as "
            "waiting for the server result, running without a stub, or setting a custom "
            "return value for the stub. For methods with async stubs, use "
            "Meteor.applyAsync instead."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": "Name of the method to invoke.",
                "optional": False,
            },
            {
                "name": "args",
                "type": "Array",
                "description": "Array of arguments to pass to the method.",
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Options object. Supported keys: 'wait' (Boolean) - block sending "
                    "subsequent methods until this one completes; 'onResultReceived' "
                    "(Function) - callback invoked with the method result before the "
                    "async callback; 'noRetry' (Boolean) - do not retry on network "
                    "failure; 'throwStubExceptions' (Boolean) - if true, stub exceptions "
                    "propagate instead of being logged; 'returnStubValue' (Boolean) - "
                    "if true, resolve with the stub return value instead of waiting for "
                    "the server."
                ),
                "optional": True,
            },
            {
                "name": "asyncCallback",
                "type": "Function",
                "description": "Callback invoked with (error, result).",
                "optional": True,
            },
        ],
        "returns": "any (when called synchronously on the server) or void",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Apply with options",
                "code": (
                    "Meteor.apply('tasks.insert', ['Buy groceries'], {\n"
                    "  wait: true,\n"
                    "  noRetry: true,\n"
                    "}, (error, result) => {\n"
                    "  if (error) {\n"
                    "    console.error(error.reason);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "For methods with async stubs, prefer Meteor.applyAsync for "
                    "Promise-based invocation with the same options."
                ),
            },
        ],
        "tags": ["methods", "rpc", "remote", "apply", "options"],
    },
    {
        "name": "Meteor.applyAsync",
        "module": "methods",
        "signature": "Meteor.applyAsync(name, args, options)",
        "description": (
            "Like Meteor.callAsync, but passes method arguments as an array and accepts "
            "an options object for fine-grained control. Returns a Promise that resolves "
            "with the method's return value or rejects with a Meteor.Error. This is the "
            "recommended replacement for Meteor.apply in Meteor v3."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": "Name of the method to invoke.",
                "optional": False,
            },
            {
                "name": "args",
                "type": "Array",
                "description": "Array of arguments to pass to the method.",
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Options object. Supported keys: 'wait' (Boolean) - block sending "
                    "subsequent methods until this one completes; 'onResultReceived' "
                    "(Function) - callback invoked with the method result; 'noRetry' "
                    "(Boolean) - do not retry on network failure; 'throwStubExceptions' "
                    "(Boolean) - if true, stub exceptions propagate instead of being "
                    "logged; 'returnStubValue' (Boolean) - if true, resolve with the "
                    "stub return value instead of waiting for the server."
                ),
                "optional": True,
            },
        ],
        "returns": "Promise<any>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Apply with wait option",
                "code": (
                    "const result = await Meteor.applyAsync(\n"
                    "  'tasks.batchInsert',\n"
                    "  [taskDataArray],\n"
                    "  { wait: true }\n"
                    ");\n"
                    "console.log('Batch insert completed:', result);"
                ),
                "description": (
                    "Calls a method with the 'wait' option, ensuring subsequent method "
                    "calls are not sent until this one completes."
                ),
            },
            {
                "title": "Apply with noRetry for non-idempotent operations",
                "code": (
                    "try {\n"
                    "  await Meteor.applyAsync(\n"
                    "    'payments.charge',\n"
                    "    [customerId, amount],\n"
                    "    { noRetry: true, wait: true }\n"
                    "  );\n"
                    "} catch (error) {\n"
                    "  console.error('Payment failed:', error.reason);\n"
                    "}"
                ),
                "description": (
                    "Using noRetry prevents Meteor from automatically retrying the "
                    "method call after a network disconnection, which is important "
                    "for non-idempotent operations like payment processing."
                ),
            },
        ],
        "tags": ["methods", "rpc", "remote", "apply", "async", "promise", "options"],
    },
    {
        "name": "Meteor.Error",
        "module": "methods",
        "signature": "Meteor.Error(error, reason, details)",
        "description": (
            "Creates a Meteor-specific error object that is transmitted to the client "
            "when thrown inside a method or publication. Unlike plain JavaScript errors, "
            "a Meteor.Error is serialized and sent over DDP so the client receives the "
            "error code, human-readable reason, and optional details. Use Meteor.Error "
            "for errors that the client should see; use standard Error for internal "
            "server errors that should not be exposed."
        ),
        "params": [
            {
                "name": "error",
                "type": "String | Number",
                "description": (
                    "A machine-readable error code string or number (e.g. 'not-authorized', "
                    "404). Conventionally a short, hyphenated string identifier."
                ),
                "optional": False,
            },
            {
                "name": "reason",
                "type": "String",
                "description": (
                    "A human-readable description of the error that can be shown to "
                    "the user."
                ),
                "optional": True,
            },
            {
                "name": "details",
                "type": "String",
                "description": (
                    "Additional machine-readable details, such as a JSON string with "
                    "field-level validation errors."
                ),
                "optional": True,
            },
        ],
        "returns": "Meteor.Error instance",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Throw an authorization error in a method",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'documents.update'(docId, changes) {\n"
                    "    check(docId, String);\n"
                    "    check(changes, Object);\n"
                    "\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error(\n"
                    "        'not-authorized',\n"
                    "        'You must be logged in to edit documents.'\n"
                    "      );\n"
                    "    }\n"
                    "\n"
                    "    const doc = await DocumentsCollection.findOneAsync(docId);\n"
                    "    if (!doc) {\n"
                    "      throw new Meteor.Error('not-found', 'Document not found.');\n"
                    "    }\n"
                    "\n"
                    "    await DocumentsCollection.updateAsync(docId, { $set: changes });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Throwing a Meteor.Error inside a method sends the error code and "
                    "reason to the client. Regular Error objects are sanitized to a "
                    "generic 'Internal server error' message for security."
                ),
            },
            {
                "title": "Error with validation details",
                "code": (
                    "const errors = { email: 'Invalid format', name: 'Required' };\n"
                    "\n"
                    "throw new Meteor.Error(\n"
                    "  'validation-error',\n"
                    "  'The form contains invalid fields.',\n"
                    "  JSON.stringify(errors)\n"
                    ");"
                ),
                "description": (
                    "The details parameter is useful for passing structured data such "
                    "as per-field validation errors. The client can parse the JSON "
                    "string from error.details."
                ),
            },
        ],
        "tags": ["methods", "error", "exception", "validation", "ddp"],
    },
    {
        "name": "this.userId",
        "module": "methods",
        "signature": "this.userId",
        "description": (
            "The id of the user who made this method call, or null if no user is "
            "logged in. Available inside a method body via 'this'. On the server, "
            "this corresponds to the user associated with the current DDP connection. "
            "In a client-side stub, this reflects the local user from Meteor.userId()."
        ),
        "params": [],
        "returns": "String | null",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Check user authentication in a method",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'posts.create'(title, body) {\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error(\n"
                    "        'not-authorized',\n"
                    "        'You must be logged in to create a post.'\n"
                    "      );\n"
                    "    }\n"
                    "\n"
                    "    return await PostsCollection.insertAsync({\n"
                    "      title,\n"
                    "      body,\n"
                    "      authorId: this.userId,\n"
                    "      createdAt: new Date(),\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "The most common use of this.userId is to verify that the caller "
                    "is authenticated before performing the operation."
                ),
            },
        ],
        "tags": ["methods", "context", "user", "authentication", "this"],
    },
    {
        "name": "this.isSimulation",
        "module": "methods",
        "signature": "this.isSimulation",
        "description": (
            "A Boolean indicating whether this method invocation is a simulation "
            "(client-side stub) rather than the authoritative server execution. When "
            "true, the method is running on the client as an optimistic UI preview. "
            "Use this to skip server-only side effects (such as sending emails or "
            "calling external APIs) during simulation."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Skip side effects during simulation",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'orders.place'(orderData) {\n"
                    "    check(orderData, OrderSchema);\n"
                    "\n"
                    "    const orderId = await OrdersCollection.insertAsync({\n"
                    "      ...orderData,\n"
                    "      status: 'pending',\n"
                    "      createdAt: new Date(),\n"
                    "      userId: this.userId,\n"
                    "    });\n"
                    "\n"
                    "    // Only send the email on the server, not in the stub\n"
                    "    if (!this.isSimulation) {\n"
                    "      const user = await Meteor.users.findOneAsync(this.userId);\n"
                    "      const email = user?.emails?.[0]?.address;\n"
                    "\n"
                    "      await Email.sendAsync({\n"
                    "        to: email,\n"
                    "        subject: 'Order Confirmation',\n"
                    "        text: `Your order ${orderId} has been placed.`,\n"
                    "      });\n"
                    "    }\n"
                    "\n"
                    "    return orderId;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "The insert runs in both the stub and on the server for optimistic "
                    "UI, but the email is only sent on the server where isSimulation "
                    "is false."
                ),
            },
        ],
        "tags": ["methods", "context", "simulation", "stub", "optimistic", "this"],
    },
    {
        "name": "this.connection",
        "module": "methods",
        "signature": "this.connection",
        "description": (
            "The DDP connection object on which the method was received, or null if "
            "the method was called directly on the server (not via DDP). The connection "
            "object has an 'id' property (the session ID), a 'clientAddress' property "
            "(the client's IP address), and an 'httpHeaders' property (the HTTP headers "
            "from the initial connection). Useful for rate limiting, IP-based access "
            "control, or per-connection state."
        ),
        "params": [],
        "returns": "Object | null",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Access client IP and connection metadata",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'analytics.logEvent'(eventName, data) {\n"
                    "    check(eventName, String);\n"
                    "\n"
                    "    const clientIp = this.connection?.clientAddress || 'unknown';\n"
                    "    const sessionId = this.connection?.id;\n"
                    "\n"
                    "    await AnalyticsCollection.insertAsync({\n"
                    "      eventName,\n"
                    "      data,\n"
                    "      clientIp,\n"
                    "      sessionId,\n"
                    "      userId: this.userId,\n"
                    "      createdAt: new Date(),\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Accesses the client's IP address and DDP session ID from the "
                    "connection object for analytics tracking."
                ),
            },
            {
                "title": "Per-connection rate limiting",
                "code": (
                    "const rateLimitMap = new Map();\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async 'messages.send'(channelId, text) {\n"
                    "    check(channelId, String);\n"
                    "    check(text, String);\n"
                    "\n"
                    "    const connId = this.connection?.id;\n"
                    "    if (connId) {\n"
                    "      const lastCall = rateLimitMap.get(connId) || 0;\n"
                    "      if (Date.now() - lastCall < 1000) {\n"
                    "        throw new Meteor.Error(\n"
                    "          'rate-limited',\n"
                    "          'Please wait before sending another message.'\n"
                    "        );\n"
                    "      }\n"
                    "      rateLimitMap.set(connId, Date.now());\n"
                    "    }\n"
                    "\n"
                    "    await MessagesCollection.insertAsync({\n"
                    "      channelId,\n"
                    "      text,\n"
                    "      sender: this.userId,\n"
                    "      createdAt: new Date(),\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Uses the connection ID to implement simple per-connection rate "
                    "limiting. For production use, consider the ddp-rate-limiter package."
                ),
            },
        ],
        "tags": ["methods", "context", "connection", "ddp", "ip", "session", "this"],
    },
    {
        "name": "this.unblock",
        "module": "methods",
        "signature": "this.unblock()",
        "description": (
            "Call this inside a method body to allow the next method from the same "
            "client to begin running before this method has finished. By default, "
            "Meteor serializes method calls from each client so that they run one at "
            "a time in order. Calling this.unblock() tells the server it is safe to "
            "start processing the next queued method without waiting for the current "
            "one to return. Useful for long-running methods that do not need to block "
            "subsequent calls."
        ),
        "params": [],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Unblock a long-running method",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'reports.generate'(reportType, filters) {\n"
                    "    check(reportType, String);\n"
                    "    check(filters, Object);\n"
                    "\n"
                    "    // Allow subsequent methods from this client to run\n"
                    "    this.unblock();\n"
                    "\n"
                    "    const data = await aggregateReportData(reportType, filters);\n"
                    "    const pdfBuffer = await generatePDF(data);\n"
                    "\n"
                    "    const fileId = await ReportsCollection.insertAsync({\n"
                    "      type: reportType,\n"
                    "      filters,\n"
                    "      pdf: pdfBuffer,\n"
                    "      generatedBy: this.userId,\n"
                    "      createdAt: new Date(),\n"
                    "    });\n"
                    "\n"
                    "    return fileId;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Calling this.unblock() early in the method allows the client's "
                    "other method calls to proceed without waiting for the slow report "
                    "generation to finish."
                ),
            },
            {
                "title": "Unblock before external API calls",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'integrations.syncWithCRM'(contactId) {\n"
                    "    check(contactId, String);\n"
                    "    this.unblock();\n"
                    "\n"
                    "    const contact = await ContactsCollection.findOneAsync(contactId);\n"
                    "    if (!contact) {\n"
                    "      throw new Meteor.Error('not-found', 'Contact not found.');\n"
                    "    }\n"
                    "\n"
                    "    // External HTTP call that may be slow\n"
                    "    const response = await fetch('https://api.crm.example.com/sync', {\n"
                    "      method: 'POST',\n"
                    "      headers: { 'Content-Type': 'application/json' },\n"
                    "      body: JSON.stringify(contact),\n"
                    "    });\n"
                    "\n"
                    "    const result = await response.json();\n"
                    "\n"
                    "    await ContactsCollection.updateAsync(contactId, {\n"
                    "      $set: { crmId: result.id, lastSynced: new Date() },\n"
                    "    });\n"
                    "\n"
                    "    return result.id;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "External API calls are a common reason to unblock. The CRM sync "
                    "may take seconds, but other methods from this client should not "
                    "be held up."
                ),
            },
        ],
        "tags": ["methods", "context", "unblock", "concurrency", "performance", "this"],
    },
    {
        "name": "Meteor.isAsyncCall",
        "module": "methods",
        "signature": "Meteor.isAsyncCall()",
        "description": (
            "Returns true if the current method invocation was made via "
            "Meteor.callAsync or Meteor.applyAsync, and false if it was made "
            "via Meteor.call or Meteor.apply. This is useful inside a method "
            "body to distinguish between async and sync callers and adjust "
            "behavior accordingly, such as returning a value directly for "
            "sync callers or performing additional async work for async callers."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Detect async vs sync caller",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'data.fetch'(query) {\n"
                    "    check(query, Object);\n"
                    "\n"
                    "    if (Meteor.isAsyncCall()) {\n"
                    "      // Caller used callAsync — safe to do async work\n"
                    "      const results = await DataCollection.find(query).fetchAsync();\n"
                    "      return results;\n"
                    "    }\n"
                    "\n"
                    "    // Caller used call — return minimal data\n"
                    "    return { message: 'Use callAsync for full results' };\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Uses Meteor.isAsyncCall() inside a method to provide "
                    "different behavior depending on whether the caller used "
                    "callAsync or the legacy call."
                ),
            },
        ],
        "tags": ["methods", "async", "context", "server", "v3"],
    },
]
