"""Meteor.js DDPRateLimiter API data for v3.4.0."""

DDP_RATE_LIMITER = [
    {
        "name": "DDPRateLimiter.addRule",
        "module": "ddp_rate_limiter",
        "signature": "DDPRateLimiter.addRule(matcher, numRequests, timeInterval, callback)",
        "description": (
            "Adds a rate-limiting rule for DDP methods and subscriptions. When incoming "
            "requests match the rule and exceed the allowed number of requests within the "
            "specified time interval, subsequent requests are rejected with a rate-limit "
            "error. The matcher object can filter by userId, clientAddress, type "
            "('method' or 'subscription'), name (the method or subscription name), and "
            "connectionId. Each matcher field can be a literal value, a function returning "
            "a boolean, or null to match any value. Returns a unique rule ID string that "
            "can be used with removeRule to unregister the rule later."
        ),
        "params": [
            {
                "name": "matcher",
                "type": "Object",
                "description": (
                    "An object describing which DDP requests this rule applies to. "
                    "Supported fields: userId (String|Function|null), clientAddress "
                    "(String|Function|null), type ('method'|'subscription'|Function), "
                    "name (String|Function), connectionId (String|Function|null). Each "
                    "field can be a literal value for exact matching, a function that "
                    "receives the value and returns a boolean, or null to match all."
                ),
                "optional": False,
            },
            {
                "name": "numRequests",
                "type": "Number",
                "description": (
                    "The maximum number of requests allowed within the time interval "
                    "before the rule triggers rate limiting."
                ),
                "optional": False,
            },
            {
                "name": "timeInterval",
                "type": "Number",
                "description": (
                    "The time window in milliseconds during which requests are counted. "
                    "For example, 1000 means one second."
                ),
                "optional": False,
            },
            {
                "name": "callback",
                "type": "Function",
                "optional": True,
                "description": (
                    "A function called when the rule is triggered. Receives an object "
                    "with timeToReset (milliseconds until the rate limit resets), "
                    "numInvocationsLeft, and numInvocationsExceeded. "
                    "Useful for logging rate-limit events."
                ),
            },
        ],
        "returns": "String - A unique rule ID that can be passed to DDPRateLimiter.removeRule.",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Limit login attempts",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "// Allow at most 5 login attempts per connection per 10 seconds\n"
                    "DDPRateLimiter.addRule(\n"
                    "  {\n"
                    "    type: 'method',\n"
                    "    name: 'login',\n"
                    "    connectionId() { return true; },\n"
                    "  },\n"
                    "  5,\n"
                    "  10000\n"
                    ");"
                ),
                "description": (
                    "Rate-limits the built-in 'login' method to 5 calls per 10 seconds "
                    "per connection, preventing brute-force login attacks."
                ),
            },
            {
                "title": "Rate-limit all methods for unauthenticated users",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "DDPRateLimiter.addRule(\n"
                    "  {\n"
                    "    type: 'method',\n"
                    "    userId(userId) { return userId === null; },\n"
                    "  },\n"
                    "  10,\n"
                    "  1000\n"
                    ");"
                ),
                "description": (
                    "Limits unauthenticated users to 10 method calls per second across "
                    "all methods. Authenticated users are not affected."
                ),
            },
            {
                "title": "Rate-limit subscriptions with a callback",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "const ruleId = DDPRateLimiter.addRule(\n"
                    "  {\n"
                    "    type: 'subscription',\n"
                    "    name(name) {\n"
                    "      // Apply to all subscriptions starting with 'admin.'\n"
                    "      return name.startsWith('admin.');\n"
                    "    },\n"
                    "  },\n"
                    "  5,\n"
                    "  5000,\n"
                    "  (reply) => {\n"
                    "    console.warn(\n"
                    "      `Rate limit hit: user ${reply.userId} exceeded ` +\n"
                    "      `${reply.numInvocationsExceeded} requests. ` +\n"
                    "      `Resets in ${reply.timeToReset}ms.`\n"
                    "    );\n"
                    "  }\n"
                    ");\n"
                    "\n"
                    "console.log('Rule registered with ID:', ruleId);"
                ),
                "description": (
                    "Rate-limits all subscriptions whose name starts with 'admin.' to 5 "
                    "requests per 5 seconds. The callback logs details when the limit is "
                    "exceeded."
                ),
            },
        ],
        "tags": [
            "rate-limit",
            "ddp",
            "security",
            "throttle",
            "brute-force",
            "methods",
            "subscriptions",
        ],
    },
    {
        "name": "DDPRateLimiter.removeRule",
        "module": "ddp_rate_limiter",
        "signature": "DDPRateLimiter.removeRule(id)",
        "description": (
            "Removes a previously registered rate-limiting rule by its ID. The ID is the "
            "string returned by DDPRateLimiter.addRule. After removal, the rule no longer "
            "applies to incoming DDP requests. Returns a boolean indicating whether the "
            "rule was successfully found and removed."
        ),
        "params": [
            {
                "name": "id",
                "type": "String",
                "description": "The unique rule ID returned by DDPRateLimiter.addRule.",
                "optional": False,
            },
        ],
        "returns": "Boolean - true if the rule was found and removed, false otherwise.",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Add and later remove a rate-limit rule",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "// Add a temporary rule\n"
                    "const ruleId = DDPRateLimiter.addRule(\n"
                    "  { type: 'method', name: 'importData' },\n"
                    "  1,\n"
                    "  60000\n"
                    ");\n"
                    "\n"
                    "// Later, remove it when no longer needed\n"
                    "const removed = DDPRateLimiter.removeRule(ruleId);\n"
                    "console.log('Rule removed:', removed); // true"
                ),
                "description": (
                    "Demonstrates adding a rate-limit rule that restricts importData to "
                    "1 call per minute, then removing it later."
                ),
            },
        ],
        "tags": ["rate-limit", "ddp", "security", "remove", "cleanup"],
    },
    {
        "name": "DDPRateLimiter.setErrorMessage",
        "module": "ddp_rate_limiter",
        "signature": "DDPRateLimiter.setErrorMessage(message)",
        "description": (
            "Sets the global error message returned to clients when any rate-limit rule "
            "is triggered. The message parameter can be a string or a function. If it is "
            "a function, it receives an object with rateLimitResult (containing "
            "timeToReset, numInvocationsLeft, and numInvocationsExceeded) and allows you "
            "to construct a dynamic error message. The default error message is "
            "'Error, too many requests. Please slow down. You must wait N seconds "
            "before trying again.'"
        ),
        "params": [
            {
                "name": "message",
                "type": "String | Function",
                "description": (
                    "A string to use as the rate-limit error message, or a function that "
                    "receives an object with rateLimitResult and returns a string. The "
                    "rateLimitResult object contains timeToReset (ms), "
                    "numInvocationsLeft, and numInvocationsExceeded."
                ),
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Set a custom static error message",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "DDPRateLimiter.setErrorMessage(\n"
                    "  'You are sending too many requests. Please try again later.'\n"
                    ");"
                ),
                "description": (
                    "Sets a simple static error message that is returned to clients when "
                    "any rate-limit rule is triggered."
                ),
            },
            {
                "title": "Set a dynamic error message with retry information",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "DDPRateLimiter.setErrorMessage(({ timeToReset }) => {\n"
                    "  const seconds = Math.ceil(timeToReset / 1000);\n"
                    "  return (\n"
                    "    `Too many requests. Please wait ${seconds} ` +\n"
                    "    `second${seconds !== 1 ? 's' : ''} and try again.`\n"
                    "  );\n"
                    "});"
                ),
                "description": (
                    "Uses a function to generate a dynamic error message that tells the "
                    "client how many seconds to wait before retrying."
                ),
            },
        ],
        "tags": [
            "rate-limit",
            "ddp",
            "error",
            "message",
            "security",
            "user-experience",
        ],
    },
    {
        "name": "DDPRateLimiter.setErrorMessageOnRule",
        "module": "ddp_rate_limiter",
        "signature": "DDPRateLimiter.setErrorMessageOnRule(ruleId, message)",
        "description": (
            "Sets a custom error message for a specific rate-limit rule identified by its "
            "rule ID. This overrides the global error message set by setErrorMessage for "
            "that particular rule. The message parameter can be a string or a function. "
            "If it is a function, it receives an object with rateLimitResult and allows "
            "you to construct a dynamic error message specific to that rule. This is "
            "useful when different rate-limit rules should provide different error messages "
            "to clients."
        ),
        "params": [
            {
                "name": "ruleId",
                "type": "String",
                "description": "The unique rule ID returned by DDPRateLimiter.addRule.",
                "optional": False,
            },
            {
                "name": "message",
                "type": "String | Function",
                "description": (
                    "A string to use as the error message for this specific rule, or a "
                    "function that receives an object with rateLimitResult and returns "
                    "a string."
                ),
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Set a rule-specific error message for login rate limiting",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "const loginRuleId = DDPRateLimiter.addRule(\n"
                    "  { type: 'method', name: 'login' },\n"
                    "  5,\n"
                    "  60000\n"
                    ");\n"
                    "\n"
                    "DDPRateLimiter.setErrorMessageOnRule(\n"
                    "  loginRuleId,\n"
                    "  ({ timeToReset }) => {\n"
                    "    const seconds = Math.ceil(timeToReset / 1000);\n"
                    "    return (\n"
                    "      `Too many login attempts. Your account is temporarily ` +\n"
                    "      `locked. Please wait ${seconds} seconds before trying again.`\n"
                    "    );\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Adds a login rate-limit rule (5 attempts per minute) and sets a "
                    "specific error message for it. Other rules will still use the global "
                    "error message."
                ),
            },
            {
                "title": "Different messages for different rules",
                "code": (
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "// Rule for API methods\n"
                    "const apiRuleId = DDPRateLimiter.addRule(\n"
                    "  {\n"
                    "    type: 'method',\n"
                    "    name(name) { return name.startsWith('api.'); },\n"
                    "  },\n"
                    "  100,\n"
                    "  60000\n"
                    ");\n"
                    "\n"
                    "DDPRateLimiter.setErrorMessageOnRule(\n"
                    "  apiRuleId,\n"
                    "  'API rate limit exceeded. Maximum 100 requests per minute.'\n"
                    ");\n"
                    "\n"
                    "// Rule for subscription spam\n"
                    "const subRuleId = DDPRateLimiter.addRule(\n"
                    "  { type: 'subscription' },\n"
                    "  20,\n"
                    "  10000\n"
                    ");\n"
                    "\n"
                    "DDPRateLimiter.setErrorMessageOnRule(\n"
                    "  subRuleId,\n"
                    "  'Too many subscription requests. Please reduce your request rate.'\n"
                    ");"
                ),
                "description": (
                    "Sets distinct error messages for an API method rate-limit rule and a "
                    "subscription rate-limit rule. Each communicates the specific limit "
                    "that was exceeded."
                ),
            },
        ],
        "tags": [
            "rate-limit",
            "ddp",
            "error",
            "message",
            "security",
            "per-rule",
        ],
    },
]
