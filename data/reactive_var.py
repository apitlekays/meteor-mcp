"""Meteor.js ReactiveVar API - standalone reactive variable (v3.4.0)."""

REACTIVE_VAR = [
    {
        "name": "new ReactiveVar",
        "module": "reactive_var",
        "signature": "new ReactiveVar(initialValue, [equalsFunc])",
        "description": (
            "Constructs a new ReactiveVar with the given initial value. A "
            "ReactiveVar is a standalone reactive data source that holds a single "
            "value and can be used outside of collections and Session.\n\n"
            "ReactiveVar is provided by the `reactive-var` package. Unlike "
            "Session, ReactiveVar instances are not global singletons. Each "
            "ReactiveVar is an independent variable, making them ideal for "
            "component-scoped or module-scoped reactive state.\n\n"
            "The optional `equalsFunc` is a comparison function used to determine "
            "whether a new value is different from the current value. If the "
            "function returns `true`, the set is considered a no-op and dependents "
            "are not invalidated. By default, ReactiveVar uses `===` for "
            "primitive values and always invalidates for object values."
        ),
        "params": [
            {
                "name": "initialValue",
                "type": "Any",
                "description": "The initial value for the ReactiveVar.",
                "optional": False,
            },
            {
                "name": "equalsFunc",
                "type": "Function",
                "optional": True,
                "description": (
                    "A function of two arguments (oldValue, newValue) that returns "
                    "`true` if the values should be considered equal. When equal, "
                    "`set()` will not invalidate dependents."
                ),
            },
        ],
        "returns": "ReactiveVar - a new ReactiveVar instance.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Creating a basic ReactiveVar",
                "code": (
                    "import { ReactiveVar } from 'meteor/reactive-var';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const counter = new ReactiveVar(0);\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  console.log('Counter:', counter.get());\n"
                    "});\n"
                    "// Logs: 'Counter: 0'\n"
                    "\n"
                    "counter.set(1);\n"
                    "// Logs: 'Counter: 1'"
                ),
                "description": (
                    "A ReactiveVar holds a single value and triggers dependent "
                    "computations when the value changes."
                ),
            },
            {
                "title": "Custom equality function for objects",
                "code": (
                    "import { ReactiveVar } from 'meteor/reactive-var';\n"
                    "import { EJSON } from 'meteor/ejson';\n"
                    "\n"
                    "// Use EJSON.equals to do deep comparison for objects\n"
                    "const filters = new ReactiveVar(\n"
                    "  { status: 'active', sort: 'name' },\n"
                    "  EJSON.equals\n"
                    ");\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  console.log('Filters:', filters.get());\n"
                    "});\n"
                    "\n"
                    "// Setting to a deeply equal object does NOT trigger a rerun\n"
                    "filters.set({ status: 'active', sort: 'name' });\n"
                    "\n"
                    "// Setting to a different object DOES trigger a rerun\n"
                    "filters.set({ status: 'archived', sort: 'date' });"
                ),
                "description": (
                    "Provide a custom equality function to prevent unnecessary "
                    "invalidation when setting object values that are deeply equal."
                ),
            },
        ],
        "tags": [
            "reactive-var",
            "constructor",
            "reactive",
            "variable",
            "state",
            "client",
        ],
    },
    {
        "name": "ReactiveVar.get",
        "module": "reactive_var",
        "signature": "reactiveVar.get()",
        "description": (
            "Returns the current value of the ReactiveVar. If called inside a "
            "reactive computation, the computation is registered as a dependent "
            "and will be invalidated when the value changes.\n\n"
            "If called outside a reactive context, it simply returns the current "
            "value without establishing any dependency."
        ),
        "params": [],
        "returns": "The current value of the ReactiveVar.",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Reading a ReactiveVar in an autorun",
                "code": (
                    "import { ReactiveVar } from 'meteor/reactive-var';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const message = new ReactiveVar('Hello');\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  // This creates a reactive dependency\n"
                    "  const msg = message.get();\n"
                    "  document.getElementById('output').textContent = msg;\n"
                    "});\n"
                    "\n"
                    "message.set('World');\n"
                    "// The autorun reruns and updates the DOM"
                ),
                "description": (
                    "Calling get() inside a reactive context registers a "
                    "dependency so the computation reruns when the value changes."
                ),
            },
            {
                "title": "Using ReactiveVar with React and useTracker",
                "code": (
                    "import React from 'react';\n"
                    "import { useTracker } from 'meteor/react-meteor-data';\n"
                    "import { ReactiveVar } from 'meteor/reactive-var';\n"
                    "\n"
                    "const searchQuery = new ReactiveVar('');\n"
                    "\n"
                    "function SearchBox() {\n"
                    "  const query = useTracker(() => searchQuery.get(), []);\n"
                    "\n"
                    "  return (\n"
                    "    <input\n"
                    "      value={query}\n"
                    "      onChange={(e) => searchQuery.set(e.target.value)}\n"
                    "      placeholder=\"Search...\"\n"
                    "    />\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "ReactiveVar integrates seamlessly with React through "
                    "the useTracker hook from react-meteor-data."
                ),
            },
        ],
        "tags": ["reactive-var", "get", "reactive", "read", "state", "client"],
    },
    {
        "name": "ReactiveVar.set",
        "module": "reactive_var",
        "signature": "reactiveVar.set(newValue)",
        "description": (
            "Sets a new value for the ReactiveVar. If the new value is different "
            "from the current value (as determined by the equality function), all "
            "reactive computations that depend on this ReactiveVar are invalidated "
            "and will rerun during the next Tracker flush cycle.\n\n"
            "If no custom `equalsFunc` was provided to the constructor, the "
            "comparison uses `===` for primitive values and always considers "
            "objects as different (even if they are deeply equal). To avoid "
            "unnecessary invalidation with objects, provide a custom equality "
            "function such as `EJSON.equals`."
        ),
        "params": [
            {
                "name": "newValue",
                "type": "Any",
                "description": "The new value to store in the ReactiveVar.",
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Setting values and triggering reactivity",
                "code": (
                    "import { ReactiveVar } from 'meteor/reactive-var';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const items = new ReactiveVar([]);\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const currentItems = items.get();\n"
                    "  console.log('Items count:', currentItems.length);\n"
                    "});\n"
                    "// Logs: 'Items count: 0'\n"
                    "\n"
                    "items.set(['apple', 'banana']);\n"
                    "// Logs: 'Items count: 2'\n"
                    "\n"
                    "items.set(['apple', 'banana']);\n"
                    "// Logs again because arrays are compared by reference (===),\n"
                    "// and these are different array objects"
                ),
                "description": (
                    "Be aware that without a custom equality function, setting "
                    "an array or object will always trigger reactivity, even if "
                    "the contents are identical."
                ),
            },
            {
                "title": "Toggling a boolean ReactiveVar",
                "code": (
                    "const isVisible = new ReactiveVar(false);\n"
                    "\n"
                    "function toggleVisibility() {\n"
                    "  isVisible.set(!isVisible.get());\n"
                    "}\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const visible = isVisible.get();\n"
                    "  document.getElementById('panel').style.display =\n"
                    "    visible ? 'block' : 'none';\n"
                    "});"
                ),
                "description": (
                    "A common pattern is toggling a boolean ReactiveVar to "
                    "control UI visibility."
                ),
            },
        ],
        "tags": [
            "reactive-var",
            "set",
            "reactive",
            "write",
            "state",
            "invalidate",
            "client",
        ],
    },
]
