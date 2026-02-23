"""Meteor.js v3.4.0 EJSON (Extended JSON) API documentation."""

EJSON = [
    {
        "name": "EJSON.stringify",
        "module": "ejson",
        "signature": "EJSON.stringify(val, options)",
        "description": (
            "Serializes an EJSON-compatible value to an Extended JSON string. Unlike "
            "`JSON.stringify`, this function properly handles Meteor-specific types "
            "such as `Date`, `Binary`, special numbers (`NaN`, `Infinity`, `-Infinity`), "
            "and any custom types registered with `EJSON.addType`. The resulting string "
            "can be parsed back with `EJSON.parse` to reconstruct the original value "
            "with types preserved. Supports indentation and canonical formatting options."
        ),
        "params": [
            {
                "name": "val",
                "type": "EJSON-compatible value",
                "description": "The value to stringify. May include Dates, Uint8Arrays, and custom EJSON types.",
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": "Optional settings for serialization.",
            },
            {
                "name": "options.indent",
                "type": "Boolean | Integer | String",
                "optional": True,
                "description": (
                    "Indents objects and arrays for readability. When `true`, uses 2-space indent. "
                    "When an integer, uses that many spaces. When a string (e.g. '\\t'), uses that string for each level."
                ),
            },
            {
                "name": "options.canonical",
                "type": "Boolean",
                "optional": True,
                "description": (
                    "When `true`, stringifies keys in sorted order to produce deterministic output. "
                    "Useful for hashing or comparing serialized documents."
                ),
            },
        ],
        "returns": "String - the EJSON string representation of the value.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Basic serialization with dates",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const doc = {\n"
                    "  name: 'Meeting',\n"
                    "  createdAt: new Date('2024-01-15T10:30:00Z'),\n"
                    "};\n"
                    "\n"
                    "const str = EJSON.stringify(doc);\n"
                    "// '{\"name\":\"Meeting\",\"createdAt\":{\"$date\":1705312200000}}'\n"
                    "\n"
                    "const restored = EJSON.parse(str);\n"
                    "console.log(restored.createdAt instanceof Date); // true"
                ),
                "description": (
                    "Dates are serialized as `{\"$date\": <milliseconds>}` and restored "
                    "as Date objects when parsed back."
                ),
            },
            {
                "title": "Canonical and indented output",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const obj = { z: 1, a: 2, m: 3 };\n"
                    "\n"
                    "// Sorted keys, 2-space indent\n"
                    "const pretty = EJSON.stringify(obj, {\n"
                    "  canonical: true,\n"
                    "  indent: true,\n"
                    "});\n"
                    "console.log(pretty);\n"
                    "// {\n"
                    "//   \"a\": 2,\n"
                    "//   \"m\": 3,\n"
                    "//   \"z\": 1\n"
                    "// }"
                ),
                "description": (
                    "Using `canonical: true` sorts keys alphabetically, making the output deterministic "
                    "across different environments."
                ),
            },
        ],
        "tags": ["ejson", "serialize", "stringify", "json", "encoding"],
    },
    {
        "name": "EJSON.parse",
        "module": "ejson",
        "signature": "EJSON.parse(str)",
        "description": (
            "Parses an Extended JSON string, returning the corresponding EJSON-compatible "
            "value. This is the inverse of `EJSON.stringify`. It recognizes Meteor's "
            "special type encodings (such as `{\"$date\": ...}` for dates, "
            "`{\"$binary\": ...}` for binary data, and `{\"$InfNaN\": ...}` for special "
            "numbers like `NaN`, `Infinity`, and `-Infinity`) and converts them back to "
            "their native JavaScript types. Throws a `SyntaxError` if the string is not "
            "valid JSON."
        ),
        "params": [
            {
                "name": "str",
                "type": "String",
                "description": "An EJSON string to parse, as produced by `EJSON.stringify`.",
                "optional": False,
            },
        ],
        "returns": "EJSON-compatible value - the parsed value with types restored.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Parsing an EJSON string with a date",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const str = '{\"title\":\"Launch\",\"date\":{\"$date\":1700000000000}}';\n"
                    "const doc = EJSON.parse(str);\n"
                    "\n"
                    "console.log(doc.title);              // 'Launch'\n"
                    "console.log(doc.date instanceof Date); // true\n"
                    "console.log(doc.date.toISOString());   // '2023-11-14T22:13:20.000Z'"
                ),
                "description": (
                    "The `$date` encoding is automatically converted back to a JavaScript Date object."
                ),
            },
        ],
        "tags": ["ejson", "parse", "deserialize", "json", "decoding"],
    },
    {
        "name": "EJSON.fromJSONValue",
        "module": "ejson",
        "signature": "EJSON.fromJSONValue(val)",
        "description": (
            "Deserializes an EJSON-compatible JSON value into its full JavaScript "
            "representation. This converts objects with special EJSON type markers "
            "(like `{\"$date\": ...}`, `{\"$binary\": ...}`, `{\"$escape\": ...}`, "
            "and custom types registered via `EJSON.addType`) back to their native "
            "types. Unlike `EJSON.parse`, this takes an already-parsed JavaScript "
            "object rather than a string."
        ),
        "params": [
            {
                "name": "val",
                "type": "JSON-compatible value",
                "description": (
                    "A value as returned by `JSON.parse` or `EJSON.toJSONValue`. May contain "
                    "EJSON type markers like `{\"$date\": <ms>}`."
                ),
                "optional": False,
            },
        ],
        "returns": "EJSON-compatible value - the deserialized value with native types restored.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Converting a JSON-parsed object to full EJSON types",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "// Imagine this came from JSON.parse of an external API response.\n"
                    "const raw = {\n"
                    "  name: 'Event',\n"
                    "  date: { $date: 1700000000000 },\n"
                    "};\n"
                    "\n"
                    "const doc = EJSON.fromJSONValue(raw);\n"
                    "console.log(doc.date instanceof Date); // true"
                ),
                "description": (
                    "Converts EJSON type markers in an already-parsed JSON object back "
                    "to their native JavaScript representations."
                ),
            },
        ],
        "tags": ["ejson", "deserialize", "json", "convert", "types"],
    },
    {
        "name": "EJSON.toJSONValue",
        "module": "ejson",
        "signature": "EJSON.toJSONValue(val)",
        "description": (
            "Serializes an EJSON-compatible value to a JSON-compatible representation. "
            "Dates become `{\"$date\": <milliseconds>}`, binary data becomes "
            "`{\"$binary\": <base64>}`, and custom EJSON types are serialized using "
            "their registered `toJSONValue` method. The result is a plain object "
            "that can be safely passed to `JSON.stringify`. This is the inverse "
            "of `EJSON.fromJSONValue`."
        ),
        "params": [
            {
                "name": "val",
                "type": "EJSON-compatible value",
                "description": "The value to convert. May include Dates, Uint8Arrays, and custom EJSON types.",
                "optional": False,
            },
        ],
        "returns": "JSON-compatible value - the value with special types encoded as EJSON markers.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Converting a value with a Date for JSON transport",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const doc = {\n"
                    "  title: 'Reminder',\n"
                    "  dueDate: new Date('2024-06-01T00:00:00Z'),\n"
                    "};\n"
                    "\n"
                    "const jsonSafe = EJSON.toJSONValue(doc);\n"
                    "console.log(jsonSafe.dueDate);\n"
                    "// { $date: 1717200000000 }\n"
                    "\n"
                    "// Now safe to use with standard JSON.stringify\n"
                    "const str = JSON.stringify(jsonSafe);"
                ),
                "description": (
                    "Converts the Date to an EJSON marker object so it survives a round-trip "
                    "through `JSON.stringify` / `JSON.parse` / `EJSON.fromJSONValue`."
                ),
            },
        ],
        "tags": ["ejson", "serialize", "json", "convert", "types"],
    },
    {
        "name": "EJSON.equals",
        "module": "ejson",
        "signature": "EJSON.equals(a, b, [options])",
        "description": (
            "Performs a deep, type-aware equality comparison between two EJSON-compatible "
            "values. Returns `true` if `a` and `b` are structurally identical, including "
            "correct handling of Date objects (compared by value, not reference), binary "
            "data (compared byte-by-byte), custom EJSON types (compared via their "
            "`equals` method), and nested objects and arrays. Primitive values are "
            "compared with `===`."
        ),
        "params": [
            {
                "name": "a",
                "type": "EJSON-compatible value",
                "description": "The first value to compare.",
                "optional": False,
            },
            {
                "name": "b",
                "type": "EJSON-compatible value",
                "description": "The second value to compare.",
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": "Optional settings for the equality comparison.",
                "optional": True,
            },
            {
                "name": "options.keyOrderSensitive",
                "type": "Boolean",
                "description": (
                    "When `true`, objects are compared with key order taken into "
                    "account. Two objects with the same keys and values but in "
                    "different order will not be considered equal. Defaults to `false`."
                ),
                "optional": True,
            },
        ],
        "returns": "Boolean - `true` if the values are deeply equal, `false` otherwise.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Comparing objects with dates",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const a = { name: 'Task', due: new Date('2024-03-01') };\n"
                    "const b = { name: 'Task', due: new Date('2024-03-01') };\n"
                    "const c = { name: 'Task', due: new Date('2024-04-01') };\n"
                    "\n"
                    "console.log(EJSON.equals(a, b)); // true  (same date value)\n"
                    "console.log(EJSON.equals(a, c)); // false (different date)\n"
                    "console.log(a === b);            // false (different references)"
                ),
                "description": (
                    "Unlike `===`, EJSON.equals compares Date objects by their underlying "
                    "timestamp, not by reference."
                ),
            },
            {
                "title": "Deep comparison of nested structures",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const x = { items: [{ id: 1 }, { id: 2 }] };\n"
                    "const y = { items: [{ id: 1 }, { id: 2 }] };\n"
                    "const z = { items: [{ id: 1 }, { id: 3 }] };\n"
                    "\n"
                    "console.log(EJSON.equals(x, y)); // true\n"
                    "console.log(EJSON.equals(x, z)); // false"
                ),
                "description": "EJSON.equals recursively compares nested objects and arrays.",
            },
        ],
        "tags": ["ejson", "equals", "comparison", "deep-equal"],
    },
    {
        "name": "EJSON.clone",
        "module": "ejson",
        "signature": "EJSON.clone(val)",
        "description": (
            "Returns a deep copy of an EJSON-compatible value. The clone is structurally "
            "identical to the original but shares no references with it, so mutating the "
            "clone will not affect the original. Correctly handles Date objects (cloned "
            "by value), binary data (copied to a new buffer), custom EJSON types "
            "(cloned via their `clone` method), and arbitrarily nested objects and arrays."
        ),
        "params": [
            {
                "name": "val",
                "type": "EJSON-compatible value",
                "description": "The value to deep-clone.",
                "optional": False,
            },
        ],
        "returns": "EJSON-compatible value - a deep copy of the input with no shared references.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Cloning a document before mutation",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const original = {\n"
                    "  title: 'Report',\n"
                    "  createdAt: new Date(),\n"
                    "  tags: ['draft', 'internal'],\n"
                    "};\n"
                    "\n"
                    "const copy = EJSON.clone(original);\n"
                    "copy.tags.push('reviewed');\n"
                    "\n"
                    "console.log(original.tags); // ['draft', 'internal'] (unchanged)\n"
                    "console.log(copy.tags);     // ['draft', 'internal', 'reviewed']"
                ),
                "description": (
                    "The clone is fully independent. Pushing to the clone's tags array "
                    "does not affect the original."
                ),
            },
        ],
        "tags": ["ejson", "clone", "deep-copy", "immutable"],
    },
    {
        "name": "EJSON.isBinary",
        "module": "ejson",
        "signature": "EJSON.isBinary(x)",
        "description": (
            "Returns `true` if the value is a binary data type that EJSON knows how to "
            "serialize. Returns `true` for values created by `EJSON.newBinary`. In "
            "Meteor v3, `EJSON.newBinary` returns a `Uint8Array`, so plain "
            "`Uint8Array` instances also return `true`. Use this to check whether "
            "a value will be handled as binary data during EJSON serialization."
        ),
        "params": [
            {
                "name": "x",
                "type": "Object",
                "description": "The value to test.",
                "optional": False,
            },
        ],
        "returns": "Boolean - `true` if the value is an EJSON-recognized binary type.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Checking for binary data",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "const bin = EJSON.newBinary(4);\n"
                    "bin[0] = 0xFF;\n"
                    "bin[1] = 0x00;\n"
                    "bin[2] = 0xAB;\n"
                    "bin[3] = 0xCD;\n"
                    "\n"
                    "console.log(EJSON.isBinary(bin));             // true\n"
                    "console.log(EJSON.isBinary(new Uint8Array(4))); // true\n"
                    "console.log(EJSON.isBinary('hello'));          // false\n"
                    "console.log(EJSON.isBinary([1, 2, 3]));       // false"
                ),
                "description": (
                    "Identifies values that EJSON will serialize as binary. Useful when "
                    "handling mixed data that might contain file contents or binary payloads."
                ),
            },
        ],
        "tags": ["ejson", "binary", "type-check", "uint8array"],
    },
    {
        "name": "EJSON.addType",
        "module": "ejson",
        "signature": "EJSON.addType(name, factory)",
        "description": (
            "Registers a custom type so that EJSON can serialize and deserialize it. "
            "The type's class must implement a `typeName()` method returning the same "
            "string as the `name` argument and a `toJSONValue()` method returning a "
            "JSON-serializable representation. Optionally, it may also implement "
            "`equals(other)` and `clone()` for custom comparison and cloning "
            "behavior; Meteor provides defaults if these are absent. The "
            "`factory` function receives the JSON value produced by `toJSONValue` and "
            "must return a new instance of the type. After registration, instances of "
            "this type can be used anywhere EJSON values are expected, including in "
            "Meteor method arguments, publication data, and Session variables."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": (
                    "A unique string identifying this type. Must match the value returned "
                    "by the class's `typeName()` method."
                ),
                "optional": False,
            },
            {
                "name": "factory",
                "type": "Function",
                "description": (
                    "A function that takes a JSON-compatible value (as produced by the type's "
                    "`toJSONValue` method) and returns a new instance of the custom type."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Registering a custom Money type",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "class Money {\n"
                    "  constructor(amount, currency) {\n"
                    "    this.amount = amount;\n"
                    "    this.currency = currency;\n"
                    "  }\n"
                    "\n"
                    "  typeName() {\n"
                    "    return 'Money';\n"
                    "  }\n"
                    "\n"
                    "  toJSONValue() {\n"
                    "    return { amount: this.amount, currency: this.currency };\n"
                    "  }\n"
                    "\n"
                    "  clone() {\n"
                    "    return new Money(this.amount, this.currency);\n"
                    "  }\n"
                    "\n"
                    "  equals(other) {\n"
                    "    return other instanceof Money\n"
                    "      && this.amount === other.amount\n"
                    "      && this.currency === other.currency;\n"
                    "  }\n"
                    "\n"
                    "  toString() {\n"
                    "    return `${this.amount} ${this.currency}`;\n"
                    "  }\n"
                    "}\n"
                    "\n"
                    "EJSON.addType('Money', (json) => new Money(json.amount, json.currency));\n"
                    "\n"
                    "// Now Money instances survive EJSON round-trips:\n"
                    "const price = new Money(19.99, 'USD');\n"
                    "const str = EJSON.stringify(price);\n"
                    "const restored = EJSON.parse(str);\n"
                    "console.log(restored instanceof Money); // true\n"
                    "console.log(restored.toString());        // '19.99 USD'"
                ),
                "description": (
                    "Defines a Money class with the required EJSON interface (typeName, toJSONValue, "
                    "clone, equals) and registers it. After registration, Money instances can be "
                    "passed through Meteor methods, publications, and EJSON serialization."
                ),
            },
        ],
        "tags": ["ejson", "custom-type", "serialize", "addtype", "extensibility"],
    },
    {
        "name": "EJSON.newBinary",
        "module": "ejson",
        "signature": "EJSON.newBinary(size)",
        "description": (
            "Creates a new binary data buffer of the given size in bytes, suitable for "
            "use with EJSON serialization. The returned object is a `Uint8Array` that "
            "EJSON recognizes as binary data. When serialized with `EJSON.stringify`, "
            "binary data is encoded using base64. Use this function rather than "
            "constructing a `Uint8Array` directly if you want to ensure maximum "
            "compatibility with EJSON serialization across all Meteor versions."
        ),
        "params": [
            {
                "name": "size",
                "type": "Number",
                "description": "The length of the binary buffer in bytes.",
                "optional": False,
            },
        ],
        "returns": "Uint8Array - a binary buffer of the specified size, initialized to zeros.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Creating and serializing binary data",
                "code": (
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "// Create a 4-byte binary buffer.\n"
                    "const buf = EJSON.newBinary(4);\n"
                    "buf[0] = 0xDE;\n"
                    "buf[1] = 0xAD;\n"
                    "buf[2] = 0xBE;\n"
                    "buf[3] = 0xEF;\n"
                    "\n"
                    "// Serialize to EJSON string (binary data becomes base64).\n"
                    "const str = EJSON.stringify({ data: buf });\n"
                    "console.log(str);\n"
                    "// '{\"data\":{\"$binary\":\"3q2+7w==\"}}'\n"
                    "\n"
                    "// Parse back to restore the binary buffer.\n"
                    "const restored = EJSON.parse(str);\n"
                    "console.log(EJSON.isBinary(restored.data)); // true\n"
                    "console.log(restored.data[0]);               // 222 (0xDE)"
                ),
                "description": (
                    "Creates a binary buffer, fills it with bytes, and demonstrates a "
                    "round-trip through EJSON serialization with base64 encoding."
                ),
            },
            {
                "title": "Storing binary data in a Meteor method",
                "code": (
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async storeChecksum(docId, checksumBytes) {\n"
                    "    check(docId, String);\n"
                    "    check(checksumBytes, Match.Where(EJSON.isBinary));\n"
                    "\n"
                    "    return await DocsCollection.updateAsync(docId, {\n"
                    "      $set: { checksum: checksumBytes },\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Validates that the checksum argument is binary data using `EJSON.isBinary` "
                    "as a `Match.Where` predicate, then stores it in the database."
                ),
            },
        ],
        "tags": ["ejson", "binary", "buffer", "uint8array", "base64"],
    },
]
