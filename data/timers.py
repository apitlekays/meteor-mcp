"""Meteor timer API entries for Meteor.js v3.4.0."""

TIMERS = [
    {
        "name": "Meteor.setTimeout",
        "module": "timers",
        "signature": "Meteor.setTimeout(func, delay)",
        "description": (
            "Call a function after a delay, similar to the native "
            "JavaScript setTimeout. The key difference is that "
            "Meteor.setTimeout binds the current Meteor environment "
            "so that the callback retains access to the current user, "
            "connection, and other environment variables that were "
            "active when setTimeout was called. This is important on "
            "the server where Meteor methods and publications run "
            "inside an environment context. Without using "
            "Meteor.setTimeout, a plain setTimeout callback would "
            "lose that context and any calls to Meteor.userId() or "
            "other context-dependent functions would fail. The "
            "function returns a handle that can be passed to "
            "Meteor.clearTimeout to cancel the pending callback."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "The function to call after the delay. Runs within "
                    "the Meteor environment that was active when "
                    "Meteor.setTimeout was called."
                ),
                "optional": False,
            },
            {
                "name": "delay",
                "type": "Number",
                "description": (
                    "The number of milliseconds to wait before calling "
                    "the function."
                ),
                "optional": False,
            },
        ],
        "returns": "Handle",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Delayed cleanup inside a Meteor method",
                "code": (
                    "Meteor.methods({\n"
                    "  async createTemporaryToken() {\n"
                    "    const userId = Meteor.userId();\n"
                    "    const token = Random.secret();\n"
                    "\n"
                    "    await Tokens.insertAsync({\n"
                    "      userId,\n"
                    "      token,\n"
                    "      createdAt: new Date(),\n"
                    "    });\n"
                    "\n"
                    "    // Remove the token after 5 minutes\n"
                    "    Meteor.setTimeout(async () => {\n"
                    "      await Tokens.removeAsync({ token });\n"
                    "      console.log(`Expired token removed for user ${userId}`);\n"
                    "    }, 5 * 60 * 1000);\n"
                    "\n"
                    "    return token;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Meteor.setTimeout preserves the Meteor environment, "
                    "so the callback can safely perform collection "
                    "operations even after the method has returned."
                ),
            },
            {
                "title": "Client-side delayed UI notification",
                "code": (
                    "Template.notifications.events({\n"
                    "  'click .dismiss-btn'(event, instance) {\n"
                    "    instance.showBanner.set(false);\n"
                    "\n"
                    "    // Re-show the banner after 30 seconds\n"
                    "    Meteor.setTimeout(() => {\n"
                    "      instance.showBanner.set(true);\n"
                    "    }, 30000);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "On the client, Meteor.setTimeout works like native "
                    "setTimeout but ensures the reactive context is "
                    "properly maintained."
                ),
            },
        ],
        "tags": ["timers", "scheduling", "async", "environment"],
    },
    {
        "name": "Meteor.setInterval",
        "module": "timers",
        "signature": "Meteor.setInterval(func, delay)",
        "description": (
            "Call a function repeatedly at a specified interval, similar "
            "to the native JavaScript setInterval. Like "
            "Meteor.setTimeout, this function binds the current Meteor "
            "environment so that each invocation of the callback "
            "retains access to the environment variables, user context, "
            "and connection that were active when setInterval was "
            "called. This is especially useful on the server for "
            "periodic tasks such as polling an external API, cleaning "
            "up stale data, or sending batch notifications. The "
            "function returns a handle that can be passed to "
            "Meteor.clearInterval to stop the repeated calls."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "The function to call repeatedly. Runs within the "
                    "Meteor environment that was active when "
                    "Meteor.setInterval was called."
                ),
                "optional": False,
            },
            {
                "name": "delay",
                "type": "Number",
                "description": (
                    "The number of milliseconds between each call to "
                    "the function."
                ),
                "optional": False,
            },
        ],
        "returns": "Handle",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Periodic server-side cleanup task",
                "code": (
                    "Meteor.startup(() => {\n"
                    "  // Clean up expired sessions every 10 minutes\n"
                    "  Meteor.setInterval(async () => {\n"
                    "    const cutoff = new Date(\n"
                    "      Date.now() - 24 * 60 * 60 * 1000\n"
                    "    );\n"
                    "    const result = await Sessions.removeAsync({\n"
                    "      lastActive: { $lt: cutoff },\n"
                    "    });\n"
                    "    if (result > 0) {\n"
                    "      console.log(\n"
                    "        `Cleaned up ${result} expired sessions`\n"
                    "      );\n"
                    "    }\n"
                    "  }, 10 * 60 * 1000);\n"
                    "});"
                ),
                "description": (
                    "Use Meteor.setInterval inside Meteor.startup to "
                    "schedule recurring server tasks. The Meteor "
                    "environment is bound so async collection operations "
                    "work correctly inside the callback."
                ),
            },
            {
                "title": "Client-side polling for updates",
                "code": (
                    "Template.dashboard.onCreated(function () {\n"
                    "  this.stats = new ReactiveVar({});\n"
                    "  this.pollingHandle = Meteor.setInterval(async () => {\n"
                    "    try {\n"
                    "      const stats = await Meteor.callAsync('getLatestStats');\n"
                    "      this.stats.set(stats);\n"
                    "    } catch (err) {\n"
                    "      console.error('Failed to fetch stats:', err);\n"
                    "    }\n"
                    "  }, 15000);\n"
                    "});\n"
                    "\n"
                    "Template.dashboard.onDestroyed(function () {\n"
                    "  Meteor.clearInterval(this.pollingHandle);\n"
                    "});"
                ),
                "description": (
                    "Poll the server for updated data every 15 seconds. "
                    "The interval handle is stored on the template "
                    "instance and cleared when the template is destroyed "
                    "to prevent memory leaks."
                ),
            },
        ],
        "tags": ["timers", "scheduling", "polling", "environment"],
    },
    {
        "name": "Meteor.clearTimeout",
        "module": "timers",
        "signature": "Meteor.clearTimeout(id)",
        "description": (
            "Cancel a timeout previously scheduled by "
            "Meteor.setTimeout. If the callback has already been "
            "called, calling Meteor.clearTimeout has no effect. This "
            "works identically to the native clearTimeout but should "
            "be used with handles returned by Meteor.setTimeout "
            "specifically. Passing a handle from native setTimeout to "
            "Meteor.clearTimeout or vice versa may not work correctly "
            "in all environments."
        ),
        "params": [
            {
                "name": "id",
                "type": "Handle",
                "description": (
                    "The handle returned by Meteor.setTimeout, "
                    "identifying the timeout to cancel."
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
                "title": "Cancelling a pending timeout",
                "code": (
                    "let autoSaveHandle = null;\n"
                    "\n"
                    "function scheduleAutoSave(document) {\n"
                    "  // Cancel any previously scheduled save\n"
                    "  if (autoSaveHandle) {\n"
                    "    Meteor.clearTimeout(autoSaveHandle);\n"
                    "  }\n"
                    "\n"
                    "  // Schedule a new save in 3 seconds\n"
                    "  autoSaveHandle = Meteor.setTimeout(async () => {\n"
                    "    await Documents.updateAsync(\n"
                    "      document._id,\n"
                    "      { $set: { content: document.content } }\n"
                    "    );\n"
                    "    autoSaveHandle = null;\n"
                    "  }, 3000);\n"
                    "}"
                ),
                "description": (
                    "A debounce pattern where each new call cancels "
                    "the previous pending timeout before scheduling a "
                    "new one. This prevents multiple saves from firing "
                    "in quick succession."
                ),
            },
            {
                "title": "Cleanup on template destruction",
                "code": (
                    "Template.editor.onCreated(function () {\n"
                    "  this.reminderHandle = Meteor.setTimeout(() => {\n"
                    "    alert('Remember to save your work!');\n"
                    "  }, 60000);\n"
                    "});\n"
                    "\n"
                    "Template.editor.onDestroyed(function () {\n"
                    "  Meteor.clearTimeout(this.reminderHandle);\n"
                    "});"
                ),
                "description": (
                    "Clear pending timeouts when a template is "
                    "destroyed to prevent callbacks from firing after "
                    "the associated UI is no longer visible."
                ),
            },
        ],
        "tags": ["timers", "cancellation", "cleanup"],
    },
    {
        "name": "Meteor.clearInterval",
        "module": "timers",
        "signature": "Meteor.clearInterval(id)",
        "description": (
            "Cancel a repeating interval previously scheduled by "
            "Meteor.setInterval. Once cancelled, the callback will no "
            "longer be called. This works identically to the native "
            "clearInterval but should be used with handles returned by "
            "Meteor.setInterval specifically. Always clear intervals "
            "when they are no longer needed to prevent memory leaks "
            "and unnecessary background work, especially on the "
            "client when components or templates are destroyed."
        ),
        "params": [
            {
                "name": "id",
                "type": "Handle",
                "description": (
                    "The handle returned by Meteor.setInterval, "
                    "identifying the interval to cancel."
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
                "title": "Stopping a server-side polling interval",
                "code": (
                    "let healthCheckHandle = null;\n"
                    "\n"
                    "function startHealthCheck() {\n"
                    "  healthCheckHandle = Meteor.setInterval(\n"
                    "    async () => {\n"
                    "      const response = await fetch(\n"
                    "        'https://api.example.com/health'\n"
                    "      );\n"
                    "      if (!response.ok) {\n"
                    "        console.error('External API health check failed');\n"
                    "      }\n"
                    "    },\n"
                    "    30000\n"
                    "  );\n"
                    "}\n"
                    "\n"
                    "function stopHealthCheck() {\n"
                    "  if (healthCheckHandle) {\n"
                    "    Meteor.clearInterval(healthCheckHandle);\n"
                    "    healthCheckHandle = null;\n"
                    "  }\n"
                    "}"
                ),
                "description": (
                    "Pair Meteor.setInterval with Meteor.clearInterval "
                    "to start and stop recurring tasks on demand. "
                    "Setting the handle to null after clearing prevents "
                    "accidental double-clearing."
                ),
            },
            {
                "title": "React component cleanup with useEffect",
                "code": (
                    "import React, { useState, useEffect } from 'react';\n"
                    "\n"
                    "function Clock() {\n"
                    "  const [time, setTime] = useState(new Date());\n"
                    "\n"
                    "  useEffect(() => {\n"
                    "    const handle = Meteor.setInterval(() => {\n"
                    "      setTime(new Date());\n"
                    "    }, 1000);\n"
                    "\n"
                    "    return () => Meteor.clearInterval(handle);\n"
                    "  }, []);\n"
                    "\n"
                    "  return <span>{time.toLocaleTimeString()}</span>;\n"
                    "}"
                ),
                "description": (
                    "In a React component, clear the interval in the "
                    "useEffect cleanup function to prevent updates "
                    "after the component unmounts."
                ),
            },
        ],
        "tags": ["timers", "cancellation", "cleanup"],
    },
]
