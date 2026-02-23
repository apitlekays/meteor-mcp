"""Meteor.js Session API - client-side reactive key-value store (v3.4.0)."""

SESSION = [
    {
        "name": "Session.set",
        "module": "session",
        "signature": "Session.set(key, value) | Session.set(object)",
        "description": (
            "Set a variable in the Session. Can also be called with an object of "
            "key-value pairs to set multiple variables at once. Any computations "
            "that called `Session.get` or `Session.equals` with the same key will "
            "be invalidated and rerun.\n\n"
            "The value can be any EJSON-compatible type including strings, numbers, "
            "booleans, arrays, objects, Date, and null. Setting a key to the same "
            "value it already holds (using EJSON equality) will not trigger "
            "invalidation.\n\n"
            "Session is a client-only API provided by the `session` package. It "
            "provides a global reactive key-value store suitable for transient UI "
            "state that does not need to persist across page reloads."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The key to set, e.g. 'selectedItemId'.",
                "optional": False,
            },
            {
                "name": "value",
                "type": "EJSON-compatible value",
                "description": (
                    "The new value for the key. Can be any EJSON-compatible type."
                ),
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Setting and reacting to session variables",
                "code": (
                    "import { Session } from 'meteor/session';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "// Set a session variable\n"
                    "Session.set('selectedTab', 'profile');\n"
                    "\n"
                    "// React to changes\n"
                    "Tracker.autorun(() => {\n"
                    "  const tab = Session.get('selectedTab');\n"
                    "  console.log('Active tab:', tab);\n"
                    "});\n"
                    "\n"
                    "// Update the variable - triggers the autorun\n"
                    "Session.set('selectedTab', 'settings');"
                ),
                "description": (
                    "Session.set stores a reactive value that triggers reruns in "
                    "any autorun that reads the same key with Session.get."
                ),
            },
            {
                "title": "Setting complex values",
                "code": (
                    "Session.set('filters', {\n"
                    "  category: 'electronics',\n"
                    "  priceRange: [100, 500],\n"
                    "  inStock: true\n"
                    "});\n"
                    "\n"
                    "Session.set('selectedDate', new Date());\n"
                    "Session.set('tags', ['javascript', 'meteor']);"
                ),
                "description": (
                    "Session supports EJSON-compatible values including objects, "
                    "arrays, and Dates."
                ),
            },
        ],
        "tags": ["session", "set", "reactive", "state", "client"],
    },
    {
        "name": "Session.setDefault",
        "module": "session",
        "signature": "Session.setDefault(key, value)",
        "description": (
            "Set a variable in the Session only if it has not already been set. "
            "This is useful for initializing session variables with default values "
            "without overwriting values that may have been set elsewhere.\n\n"
            "If the key already exists in the Session (even if its value is "
            "`undefined`), this method does nothing. Otherwise, it behaves "
            "identically to `Session.set`."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The key to set if not already defined.",
                "optional": False,
            },
            {
                "name": "value",
                "type": "EJSON-compatible value",
                "description": "The default value to use if the key is not set.",
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Initializing session defaults",
                "code": (
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "// Initialize defaults (typically in client startup code)\n"
                    "Session.setDefault('locale', 'en');\n"
                    "Session.setDefault('theme', 'light');\n"
                    "Session.setDefault('sidebarOpen', true);\n"
                    "\n"
                    "// If a user action already set 'locale' to 'fr',\n"
                    "// setDefault will not overwrite it\n"
                    "Session.set('locale', 'fr');\n"
                    "Session.setDefault('locale', 'en');\n"
                    "console.log(Session.get('locale')); // 'fr'"
                ),
                "description": (
                    "setDefault is safe to call multiple times. It only sets the "
                    "value the first time, preventing accidental overwrites."
                ),
            },
        ],
        "tags": ["session", "setDefault", "initialize", "default", "client"],
    },
    {
        "name": "Session.get",
        "module": "session",
        "signature": "Session.get(key)",
        "description": (
            "Get the value of a session variable. If called inside a reactive "
            "computation (such as `Tracker.autorun`, a Blaze template helper, or "
            "a `useTracker` hook), the computation will be invalidated and rerun "
            "whenever `Session.set` is called with the same key and a different "
            "value.\n\n"
            "Returns `undefined` if the key has never been set."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The name of the session variable to retrieve.",
                "optional": False,
            },
        ],
        "returns": "The value of the session variable, or `undefined` if not set.",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Reading session variables reactively",
                "code": (
                    "import { Session } from 'meteor/session';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "Session.set('username', 'Alice');\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const name = Session.get('username');\n"
                    "  console.log('Hello,', name);\n"
                    "});\n"
                    "// Logs: 'Hello, Alice'\n"
                    "\n"
                    "Session.set('username', 'Bob');\n"
                    "// Logs: 'Hello, Bob'"
                ),
                "description": (
                    "Session.get is reactive. When the value changes, any "
                    "computation that called get with that key will rerun."
                ),
            },
            {
                "title": "Using Session.get in a React component with useTracker",
                "code": (
                    "import React from 'react';\n"
                    "import { useTracker } from 'meteor/react-meteor-data';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "function ThemeToggle() {\n"
                    "  const theme = useTracker(() => Session.get('theme'), []);\n"
                    "\n"
                    "  return (\n"
                    "    <button onClick={() => {\n"
                    "      Session.set('theme', theme === 'light' ? 'dark' : 'light');\n"
                    "    }}>\n"
                    "      Current theme: {theme}\n"
                    "    </button>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "In React components, use useTracker to read Session variables "
                    "reactively. The component will re-render when the value changes."
                ),
            },
        ],
        "tags": ["session", "get", "reactive", "read", "state", "client"],
    },
    {
        "name": "Session.equals",
        "module": "session",
        "signature": "Session.equals(key, value)",
        "description": (
            "Test if a session variable is equal to a value. If called inside a "
            "reactive computation, the computation is invalidated only when the "
            "equality result changes (from true to false or vice versa), not on "
            "every change to the session variable.\n\n"
            "This is more efficient than using `Session.get(key) === value` because "
            "it creates a finer-grained dependency. For example, if you have a list "
            "of items and each checks `Session.equals('selectedId', item._id)`, only "
            "the previously selected and newly selected items will rerun when the "
            "selection changes.\n\n"
            "Uses EJSON equality for comparison. The value must be a scalar "
            "(string, number, boolean, null, or undefined); object and array values "
            "are not supported and will always return false."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The name of the session variable to test.",
                "optional": False,
            },
            {
                "name": "value",
                "type": "String | Number | Boolean | null | undefined",
                "description": "The value to test against.",
                "optional": False,
            },
        ],
        "returns": "Boolean - `true` if the session variable equals the given value.",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Efficient reactive equality check",
                "code": (
                    "import { Session } from 'meteor/session';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "Session.set('selectedTab', 'home');\n"
                    "\n"
                    "// This autorun only reruns when the result of the\n"
                    "// equality check changes, not on every set\n"
                    "Tracker.autorun(() => {\n"
                    "  if (Session.equals('selectedTab', 'home')) {\n"
                    "    console.log('Home tab is selected');\n"
                    "  } else {\n"
                    "    console.log('Home tab is not selected');\n"
                    "  }\n"
                    "});\n"
                    "\n"
                    "Session.set('selectedTab', 'profile');\n"
                    "// Autorun reruns because equality changed (true -> false)\n"
                    "\n"
                    "Session.set('selectedTab', 'settings');\n"
                    "// Autorun does NOT rerun because equality is still false"
                ),
                "description": (
                    "Session.equals is more efficient than Session.get for "
                    "equality checks because it only invalidates when the boolean "
                    "result of the comparison changes."
                ),
            },
            {
                "title": "Highlighting the selected item in a list",
                "code": (
                    "// In a Blaze template helper\n"
                    "Template.itemList.helpers({\n"
                    "  isSelected() {\n"
                    "    // Only this specific item's helper reruns when selection changes\n"
                    "    return Session.equals('selectedItemId', this._id);\n"
                    "  }\n"
                    "});\n"
                    "\n"
                    "Template.itemList.events({\n"
                    "  'click .item'(event, template) {\n"
                    "    Session.set('selectedItemId', this._id);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "When selecting items in a list, Session.equals ensures only "
                    "the affected items re-render, not the entire list."
                ),
            },
        ],
        "tags": [
            "session",
            "equals",
            "reactive",
            "comparison",
            "efficient",
            "optimization",
            "client",
        ],
    },
]
