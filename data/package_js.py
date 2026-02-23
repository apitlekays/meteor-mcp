"""Package.js and Npm API entries for Meteor.js v3.4.0."""

PACKAGE_JS = [
    {
        "name": "Package.describe",
        "module": "package_js",
        "signature": "Package.describe(options)",
        "description": (
            "Provide basic metadata about a Meteor package in package.js. "
            "This must be called exactly once per package.js file and is "
            "used by the Meteor package system and Atmosphere (the Meteor "
            "package registry) to display information about the package. "
            "The options object includes the package name, version (must "
            "follow semver), a brief summary, the git URL for the source "
            "repository, and an optional documentation file path. Packages "
            "intended only for testing can set 'testOnly: true'."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "An object with fields: name (String, package name in "
                    "'author:name' format for community packages or just "
                    "'name' for core packages), version (String, semver "
                    "version), summary (String, one-line description), "
                    "git (String, git repository URL), documentation "
                    "(String, path to README file, defaults to 'README.md'), "
                    "testOnly (Boolean, if true the package can only be "
                    "used in tests)."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Describe a community package",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Package.describe({\n"
                    "  name: 'acme:utils',\n"
                    "  version: '2.1.0',\n"
                    "  summary: 'Common utility functions for Acme applications',\n"
                    "  git: 'https://github.com/acme/meteor-utils',\n"
                    "  documentation: 'README.md',\n"
                    "});"
                ),
                "description": (
                    "Community packages use the 'author:name' format. "
                    "The version must follow semantic versioning and the "
                    "summary appears in Atmosphere search results."
                ),
            },
            {
                "title": "Describe a test-only package",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Package.describe({\n"
                    "  name: 'acme:test-helpers',\n"
                    "  version: '1.0.0',\n"
                    "  summary: 'Test utilities for Acme packages',\n"
                    "  testOnly: true,\n"
                    "});"
                ),
                "description": (
                    "A test-only package cannot be added to an application "
                    "directly and is only available inside package tests."
                ),
            },
        ],
        "tags": ["package", "metadata", "atmosphere", "semver", "config"],
    },
    {
        "name": "Package.onUse",
        "module": "package_js",
        "signature": "Package.onUse(func)",
        "description": (
            "Define the package's dependencies, exports, and files for "
            "normal (non-test) use. The callback function receives an "
            "'api' object that provides methods for declaring Meteor "
            "package dependencies (api.use), re-exporting packages "
            "(api.imply), exporting symbols (api.export), adding source "
            "files (api.addFiles), adding static assets (api.addAssets), "
            "and defining a main entry module (api.mainModule). The api "
            "methods accept architecture arguments ('client', 'server', "
            "or both) to control where code runs. This function is called "
            "once per package.js."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A callback function that receives the 'api' object. "
                    "Use api methods inside this callback to configure "
                    "the package."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Define a package with dependencies and a main module",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "\n"
                    "  api.use('ecmascript');\n"
                    "  api.use('mongo');\n"
                    "  api.use('check');\n"
                    "\n"
                    "  api.mainModule('client/main.js', 'client');\n"
                    "  api.mainModule('server/main.js', 'server');\n"
                    "});"
                ),
                "description": (
                    "Modern Meteor packages use api.mainModule to define "
                    "ES module entry points instead of api.addFiles with "
                    "api.export. This enables tree-shaking and standard "
                    "import/export syntax."
                ),
            },
            {
                "title": "Package with file-based exports (legacy style)",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "\n"
                    "  api.export('Utils');\n"
                    "\n"
                    "  api.addFiles('utils.js');\n"
                    "  api.addFiles('client-helpers.js', 'client');\n"
                    "  api.addFiles('server-init.js', 'server');\n"
                    "});"
                ),
                "description": (
                    "The legacy api.addFiles approach makes each file a "
                    "top-level scope file and api.export publishes global "
                    "symbols. Prefer api.mainModule for new packages."
                ),
            },
        ],
        "tags": ["package", "dependencies", "exports", "config", "api"],
    },
    {
        "name": "Package.onTest",
        "module": "package_js",
        "signature": "Package.onTest(func)",
        "description": (
            "Define the package's test dependencies and files. The callback "
            "receives the same 'api' object as Package.onUse, but the "
            "dependencies and files declared here are only used when "
            "running tests with 'meteor test-packages'. The test code "
            "automatically has access to the package's own exports. "
            "Typically you declare test framework dependencies like "
            "'tinytest' or 'meteortesting:mocha' here along with your "
            "test source files."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A callback function that receives the 'api' object. "
                    "Use api methods to declare test-specific dependencies "
                    "and test files."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Define package tests with Tinytest",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Package.onTest(function (api) {\n"
                    "  api.use('ecmascript');\n"
                    "  api.use('tinytest');\n"
                    "  api.use('acme:utils');  // The package being tested\n"
                    "\n"
                    "  api.addFiles('tests/utils-tests.js');\n"
                    "});"
                ),
                "description": (
                    "Declare 'tinytest' as a dependency and add test files. "
                    "Run tests with 'meteor test-packages ./packages/acme-utils'."
                ),
            },
            {
                "title": "Define package tests with Mocha",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Package.onTest(function (api) {\n"
                    "  api.use('ecmascript');\n"
                    "  api.use('meteortesting:mocha');\n"
                    "  api.use('acme:utils');\n"
                    "\n"
                    "  api.mainModule('tests/main.js');\n"
                    "});"
                ),
                "description": (
                    "Use api.mainModule in tests to leverage ES module "
                    "imports for organizing test suites."
                ),
            },
        ],
        "tags": ["package", "testing", "tinytest", "mocha", "config"],
    },
    {
        "name": "Package.registerBuildPlugin",
        "module": "package_js",
        "signature": "Package.registerBuildPlugin(options)",
        "description": (
            "Register a compiler or build plugin that extends Meteor's "
            "build system. Build plugins process specific file extensions "
            "during the build process and can transform source files into "
            "JavaScript, CSS, or other assets. For example, the coffeescript "
            "package registers a build plugin to compile .coffee files, and "
            "the less package compiles .less files to CSS. The options "
            "include 'name' (a unique identifier), 'use' (Meteor packages "
            "needed by the plugin), 'sources' (the plugin source files), "
            "and 'npmDependencies' (npm packages the plugin requires)."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "An object with fields: name (String, unique plugin "
                    "identifier), use (Array of Strings, Meteor packages "
                    "used by the plugin), sources (Array of Strings, "
                    "plugin source files), npmDependencies (Object, npm "
                    "package name-to-version mappings needed by the plugin)."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Register a build plugin for custom file types",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Package.registerBuildPlugin({\n"
                    "  name: 'compileMarkdown',\n"
                    "  use: ['ecmascript'],\n"
                    "  sources: ['plugin/compile-markdown.js'],\n"
                    "  npmDependencies: {\n"
                    "    marked: '12.0.0',\n"
                    "  },\n"
                    "});\n"
                    "\n"
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  // The build plugin is now available to compile .md files\n"
                    "});"
                ),
                "description": (
                    "Register a build plugin that compiles Markdown files "
                    "into importable JavaScript modules. The plugin source "
                    "must implement the compiler plugin interface."
                ),
            },
        ],
        "tags": ["package", "build", "plugin", "compiler", "config"],
    },
    {
        "name": "Npm.depends",
        "module": "package_js",
        "signature": "Npm.depends(dependencies)",
        "description": (
            "Declare npm package dependencies for a Meteor package in "
            "package.js. The dependencies argument is an object mapping "
            "npm package names to exact version strings. These packages "
            "are installed when the Meteor package is built and can be "
            "required with Npm.require() inside the package's server-side "
            "code. Unlike application-level npm dependencies in "
            "package.json, these are scoped to the Meteor package and "
            "do not pollute the application's node_modules. Version "
            "strings must be exact versions (not ranges) or URLs to "
            "tarballs."
        ),
        "params": [
            {
                "name": "dependencies",
                "type": "Object",
                "description": (
                    "An object mapping npm package names to exact version "
                    "strings (e.g., { lodash: '4.17.21' }) or tarball URLs."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Declare npm dependencies for a package",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Npm.depends({\n"
                    "  'stripe': '14.18.0',\n"
                    "  'lodash': '4.17.21',\n"
                    "  'uuid': '9.0.1',\n"
                    "});\n"
                    "\n"
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "  api.mainModule('server/main.js', 'server');\n"
                    "});"
                ),
                "description": (
                    "Npm.depends must be called at the top level of "
                    "package.js, not inside Package.onUse. Versions must "
                    "be exact, not semver ranges."
                ),
            },
        ],
        "tags": ["package", "npm", "dependencies", "node", "config"],
    },
    {
        "name": "Npm.require",
        "module": "package_js",
        "signature": "Npm.require(name)",
        "description": (
            "Require an npm module that was declared via Npm.depends in "
            "the package's package.js file. This is used inside Meteor "
            "package source code (not in package.js itself) to access "
            "npm dependencies that are scoped to the package. In modern "
            "Meteor v3 packages that use api.mainModule, you can also use "
            "standard ES module 'import' syntax to import npm packages. "
            "Npm.require is still useful in packages that use "
            "api.addFiles or need dynamic requires."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": "The name of the npm package to require.",
                "optional": False,
            },
        ],
        "returns": "any",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Require an npm package inside a Meteor package",
                "code": (
                    "// Inside a Meteor package source file (server-side)\n"
                    "\n"
                    "const stripe = Npm.require('stripe');\n"
                    "const _ = Npm.require('lodash');\n"
                    "\n"
                    "const client = stripe(Meteor.settings.stripeSecretKey);\n"
                    "\n"
                    "export async function createCharge(amount, token) {\n"
                    "  const charge = await client.charges.create({\n"
                    "    amount: _.toInteger(amount),\n"
                    "    currency: 'usd',\n"
                    "    source: token,\n"
                    "  });\n"
                    "  return charge;\n"
                    "}"
                ),
                "description": (
                    "Use Npm.require to access npm packages declared in "
                    "Npm.depends. In modern packages with api.mainModule, "
                    "you can alternatively use standard import statements."
                ),
            },
        ],
        "tags": ["package", "npm", "require", "node", "import"],
    },
    {
        "name": "Cordova.depends",
        "module": "package_js",
        "signature": "Cordova.depends(dependencies)",
        "description": (
            "Declare Cordova plugin dependencies for a Meteor package in "
            "package.js. The dependencies argument is an object mapping "
            "Cordova plugin identifiers to version strings. These plugins "
            "are installed when building the mobile app and provide access "
            "to native device features such as the camera, GPS, "
            "accelerometer, and push notifications. Plugin identifiers "
            "are npm package names for modern Cordova plugins or the "
            "legacy plugin ID format."
        ),
        "params": [
            {
                "name": "dependencies",
                "type": "Object",
                "description": (
                    "An object mapping Cordova plugin identifiers to "
                    "version strings (e.g., { 'cordova-plugin-camera': '7.0.0' })."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Declare Cordova plugin dependencies",
                "code": (
                    "// package.js\n"
                    "\n"
                    "Cordova.depends({\n"
                    "  'cordova-plugin-camera': '7.0.0',\n"
                    "  'cordova-plugin-geolocation': '5.0.0',\n"
                    "  'cordova-plugin-statusbar': '4.0.0',\n"
                    "});\n"
                    "\n"
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "  api.mainModule('client/camera.js', 'client');\n"
                    "});"
                ),
                "description": (
                    "Cordova.depends is called at the top level of "
                    "package.js. The plugins are installed into the "
                    "Cordova project when building the mobile app."
                ),
            },
        ],
        "tags": ["package", "cordova", "mobile", "plugin", "native", "config"],
    },
    {
        "name": "api.use",
        "module": "package_js",
        "signature": "api.use(packages, [architecture], [options])",
        "description": (
            "Declare dependencies on other Meteor packages within a "
            "Package.onUse or Package.onTest callback. The packages "
            "argument can be a single package name string or an array of "
            "package name strings, optionally with version constraints "
            "(e.g., 'mongo@2.0.0'). The architecture argument restricts "
            "the dependency to 'client', 'server', or both (default). "
            "The options object supports 'weak' (Boolean) to declare a "
            "weak dependency that does not cause the package to be "
            "included but uses it if present, and 'unordered' (Boolean) "
            "to declare a dependency without enforcing load order."
        ),
        "params": [
            {
                "name": "packages",
                "type": "String | Array<String>",
                "description": (
                    "A package name or array of package names, optionally "
                    "with version constraints (e.g., 'accounts-base@3.0.0')."
                ),
                "optional": False,
            },
            {
                "name": "architecture",
                "type": "String | Array<String>",
                "description": (
                    "Target architecture(s): 'client', 'server', or an "
                    "array of both. Defaults to both if omitted."
                ),
                "optional": True,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Optional configuration: weak (Boolean, the dependency "
                    "is used only if already included by another package), "
                    "unordered (Boolean, no load-order constraint is applied)."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Declare package dependencies with architecture targeting",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "\n"
                    "  // Dependencies for both client and server\n"
                    "  api.use(['ecmascript', 'check', 'mongo']);\n"
                    "\n"
                    "  // Client-only dependencies\n"
                    "  api.use('reactive-var', 'client');\n"
                    "  api.use('templating@1.4.0', 'client');\n"
                    "\n"
                    "  // Server-only dependencies\n"
                    "  api.use('email', 'server');\n"
                    "\n"
                    "  // Weak dependency (use if present, don't force inclusion)\n"
                    "  api.use('aldeed:simple-schema', { weak: true });\n"
                    "});"
                ),
                "description": (
                    "Use api.use to declare which packages your package "
                    "depends on. The architecture argument ensures "
                    "client-only packages are not loaded on the server "
                    "and vice versa."
                ),
            },
        ],
        "tags": ["package", "dependencies", "api", "architecture", "config"],
    },
    {
        "name": "api.versionsFrom",
        "module": "package_js",
        "signature": "api.versionsFrom(meteorRelease)",
        "description": (
            "Declare which version(s) of Meteor the package or application "
            "is designed for. This sets the default package version constraints "
            "based on the specified Meteor release. Accepts a single release "
            "string (e.g., '3.0') or an array of release strings for "
            "compatibility with multiple Meteor versions."
        ),
        "params": [
            {
                "name": "meteorRelease",
                "type": "String | Array<String>",
                "description": (
                    "A Meteor release version string (e.g., '3.0', '2.16') "
                    "or an array of release strings for multi-version "
                    "compatibility."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Declare Meteor v3 compatibility",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.0');\n"
                    "  api.use('ecmascript');\n"
                    "});"
                ),
                "description": (
                    "Declares that the package is designed for Meteor 3.0, "
                    "which sets default version constraints for core packages."
                ),
            },
            {
                "title": "Support multiple Meteor versions",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom(['2.16', '3.0']);\n"
                    "  api.use('ecmascript');\n"
                    "});"
                ),
                "description": (
                    "Declares compatibility with both Meteor 2.16 and 3.0, "
                    "allowing the package to work across major versions."
                ),
            },
        ],
        "tags": ["package", "version", "compatibility", "release"],
    },
    {
        "name": "api.imply",
        "module": "package_js",
        "signature": "api.imply(packages, [architecture])",
        "description": (
            "Re-export another package's API so that any application or "
            "package that depends on your package also automatically gets "
            "access to the implied packages. This is useful for creating "
            "umbrella packages that bundle several related packages "
            "together or when your package's API inherently depends on "
            "symbols from another package. For example, the 'accounts-password' "
            "package implies 'accounts-base' so that users get access "
            "to Accounts methods without explicitly adding accounts-base."
        ),
        "params": [
            {
                "name": "packages",
                "type": "String | Array<String>",
                "description": (
                    "A package name or array of package names to re-export. "
                    "Version constraints are not supported here."
                ),
                "optional": False,
            },
            {
                "name": "architecture",
                "type": "String | Array<String>",
                "description": (
                    "Restrict the implication to specific architectures. "
                    "Valid values: 'client', 'server', 'web.browser', "
                    "'web.cordova'. If omitted, implied for all architectures."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Create an umbrella package that implies sub-packages",
                "code": (
                    "// package.js for 'acme:full-stack'\n"
                    "\n"
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "\n"
                    "  api.use([\n"
                    "    'acme:collections',\n"
                    "    'acme:methods',\n"
                    "    'acme:publications',\n"
                    "  ]);\n"
                    "\n"
                    "  // Anyone who uses acme:full-stack also gets these packages\n"
                    "  api.imply([\n"
                    "    'acme:collections',\n"
                    "    'acme:methods',\n"
                    "    'acme:publications',\n"
                    "  ]);\n"
                    "});"
                ),
                "description": (
                    "Implied packages become direct dependencies of "
                    "any consumer. This avoids requiring users to "
                    "explicitly add each sub-package."
                ),
            },
        ],
        "tags": ["package", "re-export", "imply", "umbrella", "api"],
    },
    {
        "name": "api.export",
        "module": "package_js",
        "signature": "api.export(exportedObjects, [architecture])",
        "description": (
            "Export package-level symbols so they are available as globals "
            "to packages and applications that depend on this package. "
            "This is the legacy approach to sharing code between packages. "
            "In modern Meteor v3 packages, prefer using api.mainModule "
            "with standard ES module exports instead, which supports "
            "tree-shaking and avoids global namespace pollution. "
            "api.export is still needed for packages that use "
            "api.addFiles and need to expose symbols globally."
        ),
        "params": [
            {
                "name": "exportedObjects",
                "type": "String | Array<String>",
                "description": (
                    "A symbol name or array of symbol names to export "
                    "as package globals."
                ),
                "optional": False,
            },
            {
                "name": "architecture",
                "type": "String | Array<String>",
                "description": (
                    "Target architecture(s): 'client', 'server', or an "
                    "array of both. Defaults to both if omitted."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Export symbols from a package (legacy style)",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "\n"
                    "  // Export 'Utils' as a global symbol\n"
                    "  api.export('Utils');\n"
                    "\n"
                    "  // Export different symbols per architecture\n"
                    "  api.export('ClientHelpers', 'client');\n"
                    "  api.export('ServerUtils', 'server');\n"
                    "\n"
                    "  api.addFiles('utils.js');\n"
                    "  api.addFiles('client-helpers.js', 'client');\n"
                    "  api.addFiles('server-utils.js', 'server');\n"
                    "});"
                ),
                "description": (
                    "Exported symbols become globals accessible via the "
                    "package name. Prefer api.mainModule with ES module "
                    "exports for new packages."
                ),
            },
        ],
        "tags": ["package", "export", "global", "legacy", "api"],
    },
    {
        "name": "api.addFiles",
        "module": "package_js",
        "signature": "api.addFiles(filenames, [architecture])",
        "description": (
            "Add source files to the package. Each file is executed in "
            "its own scope (not as an ES module) when the package loads. "
            "Variables assigned without 'var', 'let', or 'const' become "
            "package-scoped globals, and those declared with api.export "
            "become available to consumers. Files are loaded in the order "
            "listed. This is the legacy approach; modern packages should "
            "use api.mainModule instead, which provides proper ES module "
            "semantics including import/export, tree-shaking, and "
            "on-demand loading."
        ),
        "params": [
            {
                "name": "filenames",
                "type": "String | Array<String>",
                "description": (
                    "A file path or array of file paths relative to the "
                    "package root directory."
                ),
                "optional": False,
            },
            {
                "name": "architecture",
                "type": "String | Array<String>",
                "description": (
                    "Target architecture(s): 'client', 'server', or an "
                    "array of both. Defaults to both if omitted."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Add files with architecture targeting",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "\n"
                    "  // Files for both client and server\n"
                    "  api.addFiles('lib/shared-utils.js');\n"
                    "\n"
                    "  // Client-only files\n"
                    "  api.addFiles([\n"
                    "    'client/templates.html',\n"
                    "    'client/templates.js',\n"
                    "    'client/styles.css',\n"
                    "  ], 'client');\n"
                    "\n"
                    "  // Server-only files\n"
                    "  api.addFiles('server/publications.js', 'server');\n"
                    "});"
                ),
                "description": (
                    "Files are loaded in the order specified. Use "
                    "architecture arguments to ensure client-only code "
                    "like templates does not load on the server."
                ),
            },
        ],
        "tags": ["package", "files", "source", "legacy", "api"],
    },
    {
        "name": "api.addAssets",
        "module": "package_js",
        "signature": "api.addAssets(filenames, architecture)",
        "description": (
            "Add static asset files to the package that can be accessed "
            "at runtime via Assets.getTextAsync() or Assets.getBinaryAsync() on the "
            "server. Unlike api.addFiles, assets are not executed as code; "
            "they are bundled as raw files. This is useful for including "
            "templates, JSON configuration files, images, fonts, or other "
            "static resources that your package needs at runtime. The "
            "architecture argument is required and specifies whether the "
            "assets are available on 'client', 'server', or both."
        ),
        "params": [
            {
                "name": "filenames",
                "type": "String | Array<String>",
                "description": (
                    "A file path or array of file paths relative to the "
                    "package root directory."
                ),
                "optional": False,
            },
            {
                "name": "architecture",
                "type": "String | Array<String>",
                "description": (
                    "Target architecture(s): 'client', 'server', or an "
                    "array of both. Required."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Add static assets to a package",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "\n"
                    "  api.addAssets([\n"
                    "    'assets/email-template.html',\n"
                    "    'assets/default-config.json',\n"
                    "  ], 'server');\n"
                    "\n"
                    "  api.addAssets('assets/logo.png', 'client');\n"
                    "\n"
                    "  api.mainModule('server/main.js', 'server');\n"
                    "});\n"
                    "\n"
                    "// In server/main.js:\n"
                    "// const template = Assets.getText(\n"
                    "//   'assets/email-template.html'\n"
                    "// );\n"
                    "// const config = JSON.parse(\n"
                    "//   Assets.getText('assets/default-config.json')\n"
                    "// );"
                ),
                "description": (
                    "Assets are accessed at runtime using Assets.getTextAsync() "
                    "for text files or Assets.getBinaryAsync() for binary files. "
                    "The path passed to Assets methods matches the path "
                    "given to api.addAssets."
                ),
            },
        ],
        "tags": ["package", "assets", "static", "files", "resources", "api"],
    },
    {
        "name": "api.mainModule",
        "module": "package_js",
        "signature": "api.mainModule(filePath, [architecture])",
        "description": (
            "Declare the main ES module entry point for the package. "
            "When a consumer imports the package (e.g., "
            "\"import { Foo } from 'meteor/author:package'\"), Meteor "
            "resolves to this file. The main module uses standard ES "
            "module import/export syntax, enabling tree-shaking and "
            "lazy loading. This is the recommended approach for Meteor "
            "v3 packages as it replaces the legacy api.addFiles + "
            "api.export pattern. You can specify separate entry points "
            "for client and server by calling api.mainModule twice with "
            "different architecture arguments."
        ),
        "params": [
            {
                "name": "filePath",
                "type": "String",
                "description": (
                    "The path to the main module file, relative to the "
                    "package root."
                ),
                "optional": False,
            },
            {
                "name": "architecture",
                "type": "String | Array<String>",
                "description": (
                    "Target architecture(s): 'client', 'server', or an "
                    "array of both. Defaults to both if omitted."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "package.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Define separate client and server entry points",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "  api.use('mongo');\n"
                    "\n"
                    "  api.mainModule('client/index.js', 'client');\n"
                    "  api.mainModule('server/index.js', 'server');\n"
                    "});\n"
                    "\n"
                    "// client/index.js\n"
                    "// export { TaskList } from './components/TaskList';\n"
                    "// export { formatDate } from './helpers';\n"
                    "\n"
                    "// server/index.js\n"
                    "// export { Tasks } from '../collections/tasks';\n"
                    "// export { createTask, removeTask } from './methods';"
                ),
                "description": (
                    "Separate entry points allow you to export different "
                    "APIs for client and server. Consumers import the "
                    "package normally and the correct module is resolved "
                    "based on the build target."
                ),
            },
            {
                "title": "Single entry point for an isomorphic package",
                "code": (
                    "Package.onUse(function (api) {\n"
                    "  api.versionsFrom('3.4.0');\n"
                    "  api.use('ecmascript');\n"
                    "\n"
                    "  // Same entry point for both client and server\n"
                    "  api.mainModule('index.js');\n"
                    "});\n"
                    "\n"
                    "// index.js\n"
                    "// export { validateEmail, formatCurrency } from './utils';\n"
                    "// export { CONSTANTS } from './constants';"
                ),
                "description": (
                    "For packages whose API is identical on client and "
                    "server, use a single api.mainModule call without "
                    "an architecture argument."
                ),
            },
        ],
        "tags": ["package", "module", "entry-point", "es-modules", "modern", "api"],
    },
]
