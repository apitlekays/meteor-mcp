"""Meteor environment API entries for Meteor.js v3.4.0."""

ENVIRONMENT = [
    {
        "name": "new Meteor.EnvironmentVariable()",
        "module": "environment",
        "signature": "new Meteor.EnvironmentVariable()",
        "description": (
            "Construct a new Meteor.EnvironmentVariable. Environment "
            "variables in Meteor provide a mechanism for dynamically "
            "scoped variables, similar to thread-local storage in "
            "other languages. They allow you to set a value that is "
            "visible to all code called within a specific execution "
            "context without explicitly passing it through every "
            "function call. This is the foundation of how Meteor "
            "tracks the current user, connection, and other "
            "contextual data across async boundaries. In Meteor v3, "
            "environment variables work with the async/await model "
            "and are propagated across awaited calls within the same "
            "logical execution context. The constructor takes no "
            "arguments and creates an environment variable with no "
            "initial value (undefined)."
        ),
        "params": [],
        "returns": "Meteor.EnvironmentVariable",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Creating a custom environment variable for request tracing",
                "code": (
                    "const currentRequestId =\n"
                    "  new Meteor.EnvironmentVariable();\n"
                    "\n"
                    "function logWithContext(message) {\n"
                    "  const requestId = currentRequestId.get();\n"
                    "  console.log(`[${requestId || 'no-context'}] ${message}`);\n"
                    "}\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async processOrder(orderData) {\n"
                    "    const requestId = Random.id();\n"
                    "\n"
                    "    return currentRequestId.withValue(\n"
                    "      requestId,\n"
                    "      async () => {\n"
                    "        logWithContext('Processing order');\n"
                    "        await validateOrder(orderData);\n"
                    "        logWithContext('Order validated');\n"
                    "        const id = await Orders.insertAsync(orderData);\n"
                    "        logWithContext(`Order created: ${id}`);\n"
                    "        return id;\n"
                    "      }\n"
                    "    );\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Create an environment variable to carry a request "
                    "ID through deeply nested function calls without "
                    "passing it as an explicit parameter. Every function "
                    "in the call chain can access the request ID via "
                    "currentRequestId.get()."
                ),
            },
            {
                "title": "Environment variable for feature flags",
                "code": (
                    "const featureFlags =\n"
                    "  new Meteor.EnvironmentVariable();\n"
                    "\n"
                    "function isFeatureEnabled(name) {\n"
                    "  const flags = featureFlags.get() || {};\n"
                    "  return flags[name] === true;\n"
                    "}\n"
                    "\n"
                    "// Run a block of code with specific feature flags\n"
                    "featureFlags.withValue(\n"
                    "  { newCheckout: true, darkMode: false },\n"
                    "  () => {\n"
                    "    console.log(isFeatureEnabled('newCheckout'));\n"
                    "    // => true\n"
                    "    console.log(isFeatureEnabled('darkMode'));\n"
                    "    // => false\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Environment variables can hold any value, including "
                    "objects. This pattern scopes feature flags to a "
                    "specific execution context."
                ),
            },
        ],
        "tags": ["environment", "context", "dynamic-scope", "constructor"],
    },
    {
        "name": "EnvironmentVariable.get",
        "module": "environment",
        "signature": "EnvironmentVariable.get()",
        "description": (
            "Return the current value of the environment variable in "
            "the active execution context. If the code is running "
            "inside a withValue callback, get() returns the value "
            "that was passed to withValue. If the code is running "
            "outside any withValue scope, get() returns undefined. "
            "This method is synchronous and can be called from "
            "anywhere. In Meteor v3, the value is correctly "
            "propagated across async/await boundaries within the "
            "same logical context, so calling get() after an await "
            "inside a withValue callback still returns the correct "
            "value."
        ),
        "params": [],
        "returns": "any",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Reading an environment variable in a helper function",
                "code": (
                    "const currentLocale =\n"
                    "  new Meteor.EnvironmentVariable();\n"
                    "\n"
                    "function translate(key) {\n"
                    "  const locale = currentLocale.get() || 'en';\n"
                    "  return translations[locale][key] || key;\n"
                    "}\n"
                    "\n"
                    "// Usage inside a withValue scope\n"
                    "currentLocale.withValue('fr', () => {\n"
                    "  console.log(translate('hello'));\n"
                    "  // => 'bonjour'\n"
                    "});\n"
                    "\n"
                    "// Outside any withValue scope\n"
                    "console.log(currentLocale.get());\n"
                    "// => undefined"
                ),
                "description": (
                    "get() returns the value set by the nearest enclosing "
                    "withValue call, or undefined if none is active."
                ),
            },
            {
                "title": "Accessing environment variable after async operations",
                "code": (
                    "const auditContext =\n"
                    "  new Meteor.EnvironmentVariable();\n"
                    "\n"
                    "async function performAuditedAction() {\n"
                    "  const ctx = auditContext.get();\n"
                    "  console.log(`Audit user: ${ctx.userId}`);\n"
                    "\n"
                    "  await someAsyncWork();\n"
                    "\n"
                    "  // Still accessible after await in Meteor v3\n"
                    "  const ctxAfter = auditContext.get();\n"
                    "  console.log(`Still same user: ${ctxAfter.userId}`);\n"
                    "}\n"
                    "\n"
                    "auditContext.withValue(\n"
                    "  { userId: 'abc123', action: 'update' },\n"
                    "  () => performAuditedAction()\n"
                    ");"
                ),
                "description": (
                    "In Meteor v3, environment variable values are "
                    "propagated across await boundaries, so get() "
                    "returns the correct value even after async calls."
                ),
            },
        ],
        "tags": ["environment", "context", "read", "dynamic-scope"],
    },
    {
        "name": "EnvironmentVariable.withValue",
        "module": "environment",
        "signature": "EnvironmentVariable.withValue(value, func, [options])",
        "description": (
            "Run a function with the environment variable set to the "
            "given value. Within the execution of func, calling get() "
            "on this environment variable returns value. After func "
            "completes, the environment variable reverts to its "
            "previous value. Calls to withValue can be nested, and "
            "each nested call creates a new scope that shadows the "
            "outer value. In Meteor v3, func can be an async function "
            "and the environment variable value is correctly "
            "maintained across await boundaries within that function. "
            "The return value of withValue is the return value of "
            "func, which means for async functions it returns a "
            "Promise."
        ),
        "params": [
            {
                "name": "value",
                "type": "any",
                "description": (
                    "The value to set the environment variable to for "
                    "the duration of the function call."
                ),
                "optional": False,
            },
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "The function to run with the environment variable "
                    "set to value. May be synchronous or async."
                ),
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Optional additional properties for configuring "
                    "async local storage (ALS) behavior. This is a "
                    "Meteor v3 addition for advanced use cases "
                    "involving custom ALS context propagation."
                ),
                "optional": True,
            },
        ],
        "returns": "any",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Scoping a database context for multi-tenancy",
                "code": (
                    "const currentTenant =\n"
                    "  new Meteor.EnvironmentVariable();\n"
                    "\n"
                    "async function getTenantProducts() {\n"
                    "  const tenant = currentTenant.get();\n"
                    "  return await Products.find(\n"
                    "    { tenantId: tenant }\n"
                    "  ).fetchAsync();\n"
                    "}\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async listProducts() {\n"
                    "    const user = await Meteor.userAsync();\n"
                    "    const tenantId = user.profile.tenantId;\n"
                    "\n"
                    "    return currentTenant.withValue(\n"
                    "      tenantId,\n"
                    "      async () => {\n"
                    "        const products = await getTenantProducts();\n"
                    "        return products;\n"
                    "      }\n"
                    "    );\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Use withValue to scope a tenant ID for the "
                    "duration of a method call. All functions called "
                    "within the withValue callback can access the "
                    "tenant ID via get() without explicit parameter "
                    "passing."
                ),
            },
            {
                "title": "Nested withValue scopes",
                "code": (
                    "const logLevel =\n"
                    "  new Meteor.EnvironmentVariable();\n"
                    "\n"
                    "function log(message) {\n"
                    "  const level = logLevel.get() || 'info';\n"
                    "  console.log(`[${level}] ${message}`);\n"
                    "}\n"
                    "\n"
                    "logLevel.withValue('info', () => {\n"
                    "  log('Starting process');\n"
                    "  // => [info] Starting process\n"
                    "\n"
                    "  logLevel.withValue('debug', () => {\n"
                    "    log('Detailed step');\n"
                    "    // => [debug] Detailed step\n"
                    "  });\n"
                    "\n"
                    "  log('Continuing process');\n"
                    "  // => [info] Continuing process\n"
                    "});"
                ),
                "description": (
                    "Nested withValue calls create layered scopes. "
                    "The inner scope shadows the outer value, and when "
                    "the inner scope exits, the outer value is restored."
                ),
            },
        ],
        "tags": ["environment", "context", "scope", "dynamic-scope"],
    },
    {
        "name": "Meteor.bindEnvironment",
        "module": "environment",
        "signature": "Meteor.bindEnvironment(func, onException, _this)",
        "description": (
            "Capture the current Meteor environment and return a new "
            "function that, when called, runs the original function "
            "within that captured environment. This is essential when "
            "passing callbacks to non-Meteor APIs (such as Node.js "
            "event emitters, third-party libraries, or native "
            "setTimeout) that would otherwise lose the Meteor "
            "environment context. The returned wrapper function "
            "restores the environment variables, current user, "
            "connection, and other Meteor context that were active at "
            "the time bindEnvironment was called. If the wrapped "
            "function throws an exception, the onException callback "
            "is called with the error. If onException is not provided, "
            "the error is logged via Meteor._debug. In Meteor v3, "
            "this works with the async context propagation model "
            "rather than Fibers."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "The function to wrap. When the returned wrapper "
                    "is called, func runs within the Meteor environment "
                    "that was active when bindEnvironment was called."
                ),
                "optional": False,
            },
            {
                "name": "onException",
                "type": "Function",
                "description": (
                    "A callback invoked with the error if func throws "
                    "an exception. When omitted, Meteor falls back to "
                    "logging the error via Meteor._debug. If you need "
                    "custom error handling, pass a function that "
                    "receives the Error object."
                ),
                "optional": True,
            },
            {
                "name": "_this",
                "type": "Object",
                "description": (
                    "The value of 'this' inside the wrapped function "
                    "when it is called."
                ),
                "optional": True,
            },
        ],
        "returns": "Function",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Wrapping a Node.js event listener",
                "code": (
                    "import { EventEmitter } from 'events';\n"
                    "\n"
                    "const emitter = new EventEmitter();\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async watchForChanges() {\n"
                    "    const userId = Meteor.userId();\n"
                    "\n"
                    "    emitter.on(\n"
                    "      'change',\n"
                    "      Meteor.bindEnvironment(\n"
                    "        async (data) => {\n"
                    "          await AuditLog.insertAsync({\n"
                    "            userId,\n"
                    "            action: 'external-change',\n"
                    "            data,\n"
                    "            timestamp: new Date(),\n"
                    "          });\n"
                    "        },\n"
                    "        (error) => {\n"
                    "          console.error('bindEnvironment error:', error.message);\n"
                    "        }\n"
                    "      )\n"
                    "    );\n"
                    "\n"
                    "    return 'Watcher registered';\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "When registering callbacks with non-Meteor APIs "
                    "like Node.js EventEmitters, use bindEnvironment "
                    "to ensure the callback can safely access Meteor "
                    "collections and environment variables."
                ),
            },
            {
                "title": "Using bindEnvironment with a third-party library",
                "code": (
                    "import chokidar from 'chokidar';\n"
                    "\n"
                    "Meteor.startup(() => {\n"
                    "  const watcher = chokidar.watch('/uploads');\n"
                    "\n"
                    "  watcher.on(\n"
                    "    'add',\n"
                    "    Meteor.bindEnvironment(\n"
                    "      async (filePath) => {\n"
                    "        console.log(`New file: ${filePath}`);\n"
                    "        await Files.insertAsync({\n"
                    "          path: filePath,\n"
                    "          uploadedAt: new Date(),\n"
                    "        });\n"
                    "      },\n"
                    "      (error) => {\n"
                    "        console.error(\n"
                    "          'File watcher error:',\n"
                    "          error.message\n"
                    "        );\n"
                    "      }\n"
                    "    )\n"
                    "  );\n"
                    "});"
                ),
                "description": (
                    "The onException parameter provides a custom error "
                    "handler. Without it, uncaught errors from the "
                    "wrapped callback would be logged by Meteor._debug."
                ),
            },
            {
                "title": "Binding environment for native setTimeout",
                "code": (
                    "Meteor.methods({\n"
                    "  async scheduleReminder(message, delayMs) {\n"
                    "    const userId = Meteor.userId();\n"
                    "\n"
                    "    // Using native setTimeout requires bindEnvironment\n"
                    "    setTimeout(\n"
                    "      Meteor.bindEnvironment(async () => {\n"
                    "        await Notifications.insertAsync({\n"
                    "          userId,\n"
                    "          message,\n"
                    "          createdAt: new Date(),\n"
                    "        });\n"
                    "      }),\n"
                    "      delayMs\n"
                    "    );\n"
                    "\n"
                    "    // Prefer Meteor.setTimeout instead, which\n"
                    "    // calls bindEnvironment automatically.\n"
                    "    return 'Reminder scheduled';\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "This example illustrates why Meteor.setTimeout "
                    "exists: it is equivalent to calling native "
                    "setTimeout with a Meteor.bindEnvironment-wrapped "
                    "callback. Prefer Meteor.setTimeout for cleaner code."
                ),
            },
        ],
        "tags": [
            "environment",
            "context",
            "binding",
            "callbacks",
            "async",
            "node-interop",
        ],
    },
]
