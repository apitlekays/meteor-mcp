"""Meteor.js Tracker API - reactive computation system (v3.4.0)."""

TRACKER = [
    {
        "name": "Tracker.autorun",
        "module": "tracker",
        "signature": "Tracker.autorun(runFunc, [options])",
        "description": (
            "Run a function now and rerun it later whenever its reactive data sources "
            "change. Returns a Computation object that can be used to stop or observe "
            "the reactive computation.\n\n"
            "The `runFunc` receives the Computation object as its first argument. On "
            "the first call this is the newly created computation; on subsequent reruns "
            "it is the same computation. The function is called immediately "
            "(synchronously) the first time and then again whenever any reactive data "
            "source accessed during the previous run is invalidated.\n\n"
            "If the `options.onError` callback is provided, it will be called with any "
            "errors thrown by `runFunc` instead of propagating them."
        ),
        "params": [
            {
                "name": "runFunc",
                "type": "Function",
                "description": (
                    "The function to run reactively. Receives the Computation object "
                    "as its first argument."
                ),
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": "An options object. Supports onError: a callback invoked when runFunc throws an exception.",
            },
            {
                "name": "options.onError",
                "type": "Function",
                "optional": True,
                "description": (
                    "Callback invoked with the error if `runFunc` throws, instead "
                    "of propagating the error."
                ),
            },
        ],
        "returns": "Tracker.Computation - the Computation object for this autorun.",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Basic autorun with reactive data source",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Session.set('currentPage', 'home');\n"
                    "\n"
                    "Tracker.autorun((computation) => {\n"
                    "  const page = Session.get('currentPage');\n"
                    "  console.log('Current page:', page);\n"
                    "\n"
                    "  if (computation.firstRun) {\n"
                    "    console.log('This is the initial run');\n"
                    "  }\n"
                    "});\n"
                    "\n"
                    "// Changing the session variable triggers a rerun\n"
                    "Session.set('currentPage', 'about');\n"
                    "// Logs: 'Current page: about'"
                ),
                "description": (
                    "The autorun callback runs once immediately and then reruns "
                    "every time Session.get('currentPage') changes."
                ),
            },
            {
                "title": "Stopping an autorun",
                "code": (
                    "const computation = Tracker.autorun(() => {\n"
                    "  const count = Counter.get();\n"
                    "  console.log('Count:', count);\n"
                    "});\n"
                    "\n"
                    "// Later, stop the reactive computation\n"
                    "computation.stop();"
                ),
                "description": (
                    "Store the returned Computation to stop the autorun when it "
                    "is no longer needed, preventing memory leaks."
                ),
            },
            {
                "title": "Autorun with error handling",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const data = Session.get('riskyData');\n"
                    "  if (!data) throw new Error('Data not available');\n"
                    "  processData(data);\n"
                    "}, {\n"
                    "  onError(err) {\n"
                    "    console.error('Autorun error:', err.message);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "The onError callback catches exceptions from the autorun "
                    "function, preventing them from crashing the application."
                ),
            },
        ],
        "tags": [
            "tracker",
            "autorun",
            "reactive",
            "computation",
            "reactivity",
            "dependency",
        ],
    },
    {
        "name": "Tracker.flush",
        "module": "tracker",
        "signature": "Tracker.flush()",
        "description": (
            "Process all pending reactive updates immediately and synchronously. "
            "Normally, reactive updates are batched and processed after the current "
            "code finishes executing. Calling `Tracker.flush()` forces all pending "
            "invalidated computations to rerun right away.\n\n"
            "This is rarely needed in application code but can be useful in tests or "
            "when you need to ensure the DOM is up-to-date before proceeding."
        ),
        "params": [],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Forcing reactive updates in a test",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Session.set('name', 'Alice');\n"
                    "\n"
                    "// Force all reactive computations to rerun now\n"
                    "Tracker.flush();\n"
                    "\n"
                    "// DOM is now updated and can be tested\n"
                    "assert.equal(document.getElementById('name').textContent, 'Alice');"
                ),
                "description": (
                    "In tests, flush ensures all reactive updates are applied "
                    "before making assertions on the DOM or reactive state."
                ),
            },
        ],
        "tags": ["tracker", "flush", "reactive", "synchronous", "update"],
    },
    {
        "name": "Tracker.nonreactive",
        "module": "tracker",
        "signature": "Tracker.nonreactive(func)",
        "description": (
            "Run a function without establishing any reactive dependencies. Any "
            "reactive data sources accessed inside `func` will not cause the "
            "enclosing computation to rerun.\n\n"
            "This is useful when you need to read reactive data for a one-time "
            "operation within an autorun without wanting changes to that data to "
            "trigger a rerun."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": "A function to run non-reactively. Its return value is returned.",
                "optional": False,
            },
        ],
        "returns": "The return value of `func`.",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Reading a reactive source without creating a dependency",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const name = Session.get('name'); // reactive dependency\n"
                    "\n"
                    "  // Read 'debugMode' without making it a dependency\n"
                    "  const debug = Tracker.nonreactive(() => Session.get('debugMode'));\n"
                    "\n"
                    "  if (debug) {\n"
                    "    console.log('Name changed to:', name);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "The autorun reruns when 'name' changes but not when 'debugMode' "
                    "changes, because debugMode is read non-reactively."
                ),
            },
        ],
        "tags": [
            "tracker",
            "nonreactive",
            "reactive",
            "dependency",
            "suppress",
        ],
    },
    {
        "name": "Tracker.active",
        "module": "tracker",
        "signature": "Tracker.active",
        "description": (
            "A boolean property that is `true` if there is a current reactive "
            "computation (i.e., the code is running inside a `Tracker.autorun` "
            "or similar reactive context), and `false` otherwise.\n\n"
            "This is useful for writing library code that behaves differently "
            "depending on whether it is called from a reactive context."
        ),
        "params": [],
        "returns": "Boolean - `true` if inside a reactive computation, `false` otherwise.",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Checking if code is running reactively",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "function getData() {\n"
                    "  if (Tracker.active) {\n"
                    "    console.log('Called from a reactive context');\n"
                    "  } else {\n"
                    "    console.log('Called from a non-reactive context');\n"
                    "  }\n"
                    "}\n"
                    "\n"
                    "getData(); // 'Called from a non-reactive context'\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  getData(); // 'Called from a reactive context'\n"
                    "});"
                ),
                "description": (
                    "Use Tracker.active to detect whether your function is being "
                    "called from within an autorun or other reactive computation."
                ),
            },
        ],
        "tags": ["tracker", "active", "reactive", "computation", "property"],
    },
    {
        "name": "Tracker.inFlush",
        "module": "tracker",
        "signature": "Tracker.inFlush",
        "description": (
            "A boolean property that is true if Tracker is currently in the "
            "middle of a flush cycle (i.e., running computations), and false "
            "otherwise."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Checking if inside a flush cycle",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "if (Tracker.inFlush) {\n"
                    "  console.log('Currently flushing computations');\n"
                    "} else {\n"
                    "  console.log('Not in a flush cycle');\n"
                    "}"
                ),
                "description": (
                    "Use Tracker.inFlush to determine if code is currently "
                    "executing inside a Tracker flush cycle."
                ),
            }
        ],
        "tags": ["tracker", "inFlush", "flush", "property", "state"],
    },
    {
        "name": "Tracker.currentComputation",
        "module": "tracker",
        "signature": "Tracker.currentComputation",
        "description": (
            "The current `Tracker.Computation` object, or `null` if there is no "
            "current computation (i.e., the code is not running inside a reactive "
            "context).\n\n"
            "This is primarily used by reactive data source implementations to "
            "record dependencies. Application code should generally use "
            "`Tracker.autorun` and its computation argument instead."
        ),
        "params": [],
        "returns": "Tracker.Computation | null",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Accessing the current computation",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "console.log(Tracker.currentComputation); // null\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const comp = Tracker.currentComputation;\n"
                    "  console.log('Computation ID:', comp._id);\n"
                    "  console.log('First run:', comp.firstRun);\n"
                    "});"
                ),
                "description": (
                    "Outside an autorun, currentComputation is null. Inside, it "
                    "references the active Computation object."
                ),
            },
        ],
        "tags": [
            "tracker",
            "currentComputation",
            "reactive",
            "computation",
            "property",
        ],
    },
    {
        "name": "Tracker.onInvalidate",
        "module": "tracker",
        "signature": "Tracker.onInvalidate(callback)",
        "description": (
            "Registers a callback function on the current computation that will be "
            "called when the computation is next invalidated. This is a convenience "
            "shorthand for `Tracker.currentComputation.onInvalidate(callback)`.\n\n"
            "Throws an error if there is no current computation (i.e., if called "
            "outside a reactive context)."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Function to call when the current computation is invalidated. "
                    "Receives the Computation object as its argument."
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
                "title": "Cleanup on invalidation",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  const handle = Meteor.subscribe('posts');\n"
                    "\n"
                    "  Tracker.onInvalidate(() => {\n"
                    "    console.log('Computation invalidated, cleaning up');\n"
                    "  });\n"
                    "\n"
                    "  if (handle.ready()) {\n"
                    "    const posts = Posts.find().fetch();\n"
                    "    renderPosts(posts);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "The onInvalidate callback runs just before the autorun "
                    "reruns or when it is stopped, making it useful for cleanup."
                ),
            },
        ],
        "tags": [
            "tracker",
            "onInvalidate",
            "reactive",
            "callback",
            "cleanup",
        ],
    },
    {
        "name": "Tracker.afterFlush",
        "module": "tracker",
        "signature": "Tracker.afterFlush(callback)",
        "description": (
            "Schedules a function to be called after the next flush cycle completes. "
            "A flush cycle is when all pending invalidated computations are rerun. "
            "The callback runs after all reactive computations have finished their "
            "current rerun.\n\n"
            "If called during a flush, the callback will run after the current flush "
            "completes. Multiple `afterFlush` callbacks are executed in the order they "
            "were registered."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": "Function to call after the next Tracker flush cycle.",
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Running code after all reactive updates",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Session.set('count', 1);\n"
                    "\n"
                    "Tracker.afterFlush(() => {\n"
                    "  console.log('All reactive computations have been rerun');\n"
                    "  // Safe to query the DOM or check final state here\n"
                    "  const element = document.querySelector('.count-display');\n"
                    "  console.log('Displayed count:', element.textContent);\n"
                    "});"
                ),
                "description": (
                    "afterFlush is useful when you need to run code that depends "
                    "on the DOM or other side effects being fully updated."
                ),
            },
        ],
        "tags": [
            "tracker",
            "afterFlush",
            "reactive",
            "flush",
            "callback",
            "lifecycle",
        ],
    },
    {
        "name": "Computation.stop",
        "module": "tracker",
        "signature": "computation.stop()",
        "description": (
            "Prevents this computation from rerunning. A stopped computation will "
            "never be invalidated or rerun again. Any `onStop` callbacks registered "
            "on the computation will be called.\n\n"
            "Calling `stop()` on an already stopped computation has no effect. "
            "Always stop computations when they are no longer needed to avoid memory "
            "leaks and unnecessary recomputations."
        ),
        "params": [],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Stopping a computation from inside the autorun",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Tracker.autorun((computation) => {\n"
                    "  const status = Session.get('status');\n"
                    "\n"
                    "  if (status === 'complete') {\n"
                    "    console.log('Task complete, stopping autorun');\n"
                    "    computation.stop();\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  console.log('Status:', status);\n"
                    "});"
                ),
                "description": (
                    "A computation can stop itself by calling stop() on the "
                    "computation argument passed to the autorun function."
                ),
            },
            {
                "title": "Stopping from outside the autorun",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "const comp = Tracker.autorun(() => {\n"
                    "  console.log('Value:', Session.get('value'));\n"
                    "});\n"
                    "\n"
                    "// Stop after 5 seconds\n"
                    "setTimeout(() => {\n"
                    "  comp.stop();\n"
                    "  console.log('Computation stopped');\n"
                    "}, 5000);"
                ),
                "description": (
                    "The Computation returned by Tracker.autorun can be stopped "
                    "externally at any time."
                ),
            },
        ],
        "tags": ["tracker", "computation", "stop", "cleanup", "lifecycle"],
    },
    {
        "name": "Computation.invalidate",
        "module": "tracker",
        "signature": "computation.invalidate()",
        "description": (
            "Invalidates this computation so that it will be rerun during the next "
            "flush cycle. If the computation is currently running, it will be rerun "
            "after the current execution completes.\n\n"
            "Any `onInvalidate` callbacks registered on the computation will be "
            "called. Calling `invalidate()` on an already invalidated computation "
            "has no additional effect."
        ),
        "params": [],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Manually invalidating a computation",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const comp = Tracker.autorun(() => {\n"
                    "  console.log('Running computation at', new Date().toISOString());\n"
                    "});\n"
                    "\n"
                    "// Force the computation to rerun\n"
                    "comp.invalidate();\n"
                    "Tracker.flush();"
                ),
                "description": (
                    "Manually invalidating a computation schedules it for rerun. "
                    "Call Tracker.flush() to force the rerun immediately."
                ),
            },
        ],
        "tags": [
            "tracker",
            "computation",
            "invalidate",
            "reactive",
            "rerun",
        ],
    },
    {
        "name": "Computation.onInvalidate",
        "module": "tracker",
        "signature": "computation.onInvalidate(callback)",
        "description": (
            "Registers a callback that will be called when this computation is "
            "invalidated. The callback receives the Computation object as its "
            "argument.\n\n"
            "If the computation is already invalidated at the time of registration, "
            "the callback is called immediately. Multiple callbacks can be registered "
            "and they will be called in the order they were added."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Function to call on invalidation. Receives the Computation "
                    "as its argument."
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
                "title": "Registering an invalidation callback",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Tracker.autorun((computation) => {\n"
                    "  computation.onInvalidate((comp) => {\n"
                    "    console.log('Computation', comp._id, 'was invalidated');\n"
                    "    if (comp.stopped) {\n"
                    "      console.log('It was stopped, performing final cleanup');\n"
                    "    }\n"
                    "  });\n"
                    "\n"
                    "  const data = Session.get('myData');\n"
                    "  renderData(data);\n"
                    "});"
                ),
                "description": (
                    "The onInvalidate callback fires each time the computation is "
                    "invalidated. Check computation.stopped to distinguish between "
                    "a rerun and a full stop."
                ),
            },
        ],
        "tags": [
            "tracker",
            "computation",
            "onInvalidate",
            "callback",
            "lifecycle",
        ],
    },
    {
        "name": "Computation.onStop",
        "module": "tracker",
        "signature": "computation.onStop(callback)",
        "description": (
            "Registers a callback that will be called when this computation is "
            "stopped. The callback receives the Computation object as its argument.\n\n"
            "If the computation is already stopped at the time of registration, "
            "the callback is called immediately. This is the ideal place for cleanup "
            "logic such as removing event listeners or cancelling timers."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Function to call when the computation is stopped. Receives "
                    "the Computation as its argument."
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
                "title": "Cleanup with onStop",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "Tracker.autorun((computation) => {\n"
                    "  if (computation.firstRun) {\n"
                    "    const interval = setInterval(() => {\n"
                    "      console.log('polling...');\n"
                    "    }, 1000);\n"
                    "    computation.onStop(() => {\n"
                    "      clearInterval(interval);\n"
                    "      console.log('Polling stopped, interval cleared');\n"
                    "    });\n"
                    "  }\n"
                    "  const data = Session.get('liveData');\n"
                    "  displayData(data);\n"
                    "});"
                ),
                "description": (
                    "Use onStop for resource cleanup. Unlike onInvalidate, onStop "
                    "only runs once when the computation is permanently stopped."
                ),
            },
        ],
        "tags": [
            "tracker",
            "computation",
            "onStop",
            "callback",
            "cleanup",
            "lifecycle",
        ],
    },
    {
        "name": "Computation.stopped",
        "module": "tracker",
        "signature": "computation.stopped",
        "description": (
            "A boolean property that is `true` if this computation has been stopped "
            "(by calling `computation.stop()`), and `false` otherwise. A stopped "
            "computation will never be rerun."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Checking if a computation is stopped",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "const comp = Tracker.autorun(() => {\n"
                    "  console.log('Value:', Session.get('value'));\n"
                    "});\n"
                    "\n"
                    "console.log(comp.stopped); // false\n"
                    "comp.stop();\n"
                    "console.log(comp.stopped); // true"
                ),
                "description": (
                    "The stopped property allows you to check whether a computation "
                    "has been permanently halted."
                ),
            },
        ],
        "tags": ["tracker", "computation", "stopped", "property", "state"],
    },
    {
        "name": "Computation.invalidated",
        "module": "tracker",
        "signature": "computation.invalidated",
        "description": (
            "A boolean property that is `true` if this computation has been "
            "invalidated (either by a dependency change or by a manual call to "
            "`computation.invalidate()`), but has not yet rerun. After the "
            "computation reruns, this property is reset to `false`."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Checking invalidation state",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { Session } from 'meteor/session';\n"
                    "\n"
                    "const comp = Tracker.autorun(() => {\n"
                    "  console.log('Data:', Session.get('data'));\n"
                    "});\n"
                    "\n"
                    "console.log(comp.invalidated); // false\n"
                    "\n"
                    "Session.set('data', 'new value');\n"
                    "console.log(comp.invalidated); // true (pending rerun)\n"
                    "\n"
                    "Tracker.flush();\n"
                    "console.log(comp.invalidated); // false (has rerun)"
                ),
                "description": (
                    "The invalidated property is true between when a computation "
                    "is invalidated and when it reruns."
                ),
            },
        ],
        "tags": ["tracker", "computation", "invalidated", "property", "state"],
    },
    {
        "name": "Computation.firstRun",
        "module": "tracker",
        "signature": "computation.firstRun",
        "description": (
            "A boolean property that is `true` during the first execution of the "
            "computation (when it is created by `Tracker.autorun`), and `false` "
            "on all subsequent reruns. This is useful for one-time initialization "
            "logic inside an autorun."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Skipping initialization logic on reruns",
                "code": (
                    "Tracker.autorun((computation) => {\n"
                    "  const user = Meteor.user();\n"
                    "\n"
                    "  if (computation.firstRun) {\n"
                    "    console.log('Initial load, setting up UI');\n"
                    "    initializeUI();\n"
                    "  }\n"
                    "\n"
                    "  if (user) {\n"
                    "    updateUserDisplay(user);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Use firstRun to perform one-time setup that should not repeat "
                    "when the computation reruns due to dependency changes."
                ),
            },
        ],
        "tags": [
            "tracker",
            "computation",
            "firstRun",
            "property",
            "initialization",
        ],
    },
    {
        "name": "Tracker.Dependency",
        "module": "tracker",
        "signature": "new Tracker.Dependency()",
        "description": (
            "Creates a new reactive dependency object. A Dependency tracks a set "
            "of computations that depend on it. When the dependency changes, all "
            "dependent computations are invalidated.\n\n"
            "This is the low-level primitive used to implement reactive data sources. "
            "Call `dependency.depend()` inside a computation to register the "
            "dependency, and `dependency.changed()` when the underlying data changes."
        ),
        "params": [],
        "returns": "Tracker.Dependency - a new Dependency instance.",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Creating a custom reactive data source",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const dep = new Tracker.Dependency();\n"
                    "let _currentTheme = 'light';\n"
                    "\n"
                    "const ThemeStore = {\n"
                    "  get() {\n"
                    "    dep.depend();\n"
                    "    return _currentTheme;\n"
                    "  },\n"
                    "  set(theme) {\n"
                    "    if (theme !== _currentTheme) {\n"
                    "      _currentTheme = theme;\n"
                    "      dep.changed();\n"
                    "    }\n"
                    "  }\n"
                    "};\n"
                    "\n"
                    "// Usage in an autorun\n"
                    "Tracker.autorun(() => {\n"
                    "  console.log('Current theme:', ThemeStore.get());\n"
                    "});\n"
                    "\n"
                    "ThemeStore.set('dark'); // triggers the autorun"
                ),
                "description": (
                    "Tracker.Dependency is the building block for creating custom "
                    "reactive data sources that integrate with Tracker's autorun."
                ),
            },
        ],
        "tags": [
            "tracker",
            "dependency",
            "reactive",
            "custom",
            "data source",
        ],
    },
    {
        "name": "Dependency.depend",
        "module": "tracker",
        "signature": "dependency.depend([computation])",
        "description": (
            "Declares that the current computation (or the provided computation) "
            "depends on this dependency. When `dependency.changed()` is later "
            "called, the computation will be invalidated.\n\n"
            "If there is no current computation and no computation argument is "
            "provided, this method does nothing and returns `false`. Returns "
            "`true` if the dependency was successfully registered."
        ),
        "params": [
            {
                "name": "computation",
                "type": "Tracker.Computation",
                "optional": True,
                "description": (
                    "The computation to register as dependent. Defaults to "
                    "Tracker.currentComputation."
                ),
            },
        ],
        "returns": "Boolean - `true` if a dependency was registered, `false` if there was no computation.",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Using depend() in a reactive getter",
                "code": (
                    "const dep = new Tracker.Dependency();\n"
                    "let _value = 0;\n"
                    "\n"
                    "function getValue() {\n"
                    "  dep.depend(); // register current computation\n"
                    "  return _value;\n"
                    "}\n"
                    "\n"
                    "function setValue(newVal) {\n"
                    "  if (newVal !== _value) {\n"
                    "    _value = newVal;\n"
                    "    dep.changed(); // invalidate all dependents\n"
                    "  }\n"
                    "}"
                ),
                "description": (
                    "Call depend() in your getter to record the reactive dependency, "
                    "and changed() in your setter to trigger reruns."
                ),
            },
        ],
        "tags": [
            "tracker",
            "dependency",
            "depend",
            "reactive",
            "register",
        ],
    },
    {
        "name": "Dependency.changed",
        "module": "tracker",
        "signature": "dependency.changed()",
        "description": (
            "Invalidates all computations that currently depend on this dependency, "
            "causing them to rerun during the next flush cycle. This is how reactive "
            "data sources signal that their value has changed."
        ),
        "params": [],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Signalling a change to dependents",
                "code": (
                    "const dep = new Tracker.Dependency();\n"
                    "let _color = 'red';\n"
                    "\n"
                    "function setColor(newColor) {\n"
                    "  _color = newColor;\n"
                    "  dep.changed(); // all computations using getColor() will rerun\n"
                    "}\n"
                    "\n"
                    "function getColor() {\n"
                    "  dep.depend();\n"
                    "  return _color;\n"
                    "}\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  console.log('Color is:', getColor());\n"
                    "});\n"
                    "\n"
                    "setColor('blue'); // logs: 'Color is: blue'"
                ),
                "description": (
                    "Calling changed() invalidates all registered dependents, "
                    "scheduling them for rerun on the next flush."
                ),
            },
        ],
        "tags": [
            "tracker",
            "dependency",
            "changed",
            "invalidate",
            "reactive",
        ],
    },
    {
        "name": "Dependency.hasDependents",
        "module": "tracker",
        "signature": "dependency.hasDependents()",
        "description": (
            "Returns `true` if any computations currently depend on this dependency, "
            "and `false` otherwise. This can be used to optimize reactive data "
            "sources by avoiding expensive work when no one is listening."
        ),
        "params": [],
        "returns": "Boolean - `true` if this dependency has any dependent computations.",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Conditional work based on dependents",
                "code": (
                    "const dep = new Tracker.Dependency();\n"
                    "\n"
                    "function expensiveUpdate() {\n"
                    "  if (!dep.hasDependents()) {\n"
                    "    // No one is listening, skip the expensive work\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  // Perform expensive computation\n"
                    "  recomputeData();\n"
                    "  dep.changed();\n"
                    "}"
                ),
                "description": (
                    "Use hasDependents() to avoid unnecessary computation when "
                    "no reactive consumers are currently registered."
                ),
            },
        ],
        "tags": [
            "tracker",
            "dependency",
            "hasDependents",
            "optimization",
            "reactive",
        ],
    },
    {
        "name": "Tracker.withComputation",
        "module": "tracker",
        "signature": "Tracker.withComputation(computation, func)",
        "description": (
            "Runs a function with a specific computation set as the current computation "
            "(`Tracker.currentComputation`). While `func` is executing, "
            "`Tracker.currentComputation` will be set to the provided `computation` and "
            "`Tracker.active` will be `true`.\n\n"
            "This is useful for advanced reactive patterns where you need to establish a "
            "specific reactive context programmatically, such as when bridging between "
            "different reactive systems or re-entering a computation context from an "
            "asynchronous callback."
        ),
        "params": [
            {
                "name": "computation",
                "type": "Tracker.Computation",
                "description": (
                    "The computation to set as the current computation while "
                    "`func` executes."
                ),
                "optional": False,
            },
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "The function to run with the given computation as the "
                    "current computation. Its return value is returned."
                ),
                "optional": False,
            },
        ],
        "returns": "The return value of `func`.",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Running a function within a specific computation context",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const comp = Tracker.autorun(() => {\n"
                    "  console.log('Autorun running');\n"
                    "});\n"
                    "\n"
                    "// Later, run code as if inside that computation\n"
                    "Tracker.withComputation(comp, () => {\n"
                    "  console.log('Active:', Tracker.active); // true\n"
                    "  console.log('Current:', Tracker.currentComputation === comp); // true\n"
                    "});"
                ),
                "description": (
                    "Tracker.withComputation temporarily sets the given computation "
                    "as the current one, allowing reactive dependencies to be "
                    "registered against it."
                ),
            },
        ],
        "tags": [
            "tracker",
            "withComputation",
            "reactive",
            "computation",
            "context",
        ],
    },
    {
        "name": "Computation.firstRunPromise",
        "module": "tracker",
        "signature": "computation.firstRunPromise",
        "description": (
            "A `Promise` that resolves after the first run of the computation completes. "
            "This is useful when you need to wait for the initial execution of a "
            "`Tracker.autorun` to finish before proceeding, particularly in async code.\n\n"
            "The promise resolves with `undefined` once the computation's first "
            "execution is done. If the computation's first run has already completed, "
            "the promise is already resolved."
        ),
        "params": [],
        "returns": "Promise - resolves after the first run of the computation completes.",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Waiting for the first autorun execution",
                "code": (
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "const comp = Tracker.autorun(() => {\n"
                    "  const data = SomeReactiveSource.get();\n"
                    "  console.log('Data loaded:', data);\n"
                    "});\n"
                    "\n"
                    "// Wait for the first run to complete\n"
                    "await comp.firstRunPromise;\n"
                    "console.log('First run finished, safe to proceed');"
                ),
                "description": (
                    "The firstRunPromise property allows async code to wait until "
                    "the computation has completed its initial execution."
                ),
            },
        ],
        "tags": [
            "tracker",
            "computation",
            "firstRunPromise",
            "promise",
            "async",
            "property",
        ],
    },
]
