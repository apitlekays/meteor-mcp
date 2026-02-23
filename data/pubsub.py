"""Meteor.js v3.4.0 Publish/Subscribe API data."""

PUBSUB = [
    {
        "name": "Meteor.publish",
        "module": "pubsub",
        "signature": "Meteor.publish(name, func)",
        "description": (
            "Publishes a record set to clients. Called on the server to define "
            "what data clients can subscribe to. When a client calls "
            "Meteor.subscribe for a matching name, the publish function is "
            "invoked on the server with `this` bound to a publish handler "
            "object. The function can return a cursor (or array of cursors) to "
            "automatically publish documents, or it can use the low-level "
            "added/changed/removed interface for manual control. If name is "
            "null, the record set is automatically sent to all connected "
            "clients without requiring a subscription. In Meteor v3.4.0, "
            "publish functions can be async and may use await."
        ),
        "params": [
            {
                "name": "name",
                "type": "String|Object|null",
                "description": (
                    "Name of the record set. If null, the record set is "
                    "automatically sent to all connected clients without "
                    "requiring a matching subscribe call. Can also be an "
                    "Object whose keys are publication names and values are "
                    "publish functions, allowing batch definition of multiple "
                    "publications in a single call."
                ),
                "optional": False,
            },
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "Function called on the server each time a client "
                    "subscribes. Inside the function, `this` refers to the "
                    "publish handler object, which provides methods like "
                    "this.added, this.changed, this.removed, this.ready, "
                    "this.userId, and this.connection. The function can return "
                    "a Mongo.Cursor, an array of Mongo.Cursors, or use the "
                    "low-level API to manually control the published set."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Basic cursor publication",
                "code": (
                    "Meteor.publish('posts', function () {\n"
                    "  return Posts.find({ published: true });\n"
                    "});"
                ),
                "description": (
                    "Publishes all documents in the Posts collection where "
                    "published is true. The cursor is automatically observed "
                    "for changes and synced to subscribed clients."
                ),
            },
            {
                "title": "Filtered publication using userId",
                "code": (
                    "Meteor.publish('myPosts', function () {\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "  return Posts.find({ authorId: this.userId });\n"
                    "});"
                ),
                "description": (
                    "Publishes only the posts belonging to the currently "
                    "logged-in user. Returns this.ready() immediately if the "
                    "user is not authenticated, signaling an empty publication."
                ),
            },
            {
                "title": "Multiple cursors",
                "code": (
                    "Meteor.publish('postWithComments', function (postId) {\n"
                    "  check(postId, String);\n"
                    "  return [\n"
                    "    Posts.find({ _id: postId }),\n"
                    "    Comments.find({ postId: postId }),\n"
                    "  ];\n"
                    "});"
                ),
                "description": (
                    "Returns an array of cursors to publish documents from "
                    "multiple collections in a single subscription. Each "
                    "cursor must be from a different collection."
                ),
            },
            {
                "title": "Null publication (auto-publish to all clients)",
                "code": (
                    "Meteor.publish(null, function () {\n"
                    "  if (!this.userId) return this.ready();\n"
                    "  return UserSettings.find({ userId: this.userId });\n"
                    "});"
                ),
                "description": (
                    "A null-name publication that automatically sends the "
                    "user's settings to every connected client without "
                    "requiring a subscribe call."
                ),
            },
        ],
        "tags": ["publish", "subscription", "data", "realtime", "server"],
    },
    {
        "name": "Meteor.subscribe",
        "module": "pubsub",
        "signature": "Meteor.subscribe(name, ...args)",
        "description": (
            "Subscribes to a record set published by the server. Returns a "
            "subscription handle with reactive ready() and stop() methods. "
            "The subscription begins fetching data from the server "
            "immediately. When called inside a reactive computation (such as "
            "Tracker.autorun or a Blaze helper), the subscription is "
            "automatically stopped when the computation is invalidated or "
            "stopped. Duplicate subscriptions with the same name and arguments "
            "are merged by the DDP client. The last argument may be an object "
            "with onReady and onStop callbacks."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": (
                    "Name of the subscription. Must match a name registered "
                    "with Meteor.publish on the server."
                ),
                "optional": False,
            },
            {
                "name": "args",
                "type": "Any",
                "description": (
                    "Optional arguments passed to the publish function on the "
                    "server. The last argument can be an object with onReady "
                    "and onStop callback functions."
                ),
                "optional": True,
            },
        ],
        "returns": "SubscriptionHandle",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Basic subscription",
                "code": (
                    "const handle = Meteor.subscribe('posts');\n"
                    "Tracker.autorun(() => {\n"
                    "  if (handle.ready()) {\n"
                    "    console.log('Posts are ready:', Posts.find().fetch());\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Subscribes to the 'posts' publication and reactively "
                    "waits for data to be ready before querying the local "
                    "collection."
                ),
            },
            {
                "title": "Subscription with arguments",
                "code": (
                    "Meteor.subscribe('postWithComments', postId, {\n"
                    "  onReady() {\n"
                    "    console.log('Data is ready');\n"
                    "  },\n"
                    "  onStop(error) {\n"
                    "    if (error) {\n"
                    "      console.error('Subscription stopped with error:', error);\n"
                    "    }\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Passes a postId argument to the server publish function "
                    "and provides onReady and onStop callbacks for lifecycle "
                    "management."
                ),
            },
            {
                "title": "Reactive subscription in autorun",
                "code": (
                    "Tracker.autorun(() => {\n"
                    "  const selectedTag = Session.get('selectedTag');\n"
                    "  Meteor.subscribe('postsByTag', selectedTag);\n"
                    "});"
                ),
                "description": (
                    "When the reactive data source (Session variable) changes, "
                    "the autorun re-runs, automatically stopping the old "
                    "subscription and creating a new one with the updated "
                    "arguments."
                ),
            },
        ],
        "tags": ["subscribe", "subscription", "data", "realtime", "client"],
    },
    {
        "name": "this.userId",
        "module": "pubsub",
        "signature": "this.userId",
        "description": (
            "Accesses the ID of the logged-in user inside a publish function, "
            "or null if no user is logged in. The value is constant within a "
            "single publish function invocation. However, if the logged-in "
            "user changes, Meteor will re-invoke the publish function with "
            "the new userId value. Use this to restrict published data to "
            "the authenticated user."
        ),
        "params": [],
        "returns": "String|null",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Check authentication in publish",
                "code": (
                    "Meteor.publish('privateData', function () {\n"
                    "  if (!this.userId) {\n"
                    "    this.ready();\n"
                    "    return;\n"
                    "  }\n"
                    "  return PrivateData.find({ ownerId: this.userId });\n"
                    "});"
                ),
                "description": (
                    "Checks whether the user is logged in before publishing "
                    "data. If no user is authenticated, signals ready "
                    "immediately with an empty result set."
                ),
            },
        ],
        "tags": ["publish", "userId", "authentication", "server"],
    },
    {
        "name": "this.added",
        "module": "pubsub",
        "signature": "this.added(collection, id, fields)",
        "description": (
            "Called inside a publish function to inform the client that a "
            "document has been added to the published record set. This is part "
            "of the low-level publish API for manually controlling which "
            "documents are sent to the client, as an alternative to returning "
            "cursors. Each call sends a DDP 'added' message to the subscribed "
            "client. The collection argument is the name of the collection on "
            "the client where the document should appear."
        ),
        "params": [
            {
                "name": "collection",
                "type": "String",
                "description": (
                    "The name of the collection that the document belongs to "
                    "on the client side."
                ),
                "optional": False,
            },
            {
                "name": "id",
                "type": "String",
                "description": "The unique ID of the document being added.",
                "optional": False,
            },
            {
                "name": "fields",
                "type": "Object",
                "description": (
                    "The fields of the document to publish. The _id field "
                    "should not be included in this object."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Manual publish with added/ready",
                "code": (
                    "Meteor.publish('currentTime', function () {\n"
                    "  const id = Random.id();\n"
                    "  this.added('timestamps', id, {\n"
                    "    timestamp: new Date(),\n"
                    "  });\n"
                    "\n"
                    "  const interval = Meteor.setInterval(() => {\n"
                    "    this.changed('timestamps', id, {\n"
                    "      timestamp: new Date(),\n"
                    "    });\n"
                    "  }, 1000);\n"
                    "\n"
                    "  this.onStop(() => Meteor.clearInterval(interval));\n"
                    "  this.ready();\n"
                    "});"
                ),
                "description": (
                    "Manually publishes a virtual document that does not exist "
                    "in any MongoDB collection. Uses this.added to create the "
                    "initial document and this.changed to update it every "
                    "second."
                ),
            },
            {
                "title": "Publishing aggregated data",
                "code": (
                    "Meteor.publish('userStats', async function () {\n"
                    "  if (!this.userId) return this.ready();\n"
                    "\n"
                    "  const postCount = await Posts.find({ authorId: this.userId }).countAsync();\n"
                    "  const commentCount = await Comments.find({ authorId: this.userId }).countAsync();\n"
                    "\n"
                    "  this.added('userStats', this.userId, {\n"
                    "    postCount,\n"
                    "    commentCount,\n"
                    "  });\n"
                    "\n"
                    "  this.ready();\n"
                    "});"
                ),
                "description": (
                    "Publishes computed aggregated data as a virtual document "
                    "into a client-side-only collection."
                ),
            },
        ],
        "tags": ["publish", "added", "low-level", "manual", "ddp"],
    },
    {
        "name": "this.changed",
        "module": "pubsub",
        "signature": "this.changed(collection, id, fields)",
        "description": (
            "Called inside a publish function to inform the client that a "
            "previously published document has been modified. Sends a DDP "
            "'changed' message containing only the modified fields. Fields "
            "set to undefined are removed from the document on the client. "
            "This is part of the low-level publish API for manually managing "
            "the record set."
        ),
        "params": [
            {
                "name": "collection",
                "type": "String",
                "description": (
                    "The name of the collection containing the document."
                ),
                "optional": False,
            },
            {
                "name": "id",
                "type": "String",
                "description": (
                    "The unique ID of the document that was previously added "
                    "via this.added."
                ),
                "optional": False,
            },
            {
                "name": "fields",
                "type": "Object",
                "description": (
                    "An object containing the changed fields and their new "
                    "values. Set a field to undefined to remove it from the "
                    "document on the client."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Updating a virtual document",
                "code": (
                    "Meteor.publish('onlineCount', async function () {\n"
                    "  const id = 'online-count';\n"
                    "  let count = await OnlineUsers.find().countAsync();\n"
                    "\n"
                    "  this.added('stats', id, { count });\n"
                    "\n"
                    "  const handle = OnlineUsers.find().observeChanges({\n"
                    "    added: () => {\n"
                    "      count++;\n"
                    "      this.changed('stats', id, { count });\n"
                    "    },\n"
                    "    removed: () => {\n"
                    "      count--;\n"
                    "      this.changed('stats', id, { count });\n"
                    "    },\n"
                    "  });\n"
                    "\n"
                    "  this.onStop(() => handle.stop());\n"
                    "  this.ready();\n"
                    "});"
                ),
                "description": (
                    "Publishes a live count of online users by observing "
                    "changes and calling this.changed to push updates to "
                    "the client whenever users come online or go offline."
                ),
            },
        ],
        "tags": ["publish", "changed", "low-level", "manual", "ddp"],
    },
    {
        "name": "this.removed",
        "module": "pubsub",
        "signature": "this.removed(collection, id)",
        "description": (
            "Called inside a publish function to inform the client that a "
            "previously published document has been removed from the record "
            "set. Sends a DDP 'removed' message to the subscribed client, "
            "causing the document to be removed from the client's local "
            "Minimongo cache. This is part of the low-level publish API."
        ),
        "params": [
            {
                "name": "collection",
                "type": "String",
                "description": (
                    "The name of the collection containing the document."
                ),
                "optional": False,
            },
            {
                "name": "id",
                "type": "String",
                "description": (
                    "The unique ID of the document to remove from the "
                    "client's record set."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Manual document lifecycle",
                "code": (
                    "Meteor.publish('activeTasks', function () {\n"
                    "  const self = this;\n"
                    "\n"
                    "  const handle = Tasks.find({ active: true }).observeChanges({\n"
                    "    added(id, fields) {\n"
                    "      self.added('tasks', id, fields);\n"
                    "    },\n"
                    "    changed(id, fields) {\n"
                    "      self.changed('tasks', id, fields);\n"
                    "    },\n"
                    "    removed(id) {\n"
                    "      self.removed('tasks', id);\n"
                    "    },\n"
                    "  });\n"
                    "\n"
                    "  self.onStop(() => handle.stop());\n"
                    "  self.ready();\n"
                    "});"
                ),
                "description": (
                    "Manually mirrors a cursor's changes using the low-level "
                    "API. This pattern is equivalent to returning the cursor "
                    "directly but allows for custom transformation or "
                    "filtering logic in each callback."
                ),
            },
        ],
        "tags": ["publish", "removed", "low-level", "manual", "ddp"],
    },
    {
        "name": "this.ready",
        "module": "pubsub",
        "signature": "this.ready()",
        "description": (
            "Called inside a publish function to signal that the initial set "
            "of documents has been sent to the client. After this.ready() is "
            "called, the client's subscription handle will report ready() as "
            "true. This must be called when using the low-level added/changed/"
            "removed API. When returning cursors from a publish function, "
            "ready is called automatically once the initial query results have "
            "been sent."
        ),
        "params": [],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Signaling empty publication",
                "code": (
                    "Meteor.publish('adminData', async function () {\n"
                    "  if (!this.userId) {\n"
                    "    this.ready();\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  const user = await Meteor.users.findOneAsync(this.userId);\n"
                    "  if (!user || !user.isAdmin) {\n"
                    "    this.ready();\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  return AdminData.find();\n"
                    "});"
                ),
                "description": (
                    "Calls this.ready() to signal an empty result set when "
                    "the user is not authenticated or not an admin, preventing "
                    "the client from waiting indefinitely."
                ),
            },
            {
                "title": "Ready after manual document addition",
                "code": (
                    "Meteor.publish('serverInfo', function () {\n"
                    "  this.added('serverInfo', 'server-1', {\n"
                    "    version: Meteor.release,\n"
                    "    startedAt: new Date(),\n"
                    "  });\n"
                    "  this.ready();\n"
                    "});"
                ),
                "description": (
                    "After manually adding documents with this.added, calls "
                    "this.ready() to tell the client that the initial data "
                    "set is complete."
                ),
            },
        ],
        "tags": ["publish", "ready", "low-level", "lifecycle"],
    },
    {
        "name": "this.onStop",
        "module": "pubsub",
        "signature": "this.onStop(func)",
        "description": (
            "Registers a callback inside a publish function that runs when "
            "the subscription is stopped, either by the client calling "
            "stop() or by the client disconnecting. Use this to clean up "
            "resources such as timers, external connections, or observe "
            "handles that were set up during the publication. Multiple "
            "onStop callbacks can be registered and they will all be called "
            "when the subscription ends."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "Callback function invoked when the subscription is "
                    "stopped. Receives no arguments."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Cleaning up an interval",
                "code": (
                    "Meteor.publish('heartbeat', function () {\n"
                    "  const id = Random.id();\n"
                    "  this.added('heartbeats', id, { ts: new Date() });\n"
                    "\n"
                    "  const interval = Meteor.setInterval(() => {\n"
                    "    this.changed('heartbeats', id, { ts: new Date() });\n"
                    "  }, 5000);\n"
                    "\n"
                    "  this.onStop(() => {\n"
                    "    Meteor.clearInterval(interval);\n"
                    "  });\n"
                    "\n"
                    "  this.ready();\n"
                    "});"
                ),
                "description": (
                    "Registers an onStop callback to clear the interval "
                    "timer when the client unsubscribes or disconnects, "
                    "preventing memory leaks on the server."
                ),
            },
            {
                "title": "Cleaning up an observe handle",
                "code": (
                    "Meteor.publish('transformedPosts', function () {\n"
                    "  const self = this;\n"
                    "\n"
                    "  const handle = Posts.find({ published: true }).observe({\n"
                    "    added(doc) {\n"
                    "      self.added('posts', doc._id, {\n"
                    "        ...doc,\n"
                    "        titleUpper: doc.title.toUpperCase(),\n"
                    "      });\n"
                    "    },\n"
                    "    changed(newDoc) {\n"
                    "      self.changed('posts', newDoc._id, {\n"
                    "        ...newDoc,\n"
                    "        titleUpper: newDoc.title.toUpperCase(),\n"
                    "      });\n"
                    "    },\n"
                    "    removed(oldDoc) {\n"
                    "      self.removed('posts', oldDoc._id);\n"
                    "    },\n"
                    "  });\n"
                    "\n"
                    "  self.onStop(() => handle.stop());\n"
                    "  self.ready();\n"
                    "});"
                ),
                "description": (
                    "Stops the observe handle when the subscription ends to "
                    "release server resources."
                ),
            },
        ],
        "tags": ["publish", "onStop", "cleanup", "lifecycle"],
    },
    {
        "name": "this.error",
        "module": "pubsub",
        "signature": "this.error(error)",
        "description": (
            "Called inside a publish function to signal that an error has "
            "occurred. This stops the subscription and sends the error to "
            "the client. The error is passed to the client's onStop callback "
            "if one was provided in the subscribe call. The error should be "
            "a Meteor.Error instance to ensure it is properly serialized "
            "over DDP. Calling this.error also triggers any onStop callbacks "
            "registered with this.onStop."
        ),
        "params": [
            {
                "name": "error",
                "type": "Error",
                "description": (
                    "An Error instance describing the error. Using "
                    "Meteor.Error is recommended to ensure the error details "
                    "are properly serialized and sent to the client over DDP."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Sending an error to the client",
                "code": (
                    "Meteor.publish('secureData', function (secretKey) {\n"
                    "  if (!this.userId) {\n"
                    "    this.error(\n"
                    "      new Meteor.Error('not-authorized', 'You must be logged in.')\n"
                    "    );\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  if (secretKey !== Meteor.settings.secretKey) {\n"
                    "    this.error(\n"
                    "      new Meteor.Error('invalid-key', 'The provided key is invalid.')\n"
                    "    );\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  return SecureData.find();\n"
                    "});"
                ),
                "description": (
                    "Validates the user's credentials and a secret key before "
                    "publishing data. Sends descriptive Meteor.Error instances "
                    "to the client when validation fails."
                ),
            },
        ],
        "tags": ["publish", "error", "security", "lifecycle"],
    },
    {
        "name": "this.stop",
        "module": "pubsub",
        "signature": "this.stop()",
        "description": (
            "Called inside a publish function to programmatically stop the "
            "subscription. This causes the client's subscription handle to "
            "become inactive, triggers any onStop callbacks registered with "
            "this.onStop, and removes all published documents from the "
            "client's cache (unless they are also published by another active "
            "subscription). Unlike this.error, this does not send an error to "
            "the client."
        ),
        "params": [],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Stopping a subscription after a timeout",
                "code": (
                    "Meteor.publish('temporaryAccess', function () {\n"
                    "  if (!this.userId) return this.ready();\n"
                    "\n"
                    "  const self = this;\n"
                    "  const timeout = Meteor.setTimeout(() => {\n"
                    "    self.stop();\n"
                    "  }, 60 * 1000);\n"
                    "\n"
                    "  self.onStop(() => Meteor.clearTimeout(timeout));\n"
                    "\n"
                    "  return TemporaryData.find({ userId: self.userId });\n"
                    "});"
                ),
                "description": (
                    "Automatically stops the subscription after 60 seconds, "
                    "removing the published data from the client. The onStop "
                    "callback clears the timeout if the client unsubscribes "
                    "before the timer fires."
                ),
            },
        ],
        "tags": ["publish", "stop", "lifecycle"],
    },
    {
        "name": "this.connection",
        "module": "pubsub",
        "signature": "this.connection",
        "description": (
            "Accesses the DDP connection object for the client that initiated "
            "the subscription. Available inside a publish function as a "
            "property of the publish handler. The connection object contains "
            "the id property (a string uniquely identifying this DDP "
            "connection), the clientAddress property (the client's IP "
            "address), and the httpHeaders property (an object containing "
            "headers from the initial connection request). Returns null for "
            "server-initiated subscriptions."
        ),
        "params": [],
        "returns": "Object|null",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Logging client connection details",
                "code": (
                    "Meteor.publish('loggedData', function () {\n"
                    "  console.log('Client IP:', this.connection.clientAddress);\n"
                    "  console.log('Connection ID:', this.connection.id);\n"
                    "  console.log('User-Agent:', this.connection.httpHeaders['user-agent']);\n"
                    "\n"
                    "  return SomeCollection.find();\n"
                    "});"
                ),
                "description": (
                    "Accesses the client's IP address, connection ID, and "
                    "HTTP headers from the DDP connection for logging or "
                    "security purposes."
                ),
            },
            {
                "title": "Rate limiting by connection",
                "code": (
                    "const connectionCounts = new Map();\n"
                    "\n"
                    "Meteor.publish('rateLimitedData', function () {\n"
                    "  const connId = this.connection.id;\n"
                    "  const count = connectionCounts.get(connId) || 0;\n"
                    "\n"
                    "  if (count >= 10) {\n"
                    "    this.error(\n"
                    "      new Meteor.Error('rate-limit', 'Too many subscriptions.')\n"
                    "    );\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  connectionCounts.set(connId, count + 1);\n"
                    "\n"
                    "  this.onStop(() => {\n"
                    "    const current = connectionCounts.get(connId) || 1;\n"
                    "    connectionCounts.set(connId, current - 1);\n"
                    "  });\n"
                    "\n"
                    "  return SomeData.find();\n"
                    "});"
                ),
                "description": (
                    "Tracks the number of active subscriptions per DDP "
                    "connection and rejects new subscriptions when the limit "
                    "is exceeded."
                ),
            },
        ],
        "tags": ["publish", "connection", "ddp", "server"],
    },
    {
        "name": "Subscription.ready",
        "module": "pubsub",
        "signature": "handle.ready()",
        "description": (
            "Returns true if the server has marked the subscription as ready "
            "by calling this.ready() in the publish function, or when the "
            "initial set of documents from a cursor-based publication has been "
            "fully sent. This is a reactive data source: when used inside a "
            "reactive computation such as Tracker.autorun, the computation "
            "will re-run when the ready state changes. Commonly used to "
            "display loading indicators while waiting for subscription data."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Showing a loading state",
                "code": (
                    "Template.postsList.onCreated(function () {\n"
                    "  this.subscribe('posts');\n"
                    "});\n"
                    "\n"
                    "Template.postsList.helpers({\n"
                    "  isLoading() {\n"
                    "    return !Template.instance().subscriptionsReady();\n"
                    "  },\n"
                    "  posts() {\n"
                    "    return Posts.find({}, { sort: { createdAt: -1 } });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Uses the reactive ready state to conditionally show a "
                    "loading indicator until the subscription data has arrived "
                    "from the server."
                ),
            },
            {
                "title": "Reactive ready check with Tracker",
                "code": (
                    "const handle = Meteor.subscribe('posts');\n"
                    "\n"
                    "Tracker.autorun(() => {\n"
                    "  if (handle.ready()) {\n"
                    "    const posts = Posts.find().fetch();\n"
                    "    console.log(`Loaded ${posts.length} posts`);\n"
                    "  } else {\n"
                    "    console.log('Loading posts...');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Reactively monitors the subscription's ready state "
                    "inside a Tracker.autorun computation."
                ),
            },
        ],
        "tags": ["subscribe", "ready", "reactive", "loading", "client"],
    },
    {
        "name": "Subscription.stop",
        "module": "pubsub",
        "signature": "handle.stop()",
        "description": (
            "Stops the subscription, telling the server to stop sending data "
            "and removing the subscription's documents from the client's "
            "Minimongo cache (unless they are also provided by another active "
            "subscription). If the subscription was created inside a reactive "
            "computation, it is automatically stopped when the computation is "
            "invalidated or stopped, so calling stop() manually is usually "
            "only necessary for subscriptions created outside of reactive "
            "contexts."
        ),
        "params": [],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Manually stopping a subscription",
                "code": (
                    "const handle = Meteor.subscribe('notifications');\n"
                    "\n"
                    "// Later, when the data is no longer needed:\n"
                    "handle.stop();"
                ),
                "description": (
                    "Explicitly stops a subscription when the data is no "
                    "longer needed, freeing server and client resources."
                ),
            },
            {
                "title": "Stopping on component unmount",
                "code": (
                    "Template.dashboard.onCreated(function () {\n"
                    "  this.handle = Meteor.subscribe('dashboardData');\n"
                    "});\n"
                    "\n"
                    "Template.dashboard.onDestroyed(function () {\n"
                    "  this.handle.stop();\n"
                    "});"
                ),
                "description": (
                    "Stops the subscription when the Blaze template is "
                    "destroyed to prevent unnecessary data transfer. Note "
                    "that subscriptions created via Template.subscribe are "
                    "automatically stopped on destroy."
                ),
            },
        ],
        "tags": ["subscribe", "stop", "cleanup", "client"],
    },
    {
        "name": "Meteor.server.setPublicationStrategy",
        "module": "pubsub",
        "signature": "Meteor.server.setPublicationStrategy(publicationName, strategy)",
        "description": (
            "Sets the DDP merge strategy for a specific publication. Meteor uses "
            "merge strategies to decide how documents from overlapping publications "
            "are combined before being sent to clients. The available strategies are: "
            "DDP.SERVER_MERGE (default) -- the server de-duplicates documents across "
            "subscriptions, merging fields from all publications that publish the "
            "same document; "
            "DDP.NO_MERGE -- the server sends each publication's documents "
            "independently without merging, which reduces server memory usage but "
            "may send duplicate documents to the client; "
            "DDP.NO_MERGE_NO_HISTORY -- like NO_MERGE but also does not track which "
            "documents have been sent, further reducing server memory at the cost of "
            "sending all documents on every re-subscription. "
            "Must be called before any subscription to the publication is made."
        ),
        "params": [
            {
                "name": "publicationName",
                "type": "String",
                "description": "The name of the publication to configure.",
                "optional": False,
            },
            {
                "name": "strategy",
                "type": "Object",
                "description": (
                    "An object with `useCollectionView` (Boolean) and "
                    "`doAccountingForCollection` (Boolean) fields, or one of the "
                    "predefined constants: DDP.SERVER_MERGE, DDP.NO_MERGE, "
                    "DDP.NO_MERGE_NO_HISTORY."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Optimize a high-traffic publication",
                "code": (
                    "// Disable merge for a publication that sends many documents\n"
                    "Meteor.server.setPublicationStrategy('logs', DDPServer.publicationStrategies.NO_MERGE);\n"
                    "\n"
                    "Meteor.publish('logs', function () {\n"
                    "  return Logs.find({}, { limit: 1000, sort: { createdAt: -1 } });\n"
                    "});"
                ),
                "description": (
                    "Uses NO_MERGE to reduce server memory for a publication that "
                    "sends a large number of documents where field merging is not needed."
                ),
            },
        ],
        "tags": ["publish", "merge", "strategy", "performance", "server", "ddp"],
    },
    {
        "name": "Meteor.server.getPublicationStrategy",
        "module": "pubsub",
        "signature": "Meteor.server.getPublicationStrategy(publicationName)",
        "description": (
            "Returns the current DDP merge strategy for a specific publication. "
            "The returned object has `useCollectionView` (Boolean) and "
            "`doAccountingForCollection` (Boolean) fields that describe the "
            "merge behavior. This is useful for debugging or verifying that a "
            "publication strategy has been set correctly."
        ),
        "params": [
            {
                "name": "publicationName",
                "type": "String",
                "description": "The name of the publication to query.",
                "optional": False,
            },
        ],
        "returns": (
            "Object -- { useCollectionView: Boolean, doAccountingForCollection: Boolean }"
        ),
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Check a publication's merge strategy",
                "code": (
                    "const strategy = Meteor.server.getPublicationStrategy('logs');\n"
                    "console.log('useCollectionView:', strategy.useCollectionView);\n"
                    "console.log('doAccountingForCollection:', strategy.doAccountingForCollection);"
                ),
                "description": (
                    "Retrieves and logs the merge strategy configuration for the "
                    "'logs' publication."
                ),
            },
        ],
        "tags": ["publish", "merge", "strategy", "server", "ddp"],
    },
]
