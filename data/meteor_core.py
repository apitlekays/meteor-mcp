"""Meteor core API entries for Meteor.js v3.4.0."""

METEOR_CORE = [
    {
        "name": "Meteor.startup",
        "module": "meteor_core",
        "signature": "Meteor.startup(callback)",
        "description": (
            "Register a callback function to run when the client or server "
            "is ready. On the server, the callback runs as soon as the server "
            "process has finished starting up. On the client, it fires when "
            "the DOM is ready. Multiple callbacks are executed in the order "
            "they were registered. In Meteor v3, startup callbacks on the "
            "server can be async functions and Meteor will await them "
            "sequentially before marking the server as ready."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": "A function to run on startup. May be async on the server.",
                "optional": False,
            }
        ],
        "returns": "void",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Server startup with async initialization",
                "code": (
                    "Meteor.startup(async () => {\n"
                    "  const count = await MyCollection.find().countAsync();\n"
                    "  console.log(`Server started with ${count} documents`);\n"
                    "\n"
                    "  if (count === 0) {\n"
                    "    await MyCollection.insertAsync({\n"
                    "      title: 'Welcome',\n"
                    "      createdAt: new Date(),\n"
                    "    });\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Server startup callbacks in Meteor v3 support async/await. "
                    "Meteor awaits each callback before proceeding to the next."
                ),
            },
            {
                "title": "Client startup for DOM-dependent initialization",
                "code": (
                    "Meteor.startup(() => {\n"
                    "  // DOM is now ready\n"
                    "  console.log('Client app initialized');\n"
                    "  document.title = 'My Meteor App';\n"
                    "});"
                ),
                "description": (
                    "On the client, Meteor.startup runs after the DOM is ready, "
                    "similar to jQuery's document-ready handler."
                ),
            },
        ],
        "tags": ["startup", "initialization", "lifecycle"],
    },
    {
        "name": "Meteor.isClient",
        "module": "meteor_core",
        "signature": "Meteor.isClient",
        "description": (
            "Boolean variable. True if running in client environment. "
            "This is useful for writing code that runs in both environments "
            "inside shared modules. Meteor's build system also uses this as "
            "a compile-time constant to tree-shake server-only code from "
            "client bundles when used in an if-block guard."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Conditional logic based on environment",
                "code": (
                    "if (Meteor.isClient) {\n"
                    "  // This code only runs on the client.\n"
                    "  // Meteor's bundler will also strip this block\n"
                    "  // from the server bundle.\n"
                    "  import('./client-only-module.js');\n"
                    "}"
                ),
                "description": (
                    "Code inside an if (Meteor.isClient) block is removed from "
                    "the server bundle at build time, reducing server bundle size."
                ),
            },
        ],
        "tags": ["environment", "client", "isomorphic"],
    },
    {
        "name": "Meteor.isServer",
        "module": "meteor_core",
        "signature": "Meteor.isServer",
        "description": (
            "Boolean variable. True if running in server environment. "
            "Use this to guard server-only code in shared modules. "
            "Note that code inside an if (Meteor.isServer) block is still "
            "sent to the client unless the file is placed in a server-only "
            "directory (e.g., /server). For true code exclusion from the "
            "client bundle, place files in a server-only directory instead."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Server-only logic in a shared module",
                "code": (
                    "if (Meteor.isServer) {\n"
                    "  Meteor.publish('allPosts', function () {\n"
                    "    return Posts.find({}, { limit: 100 });\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "Wrapping server-only code such as publications in an "
                    "isServer guard ensures it does not execute on the client. "
                    "However, the code is still included in the client bundle "
                    "unless placed in a server-only directory."
                ),
            },
        ],
        "tags": ["environment", "server", "isomorphic"],
    },
    {
        "name": "Meteor.isCordova",
        "module": "meteor_core",
        "signature": "Meteor.isCordova",
        "description": (
            "Boolean variable. True if running in a Cordova mobile environment. "
            "Use this to detect whether the app is packaged as a native mobile "
            "app via Cordova integration. This is useful for enabling "
            "mobile-specific features such as push notifications, camera access, "
            "or native file system APIs."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Mobile-specific feature detection",
                "code": (
                    "if (Meteor.isCordova) {\n"
                    "  // Enable mobile-specific features\n"
                    "  StatusBar.styleDefault();\n"
                    "  navigator.splashscreen.hide();\n"
                    "} else {\n"
                    "  console.log('Running in a web browser');\n"
                    "}"
                ),
                "description": (
                    "Use Meteor.isCordova to conditionally enable mobile-only "
                    "APIs that are not available in a standard browser."
                ),
            },
        ],
        "tags": ["environment", "mobile", "cordova"],
    },
    {
        "name": "Meteor.isDevelopment",
        "module": "meteor_core",
        "signature": "Meteor.isDevelopment",
        "description": (
            "Boolean variable. True if running in development mode. "
            "Development mode is active when running the app with "
            "'meteor run' or 'meteor' without the --production flag. "
            "Use this to enable debug logging, development tools, "
            "or seed data that should not be present in production."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Conditional debug logging",
                "code": (
                    "if (Meteor.isDevelopment) {\n"
                    "  console.log('Debug: current user data', Meteor.user());\n"
                    "\n"
                    "  // Seed test data on the server\n"
                    "  if (Meteor.isServer) {\n"
                    "    Meteor.startup(async () => {\n"
                    "      const count = await Items.find().countAsync();\n"
                    "      if (count === 0) {\n"
                    "        await Items.insertAsync({ name: 'Test Item' });\n"
                    "      }\n"
                    "    });\n"
                    "  }\n"
                    "}"
                ),
                "description": (
                    "Enable verbose logging and test data seeding only in "
                    "development mode to avoid polluting production environments."
                ),
            },
        ],
        "tags": ["environment", "development", "debug"],
    },
    {
        "name": "Meteor.isProduction",
        "module": "meteor_core",
        "signature": "Meteor.isProduction",
        "description": (
            "Boolean variable. True if running in production mode. "
            "Production mode is active when the app is built with "
            "'meteor build' or run with the --production flag. "
            "Use this to enable production-specific optimizations such "
            "as error tracking services, analytics, or stricter security "
            "policies."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Production-only error tracking",
                "code": (
                    "Meteor.startup(() => {\n"
                    "  if (Meteor.isProduction) {\n"
                    "    // Initialize error tracking in production only\n"
                    "    ErrorTracking.init({\n"
                    "      dsn: Meteor.settings.public.sentryDsn,\n"
                    "      environment: 'production',\n"
                    "    });\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Initialize third-party services like error tracking only "
                    "in production to avoid noise during development."
                ),
            },
        ],
        "tags": ["environment", "production", "deployment"],
    },
    {
        "name": "Meteor.isTest",
        "module": "meteor_core",
        "signature": "Meteor.isTest",
        "description": (
            "Boolean variable. True when running unit tests with "
            "'meteor test' (without the --full-app flag). False if running "
            "tests in full app mode or running normally. Use this to "
            "conditionally load test fixtures or test-only code."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Load test fixtures conditionally",
                "code": (
                    "if (Meteor.isTest) {\n"
                    "  // Only loaded during unit testing\n"
                    "  import './test-fixtures.js';\n"
                    "}"
                ),
                "description": (
                    "Conditionally imports test fixtures only when running "
                    "in unit test mode."
                ),
            },
        ],
        "tags": ["environment", "testing", "test"],
    },
    {
        "name": "Meteor.isAppTest",
        "module": "meteor_core",
        "signature": "Meteor.isAppTest",
        "description": (
            "Boolean variable. True if running tests against your application "
            "in full-app mode, i.e. with 'meteor test --full-app'. In this "
            "mode, the full application is loaded alongside test code, allowing "
            "integration and acceptance testing against the running app."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Run integration tests in full-app mode",
                "code": (
                    "if (Meteor.isAppTest) {\n"
                    "  // Full app is running — perform integration tests\n"
                    "  import './integration-tests.js';\n"
                    "}"
                ),
                "description": (
                    "Loads integration test files only when running in "
                    "full-app test mode."
                ),
            },
        ],
        "tags": ["environment", "testing", "integration", "full-app"],
    },
    {
        "name": "Meteor.isPackageTest",
        "module": "meteor_core",
        "signature": "Meteor.isPackageTest",
        "description": (
            "Boolean variable. True if running tests against a Meteor package "
            "using 'meteor test-packages'. Use this to detect the package "
            "testing environment and load package-specific test code."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Detect package test mode",
                "code": (
                    "if (Meteor.isPackageTest) {\n"
                    "  Tinytest.add('my-package - basic test', (test) => {\n"
                    "    test.equal(1 + 1, 2);\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "Registers package tests only when running in "
                    "package test mode."
                ),
            },
        ],
        "tags": ["environment", "testing", "package"],
    },
    {
        "name": "Meteor.isModern",
        "module": "meteor_core",
        "signature": "Meteor.isModern",
        "description": (
            "Boolean variable. True if the code is running in a modern "
            "browser bundle. Meteor builds two client bundles: a modern "
            "bundle for browsers that support ES2015+ features natively, "
            "and a legacy bundle for older browsers. Use this to take "
            "advantage of modern APIs when available while maintaining "
            "backward compatibility."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Feature detection based on bundle type",
                "code": (
                    "if (Meteor.isModern) {\n"
                    "  console.log('Running modern bundle with native ES2015+ support');\n"
                    "} else {\n"
                    "  console.log('Running legacy bundle with transpiled code');\n"
                    "}"
                ),
                "description": (
                    "Meteor.isModern can be used to conditionally load "
                    "polyfills or choose between modern and legacy API paths."
                ),
            },
        ],
        "tags": ["environment", "modern", "legacy", "bundle"],
    },
    {
        "name": "Meteor.settings",
        "module": "meteor_core",
        "signature": "Meteor.settings",
        "description": (
            "An object containing deployment-specific configuration options. "
            "On the server, Meteor.settings contains the full JSON data "
            "provided via the --settings flag or the METEOR_SETTINGS "
            "environment variable. On the client, only the 'public' sub-object "
            "of Meteor.settings is available. Settings are read-only and loaded "
            "once at startup. Use settings to store API keys, feature flags, "
            "and environment-specific configuration without hardcoding values."
        ),
        "params": [],
        "returns": "Object",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Using settings for server-side API keys",
                "code": (
                    "// settings.json:\n"
                    "// {\n"
                    "//   \"private\": { \"stripeSecretKey\": \"sk_live_...\" },\n"
                    "//   \"public\": { \"appName\": \"My App\" }\n"
                    "// }\n"
                    "\n"
                    "// Server-side: access all settings\n"
                    "const stripeKey = Meteor.settings.private.stripeSecretKey;\n"
                    "\n"
                    "// Client-side: only public settings are available\n"
                    "const appName = Meteor.settings.public.appName;\n"
                    "console.log(`Welcome to ${appName}`);"
                ),
                "description": (
                    "Place secrets under a top-level key like 'private' to keep "
                    "them server-only. The 'public' key is automatically shipped "
                    "to the client via __meteor_runtime_config__."
                ),
            },
            {
                "title": "Loading settings via environment variable",
                "code": (
                    "// Run with:\n"
                    "// METEOR_SETTINGS=$(cat settings.json) meteor run\n"
                    "\n"
                    "Meteor.startup(() => {\n"
                    "  if (Meteor.isServer) {\n"
                    "    console.log('Settings loaded:', Object.keys(Meteor.settings));\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "In production, settings are typically provided via the "
                    "METEOR_SETTINGS environment variable containing the JSON string."
                ),
            },
        ],
        "tags": ["settings", "configuration", "environment", "deployment"],
    },
    {
        "name": "Meteor.release",
        "module": "meteor_core",
        "signature": "Meteor.release",
        "description": (
            "A string containing the name of the Meteor release the project is "
            "built with, for example 'METEOR@3.4.0'. This corresponds to the "
            "release track and version specified in the .meteor/release file. "
            "Returns undefined if the app is running from a checkout of the "
            "Meteor source code rather than an official release."
        ),
        "params": [],
        "returns": "String | undefined",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Display the current Meteor release",
                "code": (
                    "Meteor.startup(() => {\n"
                    "  console.log(`Running Meteor release: ${Meteor.release}`);\n"
                    "  // Output: Running Meteor release: METEOR@3.4.0\n"
                    "});"
                ),
                "description": (
                    "Useful for logging the Meteor version at startup or for "
                    "version-dependent feature flags."
                ),
            },
        ],
        "tags": ["release", "version", "metadata"],
    },
    {
        "name": "Meteor.gitCommitHash",
        "module": "meteor_core",
        "signature": "Meteor.gitCommitHash",
        "description": (
            "A string containing the hexadecimal Git commit hash of the "
            "application, if the application is using Git for version control. "
            "Returns undefined if the application is not in a Git repository. "
            "Useful for logging, error reporting, or displaying the current "
            "deployed version."
        ),
        "params": [],
        "returns": "String | undefined",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log the Git commit hash at startup",
                "code": (
                    "Meteor.startup(() => {\n"
                    "  if (Meteor.gitCommitHash) {\n"
                    "    console.log(`Running Git commit: ${Meteor.gitCommitHash}`);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Logs the current Git commit hash at server startup for "
                    "deployment tracking and debugging."
                ),
            },
        ],
        "tags": ["git", "version", "metadata", "deployment"],
    },
    {
        "name": "Meteor.wrapAsync",
        "module": "meteor_core",
        "signature": "Meteor.wrapAsync(func, [context])",
        "description": (
            "Wrap a function that takes a Node.js-style callback (err, result) "
            "and return a new function that runs synchronously in a Fiber. "
            "This function has been removed from the Meteor v3.4 API surface "
            "because Fibers have been removed in favor of native async/await. "
            "Use Meteor.promisify or util.promisify to convert callback-based "
            "APIs to Promises instead. Included here for migration reference only."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A function that accepts a callback as its last argument, "
                    "where the callback follows the (error, result) convention."
                ),
                "optional": False,
            },
            {
                "name": "context",
                "type": "Object",
                "description": (
                    "Optional 'this' context to bind when calling the wrapped function."
                ),
                "optional": True,
            },
        ],
        "returns": "Function",
        "environment": "server",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Legacy wrapAsync usage (deprecated)",
                "code": (
                    "// DEPRECATED in Meteor v3 - use async/await instead\n"
                    "import fs from 'fs';\n"
                    "\n"
                    "// Old Fiber-based approach (no longer works in v3):\n"
                    "// const readFileSync = Meteor.wrapAsync(fs.readFile);\n"
                    "// const content = readFileSync('/path/to/file', 'utf8');\n"
                    "\n"
                    "// Recommended v3 approach using async/await:\n"
                    "import { promisify } from 'util';\n"
                    "\n"
                    "const readFile = promisify(fs.readFile);\n"
                    "\n"
                    "async function getFileContent(path) {\n"
                    "  const content = await readFile(path, 'utf8');\n"
                    "  return content;\n"
                    "}"
                ),
                "description": (
                    "Meteor v3 removed Fibers. Migrate wrapAsync calls to "
                    "async/await using util.promisify or native Promise wrappers."
                ),
            },
        ],
        "tags": ["async", "fibers", "callback", "deprecated", "migration"],
    },
    {
        "name": "Meteor.promisify",
        "module": "meteor_core",
        "signature": "Meteor.promisify(fn, [context], [errorFirst])",
        "description": (
            "Wraps a function that takes a Node.js-style callback and returns "
            "a new function that returns a Promise. This is the Meteor v3 "
            "replacement for Meteor.wrapAsync. By default, assumes an "
            "error-first callback convention (err, result). Set errorFirst to "
            "false for callbacks that do not follow this convention."
        ),
        "params": [
            {
                "name": "fn",
                "type": "Function",
                "description": (
                    "A function that accepts a callback as its last argument."
                ),
                "optional": False,
            },
            {
                "name": "context",
                "type": "Object",
                "description": (
                    "Optional 'this' context to bind when calling the function."
                ),
                "optional": True,
            },
            {
                "name": "errorFirst",
                "type": "Boolean",
                "description": (
                    "Whether the callback follows the error-first (err, result) "
                    "convention. Defaults to true."
                ),
                "optional": True,
            },
        ],
        "returns": "Function -- A new function that returns a Promise.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Promisify a callback-based API",
                "code": (
                    "import fs from 'fs';\n"
                    "\n"
                    "const readFile = Meteor.promisify(fs.readFile);\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async 'files.read'(filePath) {\n"
                    "    check(filePath, String);\n"
                    "    const content = await readFile(filePath, 'utf8');\n"
                    "    return content;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Converts Node.js fs.readFile to a Promise-returning function "
                    "using Meteor.promisify, the v3 replacement for wrapAsync."
                ),
            },
            {
                "title": "Promisify with a context",
                "code": (
                    "const boundMethod = Meteor.promisify(someObj.method, someObj);\n"
                    "const result = await boundMethod(arg1, arg2);"
                ),
                "description": (
                    "Passes a 'this' context so the promisified function "
                    "retains the correct binding when called."
                ),
            },
        ],
        "tags": ["async", "promise", "callback", "migration", "v3"],
    },
    {
        "name": "Meteor.defer",
        "module": "meteor_core",
        "signature": "Meteor.defer(callback)",
        "description": (
            "Defer the execution of a callback function to run after the "
            "current computation or method invocation completes. On the server, "
            "this is similar to Meteor.setTimeout with a delay of 0 but runs "
            "within the current environment (preserving the current user, "
            "connection, etc.). On the client, it defers execution until the "
            "current reactive flush cycle completes. Useful for running "
            "non-critical work without blocking the current operation."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": "A function to call after the current execution context yields.",
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Deferring non-critical server work",
                "code": (
                    "Meteor.methods({\n"
                    "  async submitOrder(orderData) {\n"
                    "    check(orderData, Object);\n"
                    "\n"
                    "    const orderId = await Orders.insertAsync(orderData);\n"
                    "\n"
                    "    // Send confirmation email without blocking the method return\n"
                    "    Meteor.defer(() => {\n"
                    "      Email.send({\n"
                    "        to: orderData.email,\n"
                    "        subject: 'Order Confirmation',\n"
                    "        text: `Your order ${orderId} has been placed.`,\n"
                    "      });\n"
                    "    });\n"
                    "\n"
                    "    return orderId;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Meteor.defer allows the method to return the orderId "
                    "immediately while the email is sent asynchronously afterward."
                ),
            },
            {
                "title": "Deferring client-side cleanup",
                "code": (
                    "Template.dashboard.events({\n"
                    "  'click .refresh-btn'(event, instance) {\n"
                    "    instance.loading.set(true);\n"
                    "\n"
                    "    Meteor.defer(() => {\n"
                    "      // Runs after the reactive flush updates the UI\n"
                    "      console.log('UI updated, performing cleanup');\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "On the client, Meteor.defer runs the callback after the "
                    "current reactive computation and DOM update cycle finishes."
                ),
            },
        ],
        "tags": ["async", "defer", "scheduling", "non-blocking"],
    },
    {
        "name": "Meteor.absoluteUrl",
        "module": "meteor_core",
        "signature": "Meteor.absoluteUrl([path], [options])",
        "description": (
            "Generate an absolute URL pointing to the application. The base URL "
            "is determined by the ROOT_URL environment variable, or defaults to "
            "localhost. This is useful for generating links in emails, OAuth "
            "callbacks, and API endpoint references where a full URL is required. "
            "The returned URL always ends without a trailing slash unless the "
            "path itself includes one."
        ),
        "params": [
            {
                "name": "path",
                "type": "String",
                "description": (
                    "A path to append to the root URL. Leading slashes are "
                    "handled automatically."
                ),
                "optional": True,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "An options object. Supported fields: 'secure' (Boolean) to "
                    "force HTTPS, 'replaceLocalhost' (Boolean) to replace "
                    "localhost with 127.0.0.1, and 'rootUrl' (String) to override "
                    "the default ROOT_URL."
                ),
                "optional": True,
            },
        ],
        "returns": "String",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Generate absolute URLs for email links",
                "code": (
                    "// Assuming ROOT_URL=https://myapp.com\n"
                    "\n"
                    "const homeUrl = Meteor.absoluteUrl();\n"
                    "// => 'https://myapp.com/'\n"
                    "\n"
                    "const verifyUrl = Meteor.absoluteUrl('verify-email/abc123');\n"
                    "// => 'https://myapp.com/verify-email/abc123'\n"
                    "\n"
                    "const secureUrl = Meteor.absoluteUrl('api/webhook', {\n"
                    "  secure: true,\n"
                    "});\n"
                    "// => 'https://myapp.com/api/webhook'"
                ),
                "description": (
                    "Use Meteor.absoluteUrl to build full URLs for email "
                    "verification links, OAuth redirects, or webhook endpoints."
                ),
            },
            {
                "title": "Override root URL for multi-tenant apps",
                "code": (
                    "const tenantUrl = Meteor.absoluteUrl('dashboard', {\n"
                    "  rootUrl: 'https://tenant1.myapp.com',\n"
                    "});\n"
                    "// => 'https://tenant1.myapp.com/dashboard'"
                ),
                "description": (
                    "The rootUrl option allows generating URLs for a different "
                    "base domain, useful in multi-tenant deployments."
                ),
            },
        ],
        "tags": ["url", "routing", "configuration", "ROOT_URL"],
    },
]
