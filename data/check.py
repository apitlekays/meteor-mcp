"""Meteor.js v3.4.0 check and Match API documentation."""

CHECK = [
    {
        "name": "check",
        "module": "check",
        "signature": "check(value, pattern, [options])",
        "description": (
            "Checks that a value matches a pattern. If the value does not match, "
            "throws a `Match.Error` describing how it failed. This is especially "
            "useful for validating arguments to Meteor methods and publish functions. "
            "By calling `check` at the top of your method body, you ensure that "
            "malformed or malicious input is rejected before any real work is done. "
            "On the server, failed checks on method arguments are automatically "
            "logged and result in a [400] error returned to the client."
        ),
        "params": [
            {
                "name": "value",
                "type": "Any",
                "description": "The value to check against the pattern.",
                "optional": False,
            },
            {
                "name": "pattern",
                "type": "MatchPattern",
                "description": (
                    "The pattern to match against. Can be a constructor (String, Number, Boolean, Object, Array, Function), "
                    "a specific value for exact equality, a Match pattern (Match.Optional, Match.OneOf, etc.), "
                    "an array containing a single pattern (matches arrays whose elements all match the pattern), "
                    "or a plain object whose values are patterns (matches objects with the same keys whose values match)."
                ),
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": "Optional settings for the check operation.",
                "optional": True,
            },
            {
                "name": "options.throwAllErrors",
                "type": "Boolean",
                "description": (
                    "If true, throw all validation errors instead of stopping at "
                    "the first one. Defaults to false."
                ),
                "optional": True,
            },
        ],
        "returns": "void (throws Match.Error on failure)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Validating Meteor method arguments",
                "code": (
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async updateProfile(userId, profile) {\n"
                    "    check(userId, String);\n"
                    "    check(profile, {\n"
                    "      name: String,\n"
                    "      age: Number,\n"
                    "      bio: String,\n"
                    "    });\n"
                    "\n"
                    "    return await Meteor.users.updateAsync(userId, {\n"
                    "      $set: { profile },\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Validates that userId is a string and profile is an object with the expected shape. "
                    "If a client sends a number for userId or omits a required field, "
                    "a Match.Error is thrown and the method returns a 400 error."
                ),
            },
            {
                "title": "Checking an array of objects",
                "code": (
                    "import { check } from 'meteor/check';\n"
                    "\n"
                    "const items = [\n"
                    "  { name: 'Widget', price: 9.99 },\n"
                    "  { name: 'Gadget', price: 24.50 },\n"
                    "];\n"
                    "\n"
                    "check(items, [{ name: String, price: Number }]);\n"
                    "// Passes: every element matches the object pattern."
                ),
                "description": (
                    "Wrapping a pattern in an array means every element of the value must match that pattern."
                ),
            },
        ],
        "tags": ["check", "validation", "match", "security", "methods"],
    },
    {
        "name": "Match.test",
        "module": "check",
        "signature": "Match.test(value, pattern)",
        "description": (
            "Returns `true` if the value matches the pattern, `false` otherwise. "
            "Unlike `check`, this function does not throw an exception on failure, "
            "making it suitable for conditional logic where you want to branch based "
            "on whether data conforms to a shape rather than reject it outright."
        ),
        "params": [
            {
                "name": "value",
                "type": "Any",
                "description": "The value to test against the pattern.",
                "optional": False,
            },
            {
                "name": "pattern",
                "type": "MatchPattern",
                "description": "The pattern to test against. Accepts the same patterns as `check`.",
                "optional": False,
            },
        ],
        "returns": "Boolean - `true` if the value matches, `false` otherwise.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Conditional validation without throwing",
                "code": (
                    "import { Match } from 'meteor/check';\n"
                    "\n"
                    "const input = getUserInput();\n"
                    "\n"
                    "if (Match.test(input, { email: String, age: Number })) {\n"
                    "  // input is well-formed, proceed\n"
                    "  processUser(input);\n"
                    "} else {\n"
                    "  // input is invalid, show a friendly message\n"
                    "  showError('Please provide a valid email and age.');\n"
                    "}"
                ),
                "description": (
                    "Uses Match.test to check if the input matches an expected shape "
                    "before processing, allowing graceful handling of invalid data."
                ),
            },
            {
                "title": "Type narrowing with Match.test",
                "code": (
                    "import { Match } from 'meteor/check';\n"
                    "\n"
                    "function formatValue(val) {\n"
                    "  if (Match.test(val, String)) {\n"
                    "    return val.toUpperCase();\n"
                    "  }\n"
                    "  if (Match.test(val, Number)) {\n"
                    "    return val.toFixed(2);\n"
                    "  }\n"
                    "  return String(val);\n"
                    "}"
                ),
                "description": "Uses Match.test to determine the type of a value and handle each case differently.",
            },
        ],
        "tags": ["match", "test", "validation", "check", "boolean"],
    },
    {
        "name": "Match.ObjectIncluding",
        "module": "check",
        "signature": "Match.ObjectIncluding(pattern)",
        "description": (
            "Matches any object that includes at least the keys specified in `pattern`, "
            "with values matching the corresponding sub-patterns. The object may contain "
            "additional keys beyond those listed in the pattern and the match will still "
            "succeed. This is useful when you only care about validating certain fields "
            "of a larger object, such as checking a subset of fields on a user profile "
            "while ignoring other fields that may be present."
        ),
        "params": [
            {
                "name": "pattern",
                "type": "Object",
                "description": (
                    "An object whose keys define the minimum required keys, and whose values "
                    "are patterns that the corresponding values must match."
                ),
                "optional": False,
            },
        ],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Validating a subset of fields",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "const user = {\n"
                    "  name: 'Alice',\n"
                    "  email: 'alice@example.com',\n"
                    "  age: 30,\n"
                    "  avatarUrl: 'https://example.com/alice.png',\n"
                    "};\n"
                    "\n"
                    "// Only validate name and email; ignore other keys.\n"
                    "check(user, Match.ObjectIncluding({\n"
                    "  name: String,\n"
                    "  email: String,\n"
                    "}));\n"
                    "// Passes even though age and avatarUrl are present."
                ),
                "description": (
                    "Validates that the object has at least the `name` and `email` fields as strings. "
                    "Extra fields like `age` and `avatarUrl` are ignored."
                ),
            },
        ],
        "tags": ["match", "object", "partial", "validation", "check"],
    },
    {
        "name": "Match.Optional",
        "module": "check",
        "signature": "Match.Optional(pattern)",
        "description": (
            "Matches `undefined` or a value that matches the given pattern. This is "
            "intended for use inside object patterns to mark fields that may be absent. "
            "It does not match `null`; use `Match.Maybe` if you need to also accept "
            "`null`. When used within an object pattern passed to `check`, a key whose "
            "value is `undefined` or that is missing from the object entirely will pass validation."
        ),
        "params": [
            {
                "name": "pattern",
                "type": "MatchPattern",
                "description": "The pattern to match when the value is not `undefined`.",
                "optional": False,
            },
        ],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Optional fields in an object pattern",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async createPost(data) {\n"
                    "    check(data, {\n"
                    "      title: String,\n"
                    "      body: String,\n"
                    "      subtitle: Match.Optional(String),\n"
                    "      tags: Match.Optional([String]),\n"
                    "    });\n"
                    "\n"
                    "    // subtitle and tags may be omitted entirely.\n"
                    "    return await PostsCollection.insertAsync(data);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "The `subtitle` and `tags` fields are optional. Passing an object without them "
                    "is valid, but if present they must be a String and an array of Strings respectively."
                ),
            },
        ],
        "tags": ["match", "optional", "undefined", "validation", "check"],
    },
    {
        "name": "Match.Maybe",
        "module": "check",
        "signature": "Match.Maybe(pattern)",
        "description": (
            "Matches `undefined`, `null`, or a value that matches the given pattern. "
            "This is like `Match.Optional` but also accepts `null`. Use this when "
            "a field may be explicitly set to `null` in addition to being absent or "
            "`undefined`. This is particularly useful when dealing with database "
            "documents where fields may be stored as `null` rather than omitted."
        ),
        "params": [
            {
                "name": "pattern",
                "type": "MatchPattern",
                "description": "The pattern to match when the value is not `undefined` or `null`.",
                "optional": False,
            },
        ],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Accepting null values from a form",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async updateSettings(settings) {\n"
                    "    check(settings, {\n"
                    "      theme: String,\n"
                    "      nickname: Match.Maybe(String),\n"
                    "    });\n"
                    "\n"
                    "    // nickname can be a string, null, or undefined.\n"
                    "    const userId = this.userId;\n"
                    "    return await SettingsCollection.updateAsync(\n"
                    "      { userId },\n"
                    "      { $set: settings },\n"
                    "    );\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "The `nickname` field accepts a string, `null` (explicitly cleared), "
                    "or `undefined` (not provided). The `theme` field is always required."
                ),
            },
        ],
        "tags": ["match", "maybe", "null", "optional", "validation", "check"],
    },
    {
        "name": "Match.OneOf",
        "module": "check",
        "signature": "Match.OneOf(...patterns)",
        "description": (
            "Matches a value that matches at least one of the given patterns. "
            "This is useful for accepting multiple types for a single parameter, "
            "such as allowing both a string ID and a numeric ID, or accepting "
            "different object shapes for a polymorphic argument. The patterns are "
            "tested in order; the value passes if any pattern matches."
        ),
        "params": [
            {
                "name": "patterns",
                "type": "MatchPattern (variadic)",
                "description": "Two or more patterns. The value must match at least one of them.",
                "optional": False,
            },
        ],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Accepting multiple types",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async findItem(idOrSlug) {\n"
                    "    check(idOrSlug, Match.OneOf(String, Number));\n"
                    "\n"
                    "    const query = typeof idOrSlug === 'string'\n"
                    "      ? { slug: idOrSlug }\n"
                    "      : { legacyId: idOrSlug };\n"
                    "\n"
                    "    return await ItemsCollection.findOneAsync(query);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Accepts either a string slug or a numeric legacy ID. "
                    "After validation, the code branches based on the actual type."
                ),
            },
            {
                "title": "Union of object shapes",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "check(event, Match.OneOf(\n"
                    "  { type: 'click', x: Number, y: Number },\n"
                    "  { type: 'keypress', key: String },\n"
                    "));"
                ),
                "description": "Validates that an event matches one of two possible shapes.",
            },
        ],
        "tags": ["match", "oneof", "union", "validation", "check"],
    },
    {
        "name": "Match.Where",
        "module": "check",
        "signature": "Match.Where(condition)",
        "description": (
            "Calls the `condition` function with the value. If it returns `true`, the "
            "match succeeds. If it returns `false` or throws, the match fails. This "
            "lets you define custom validation logic beyond what the built-in patterns "
            "support, such as range checks, regex tests, or cross-field validations. "
            "The condition function should be a pure predicate with no side effects."
        ),
        "params": [
            {
                "name": "condition",
                "type": "Function",
                "description": (
                    "A function that takes the value and returns `true` if it is valid. "
                    "Returning `false` or throwing causes the match to fail."
                ),
                "optional": False,
            },
        ],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Custom range validation",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "const PositiveNumber = Match.Where((x) => {\n"
                    "  check(x, Number);\n"
                    "  return x > 0;\n"
                    "});\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async setPrice(productId, price) {\n"
                    "    check(productId, String);\n"
                    "    check(price, PositiveNumber);\n"
                    "\n"
                    "    return await ProductsCollection.updateAsync(productId, {\n"
                    "      $set: { price },\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Defines a reusable PositiveNumber pattern that first checks the value "
                    "is a Number, then verifies it is greater than zero."
                ),
            },
            {
                "title": "Regex-based string validation",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "const EmailString = Match.Where((x) => {\n"
                    "  check(x, String);\n"
                    "  return /^[^@]+@[^@]+\\.[^@]+$/.test(x);\n"
                    "});\n"
                    "\n"
                    "check('user@example.com', EmailString); // passes\n"
                    "check('not-an-email', EmailString);      // throws Match.Error"
                ),
                "description": "Creates a custom pattern that validates strings against a regex.",
            },
        ],
        "tags": ["match", "where", "custom", "validation", "predicate", "check"],
    },
    {
        "name": "Match.Integer",
        "module": "check",
        "signature": "Match.Integer",
        "description": (
            "Matches a signed 32-bit integer. The value must be a number with no "
            "fractional part, and must be within the range of a 32-bit signed integer "
            "(-2147483648 to 2147483647). Values like `1.5`, `Infinity`, `NaN`, and "
            "numbers outside the 32-bit range will not match. This is useful for "
            "validating database IDs, pagination offsets, or any parameter that should "
            "be a whole number."
        ),
        "params": [],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Validating pagination parameters",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async getPage(pageNumber, pageSize) {\n"
                    "    check(pageNumber, Match.Integer);\n"
                    "    check(pageSize, Match.Integer);\n"
                    "\n"
                    "    const skip = (pageNumber - 1) * pageSize;\n"
                    "    return await ItemsCollection.find({}, {\n"
                    "      skip,\n"
                    "      limit: pageSize,\n"
                    "    }).fetchAsync();\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Ensures page number and page size are integers, not floats or other number types."
                ),
            },
        ],
        "tags": ["match", "integer", "number", "validation", "check"],
    },
    {
        "name": "Match.Any",
        "module": "check",
        "signature": "Match.Any",
        "description": (
            "Matches any value. This is useful as a placeholder in object patterns "
            "when you want to ensure a key exists but do not care about its type. "
            "It will match strings, numbers, booleans, objects, arrays, null, "
            "undefined, and any other JavaScript value."
        ),
        "params": [],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Requiring a key exists with any value",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async logEvent(event) {\n"
                    "    check(event, {\n"
                    "      type: String,\n"
                    "      timestamp: Number,\n"
                    "      payload: Match.Any,\n"
                    "    });\n"
                    "\n"
                    "    // payload can be anything: string, object, array, etc.\n"
                    "    return await EventsCollection.insertAsync(event);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "The `type` must be a string and `timestamp` a number, but "
                    "`payload` is accepted regardless of its type."
                ),
            },
        ],
        "tags": ["match", "any", "wildcard", "validation", "check"],
    },
    {
        "name": "Match.NonEmptyString",
        "module": "check",
        "signature": "Match.NonEmptyString",
        "description": (
            "Matches any non-empty string. The value must be of type `String` and "
            "must have a length of at least 1. Empty strings (`''`) will not match. "
            "This is a convenient shorthand for validating that a string argument is "
            "not blank, without needing to write a custom `Match.Where` predicate."
        ),
        "params": [],
        "returns": "MatchPattern - a pattern that can be used with `check` or `Match.test`.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Validating a required non-empty name",
                "code": (
                    "import { check, Match } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async createProject(name) {\n"
                    "    check(name, Match.NonEmptyString);\n"
                    "\n"
                    "    return await ProjectsCollection.insertAsync({ name });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Ensures the project name is a string with at least one character. "
                    "Passing an empty string will throw a Match.Error."
                ),
            },
        ],
        "tags": ["match", "string", "nonempty", "validation", "check"],
    },
]
