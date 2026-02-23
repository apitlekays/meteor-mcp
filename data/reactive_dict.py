"""Meteor.js ReactiveDict API - reactive dictionary for key-value state (v3.4.0)."""

REACTIVE_DICT = [
    {
        "name": "new ReactiveDict",
        "module": "reactive_dict",
        "signature": "new ReactiveDict([name], [initialValue])",
        "description": (
            "Constructs a new ReactiveDict, a reactive key-value store. "
            "ReactiveDict is provided by the `reactive-dict` package and is the "
            "underlying implementation used by Session.\n\n"
            "If a `name` is provided and the `reload` package is loaded, the "
            "ReactiveDict will survive hot code pushes and its state will be "
            "restored after a reload. The name must be unique across all "
            "ReactiveDict instances.\n\n"
            "The optional `initialValue` is a plain object whose keys and values "
            "will be used to populate the dict on construction."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "optional": True,
                "description": (
                    "Optional name for persistence across hot code pushes. "
                    "Must be unique across all ReactiveDict instances."
                ),
            },
            {
                "name": "initialValue",
                "type": "Object",
                "optional": True,
                "description": (
                    "An object of initial key-value pairs to populate the dict."
                ),
            },
        ],
        "returns": "ReactiveDict - a new ReactiveDict instance.",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Creating a ReactiveDict with initial values",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "\n"
                    "// Simple unnamed dict\n"
                    "const state = new ReactiveDict();\n"
                    "\n"
                    "// Named dict that survives hot code pushes\n"
                    "const persistentState = new ReactiveDict('appState');\n"
                    "\n"
                    "// Dict with initial values\n"
                    "const filters = new ReactiveDict('filters', {\n"
                    "  category: 'all',\n"
                    "  sortBy: 'date',\n"
                    "  ascending: true\n"
                    "});"
                ),
                "description": (
                    "ReactiveDict can be created with no arguments, a name for "
                    "persistence, initial values, or both."
                ),
            },
            {
                "title": "Using ReactiveDict in a Blaze template",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "import { Template } from 'meteor/templating';\n"
                    "\n"
                    "Template.dashboard.onCreated(function () {\n"
                    "  this.state = new ReactiveDict();\n"
                    "  this.state.set('activePanel', 'overview');\n"
                    "  this.state.set('isLoading', false);\n"
                    "});\n"
                    "\n"
                    "Template.dashboard.helpers({\n"
                    "  activePanel() {\n"
                    "    return Template.instance().state.get('activePanel');\n"
                    "  },\n"
                    "  isLoading() {\n"
                    "    return Template.instance().state.get('isLoading');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "A common pattern in Blaze is to attach a ReactiveDict to a "
                    "template instance for component-scoped reactive state."
                ),
            },
        ],
        "tags": [
            "reactive-dict",
            "constructor",
            "reactive",
            "dictionary",
            "state",
            "client",
        ],
    },
    {
        "name": "ReactiveDict.set",
        "module": "reactive_dict",
        "signature": "reactiveDict.set(key, value)",
        "description": (
            "Set a key-value pair in the ReactiveDict. If the new value is "
            "different from the current value for that key (using EJSON equality), "
            "all computations that called `get` or `equals` with the same key "
            "will be invalidated.\n\n"
            "Can also be called with an object argument to set multiple keys at "
            "once: `reactiveDict.set({ key1: value1, key2: value2 })`."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The key to set.",
                "optional": False,
            },
            {
                "name": "value",
                "type": "EJSON-compatible value",
                "description": "The value to associate with the key.",
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Setting individual and multiple keys",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "\n"
                    "const state = new ReactiveDict();\n"
                    "\n"
                    "// Set a single key\n"
                    "state.set('page', 'home');\n"
                    "state.set('count', 42);\n"
                    "\n"
                    "// Set multiple keys at once\n"
                    "state.set({\n"
                    "  page: 'about',\n"
                    "  count: 0,\n"
                    "  loading: true\n"
                    "});"
                ),
                "description": (
                    "When called with an object argument, set updates all "
                    "specified keys in a single call."
                ),
            },
        ],
        "tags": ["reactive-dict", "set", "reactive", "write", "state", "client"],
    },
    {
        "name": "ReactiveDict.setDefault",
        "module": "reactive_dict",
        "signature": "reactiveDict.setDefault(key, value)",
        "description": (
            "Set a key-value pair in the ReactiveDict only if the key has not "
            "already been set. This is useful for initializing default values "
            "without overwriting existing state.\n\n"
            "Can also be called with an object argument to set defaults for "
            "multiple keys at once."
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
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Setting defaults for a reactive dict",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "\n"
                    "const settings = new ReactiveDict();\n"
                    "\n"
                    "// Set defaults - only takes effect if not already set\n"
                    "settings.setDefault('volume', 80);\n"
                    "settings.setDefault('muted', false);\n"
                    "\n"
                    "// Set multiple defaults at once\n"
                    "settings.setDefault({\n"
                    "  volume: 80,\n"
                    "  muted: false,\n"
                    "  quality: 'high'\n"
                    "});\n"
                    "\n"
                    "// Existing keys are not overwritten\n"
                    "settings.set('volume', 50);\n"
                    "settings.setDefault('volume', 80);\n"
                    "console.log(settings.get('volume')); // 50"
                ),
                "description": (
                    "setDefault is safe to call repeatedly. It only stores the "
                    "value if the key has never been set before."
                ),
            },
        ],
        "tags": [
            "reactive-dict",
            "setDefault",
            "initialize",
            "default",
            "client",
        ],
    },
    {
        "name": "ReactiveDict.get",
        "module": "reactive_dict",
        "signature": "reactiveDict.get(key)",
        "description": (
            "Get the value for a key from the ReactiveDict. If called inside a "
            "reactive computation, the computation is registered as a dependent "
            "and will be invalidated when the value for that key changes.\n\n"
            "Returns `undefined` if the key has never been set."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The key to look up.",
                "optional": False,
            },
        ],
        "returns": "The value associated with the key, or `undefined` if not set.",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Reading values reactively from a ReactiveDict",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const state = new ReactiveDict();\n"
                    "state.set('language', 'en');\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const lang = state.get('language');\n"
                    "  console.log('Current language:', lang);\n"
                    "  loadTranslations(lang);\n"
                    "});\n"
                    "\n"
                    "state.set('language', 'fr');\n"
                    "// Autorun reruns, logs: 'Current language: fr'"
                ),
                "description": (
                    "get() establishes a reactive dependency on the specific key, "
                    "causing the computation to rerun when that key's value changes."
                ),
            },
        ],
        "tags": ["reactive-dict", "get", "reactive", "read", "state", "client"],
    },
    {
        "name": "ReactiveDict.equals",
        "module": "reactive_dict",
        "signature": "reactiveDict.equals(key, value)",
        "description": (
            "Test if the value for a key equals the given value. Like "
            "`Session.equals`, this creates a more efficient reactive dependency "
            "that only invalidates when the equality result changes (true to false "
            "or vice versa), rather than on every change to the key.\n\n"
            "The value must be a scalar type (string, number, boolean, null, or "
            "undefined). Object and array comparisons are not supported and will "
            "always return false."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The key to test.",
                "optional": False,
            },
            {
                "name": "value",
                "type": "String | Number | Boolean | null | undefined",
                "description": "The scalar value to compare against.",
                "optional": False,
            },
        ],
        "returns": "Boolean - `true` if the stored value equals the given value.",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Efficient equality checking in a reactive context",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const state = new ReactiveDict();\n"
                    "state.set('view', 'list');\n"
                    "\n"
                    "// Only reruns when the boolean result changes\n"
                    "Tracker.autorun(() => {\n"
                    "  if (state.equals('view', 'grid')) {\n"
                    "    showGridView();\n"
                    "  } else {\n"
                    "    showListView();\n"
                    "  }\n"
                    "});\n"
                    "\n"
                    "state.set('view', 'table');\n"
                    "// Does NOT rerun because equals('view', 'grid') is still false\n"
                    "\n"
                    "state.set('view', 'grid');\n"
                    "// Reruns because equals('view', 'grid') changed to true"
                ),
                "description": (
                    "equals() provides finer-grained reactivity than get() "
                    "when you only care about whether a specific value matches."
                ),
            },
        ],
        "tags": [
            "reactive-dict",
            "equals",
            "reactive",
            "comparison",
            "efficient",
            "client",
        ],
    },
    {
        "name": "ReactiveDict.all",
        "module": "reactive_dict",
        "signature": "reactiveDict.all()",
        "description": (
            "Returns a plain object containing all key-value pairs in the "
            "ReactiveDict. If called inside a reactive computation, the "
            "computation depends on all keys and will be invalidated when any "
            "key changes.\n\n"
            "This is useful for serializing or inspecting the entire state, but "
            "creates a broad dependency. Prefer `get()` for individual keys when "
            "fine-grained reactivity is needed."
        ),
        "params": [],
        "returns": "Object - a plain object with all key-value pairs.",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Getting all values from a ReactiveDict",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const formState = new ReactiveDict('form', {\n"
                    "  name: '',\n"
                    "  email: '',\n"
                    "  agreed: false\n"
                    "});\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const allValues = formState.all();\n"
                    "  console.log('Form state:', allValues);\n"
                    "  // { name: '', email: '', agreed: false }\n"
                    "});\n"
                    "\n"
                    "formState.set('name', 'Alice');\n"
                    "// Autorun reruns because all() depends on every key"
                ),
                "description": (
                    "all() returns a snapshot of the entire dict. The reactive "
                    "dependency covers all keys, so any change triggers a rerun."
                ),
            },
            {
                "title": "Serializing state for debugging",
                "code": (
                    "const state = new ReactiveDict();\n"
                    "state.set('page', 'dashboard');\n"
                    "state.set('userId', 'abc123');\n"
                    "\n"
                    "// Non-reactive read for debugging\n"
                    "Tracker.nonreactive(() => {\n"
                    "  console.log(JSON.stringify(state.all(), null, 2));\n"
                    "});"
                ),
                "description": (
                    "Wrap all() in Tracker.nonreactive() to read the entire "
                    "state without creating reactive dependencies."
                ),
            },
        ],
        "tags": ["reactive-dict", "all", "reactive", "read", "serialize", "client"],
    },
    {
        "name": "ReactiveDict.clear",
        "module": "reactive_dict",
        "signature": "reactiveDict.clear()",
        "description": (
            "Remove all key-value pairs from the ReactiveDict. All computations "
            "that depend on any key in the dict will be invalidated."
        ),
        "params": [],
        "returns": "undefined",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Clearing a ReactiveDict",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "\n"
                    "const state = new ReactiveDict();\n"
                    "state.set('name', 'Alice');\n"
                    "state.set('role', 'admin');\n"
                    "\n"
                    "console.log(state.all()); // { name: 'Alice', role: 'admin' }\n"
                    "\n"
                    "state.clear();\n"
                    "console.log(state.all()); // {}\n"
                    "console.log(state.get('name')); // undefined"
                ),
                "description": (
                    "clear() removes all entries and invalidates any computations "
                    "that were reading from the dict."
                ),
            },
            {
                "title": "Resetting form state",
                "code": (
                    "const formState = new ReactiveDict();\n"
                    "\n"
                    "function resetForm() {\n"
                    "  formState.clear();\n"
                    "  formState.set({\n"
                    "    name: '',\n"
                    "    email: '',\n"
                    "    message: ''\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "A common pattern is to clear and re-initialize a ReactiveDict "
                    "to reset form state."
                ),
            },
        ],
        "tags": [
            "reactive-dict",
            "clear",
            "reset",
            "remove",
            "state",
            "client",
        ],
    },
    {
        "name": "ReactiveDict.delete",
        "module": "reactive_dict",
        "signature": "reactiveDict.delete(key)",
        "description": (
            "Remove a single key-value pair from the ReactiveDict. Any "
            "reactive computations that depend on this key will be "
            "invalidated. After deletion, calling get(key) will return "
            "undefined."
        ),
        "params": [
            {
                "name": "key",
                "type": "String",
                "description": "The key to remove from the dict.",
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Delete a single key from a ReactiveDict",
                "code": (
                    "const state = new ReactiveDict();\n"
                    "state.set('theme', 'dark');\n"
                    "state.set('lang', 'en');\n\n"
                    "state.delete('theme');\n"
                    "console.log(state.get('theme')); // undefined\n"
                    "console.log(state.get('lang'));   // 'en'"
                ),
                "description": (
                    "Removes only the 'theme' key, leaving other keys intact."
                ),
            },
        ],
        "tags": ["reactive-dict", "reactivity", "state", "delete"],
    },
    {
        "name": "ReactiveDict.destroy",
        "module": "reactive_dict",
        "signature": "reactiveDict.destroy()",
        "description": (
            "Destroy the ReactiveDict, removing its name from the global registry "
            "of named ReactiveDict instances. After calling destroy, the dict's "
            "name can be reused by a new ReactiveDict.\n\n"
            "This is primarily relevant for named ReactiveDict instances that "
            "persist across hot code pushes. Calling destroy on an unnamed dict "
            "has no additional effect beyond clearing it."
        ),
        "params": [],
        "returns": "undefined",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Destroying a named ReactiveDict",
                "code": (
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "\n"
                    "const state = new ReactiveDict('myComponentState');\n"
                    "state.set('initialized', true);\n"
                    "\n"
                    "// When the component is removed or no longer needed\n"
                    "state.destroy();\n"
                    "\n"
                    "// The name 'myComponentState' can now be reused\n"
                    "const newState = new ReactiveDict('myComponentState');"
                ),
                "description": (
                    "Call destroy when a named ReactiveDict is no longer needed "
                    "to free the name for future use and clean up persistence."
                ),
            },
            {
                "title": "Cleanup in a Blaze template",
                "code": (
                    "Template.myComponent.onCreated(function () {\n"
                    "  this.state = new ReactiveDict('myComponent');\n"
                    "  this.state.set('view', 'default');\n"
                    "});\n"
                    "\n"
                    "Template.myComponent.onDestroyed(function () {\n"
                    "  this.state.destroy();\n"
                    "});"
                ),
                "description": (
                    "In Blaze templates, destroy the ReactiveDict in the "
                    "onDestroyed callback to prevent name collisions."
                ),
            },
        ],
        "tags": [
            "reactive-dict",
            "destroy",
            "cleanup",
            "lifecycle",
            "named",
            "client",
        ],
    },
]
