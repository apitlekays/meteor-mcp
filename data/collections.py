"""Meteor.js Mongo Collections API data for v3.4.0.

Covers the Mongo.Collection constructor, collection CRUD methods (both deprecated
sync variants and the async-first replacements), Cursor iteration/observation
methods, and Mongo.ObjectID.
"""

COLLECTIONS: list[dict] = [
    # -------------------------------------------------------------------------
    # Mongo.Collection constructor
    # -------------------------------------------------------------------------
    {
        "name": "Mongo.Collection",
        "module": "collections",
        "signature": "new Mongo.Collection(name, options)",
        "description": (
            "Constructor that creates and returns a Mongo.Collection object. "
            "The `name` argument is the name of the MongoDB collection on the "
            "server; pass `null` to create a local-only (unmanaged) collection "
            "that is not synchronized between client and server. On the client "
            "a local Minimongo cache is created for the collection. On the "
            "server a connection to the underlying MongoDB database is "
            "established. If a collection with the same name has already been "
            "constructed, the existing instance is returned."
        ),
        "params": [
            {
                "name": "name",
                "type": "String | null",
                "optional": False,
                "description": (
                    "The name of the collection. Pass null to create an "
                    "unmanaged (local-only) collection."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Optional configuration. Accepted keys: "
                    "`connection` (Object) - the server connection that will "
                    "manage this collection, defaults to `Meteor.connection`; "
                    "`idGeneration` (String) - method of generating `_id` fields, "
                    "either 'STRING' or 'MONGO'; "
                    "`transform` (Function) - an optional transformation function "
                    "applied to documents before they are returned from fetch, "
                    "findOne, and passed to callbacks of observe and observeChanges; "
                    "`defineMutationMethods` (Boolean) - set to false to skip "
                    "creating mutation methods for insert/update/remove, "
                    "defaults to true."
                ),
            },
        ],
        "returns": "Mongo.Collection",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Create a standard collection",
                "code": (
                    "import { Mongo } from 'meteor/mongo';\n\n"
                    "export const Tasks = new Mongo.Collection('tasks');"
                ),
                "description": (
                    "Creates a 'tasks' collection accessible on both client "
                    "and server. On the server it maps to the MongoDB 'tasks' "
                    "collection; on the client a Minimongo cache is created."
                ),
            },
            {
                "title": "Create a local-only collection",
                "code": (
                    "import { Mongo } from 'meteor/mongo';\n\n"
                    "// Local-only collection, not synced to the server\n"
                    "const Scratch = new Mongo.Collection(null);"
                ),
                "description": (
                    "Passing null creates an in-memory collection that is not "
                    "persisted to MongoDB and not synchronized between client "
                    "and server. Useful for temporary UI state."
                ),
            },
            {
                "title": "Collection with a transform function",
                "code": (
                    "import { Mongo } from 'meteor/mongo';\n\n"
                    "const Animals = new Mongo.Collection('animals', {\n"
                    "  transform(doc) {\n"
                    "    doc.fullName = `${doc.genus} ${doc.species}`;\n"
                    "    return doc;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "The transform function is applied to every document "
                    "returned by fetch, findOne, and passed to observe and "
                    "observeChanges callbacks."
                ),
            },
        ],
        "tags": ["collection", "mongo", "database", "constructor"],
    },
    # -------------------------------------------------------------------------
    # Collection.findOne (deprecated sync)
    # -------------------------------------------------------------------------
    {
        "name": "Collection.findOne",
        "module": "collections",
        "signature": "collection.findOne(selector, options)",
        "description": (
            "Finds the first document that matches the selector. This is the "
            "synchronous variant and is deprecated in Meteor v3. Use "
            "`findOneAsync` instead. On the client inside reactive "
            "computations this method is reactive -- it will re-run when the "
            "matching document changes. Returns `undefined` if no document "
            "matches."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": True,
                "description": (
                    "A MongoDB selector, or a string interpreted as the _id. "
                    "An empty selector ({}) matches all documents."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options: `sort` (Object) - sort order; "
                    "`skip` (Number) - number of results to skip; "
                    "`fields` (Object) - field inclusion/exclusion specifier; "
                    "`reactive` (Boolean) - default true, set to false to "
                    "disable reactivity; "
                    "`transform` (Function) - override the collection-level transform."
                ),
            },
        ],
        "returns": "Object | undefined",
        "environment": "client",
        "is_reactive": True,
        "deprecated": True,
        "examples": [
            {
                "title": "Find a document by _id (deprecated)",
                "code": (
                    "// Deprecated -- use findOneAsync instead\n"
                    "const task = Tasks.findOne(taskId);\n"
                    "console.log(task.title);"
                ),
                "description": (
                    "Synchronously returns the document with the given _id. "
                    "This pattern is deprecated in Meteor v3 and will be "
                    "removed in a future release."
                ),
            },
        ],
        "tags": ["collection", "mongo", "query", "find", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Collection.findOneAsync
    # -------------------------------------------------------------------------
    {
        "name": "Collection.findOneAsync",
        "module": "collections",
        "signature": "collection.findOneAsync(selector, options)",
        "description": (
            "Asynchronously finds the first document that matches the "
            "selector. Returns a Promise that resolves to the matching "
            "document or `undefined` if no match is found. This is the "
            "preferred replacement for the deprecated synchronous `findOne` "
            "in Meteor v3's async-first API."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": True,
                "description": (
                    "A MongoDB selector, or a string interpreted as the _id. "
                    "An empty selector ({}) matches all documents."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options: `sort` (Object) - sort order; "
                    "`skip` (Number) - number of results to skip; "
                    "`fields` (Object) - field inclusion/exclusion specifier; "
                    "`transform` (Function) - override the collection-level transform."
                ),
            },
        ],
        "returns": "Promise<Object | undefined>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Find a document by _id",
                "code": (
                    "const task = await Tasks.findOneAsync(taskId);\n"
                    "if (task) {\n"
                    "  console.log(task.title);\n"
                    "}"
                ),
                "description": (
                    "Resolves to the document matching the given _id, or "
                    "undefined if not found."
                ),
            },
            {
                "title": "Find with a query selector and options",
                "code": (
                    "const latestTask = await Tasks.findOneAsync(\n"
                    "  { status: 'active', owner: userId },\n"
                    "  { sort: { createdAt: -1 } }\n"
                    ");"
                ),
                "description": (
                    "Finds the most recently created active task owned by "
                    "the specified user."
                ),
            },
        ],
        "tags": ["collection", "mongo", "query", "find", "async"],
    },
    # -------------------------------------------------------------------------
    # Collection.find
    # -------------------------------------------------------------------------
    {
        "name": "Collection.find",
        "module": "collections",
        "signature": "collection.find(selector, options)",
        "description": (
            "Returns a Cursor object representing a set of documents that "
            "match the selector. The find method does not immediately access "
            "the database or return documents; instead it returns a lazy "
            "cursor. Documents are fetched when you call `fetchAsync`, "
            "`forEachAsync`, `mapAsync`, or iterate the cursor. On the "
            "client inside reactive computations the cursor is reactive. "
            "The cursor is also the primary return value from Meteor publish "
            "functions."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": True,
                "description": (
                    "A MongoDB selector, or a string interpreted as the _id. "
                    "An empty selector ({}) or no argument matches all "
                    "documents in the collection."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options: `sort` (Object) - sort order as a MongoDB sort "
                    "specifier; `skip` (Number) - number of results to skip "
                    "from the beginning; `limit` (Number) - maximum number of "
                    "results to return; `fields` (Object) - field "
                    "inclusion/exclusion specifier (use 1 to include, 0 to "
                    "exclude); `reactive` (Boolean) - default true on client, "
                    "set to false to disable; `transform` (Function) - "
                    "override the collection-level transform."
                ),
            },
        ],
        "returns": "Mongo.Cursor",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Find all active tasks sorted by creation date",
                "code": (
                    "const cursor = Tasks.find(\n"
                    "  { status: 'active' },\n"
                    "  { sort: { createdAt: -1 }, limit: 50 }\n"
                    ");\n\n"
                    "const tasks = await cursor.fetchAsync();"
                ),
                "description": (
                    "Returns a cursor for all active tasks, sorted newest "
                    "first, limited to 50 results. Documents are fetched "
                    "asynchronously with fetchAsync."
                ),
            },
            {
                "title": "Return a cursor from a publish function",
                "code": (
                    "Meteor.publish('userTasks', function () {\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "  return Tasks.find(\n"
                    "    { owner: this.userId },\n"
                    "    { fields: { title: 1, status: 1, createdAt: 1 } }\n"
                    "  );\n"
                    "});"
                ),
                "description": (
                    "In a publish function the returned cursor automatically "
                    "syncs matching documents to subscribed clients."
                ),
            },
            {
                "title": "Field projection to limit transferred data",
                "code": (
                    "const cursor = Users.find(\n"
                    "  {},\n"
                    "  { fields: { username: 1, 'profile.avatar': 1 } }\n"
                    ");"
                ),
                "description": (
                    "Only the username and profile.avatar fields are included "
                    "in the returned documents. The _id field is always "
                    "included by default."
                ),
            },
        ],
        "tags": ["collection", "mongo", "query", "find", "cursor", "reactive"],
    },
    # -------------------------------------------------------------------------
    # Collection.insert (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Collection.insert",
        "module": "collections",
        "signature": "collection.insert(doc, callback)",
        "description": (
            "Synchronously inserts a document into the collection. This "
            "method is deprecated in Meteor v3; use `insertAsync` instead. "
            "If the document does not contain an `_id` field, one is "
            "generated automatically. Returns the `_id` of the inserted "
            "document."
        ),
        "params": [
            {
                "name": "doc",
                "type": "Object",
                "optional": False,
                "description": "The document to insert. May include an _id field.",
            },
            {
                "name": "callback",
                "type": "Function",
                "optional": True,
                "description": (
                    "Optional callback. If present, called with an error "
                    "object as the first argument and the _id as the second "
                    "on success."
                ),
            },
        ],
        "returns": "String",
        "environment": "client",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Insert a document (deprecated)",
                "code": (
                    "// Deprecated -- use insertAsync instead\n"
                    "const id = Tasks.insert({\n"
                    "  title: 'Buy groceries',\n"
                    "  status: 'active',\n"
                    "  createdAt: new Date(),\n"
                    "});"
                ),
                "description": (
                    "Synchronously inserts a task document and returns its "
                    "generated _id. Deprecated in favor of insertAsync."
                ),
            },
        ],
        "tags": ["collection", "mongo", "insert", "write", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Collection.insertAsync
    # -------------------------------------------------------------------------
    {
        "name": "Collection.insertAsync",
        "module": "collections",
        "signature": "collection.insertAsync(doc)",
        "description": (
            "Asynchronously inserts a document into the collection and "
            "returns a Promise that resolves to the `_id` of the newly "
            "inserted document. If the document does not contain an `_id` "
            "field, one is generated automatically. This is the async-first "
            "replacement for the deprecated `insert` method in Meteor v3."
        ),
        "params": [
            {
                "name": "doc",
                "type": "Object",
                "optional": False,
                "description": "The document to insert. May include an _id field.",
            },
        ],
        "returns": "Promise<String>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Insert a document",
                "code": (
                    "const taskId = await Tasks.insertAsync({\n"
                    "  title: 'Buy groceries',\n"
                    "  status: 'active',\n"
                    "  owner: Meteor.userId(),\n"
                    "  createdAt: new Date(),\n"
                    "});\n\n"
                    "console.log('Inserted task:', taskId);"
                ),
                "description": (
                    "Inserts a new task document and resolves to the generated _id."
                ),
            },
            {
                "title": "Insert inside a Meteor method",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'tasks.create'(title) {\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "    const taskId = await Tasks.insertAsync({\n"
                    "      title,\n"
                    "      status: 'active',\n"
                    "      owner: this.userId,\n"
                    "      createdAt: new Date(),\n"
                    "    });\n"
                    "    return taskId;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "A typical Meteor method that validates the user and "
                    "inserts a document using the async API."
                ),
            },
        ],
        "tags": ["collection", "mongo", "insert", "write", "async"],
    },
    # -------------------------------------------------------------------------
    # Collection.update (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Collection.update",
        "module": "collections",
        "signature": "collection.update(selector, modifier, options, callback)",
        "description": (
            "Synchronously modifies one or more documents in the collection. "
            "This method is deprecated in Meteor v3; use `updateAsync` "
            "instead. On the client, only a single document can be updated "
            "at a time, selected by its `_id`. On the server, multiple "
            "documents can be updated by passing `{ multi: true }` in options. "
            "Returns the number of affected documents."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": False,
                "description": (
                    "Specifies which documents to modify. A string is "
                    "interpreted as an _id."
                ),
            },
            {
                "name": "modifier",
                "type": "Object",
                "optional": False,
                "description": (
                    "A MongoDB modifier object using operators like $set, "
                    "$unset, $inc, $push, $pull, etc."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options: `multi` (Boolean) - true to modify all matching "
                    "documents, server only; `upsert` (Boolean) - true to "
                    "insert a document if no match is found."
                ),
            },
            {
                "name": "callback",
                "type": "Function",
                "optional": True,
                "description": (
                    "Optional callback. Called with an error object as the "
                    "first argument and the number of affected documents as "
                    "the second."
                ),
            },
        ],
        "returns": "Number",
        "environment": "client",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Update a single document (deprecated)",
                "code": (
                    "// Deprecated -- use updateAsync instead\n"
                    "Tasks.update(taskId, {\n"
                    "  $set: { status: 'completed' },\n"
                    "});"
                ),
                "description": (
                    "Sets the status field to 'completed' on the document "
                    "matching taskId. Deprecated in favor of updateAsync."
                ),
            },
        ],
        "tags": ["collection", "mongo", "update", "write", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Collection.updateAsync
    # -------------------------------------------------------------------------
    {
        "name": "Collection.updateAsync",
        "module": "collections",
        "signature": "collection.updateAsync(selector, modifier, options)",
        "description": (
            "Asynchronously modifies one or more documents matching the "
            "selector. Returns a Promise that resolves to the number of "
            "affected documents. On the client, only a single document can "
            "be modified at a time (by _id). On the server, pass "
            "`{ multi: true }` to modify all matching documents. This is "
            "the async-first replacement for the deprecated `update` method "
            "in Meteor v3."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": False,
                "description": (
                    "Specifies which documents to modify. A string is "
                    "interpreted as an _id."
                ),
            },
            {
                "name": "modifier",
                "type": "Object",
                "optional": False,
                "description": (
                    "A MongoDB modifier object using operators like $set, "
                    "$unset, $inc, $push, $pull, etc."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options: `multi` (Boolean) - true to modify all matching "
                    "documents, server only; `upsert` (Boolean) - true to "
                    "insert a document if no match is found."
                ),
            },
        ],
        "returns": "Promise<Number>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Update a single document by _id",
                "code": (
                    "const affected = await Tasks.updateAsync(taskId, {\n"
                    "  $set: { status: 'completed', completedAt: new Date() },\n"
                    "});\n\n"
                    "console.log(`${affected} document(s) updated`);"
                ),
                "description": (
                    "Sets the status and completedAt fields on the document "
                    "matching taskId."
                ),
            },
            {
                "title": "Update multiple documents on the server",
                "code": (
                    "// Server only -- multi update\n"
                    "const affected = await Tasks.updateAsync(\n"
                    "  { status: 'active', dueDate: { $lt: new Date() } },\n"
                    "  { $set: { status: 'overdue' } },\n"
                    "  { multi: true }\n"
                    ");\n\n"
                    "console.log(`Marked ${affected} tasks as overdue`);"
                ),
                "description": (
                    "On the server, the multi option allows updating all "
                    "documents matching the selector."
                ),
            },
            {
                "title": "Increment a counter with $inc",
                "code": (
                    "await Posts.updateAsync(postId, {\n"
                    "  $inc: { viewCount: 1 },\n"
                    "});"
                ),
                "description": (
                    "Atomically increments the viewCount field by 1."
                ),
            },
        ],
        "tags": ["collection", "mongo", "update", "write", "async"],
    },
    # -------------------------------------------------------------------------
    # Collection.upsert (deprecated sync)
    # -------------------------------------------------------------------------
    {
        "name": "Collection.upsert",
        "module": "collections",
        "signature": "collection.upsert(selector, modifier, options, callback)",
        "description": (
            "Synchronously modifies a document matching the selector, or "
            "inserts a new document if no match is found. This method is "
            "deprecated in Meteor v3; use `upsertAsync` instead. Returns an "
            "object with keys: `numberAffected` (Number) indicating how many "
            "documents were updated, and optionally `insertedId` (String) if "
            "a new document was inserted."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": False,
                "description": (
                    "Specifies which documents to modify. A string is "
                    "interpreted as an _id."
                ),
            },
            {
                "name": "modifier",
                "type": "Object",
                "optional": False,
                "description": (
                    "A MongoDB modifier object using operators like $set, "
                    "$setOnInsert, $inc, etc."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options: `multi` (Boolean) - true to modify all matching "
                    "documents, server only."
                ),
            },
            {
                "name": "callback",
                "type": "Function",
                "optional": True,
                "description": (
                    "Optional callback. Called with an error object as the "
                    "first argument and the result object as the second."
                ),
            },
        ],
        "returns": "Object ({ numberAffected: Number, insertedId: String | undefined })",
        "environment": "client",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Upsert a document (deprecated)",
                "code": (
                    "// Deprecated -- use upsertAsync instead\n"
                    "const result = Preferences.upsert(\n"
                    "  { userId, key: 'theme' },\n"
                    "  { $set: { value: 'dark' } }\n"
                    ");\n\n"
                    "console.log(result.numberAffected);"
                ),
                "description": (
                    "Synchronously upserts a preference document. Deprecated "
                    "in favor of upsertAsync."
                ),
            },
        ],
        "tags": ["collection", "mongo", "upsert", "write", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Collection.upsertAsync
    # -------------------------------------------------------------------------
    {
        "name": "Collection.upsertAsync",
        "module": "collections",
        "signature": "collection.upsertAsync(selector, modifier, options)",
        "description": (
            "Asynchronously modifies a document matching the selector, or "
            "inserts a new document if no match is found. Returns a Promise "
            "that resolves to an object with keys: `numberAffected` (Number) "
            "indicating how many documents were updated, and optionally "
            "`insertedId` (String) if a new document was inserted. This "
            "combines the semantics of update-or-insert into a single "
            "atomic operation."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": False,
                "description": (
                    "Specifies which documents to modify. A string is "
                    "interpreted as an _id."
                ),
            },
            {
                "name": "modifier",
                "type": "Object",
                "optional": False,
                "description": (
                    "A MongoDB modifier object using operators like $set, "
                    "$setOnInsert, $inc, etc."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options: `multi` (Boolean) - true to modify all matching "
                    "documents, server only."
                ),
            },
        ],
        "returns": "Promise<{ numberAffected: Number, insertedId: String | undefined }>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Upsert a user preference",
                "code": (
                    "const result = await Preferences.upsertAsync(\n"
                    "  { userId, key: 'theme' },\n"
                    "  {\n"
                    "    $set: { value: 'dark', updatedAt: new Date() },\n"
                    "    $setOnInsert: { createdAt: new Date() },\n"
                    "  }\n"
                    ");\n\n"
                    "if (result.insertedId) {\n"
                    "  console.log('Created new preference:', result.insertedId);\n"
                    "} else {\n"
                    "  console.log('Updated existing preference');\n"
                    "}"
                ),
                "description": (
                    "If a preference matching the userId and key exists, it "
                    "is updated. Otherwise a new document is inserted with "
                    "both the $set and $setOnInsert fields applied."
                ),
            },
            {
                "title": "Track page views with upsert",
                "code": (
                    "await Analytics.upsertAsync(\n"
                    "  { page: '/home', date: today },\n"
                    "  {\n"
                    "    $inc: { views: 1 },\n"
                    "    $setOnInsert: { page: '/home', date: today },\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Atomically increments the view count for today's date, "
                    "or creates the analytics document if it does not exist."
                ),
            },
        ],
        "tags": ["collection", "mongo", "upsert", "write", "async"],
    },
    # -------------------------------------------------------------------------
    # Collection.remove (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Collection.remove",
        "module": "collections",
        "signature": "collection.remove(selector, callback)",
        "description": (
            "Synchronously removes documents matching the selector from the "
            "collection. This method is deprecated in Meteor v3; use "
            "`removeAsync` instead. On the client, only a single document "
            "can be removed at a time (by _id). On the server, all matching "
            "documents are removed. Returns the number of removed documents."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": False,
                "description": (
                    "Specifies which documents to remove. A string is "
                    "interpreted as an _id."
                ),
            },
            {
                "name": "callback",
                "type": "Function",
                "optional": True,
                "description": (
                    "Optional callback. Called with an error object as the "
                    "first argument and the number of removed documents as "
                    "the second."
                ),
            },
        ],
        "returns": "Number",
        "environment": "client",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Remove a document (deprecated)",
                "code": (
                    "// Deprecated -- use removeAsync instead\n"
                    "Tasks.remove(taskId);"
                ),
                "description": (
                    "Synchronously removes the document matching taskId. "
                    "Deprecated in favor of removeAsync."
                ),
            },
        ],
        "tags": ["collection", "mongo", "remove", "delete", "write", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Collection.removeAsync
    # -------------------------------------------------------------------------
    {
        "name": "Collection.removeAsync",
        "module": "collections",
        "signature": "collection.removeAsync(selector)",
        "description": (
            "Asynchronously removes documents matching the selector from the "
            "collection. Returns a Promise that resolves to the number of "
            "removed documents. On the client, only a single document can "
            "be removed at a time (by _id). On the server, all matching "
            "documents are removed. This is the async-first replacement for "
            "the deprecated `remove` method in Meteor v3."
        ),
        "params": [
            {
                "name": "selector",
                "type": "Object | String",
                "optional": False,
                "description": (
                    "Specifies which documents to remove. A string is "
                    "interpreted as an _id."
                ),
            },
        ],
        "returns": "Promise<Number>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Remove a single document by _id",
                "code": (
                    "const removed = await Tasks.removeAsync(taskId);\n"
                    "console.log(`${removed} document(s) removed`);"
                ),
                "description": (
                    "Removes the document with the given _id and resolves to "
                    "the number of documents removed (0 or 1)."
                ),
            },
            {
                "title": "Remove inside a Meteor method",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'tasks.delete'(taskId) {\n"
                    "    const task = await Tasks.findOneAsync(taskId);\n"
                    "    if (!task) {\n"
                    "      throw new Meteor.Error('not-found', 'Task not found');\n"
                    "    }\n"
                    "    if (task.owner !== this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "    return Tasks.removeAsync(taskId);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "A Meteor method that checks ownership before deleting "
                    "a task document."
                ),
            },
        ],
        "tags": ["collection", "mongo", "remove", "delete", "write", "async"],
    },
    # -------------------------------------------------------------------------
    # Collection.rawCollection
    # -------------------------------------------------------------------------
    {
        "name": "Collection.rawCollection",
        "module": "collections",
        "signature": "collection.rawCollection()",
        "description": (
            "Returns the underlying Node.js MongoDB driver Collection "
            "object for this Meteor collection. This gives you direct "
            "access to the full MongoDB Node.js driver API, including "
            "operations not exposed by Meteor such as aggregation "
            "pipelines, bulk writes, and advanced index management. "
            "Available on the server only."
        ),
        "params": [],
        "returns": "MongoDB.Collection (Node.js driver Collection object)",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Run an aggregation pipeline",
                "code": (
                    "const raw = Orders.rawCollection();\n\n"
                    "const pipeline = [\n"
                    "  { $match: { status: 'completed' } },\n"
                    "  { $group: {\n"
                    "    _id: '$customerId',\n"
                    "    totalSpent: { $sum: '$amount' },\n"
                    "    orderCount: { $sum: 1 },\n"
                    "  }},\n"
                    "  { $sort: { totalSpent: -1 } },\n"
                    "  { $limit: 10 },\n"
                    "];\n\n"
                    "const topCustomers = await raw.aggregate(pipeline).toArray();"
                ),
                "description": (
                    "Uses the native MongoDB aggregation pipeline to "
                    "calculate the top 10 customers by total spending."
                ),
            },
            {
                "title": "Perform a bulk write",
                "code": (
                    "const raw = Logs.rawCollection();\n\n"
                    "const operations = entries.map((entry) => ({\n"
                    "  insertOne: { document: entry },\n"
                    "}));\n\n"
                    "const result = await raw.bulkWrite(operations, {\n"
                    "  ordered: false,\n"
                    "});\n\n"
                    "console.log(`Inserted ${result.insertedCount} log entries`);"
                ),
                "description": (
                    "Bulk inserts log entries using the native MongoDB driver "
                    "for better performance with large batches."
                ),
            },
        ],
        "tags": ["collection", "mongo", "raw", "server", "driver", "aggregation"],
    },
    # -------------------------------------------------------------------------
    # Collection.rawDatabase
    # -------------------------------------------------------------------------
    {
        "name": "Collection.rawDatabase",
        "module": "collections",
        "signature": "collection.rawDatabase()",
        "description": (
            "Returns the underlying Node.js MongoDB driver Db object, giving "
            "direct access to the full database-level API including admin "
            "commands, collection listing, and database management operations. "
            "Available on the server only."
        ),
        "params": [],
        "returns": "MongoDB.Db (Node.js driver Db object)",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "List all collections in the database",
                "code": (
                    "const db = Tasks.rawDatabase();\n\n"
                    "const collections = await db.listCollections().toArray();\n"
                    "collections.forEach((col) => {\n"
                    "  console.log(col.name);\n"
                    "});"
                ),
                "description": (
                    "Gets the Db object to list all collections in the "
                    "underlying MongoDB database."
                ),
            },
            {
                "title": "Run an admin command",
                "code": (
                    "const db = Tasks.rawDatabase();\n\n"
                    "const stats = await db.stats();\n"
                    "console.log('Database size:', stats.dataSize);"
                ),
                "description": (
                    "Uses the Db object to retrieve database-level statistics "
                    "such as total data size."
                ),
            },
        ],
        "tags": ["collection", "mongo", "raw", "server", "driver", "database"],
    },
    # -------------------------------------------------------------------------
    # Collection.createIndex (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Collection.createIndex",
        "module": "collections",
        "signature": "collection.createIndex(index, options)",
        "description": (
            "Synchronously creates an index on the collection. This method "
            "is deprecated in Meteor v3; use `createIndexAsync` instead. "
            "Available on the server only. Indexes improve query performance "
            "by allowing MongoDB to efficiently locate documents."
        ),
        "params": [
            {
                "name": "index",
                "type": "Object",
                "optional": False,
                "description": (
                    "A document specifying the index fields and their sort "
                    "order: 1 for ascending, -1 for descending. "
                    "Example: { email: 1 } or { location: '2dsphere' }."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options passed directly to the MongoDB createIndex "
                    "command: `unique` (Boolean), `sparse` (Boolean), "
                    "`name` (String), `expireAfterSeconds` (Number) for "
                    "TTL indexes, etc."
                ),
            },
        ],
        "returns": "undefined",
        "environment": "server",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Create an index (deprecated)",
                "code": (
                    "// Deprecated -- use createIndexAsync instead\n"
                    "Tasks.createIndex({ owner: 1, createdAt: -1 });"
                ),
                "description": (
                    "Creates a compound index on owner (ascending) and "
                    "createdAt (descending). Deprecated in favor of "
                    "createIndexAsync."
                ),
            },
        ],
        "tags": ["collection", "mongo", "index", "server", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Collection.createIndexAsync
    # -------------------------------------------------------------------------
    {
        "name": "Collection.createIndexAsync",
        "module": "collections",
        "signature": "collection.createIndexAsync(index, options)",
        "description": (
            "Asynchronously creates an index on the collection. Returns a "
            "Promise that resolves when the index has been created. "
            "Available on the server only. Typically called during server "
            "startup to ensure indexes exist. This is the async-first "
            "replacement for the deprecated `createIndex` in Meteor v3."
        ),
        "params": [
            {
                "name": "index",
                "type": "Object",
                "optional": False,
                "description": (
                    "A document specifying the index fields and their sort "
                    "order: 1 for ascending, -1 for descending. "
                    "Example: { email: 1 } or { location: '2dsphere' }."
                ),
            },
            {
                "name": "options",
                "type": "Object",
                "optional": True,
                "description": (
                    "Options passed directly to the MongoDB createIndex "
                    "command: `unique` (Boolean), `sparse` (Boolean), "
                    "`name` (String), `expireAfterSeconds` (Number) for "
                    "TTL indexes, etc."
                ),
            },
        ],
        "returns": "Promise<undefined>",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Create a compound index at startup",
                "code": (
                    "Meteor.startup(async () => {\n"
                    "  await Tasks.createIndexAsync({ owner: 1, createdAt: -1 });\n"
                    "  await Tasks.createIndexAsync({ status: 1 });\n"
                    "});"
                ),
                "description": (
                    "Creates indexes when the server starts up. Each call "
                    "is a no-op if the index already exists."
                ),
            },
            {
                "title": "Create a unique index",
                "code": (
                    "await Invitations.createIndexAsync(\n"
                    "  { email: 1 },\n"
                    "  { unique: true }\n"
                    ");"
                ),
                "description": (
                    "Creates a unique index on the email field, preventing "
                    "duplicate invitation entries."
                ),
            },
            {
                "title": "Create a TTL index for auto-expiring documents",
                "code": (
                    "await Sessions.createIndexAsync(\n"
                    "  { createdAt: 1 },\n"
                    "  { expireAfterSeconds: 3600 }\n"
                    ");"
                ),
                "description": (
                    "Creates a TTL index that causes MongoDB to "
                    "automatically remove session documents one hour after "
                    "their createdAt timestamp."
                ),
            },
        ],
        "tags": ["collection", "mongo", "index", "server", "async"],
    },
    # -------------------------------------------------------------------------
    # Cursor.fetch (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.fetch",
        "module": "collections",
        "signature": "cursor.fetch()",
        "description": (
            "Synchronously returns all matching documents as an Array. This "
            "method is deprecated in Meteor v3; use `fetchAsync` instead. "
            "The cursor is fully consumed and cannot be iterated again."
        ),
        "params": [],
        "returns": "Array<Object>",
        "environment": "client",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Fetch all documents (deprecated)",
                "code": (
                    "// Deprecated -- use fetchAsync instead\n"
                    "const tasks = Tasks.find({ status: 'active' }).fetch();"
                ),
                "description": (
                    "Synchronously returns an array of all active task "
                    "documents. Deprecated in favor of fetchAsync."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "fetch", "query", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Cursor.fetchAsync
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.fetchAsync",
        "module": "collections",
        "signature": "cursor.fetchAsync()",
        "description": (
            "Asynchronously returns all matching documents as an Array. "
            "Returns a Promise that resolves to an Array of documents. This "
            "is the async-first replacement for the deprecated `fetch` "
            "method in Meteor v3."
        ),
        "params": [],
        "returns": "Promise<Array<Object>>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Fetch all matching documents",
                "code": (
                    "const activeTasks = await Tasks.find(\n"
                    "  { status: 'active' },\n"
                    "  { sort: { createdAt: -1 } }\n"
                    ").fetchAsync();\n\n"
                    "console.log(`Found ${activeTasks.length} active tasks`);"
                ),
                "description": (
                    "Fetches all active tasks sorted by creation date and "
                    "returns them as an array."
                ),
            },
            {
                "title": "Fetch inside a Meteor method",
                "code": (
                    "Meteor.methods({\n"
                    "  async 'tasks.listForUser'(userId) {\n"
                    "    check(userId, String);\n"
                    "    return Tasks.find(\n"
                    "      { owner: userId },\n"
                    "      { fields: { title: 1, status: 1 }, limit: 100 }\n"
                    "    ).fetchAsync();\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Returns up to 100 tasks for the specified user with "
                    "only the title and status fields."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "fetch", "query", "async"],
    },
    # -------------------------------------------------------------------------
    # Cursor.forEach (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.forEach",
        "module": "collections",
        "signature": "cursor.forEach(callback, thisArg)",
        "description": (
            "Synchronously calls the callback function once for each "
            "matching document. This method is deprecated in Meteor v3; "
            "use `forEachAsync` instead."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "optional": False,
                "description": (
                    "Function to call for each document. Receives the "
                    "document as the first argument, the index as the "
                    "second, and the cursor as the third."
                ),
            },
            {
                "name": "thisArg",
                "type": "Any",
                "optional": True,
                "description": "Value to use as `this` when executing callback.",
            },
        ],
        "returns": "undefined",
        "environment": "client",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Iterate over documents (deprecated)",
                "code": (
                    "// Deprecated -- use forEachAsync instead\n"
                    "Tasks.find({ status: 'active' }).forEach((task) => {\n"
                    "  console.log(task.title);\n"
                    "});"
                ),
                "description": (
                    "Synchronously iterates over matching documents. "
                    "Deprecated in favor of forEachAsync."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "iterate", "forEach", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Cursor.forEachAsync
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.forEachAsync",
        "module": "collections",
        "signature": "cursor.forEachAsync(callback, thisArg)",
        "description": (
            "Asynchronously calls the callback function once for each "
            "matching document. The callback may be an async function. "
            "Returns a Promise that resolves when all documents have been "
            "processed. This is the async-first replacement for the "
            "deprecated `forEach` in Meteor v3."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "optional": False,
                "description": (
                    "Function to call for each document. Receives the "
                    "document as the first argument, the index as the "
                    "second, and the cursor as the third. May be async."
                ),
            },
            {
                "name": "thisArg",
                "type": "Any",
                "optional": True,
                "description": "Value to use as `this` when executing callback.",
            },
        ],
        "returns": "Promise<undefined>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Iterate with an async callback",
                "code": (
                    "await Tasks.find({ status: 'overdue' }).forEachAsync(\n"
                    "  async (task) => {\n"
                    "    await sendReminderEmail(task.owner, task.title);\n"
                    "    await Tasks.updateAsync(task._id, {\n"
                    "      $set: { reminderSent: true },\n"
                    "    });\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Iterates over all overdue tasks, sends a reminder "
                    "email for each one, and marks it as reminded."
                ),
            },
            {
                "title": "Simple iteration over documents",
                "code": (
                    "await Tasks.find().forEachAsync((task, index) => {\n"
                    "  console.log(`${index + 1}. ${task.title}`);\n"
                    "});"
                ),
                "description": (
                    "Iterates over all tasks and logs each title with its "
                    "position number."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "iterate", "forEach", "async"],
    },
    # -------------------------------------------------------------------------
    # Cursor.map (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.map",
        "module": "collections",
        "signature": "cursor.map(callback, thisArg)",
        "description": (
            "Synchronously maps each matching document through the callback "
            "and returns an Array of the results. This method is deprecated "
            "in Meteor v3; use `mapAsync` instead."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "optional": False,
                "description": (
                    "Function called for each document. Receives the "
                    "document as the first argument, the index as the "
                    "second, and the cursor as the third. The return value "
                    "is collected into the result array."
                ),
            },
            {
                "name": "thisArg",
                "type": "Any",
                "optional": True,
                "description": "Value to use as `this` when executing callback.",
            },
        ],
        "returns": "Array",
        "environment": "client",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Map documents to titles (deprecated)",
                "code": (
                    "// Deprecated -- use mapAsync instead\n"
                    "const titles = Tasks.find().map((task) => task.title);"
                ),
                "description": (
                    "Synchronously maps each task document to its title. "
                    "Deprecated in favor of mapAsync."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "map", "transform", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Cursor.mapAsync
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.mapAsync",
        "module": "collections",
        "signature": "cursor.mapAsync(callback, thisArg)",
        "description": (
            "Asynchronously maps each matching document through the callback "
            "and returns a Promise that resolves to an Array of the results. "
            "The callback may be an async function. This is the async-first "
            "replacement for the deprecated `map` in Meteor v3."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "optional": False,
                "description": (
                    "Function called for each document. Receives the "
                    "document as the first argument, the index as the "
                    "second, and the cursor as the third. The return value "
                    "(or resolved Promise) is collected into the result "
                    "array. May be async."
                ),
            },
            {
                "name": "thisArg",
                "type": "Any",
                "optional": True,
                "description": "Value to use as `this` when executing callback.",
            },
        ],
        "returns": "Promise<Array>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Map documents to a derived structure",
                "code": (
                    "const taskSummaries = await Tasks.find(\n"
                    "  { status: 'active' }\n"
                    ").mapAsync((task) => ({\n"
                    "  id: task._id,\n"
                    "  title: task.title,\n"
                    "  overdue: task.dueDate < new Date(),\n"
                    "}));"
                ),
                "description": (
                    "Transforms each active task into a summary object "
                    "containing only the id, title, and overdue status."
                ),
            },
            {
                "title": "Map with an async callback",
                "code": (
                    "const enrichedTasks = await Tasks.find().mapAsync(\n"
                    "  async (task) => {\n"
                    "    const owner = await Meteor.users.findOneAsync(task.owner);\n"
                    "    return {\n"
                    "      ...task,\n"
                    "      ownerName: owner?.profile?.name ?? 'Unknown',\n"
                    "    };\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Enriches each task document with the owner's display "
                    "name by performing an async lookup."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "map", "transform", "async"],
    },
    # -------------------------------------------------------------------------
    # Cursor.count (deprecated)
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.count",
        "module": "collections",
        "signature": "cursor.count()",
        "description": (
            "Synchronously returns the number of documents that match the "
            "cursor's selector. This method is deprecated in Meteor v3; "
            "use `countAsync` instead. On the client inside a reactive "
            "computation this method is reactive."
        ),
        "params": [],
        "returns": "Number",
        "environment": "client",
        "is_reactive": True,
        "deprecated": True,
        "examples": [
            {
                "title": "Count matching documents (deprecated)",
                "code": (
                    "// Deprecated -- use countAsync instead\n"
                    "const count = Tasks.find({ status: 'active' }).count();"
                ),
                "description": (
                    "Synchronously returns the number of active tasks. "
                    "Deprecated in favor of countAsync."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "count", "query", "deprecated", "sync"],
    },
    # -------------------------------------------------------------------------
    # Cursor.countAsync
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.countAsync",
        "module": "collections",
        "signature": "cursor.countAsync()",
        "description": (
            "Asynchronously returns the number of documents that match the "
            "cursor's selector. Returns a Promise that resolves to a Number. "
            "This is the async-first replacement for the deprecated `count` "
            "in Meteor v3."
        ),
        "params": [],
        "returns": "Promise<Number>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Count active tasks",
                "code": (
                    "const activeCount = await Tasks.find(\n"
                    "  { status: 'active' }\n"
                    ").countAsync();\n\n"
                    "console.log(`There are ${activeCount} active tasks`);"
                ),
                "description": (
                    "Asynchronously counts all tasks with an active status."
                ),
            },
            {
                "title": "Check if any documents exist",
                "code": (
                    "const hasOverdue = (await Tasks.find(\n"
                    "  { status: 'overdue' }\n"
                    ").countAsync()) > 0;\n\n"
                    "if (hasOverdue) {\n"
                    "  console.log('There are overdue tasks!');\n"
                    "}"
                ),
                "description": (
                    "Uses countAsync to check whether any overdue tasks "
                    "exist in the collection."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "count", "query", "async"],
    },
    # -------------------------------------------------------------------------
    # Cursor.observe
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.observe",
        "module": "collections",
        "signature": "cursor.observe(callbacks)",
        "description": (
            "Observes a cursor and calls the provided callback functions "
            "when documents are added, changed, or removed from the result "
            "set. Returns a live query handle with a `stop()` method that "
            "must be called to clean up the observation. The callbacks "
            "receive full document objects. Available on the client. The "
            "initial result set is delivered synchronously through `added` "
            "callbacks before observe returns."
        ),
        "params": [
            {
                "name": "callbacks",
                "type": "Object",
                "optional": False,
                "description": (
                    "An object with callback functions: "
                    "`added(document)` - called when a new document enters "
                    "the result set; "
                    "`addedAt(document, atIndex, before)` - like added but "
                    "includes position information; "
                    "`changed(newDocument, oldDocument)` - called when a "
                    "document in the result set is modified; "
                    "`changedAt(newDocument, oldDocument, atIndex)` - like "
                    "changed but includes position; "
                    "`removed(oldDocument)` - called when a document leaves "
                    "the result set; "
                    "`removedAt(oldDocument, atIndex)` - like removed but "
                    "includes position; "
                    "`movedTo(document, fromIndex, toIndex, before)` - "
                    "called when a document changes position in the sorted "
                    "result set."
                ),
            },
        ],
        "returns": "LiveQueryHandle (object with stop() method)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Observe additions and removals",
                "code": (
                    "const handle = Tasks.find({ status: 'active' }).observe({\n"
                    "  added(task) {\n"
                    "    console.log('New task:', task.title);\n"
                    "  },\n"
                    "  changed(newTask, oldTask) {\n"
                    "    console.log(`Task updated: ${oldTask.title} -> ${newTask.title}`);\n"
                    "  },\n"
                    "  removed(task) {\n"
                    "    console.log('Task removed:', task.title);\n"
                    "  },\n"
                    "});\n\n"
                    "// Later: stop observing\n"
                    "handle.stop();"
                ),
                "description": (
                    "Sets up callbacks for when active tasks are added, "
                    "changed, or removed. The returned handle must be "
                    "stopped when observation is no longer needed to avoid "
                    "memory leaks."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "observe", "reactive", "live-query", "client"],
    },
    # -------------------------------------------------------------------------
    # Cursor.observeChanges
    # -------------------------------------------------------------------------
    {
        "name": "Cursor.observeChanges",
        "module": "collections",
        "signature": "cursor.observeChanges(callbacks)",
        "description": (
            "Observes a cursor and calls callback functions when documents "
            "are added, changed, or removed from the result set. Unlike "
            "`observe`, the `changed` callback receives only the fields "
            "that changed rather than the entire document, making it more "
            "efficient for large documents. Returns a live query handle "
            "with a `stop()` method. Available on the client."
        ),
        "params": [
            {
                "name": "callbacks",
                "type": "Object",
                "optional": False,
                "description": (
                    "An object with callback functions: "
                    "`added(id, fields)` - called when a new document enters "
                    "the result set, receives the _id and all fields; "
                    "`addedBefore(id, fields, before)` - like added but "
                    "includes the _id of the next document in sort order; "
                    "`changed(id, fields)` - called when a document is "
                    "modified, receives only the changed fields; "
                    "`movedBefore(id, before)` - called when a document "
                    "changes position; "
                    "`removed(id)` - called when a document leaves the "
                    "result set, receives only the _id."
                ),
            },
        ],
        "returns": "LiveQueryHandle (object with stop() method)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Observe changes efficiently",
                "code": (
                    "const handle = Messages.find(\n"
                    "  { chatId },\n"
                    "  { sort: { createdAt: 1 } }\n"
                    ").observeChanges({\n"
                    "  added(id, fields) {\n"
                    "    appendMessageToUI(id, fields);\n"
                    "  },\n"
                    "  changed(id, fields) {\n"
                    "    updateMessageInUI(id, fields);\n"
                    "  },\n"
                    "  removed(id) {\n"
                    "    removeMessageFromUI(id);\n"
                    "  },\n"
                    "});\n\n"
                    "// Clean up when leaving the chat\n"
                    "handle.stop();"
                ),
                "description": (
                    "Watches for changes to messages in a chat room. The "
                    "changed callback only receives the fields that were "
                    "modified, which is more efficient than observe when "
                    "documents are large."
                ),
            },
            {
                "title": "Track document count without fetching data",
                "code": (
                    "let count = 0;\n\n"
                    "const handle = Notifications.find(\n"
                    "  { userId: Meteor.userId(), read: false }\n"
                    ").observeChanges({\n"
                    "  added() {\n"
                    "    count += 1;\n"
                    "    updateBadge(count);\n"
                    "  },\n"
                    "  removed() {\n"
                    "    count -= 1;\n"
                    "    updateBadge(count);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Efficiently tracks the number of unread notifications "
                    "without needing to process full document data."
                ),
            },
        ],
        "tags": ["cursor", "mongo", "observe", "reactive", "live-query", "client", "efficient"],
    },
    # -------------------------------------------------------------------------
    # Mongo.ObjectID
    # -------------------------------------------------------------------------
    {
        "name": "Mongo.ObjectID",
        "module": "collections",
        "signature": "new Mongo.ObjectID(hexString)",
        "description": (
            "Creates a Mongo-style ObjectID value. If called without "
            "arguments, generates a new unique ObjectID. If called with a "
            "24-character hex string, wraps that string as an ObjectID. "
            "By default Meteor uses random strings for document _id fields, "
            "but you can configure a collection to use MongoDB ObjectIDs "
            "by passing `{ idGeneration: 'MONGO' }` to the Collection "
            "constructor."
        ),
        "params": [
            {
                "name": "hexString",
                "type": "String",
                "optional": True,
                "description": (
                    "A 24-character hexadecimal string representing an "
                    "existing ObjectID. If omitted, a new unique ObjectID "
                    "is generated."
                ),
            },
        ],
        "returns": "Mongo.ObjectID",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Generate a new ObjectID",
                "code": (
                    "import { Mongo } from 'meteor/mongo';\n\n"
                    "const id = new Mongo.ObjectID();\n"
                    "console.log(id.toHexString()); // 24-char hex string"
                ),
                "description": (
                    "Generates a new unique ObjectID and prints its hex "
                    "string representation."
                ),
            },
            {
                "title": "Wrap an existing hex string",
                "code": (
                    "import { Mongo } from 'meteor/mongo';\n\n"
                    "const id = new Mongo.ObjectID('507f1f77bcf86cd799439011');\n"
                    "console.log(id.toHexString()); // '507f1f77bcf86cd799439011'"
                ),
                "description": (
                    "Wraps an existing 24-character hex string as a "
                    "Mongo.ObjectID instance."
                ),
            },
            {
                "title": "Collection with MONGO id generation",
                "code": (
                    "import { Mongo } from 'meteor/mongo';\n\n"
                    "const LegacyData = new Mongo.Collection('legacyData', {\n"
                    "  idGeneration: 'MONGO',\n"
                    "});\n\n"
                    "// Documents in this collection use ObjectIDs instead\n"
                    "// of random strings for their _id field\n"
                    "const docId = await LegacyData.insertAsync({ value: 42 });\n"
                    "console.log(docId instanceof Mongo.ObjectID); // true"
                ),
                "description": (
                    "When a collection uses MONGO id generation, inserted "
                    "documents receive ObjectID values instead of the "
                    "default random strings."
                ),
            },
        ],
        "tags": ["mongo", "objectid", "id", "identifier"],
    },
]
