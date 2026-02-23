"""Meteor.js v3.4.0 code examples organized by topic.

Provides the EXAMPLES dictionary mapping topic strings to collections of
annotated code snippets covering methods, publications, collections, accounts,
authentication, security, reactive programming, routing, testing, deployment,
REST APIs, file structure, schema validation, email, and environment config.
"""

EXAMPLES = {
    "methods": {
        "title": "Meteor Methods",
        "intro": (
            "Methods are Meteor's RPC system for secure server-side operations. "
            "In Meteor v3, methods should be async functions that use await for "
            "all database operations and other asynchronous work."
        ),
        "snippets": [
            {
                "title": "Define an async method",
                "code": (
                    "// server/methods.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check } from 'meteor/check';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async 'tasks.insert'(text) {\n"
                    "    check(text, String);\n"
                    "\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized',\n"
                    "        'You must be logged in to create a task.');\n"
                    "    }\n"
                    "\n"
                    "    const taskId = await TasksCollection.insertAsync({\n"
                    "      text,\n"
                    "      createdAt: new Date(),\n"
                    "      userId: this.userId,\n"
                    "    });\n"
                    "\n"
                    "    return taskId;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Methods in Meteor v3 should be async and use await for all "
                    "collection operations. The method context (this) provides "
                    "userId, connection, isSimulation, and unblock."
                ),
            },
            {
                "title": "Call a method from the client with callAsync",
                "code": (
                    "// client/taskForm.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "async function handleSubmit(text) {\n"
                    "  try {\n"
                    "    const taskId = await Meteor.callAsync('tasks.insert', text);\n"
                    "    console.log('Task created with id:', taskId);\n"
                    "  } catch (error) {\n"
                    "    console.error('Failed to create task:', error.reason);\n"
                    "  }\n"
                    "}"
                ),
                "description": (
                    "Meteor.callAsync is the v3 replacement for Meteor.call. It "
                    "returns a Promise that resolves with the method's return value "
                    "or rejects with a Meteor.Error."
                ),
            },
            {
                "title": "Method with optimistic UI (client stub)",
                "code": (
                    "// imports/api/tasks/methods.js (shared code)\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check } from 'meteor/check';\n"
                    "import { TasksCollection } from './collection';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async 'tasks.setChecked'(taskId, isChecked) {\n"
                    "    check(taskId, String);\n"
                    "    check(isChecked, Boolean);\n"
                    "\n"
                    "    const task = await TasksCollection.findOneAsync(taskId);\n"
                    "    if (!task) {\n"
                    "      throw new Meteor.Error('not-found', 'Task not found.');\n"
                    "    }\n"
                    "\n"
                    "    if (task.userId !== this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized',\n"
                    "        'You can only update your own tasks.');\n"
                    "    }\n"
                    "\n"
                    "    await TasksCollection.updateAsync(taskId, {\n"
                    "      $set: { isChecked },\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "When a method file is imported on both client and server, the "
                    "client runs the method body as a stub for instant UI feedback. "
                    "The server result replaces the stub's changes if they differ."
                ),
            },
        ],
    },
    "publications": {
        "title": "Publications and Subscriptions",
        "intro": (
            "Publications define what data the server sends to clients via DDP. "
            "Clients subscribe to publications and receive reactive updates. "
            "In Meteor v3, publish functions can be async for setup logic, but "
            "must return a cursor (or array of cursors) for reactive data."
        ),
        "snippets": [
            {
                "title": "Publish a filtered dataset",
                "code": (
                    "// server/publications.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check } from 'meteor/check';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "Meteor.publish('tasks.mine', function () {\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "\n"
                    "  return TasksCollection.find(\n"
                    "    { userId: this.userId },\n"
                    "    { fields: { text: 1, isChecked: 1, createdAt: 1 } }\n"
                    "  );\n"
                    "});\n"
                    "\n"
                    "Meteor.publish('tasks.byProject', function (projectId) {\n"
                    "  check(projectId, String);\n"
                    "\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "\n"
                    "  return TasksCollection.find(\n"
                    "    { projectId, userId: this.userId },\n"
                    "    { sort: { createdAt: -1 }, limit: 50 }\n"
                    "  );\n"
                    "});"
                ),
                "description": (
                    "Publish functions use 'function' syntax (not arrows) to access "
                    "this.userId. Return this.ready() for unauthenticated users to "
                    "signal that the subscription is complete with no data."
                ),
            },
            {
                "title": "Subscribe from a React component",
                "code": (
                    "// imports/ui/TaskList.jsx\n"
                    "import React from 'react';\n"
                    "import { useSubscribe, useFind } from 'meteor/react-meteor-data';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "export function TaskList() {\n"
                    "  const isLoading = useSubscribe('tasks.mine');\n"
                    "  const tasks = useFind(() =>\n"
                    "    TasksCollection.find({}, { sort: { createdAt: -1 } })\n"
                    "  );\n"
                    "\n"
                    "  if (isLoading()) {\n"
                    "    return <div>Loading tasks...</div>;\n"
                    "  }\n"
                    "\n"
                    "  return (\n"
                    "    <ul>\n"
                    "      {tasks.map(task => (\n"
                    "        <li key={task._id}>{task.text}</li>\n"
                    "      ))}\n"
                    "    </ul>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "The react-meteor-data package provides useSubscribe and useFind "
                    "hooks for Meteor v3. useSubscribe returns a reactive loading "
                    "function, and useFind reactively tracks cursor results."
                ),
            },
            {
                "title": "Publish multiple cursors from one publication",
                "code": (
                    "// server/publications.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "import { ProjectsCollection } from '/imports/api/projects';\n"
                    "\n"
                    "Meteor.publish('dashboard.data', function () {\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "\n"
                    "  return [\n"
                    "    TasksCollection.find(\n"
                    "      { userId: this.userId },\n"
                    "      { limit: 20, sort: { createdAt: -1 } }\n"
                    "    ),\n"
                    "    ProjectsCollection.find(\n"
                    "      { members: this.userId },\n"
                    "      { fields: { name: 1, status: 1 } }\n"
                    "    ),\n"
                    "  ];\n"
                    "});"
                ),
                "description": (
                    "A publish function can return an array of cursors. Each cursor "
                    "must come from a different collection. The client receives "
                    "reactive updates for all cursors as a single subscription."
                ),
            },
        ],
    },
    "collections": {
        "title": "Collections (CRUD Operations)",
        "intro": (
            "Mongo.Collection is the primary data layer in Meteor. In v3, all "
            "mutation and query operations that touch the database are async and "
            "end with the Async suffix (insertAsync, updateAsync, removeAsync, "
            "findOneAsync, etc.). Cursor methods like fetch, count, and forEach "
            "also have async variants."
        ),
        "snippets": [
            {
                "title": "Define a collection and perform CRUD",
                "code": (
                    "// imports/api/tasks/collection.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { Mongo } from 'meteor/mongo';\n"
                    "\n"
                    "export const TasksCollection = new Mongo.Collection('tasks');\n"
                    "\n"
                    "// --- CRUD operations (server-side) ---\n"
                    "\n"
                    "// Create\n"
                    "const taskId = await TasksCollection.insertAsync({\n"
                    "  text: 'Buy groceries',\n"
                    "  isChecked: false,\n"
                    "  createdAt: new Date(),\n"
                    "  userId: Meteor.userId(),\n"
                    "});\n"
                    "\n"
                    "// Read\n"
                    "const task = await TasksCollection.findOneAsync(taskId);\n"
                    "const allTasks = await TasksCollection.find({}).fetchAsync();\n"
                    "const count = await TasksCollection.find({}).countAsync();\n"
                    "\n"
                    "// Update\n"
                    "await TasksCollection.updateAsync(taskId, {\n"
                    "  $set: { isChecked: true },\n"
                    "});\n"
                    "\n"
                    "// Upsert\n"
                    "await TasksCollection.upsertAsync(\n"
                    "  { externalId: 'abc-123' },\n"
                    "  { $set: { text: 'Updated task', updatedAt: new Date() } }\n"
                    ");\n"
                    "\n"
                    "// Delete\n"
                    "await TasksCollection.removeAsync(taskId);"
                ),
                "description": (
                    "All write operations in Meteor v3 use the Async suffix. "
                    "The synchronous versions (insert, update, remove) are removed. "
                    "Cursor methods like fetch() become fetchAsync()."
                ),
            },
            {
                "title": "Query with selectors and options",
                "code": (
                    "// Complex queries with MongoDB selectors\n"
                    "const recentTasks = await TasksCollection.find(\n"
                    "  {\n"
                    "    createdAt: { $gte: new Date('2025-01-01') },\n"
                    "    isChecked: false,\n"
                    "    $or: [\n"
                    "      { priority: 'high' },\n"
                    "      { dueDate: { $lte: new Date() } },\n"
                    "    ],\n"
                    "  },\n"
                    "  {\n"
                    "    sort: { createdAt: -1 },\n"
                    "    limit: 20,\n"
                    "    fields: { text: 1, priority: 1, dueDate: 1 },\n"
                    "  }\n"
                    ").fetchAsync();\n"
                    "\n"
                    "// Iterate with forEachAsync\n"
                    "await TasksCollection.find({ isChecked: true }).forEachAsync(\n"
                    "  async (task) => {\n"
                    "    console.log(`Completed: ${task.text}`);\n"
                    "    await ArchiveCollection.insertAsync({\n"
                    "      ...task,\n"
                    "      archivedAt: new Date(),\n"
                    "    });\n"
                    "  }\n"
                    ");\n"
                    "\n"
                    "// Map with mapAsync\n"
                    "const titles = await TasksCollection.find({}).mapAsync(\n"
                    "  (task) => task.text\n"
                    ");"
                ),
                "description": (
                    "Meteor supports standard MongoDB query selectors. Cursor iteration "
                    "methods (forEach, map) have async variants in v3 that must be "
                    "awaited on the server."
                ),
            },
            {
                "title": "Collection hooks and transforms",
                "code": (
                    "// imports/api/tasks/collection.js\n"
                    "import { Mongo } from 'meteor/mongo';\n"
                    "\n"
                    "export const TasksCollection = new Mongo.Collection('tasks', {\n"
                    "  transform(doc) {\n"
                    "    doc.isOverdue = doc.dueDate && doc.dueDate < new Date();\n"
                    "    doc.displayName = `${doc.text} (${doc.priority || 'normal'})`;\n"
                    "    return doc;\n"
                    "  },\n"
                    "});\n"
                    "\n"
                    "// The transform is applied to documents returned by find/findOne\n"
                    "const task = await TasksCollection.findOneAsync(taskId);\n"
                    "console.log(task.isOverdue);    // true or false\n"
                    "console.log(task.displayName);  // 'Buy groceries (high)'"
                ),
                "description": (
                    "The transform option lets you attach computed properties to "
                    "documents. The transform runs on every document returned by "
                    "find and findOne. You can bypass it with transform: null in "
                    "query options."
                ),
            },
        ],
    },
    "accounts": {
        "title": "Accounts and User Management",
        "intro": (
            "Meteor's accounts system provides a complete user management solution "
            "including password authentication, OAuth integration, and email "
            "verification. In v3, account operations like createUser and "
            "setPassword have async variants."
        ),
        "snippets": [
            {
                "title": "Create users and manage passwords",
                "code": (
                    "// server/accounts.js\n"
                    "import { Accounts } from 'meteor/accounts-base';\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "// Create a user on the server\n"
                    "Meteor.startup(async () => {\n"
                    "  const existingUser = await Accounts.findUserByUsernameAsync('admin');\n"
                    "  if (!existingUser) {\n"
                    "    await Accounts.createUserAsync({\n"
                    "      username: 'admin',\n"
                    "      email: 'admin@example.com',\n"
                    "      password: 'secure-password',\n"
                    "      profile: { name: 'Admin User', role: 'admin' },\n"
                    "    });\n"
                    "  }\n"
                    "});\n"
                    "\n"
                    "// Admin helper: set password for a user by ID\n"
                    "async function resetUserPassword(userId) {\n"
                    "  await Accounts.setPasswordAsync(userId, 'new-password');\n"
                    "  await Accounts.sendEnrollmentEmail(userId);\n"
                    "  await Accounts.sendResetPasswordEmail(userId);\n"
                    "}"
                ),
                "description": (
                    "Accounts.createUserAsync is the v3 async replacement for "
                    "createUser. Use findUserByUsernameAsync or findUserByEmailAsync "
                    "to check for existing users before creation."
                ),
            },
            {
                "title": "Client-side registration and login",
                "code": (
                    "// client/auth.js\n"
                    "import { Accounts } from 'meteor/accounts-base';\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "// Register a new user from the client\n"
                    "async function register(email, password, name) {\n"
                    "  try {\n"
                    "    await Accounts.createUserAsync({\n"
                    "      email,\n"
                    "      password,\n"
                    "      profile: { name },\n"
                    "    });\n"
                    "    // User is automatically logged in after creation\n"
                    "    console.log('Registered and logged in as:', Meteor.userId());\n"
                    "  } catch (error) {\n"
                    "    console.error('Registration failed:', error.reason);\n"
                    "  }\n"
                    "}\n"
                    "\n"
                    "// Log in with password\n"
                    "async function login(email, password) {\n"
                    "  try {\n"
                    "    await Meteor.loginWithPassword(email, password);\n"
                    "    console.log('Logged in as:', Meteor.userId());\n"
                    "  } catch (error) {\n"
                    "    console.error('Login failed:', error.reason);\n"
                    "  }\n"
                    "}\n"
                    "\n"
                    "// Log out\n"
                    "async function logout() {\n"
                    "  await Meteor.logout();\n"
                    "  console.log('Logged out');\n"
                    "}"
                ),
                "description": (
                    "Client-side auth operations in Meteor v3 return Promises: "
                    "Meteor.loginWithPassword, Meteor.logout, and "
                    "Accounts.createUserAsync all support await. These keep their "
                    "original names but no longer require callbacks."
                ),
            },
            {
                "title": "Email verification and account hooks",
                "code": (
                    "// server/accounts.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { Accounts } from 'meteor/accounts-base';\n"
                    "\n"
                    "// Customize email verification template\n"
                    "Accounts.emailTemplates.siteName = 'My Meteor App';\n"
                    "Accounts.emailTemplates.from = 'My App <no-reply@myapp.com>';\n"
                    "\n"
                    "Accounts.emailTemplates.verifyEmail = {\n"
                    "  subject() {\n"
                    "    return 'Verify your email address';\n"
                    "  },\n"
                    "  text(user, url) {\n"
                    "    return `Hello ${user.profile.name},\\n\\n`\n"
                    "      + `Please verify your email by clicking: ${url}\\n\\n`\n"
                    "      + 'Thanks,\\nThe Team';\n"
                    "  },\n"
                    "};\n"
                    "\n"
                    "// Run logic on new user creation (register only once)\n"
                    "Accounts.onCreateUser((options, user) => {\n"
                    "  user.profile = options.profile || {};\n"
                    "  user.createdAt = new Date();\n"
                    "  user.roles = ['member'];\n"
                    "\n"
                    "  // Queue verification email after user is saved\n"
                    "  Meteor.defer(() => {\n"
                    "    Accounts.sendVerificationEmail(user._id);\n"
                    "  });\n"
                    "\n"
                    "  return user;\n"
                    "});\n"
                    "\n"
                    "// Validate new user creation\n"
                    "Accounts.validateNewUser((user) => {\n"
                    "  if (!user.emails || user.emails.length === 0) {\n"
                    "    throw new Meteor.Error('email-required',\n"
                    "      'An email address is required.');\n"
                    "  }\n"
                    "  return true;\n"
                    "});"
                ),
                "description": (
                    "Accounts.onCreateUser lets you customize the user document "
                    "before it is stored. Accounts.validateNewUser can reject "
                    "invalid registrations. Email templates control the content "
                    "of verification and reset emails."
                ),
            },
        ],
    },
    "authentication": {
        "title": "Authentication and Login Flows",
        "intro": (
            "Meteor supports password-based authentication out of the box and "
            "OAuth providers (Google, GitHub, Facebook, etc.) via packages. In v3, "
            "login methods are async and return Promises."
        ),
        "snippets": [
            {
                "title": "Password-based login flow",
                "code": (
                    "// client/loginForm.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "async function handleLogin(emailOrUsername, password) {\n"
                    "  try {\n"
                    "    await Meteor.loginWithPassword(emailOrUsername, password);\n"
                    "    console.log('Login successful, userId:', Meteor.userId());\n"
                    "  } catch (error) {\n"
                    "    if (error.error === 403) {\n"
                    "      console.error('Invalid credentials');\n"
                    "    } else {\n"
                    "      console.error('Login error:', error.reason);\n"
                    "    }\n"
                    "  }\n"
                    "}\n"
                    "\n"
                    "// Change password for current user\n"
                    "async function changePassword(oldPassword, newPassword) {\n"
                    "  try {\n"
                    "    await Accounts.changePassword(oldPassword, newPassword);\n"
                    "    console.log('Password changed successfully');\n"
                    "  } catch (error) {\n"
                    "    console.error('Password change failed:', error.reason);\n"
                    "  }\n"
                    "}\n"
                    "\n"
                    "// Forgot password flow\n"
                    "async function forgotPassword(email) {\n"
                    "  try {\n"
                    "    await Accounts.forgotPassword({ email });\n"
                    "    console.log('Reset email sent');\n"
                    "  } catch (error) {\n"
                    "    console.error('Error:', error.reason);\n"
                    "  }\n"
                    "}"
                ),
                "description": (
                    "Password authentication uses Meteor.loginWithPassword on "
                    "the client. The Accounts package provides changePassword "
                    "and forgotPassword for password management. In v3 these "
                    "methods return Promises while keeping their original names."
                ),
            },
            {
                "title": "OAuth login with Google",
                "code": (
                    "// Install required packages:\n"
                    "// meteor add accounts-google service-configuration\n"
                    "\n"
                    "// server/oauth-config.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { ServiceConfiguration } from "
                    "'meteor/service-configuration';\n"
                    "\n"
                    "Meteor.startup(async () => {\n"
                    "  await ServiceConfiguration.configurations.upsertAsync(\n"
                    "    { service: 'google' },\n"
                    "    {\n"
                    "      $set: {\n"
                    "        clientId: Meteor.settings.google.clientId,\n"
                    "        secret: Meteor.settings.google.secret,\n"
                    "        loginStyle: 'popup',\n"
                    "      },\n"
                    "    }\n"
                    "  );\n"
                    "});\n"
                    "\n"
                    "// client/loginButtons.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "async function loginWithGoogle() {\n"
                    "  try {\n"
                    "    await Meteor.loginWithGoogle({\n"
                    "      requestPermissions: ['email', 'profile'],\n"
                    "    });\n"
                    "    console.log('Google login successful');\n"
                    "  } catch (error) {\n"
                    "    console.error('Google login failed:', error.reason);\n"
                    "  }\n"
                    "}"
                ),
                "description": (
                    "OAuth setup requires the accounts-<provider> and "
                    "service-configuration packages. Configure credentials on the "
                    "server via ServiceConfiguration and call "
                    "Meteor.loginWith<Provider> on the client (returns a Promise in v3)."
                ),
            },
            {
                "title": "Custom login handler and token-based auth",
                "code": (
                    "// server/custom-auth.js\n"
                    "import { Accounts } from 'meteor/accounts-base';\n"
                    "import { check } from 'meteor/check';\n"
                    "\n"
                    "// Register a custom login handler\n"
                    "Accounts.registerLoginHandler('apiKey', async (options) => {\n"
                    "  if (!options.apiKey) {\n"
                    "    return undefined; // Not handled by this handler\n"
                    "  }\n"
                    "\n"
                    "  check(options.apiKey, String);\n"
                    "\n"
                    "  const user = await Meteor.users.findOneAsync({\n"
                    "    'services.apiKey.key': options.apiKey,\n"
                    "  });\n"
                    "\n"
                    "  if (!user) {\n"
                    "    throw new Meteor.Error('invalid-api-key',\n"
                    "      'The API key is not valid.');\n"
                    "  }\n"
                    "\n"
                    "  return { userId: user._id };\n"
                    "});\n"
                    "\n"
                    "// client: log in with the custom handler\n"
                    "// await Accounts.callLoginMethod({\n"
                    "//   methodArguments: [{ apiKey: 'my-secret-key' }],\n"
                    "// });"
                ),
                "description": (
                    "Accounts.registerLoginHandler lets you implement custom "
                    "authentication strategies. Return undefined to pass to the "
                    "next handler, throw to reject, or return { userId } to accept."
                ),
            },
        ],
    },
    "security": {
        "title": "Security Best Practices",
        "intro": (
            "Meteor security centers on validating inputs in methods, restricting "
            "data in publications, and removing the insecure and autopublish "
            "packages. Allow/deny rules exist but methods are the recommended "
            "approach for writes in production apps."
        ),
        "snippets": [
            {
                "title": "Method validation and authorization",
                "code": (
                    "// imports/api/documents/methods.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check, Match } from 'meteor/check';\n"
                    "import { DocumentsCollection } from './collection';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async 'documents.update'(docId, updates) {\n"
                    "    // 1. Validate all inputs\n"
                    "    check(docId, String);\n"
                    "    check(updates, {\n"
                    "      title: Match.Maybe(String),\n"
                    "      content: Match.Maybe(String),\n"
                    "      tags: Match.Maybe([String]),\n"
                    "    });\n"
                    "\n"
                    "    // 2. Require authentication\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized',\n"
                    "        'You must be logged in.');\n"
                    "    }\n"
                    "\n"
                    "    // 3. Check ownership or role\n"
                    "    const doc = await DocumentsCollection.findOneAsync(docId);\n"
                    "    if (!doc) {\n"
                    "      throw new Meteor.Error('not-found', 'Document not found.');\n"
                    "    }\n"
                    "\n"
                    "    const isOwner = doc.userId === this.userId;\n"
                    "    const isAdmin = await Meteor.users.findOneAsync({\n"
                    "      _id: this.userId,\n"
                    "      'profile.role': 'admin',\n"
                    "    });\n"
                    "\n"
                    "    if (!isOwner && !isAdmin) {\n"
                    "      throw new Meteor.Error('not-authorized',\n"
                    "        'You do not have permission to edit this document.');\n"
                    "    }\n"
                    "\n"
                    "    // 4. Perform the update with sanitized fields\n"
                    "    await DocumentsCollection.updateAsync(docId, {\n"
                    "      $set: { ...updates, updatedAt: new Date() },\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Always validate inputs with check(), verify authentication "
                    "via this.userId, and confirm authorization (ownership or role) "
                    "before performing any database operations."
                ),
            },
            {
                "title": "Rate limiting methods and subscriptions",
                "code": (
                    "// server/rate-limiting.js\n"
                    "import { DDPRateLimiter } from 'meteor/ddp-rate-limiter';\n"
                    "\n"
                    "// Limit login attempts: 5 per 10 seconds per connection\n"
                    "DDPRateLimiter.addRule(\n"
                    "  {\n"
                    "    type: 'method',\n"
                    "    name: 'login',\n"
                    "    connectionId() {\n"
                    "      return true; // Apply to all connections\n"
                    "    },\n"
                    "  },\n"
                    "  5,    // max requests\n"
                    "  10000 // per time window (ms)\n"
                    ");\n"
                    "\n"
                    "// Limit all methods for a specific user\n"
                    "DDPRateLimiter.addRule(\n"
                    "  {\n"
                    "    type: 'method',\n"
                    "    userId(userId) {\n"
                    "      return userId != null;\n"
                    "    },\n"
                    "  },\n"
                    "  20,   // max requests\n"
                    "  1000  // per 1 second\n"
                    ");\n"
                    "\n"
                    "// Limit subscriptions\n"
                    "DDPRateLimiter.addRule(\n"
                    "  {\n"
                    "    type: 'subscription',\n"
                    "    name: 'search.results',\n"
                    "  },\n"
                    "  5,\n"
                    "  1000\n"
                    ");"
                ),
                "description": (
                    "DDPRateLimiter protects against brute-force attacks and abuse. "
                    "Rules can match by method/subscription name, userId, and "
                    "connectionId. The callback receives a boolean indicating "
                    "whether the request was allowed."
                ),
            },
            {
                "title": "Publication field filtering for data security",
                "code": (
                    "// server/publications.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "// Never publish sensitive fields to the client\n"
                    "Meteor.publish('users.directory', function () {\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "\n"
                    "  return Meteor.users.find(\n"
                    "    { 'profile.isPublic': true },\n"
                    "    {\n"
                    "      fields: {\n"
                    "        // Use exclusion-only projection to hide sensitive fields\n"
                    "        'services': 0,\n"
                    "        'emails': 0,\n"
                    "      },\n"
                    "    }\n"
                    "  );\n"
                    "});\n"
                    "\n"
                    "// Publish the current user's own data with more fields\n"
                    "Meteor.publish('users.current', function () {\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "\n"
                    "  return Meteor.users.find(\n"
                    "    { _id: this.userId },\n"
                    "    {\n"
                    "      fields: {\n"
                    "        'profile': 1,\n"
                    "        'emails': 1,\n"
                    "      },\n"
                    "    }\n"
                    "  );\n"
                    "});"
                ),
                "description": (
                    "Always use field projections in publications to avoid leaking "
                    "sensitive data. Never publish the services field which contains "
                    "hashed passwords and OAuth tokens. Provide different field sets "
                    "based on the requesting user's relationship to the data."
                ),
            },
        ],
    },
    "reactive": {
        "title": "Reactive Programming",
        "intro": (
            "Meteor's reactivity system automatically re-runs computations when "
            "their data dependencies change. Tracker.autorun, ReactiveVar, and "
            "ReactiveDict are the core primitives. In v3 with React, the "
            "useTracker hook is the primary way to consume reactive data."
        ),
        "snippets": [
            {
                "title": "Tracker.autorun and ReactiveVar",
                "code": (
                    "// client/reactive-example.js\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "import { ReactiveVar } from 'meteor/reactive-var';\n"
                    "\n"
                    "const selectedFilter = new ReactiveVar('all');\n"
                    "const searchQuery = new ReactiveVar('');\n"
                    "\n"
                    "// Autorun re-executes whenever a reactive dependency changes\n"
                    "Tracker.autorun((computation) => {\n"
                    "  const filter = selectedFilter.get();\n"
                    "  const query = searchQuery.get();\n"
                    "  console.log(`Filter: ${filter}, Search: ${query}`);\n"
                    "\n"
                    "  // Stop after first run if needed\n"
                    "  // computation.stop();\n"
                    "});\n"
                    "\n"
                    "// Changing a ReactiveVar triggers all dependent autoruns\n"
                    "selectedFilter.set('active');\n"
                    "searchQuery.set('meteor');\n"
                    "\n"
                    "// Cleanup: stop the computation when done\n"
                    "// computation.stop();"
                ),
                "description": (
                    "Tracker.autorun creates a reactive computation that re-runs "
                    "whenever any reactive data source it reads changes. ReactiveVar "
                    "stores a single reactive value. Call computation.stop() to "
                    "prevent memory leaks when the computation is no longer needed."
                ),
            },
            {
                "title": "useTracker hook with React",
                "code": (
                    "// imports/ui/Dashboard.jsx\n"
                    "import React, { useState } from 'react';\n"
                    "import { useTracker } from 'meteor/react-meteor-data';\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "export function Dashboard() {\n"
                    "  const [showCompleted, setShowCompleted] = useState(false);\n"
                    "\n"
                    "  const { user, tasks, taskCount, isLoading } = useTracker(() => {\n"
                    "    const handle = Meteor.subscribe('tasks.mine');\n"
                    "    const filter = showCompleted ? {} : { isChecked: false };\n"
                    "\n"
                    "    return {\n"
                    "      user: Meteor.user(),\n"
                    "      tasks: TasksCollection.find(filter, {\n"
                    "        sort: { createdAt: -1 },\n"
                    "      }).fetch(),\n"
                    "      taskCount: TasksCollection.find(filter).count(),\n"
                    "      isLoading: !handle.ready(),\n"
                    "    };\n"
                    "  }, [showCompleted]);\n"
                    "\n"
                    "  if (isLoading) return <div>Loading...</div>;\n"
                    "\n"
                    "  return (\n"
                    "    <div>\n"
                    "      <h1>Welcome, {user?.profile?.name}</h1>\n"
                    "      <p>{taskCount} tasks</p>\n"
                    "      <button onClick={() => setShowCompleted(!showCompleted)}>\n"
                    "        {showCompleted ? 'Hide' : 'Show'} Completed\n"
                    "      </button>\n"
                    "      <ul>\n"
                    "        {tasks.map(t => <li key={t._id}>{t.text}</li>)}\n"
                    "      </ul>\n"
                    "    </div>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "useTracker integrates Meteor reactivity with React. It accepts "
                    "a reactive function and an optional deps array. The component "
                    "re-renders when any Meteor reactive source inside the function "
                    "changes or when the deps change."
                ),
            },
            {
                "title": "ReactiveDict for component state",
                "code": (
                    "// client/state.js\n"
                    "import { ReactiveDict } from 'meteor/reactive-dict';\n"
                    "import { Tracker } from 'meteor/tracker';\n"
                    "\n"
                    "// ReactiveDict stores multiple key-value pairs reactively\n"
                    "const appState = new ReactiveDict('appState');\n"
                    "\n"
                    "// Set values (supports String, Number, Boolean,\n"
                    "// Date, Array, Object, and null/undefined)\n"
                    "appState.set('currentPage', 'dashboard');\n"
                    "appState.set('sidebarOpen', true);\n"
                    "appState.set('filters', { status: 'active', priority: 'high' });\n"
                    "\n"
                    "// Read values reactively\n"
                    "Tracker.autorun(() => {\n"
                    "  const page = appState.get('currentPage');\n"
                    "  const sidebar = appState.get('sidebarOpen');\n"
                    "  console.log(`Page: ${page}, Sidebar: ${sidebar}`);\n"
                    "});\n"
                    "\n"
                    "// Check for equality before triggering reactivity\n"
                    "Tracker.autorun(() => {\n"
                    "  const filters = appState.get('filters');\n"
                    "  if (appState.equals('currentPage', 'dashboard')) {\n"
                    "    console.log('On dashboard with filters:', filters);\n"
                    "  }\n"
                    "});\n"
                    "\n"
                    "// Named ReactiveDict persists across hot code pushes\n"
                    "// when given a name as the first argument."
                ),
                "description": (
                    "ReactiveDict is like ReactiveVar but stores multiple key-value "
                    "pairs. The equals() method avoids unnecessary re-runs by doing "
                    "an equality check. A named ReactiveDict survives hot code push "
                    "in development."
                ),
            },
        ],
    },
    "routing": {
        "title": "Routing Patterns",
        "intro": (
            "Meteor does not include a built-in router. The community packages "
            "ostrio:flow-router-extra and iron:router are popular choices. For "
            "React-based apps, react-router is also commonly used alongside "
            "Meteor."
        ),
        "snippets": [
            {
                "title": "Routing with ostrio:flow-router-extra",
                "code": (
                    "// Install: meteor add ostrio:flow-router-extra\n"
                    "\n"
                    "// imports/startup/client/routes.js\n"
                    "import { FlowRouter } from 'meteor/ostrio:flow-router-extra';\n"
                    "\n"
                    "FlowRouter.route('/', {\n"
                    "  name: 'home',\n"
                    "  action() {\n"
                    "    this.render('mainLayout', 'home');\n"
                    "  },\n"
                    "});\n"
                    "\n"
                    "FlowRouter.route('/tasks/:projectId', {\n"
                    "  name: 'tasks',\n"
                    "  action(params, queryParams) {\n"
                    "    console.log('Project:', params.projectId);\n"
                    "    console.log('Page:', queryParams.page);\n"
                    "    this.render('mainLayout', 'taskList');\n"
                    "  },\n"
                    "});\n"
                    "\n"
                    "// Route groups for shared logic\n"
                    "const adminRoutes = FlowRouter.group({\n"
                    "  prefix: '/admin',\n"
                    "  name: 'admin',\n"
                    "  triggersEnter: [\n"
                    "    (context, redirect) => {\n"
                    "      if (!Meteor.userId()) {\n"
                    "        redirect('/login');\n"
                    "      }\n"
                    "    },\n"
                    "  ],\n"
                    "});\n"
                    "\n"
                    "adminRoutes.route('/users', {\n"
                    "  name: 'adminUsers',\n"
                    "  action() {\n"
                    "    this.render('adminLayout', 'userManagement');\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "FlowRouter provides client-side routing with route parameters, "
                    "query strings, route groups, and trigger hooks. It is designed "
                    "to work well with Meteor's reactivity system and supports both "
                    "Blaze and React rendering."
                ),
            },
            {
                "title": "React Router with Meteor",
                "code": (
                    "// Install: meteor npm install react-router-dom\n"
                    "\n"
                    "// imports/ui/App.jsx\n"
                    "import React from 'react';\n"
                    "import { BrowserRouter, Routes, Route, Navigate } from "
                    "'react-router-dom';\n"
                    "import { useTracker } from 'meteor/react-meteor-data';\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { Dashboard } from './Dashboard';\n"
                    "import { LoginPage } from './LoginPage';\n"
                    "import { TaskDetail } from './TaskDetail';\n"
                    "\n"
                    "function PrivateRoute({ children }) {\n"
                    "  const { user, isLoading } = useTracker(() => ({\n"
                    "    user: Meteor.user(),\n"
                    "    isLoading: Meteor.loggingIn(),\n"
                    "  }));\n"
                    "\n"
                    "  if (isLoading) return <div>Loading...</div>;\n"
                    "  if (!user) return <Navigate to=\"/login\" />;\n"
                    "  return children;\n"
                    "}\n"
                    "\n"
                    "export function App() {\n"
                    "  return (\n"
                    "    <BrowserRouter>\n"
                    "      <Routes>\n"
                    "        <Route path=\"/login\" element={<LoginPage />} />\n"
                    "        <Route\n"
                    "          path=\"/\"\n"
                    "          element={\n"
                    "            <PrivateRoute>\n"
                    "              <Dashboard />\n"
                    "            </PrivateRoute>\n"
                    "          }\n"
                    "        />\n"
                    "        <Route\n"
                    "          path=\"/tasks/:id\"\n"
                    "          element={\n"
                    "            <PrivateRoute>\n"
                    "              <TaskDetail />\n"
                    "            </PrivateRoute>\n"
                    "          }\n"
                    "        />\n"
                    "      </Routes>\n"
                    "    </BrowserRouter>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "React Router integrates cleanly with Meteor. Use useTracker "
                    "inside a PrivateRoute component to reactively check auth state "
                    "and redirect unauthenticated users."
                ),
            },
        ],
    },
    "testing": {
        "title": "Testing Meteor Applications",
        "intro": (
            "Meteor has built-in test infrastructure. Use 'meteor test' to run "
            "unit and integration tests with the meteortesting:mocha package, or "
            "'meteor test --full-app' for full-app acceptance tests."
        ),
        "snippets": [
            {
                "title": "Unit testing a Meteor method",
                "code": (
                    "// Install: meteor add meteortesting:mocha\n"
                    "// Run: meteor test --driver-package meteortesting:mocha\n"
                    "\n"
                    "// tests/methods.test.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { assert } from 'chai';\n"
                    "import { Random } from 'meteor/random';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "import '/imports/api/tasks/methods';\n"
                    "\n"
                    "if (Meteor.isServer) {\n"
                    "  describe('tasks.insert method', function () {\n"
                    "    const userId = Random.id();\n"
                    "\n"
                    "    beforeEach(async function () {\n"
                    "      await TasksCollection.removeAsync({});\n"
                    "    });\n"
                    "\n"
                    "    it('inserts a task for an authenticated user', async function () {\n"
                    "      // Simulate a logged-in user by binding userId to the method\n"
                    "      const invocation = { userId };\n"
                    "      const insertTask = Meteor.server.method_handlers['tasks.insert'];\n"
                    "\n"
                    "      const taskId = await insertTask.apply(invocation, ['Test task']);\n"
                    "\n"
                    "      const task = await TasksCollection.findOneAsync(taskId);\n"
                    "      assert.equal(task.text, 'Test task');\n"
                    "      assert.equal(task.userId, userId);\n"
                    "    });\n"
                    "\n"
                    "    it('rejects insert for unauthenticated user', async function () {\n"
                    "      const invocation = { userId: null };\n"
                    "      const insertTask = Meteor.server.method_handlers['tasks.insert'];\n"
                    "\n"
                    "      try {\n"
                    "        await insertTask.apply(invocation, ['Test task']);\n"
                    "        assert.fail('Should have thrown');\n"
                    "      } catch (error) {\n"
                    "        assert.equal(error.error, 'not-authorized');\n"
                    "      }\n"
                    "    });\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "Test methods by accessing them via "
                    "Meteor.server.method_handlers and calling .apply() with a "
                    "simulated invocation context. This bypasses DDP and tests "
                    "the method logic directly."
                ),
            },
            {
                "title": "Testing a publication",
                "code": (
                    "// tests/publications.test.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { assert } from 'chai';\n"
                    "import { Random } from 'meteor/random';\n"
                    "import { PublicationCollector } from 'meteor/johanbrook:publication-collector';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "import '/imports/api/tasks/publications';\n"
                    "\n"
                    "if (Meteor.isServer) {\n"
                    "  describe('tasks.mine publication', function () {\n"
                    "    const userId = Random.id();\n"
                    "    const otherUserId = Random.id();\n"
                    "\n"
                    "    beforeEach(async function () {\n"
                    "      await TasksCollection.removeAsync({});\n"
                    "      await TasksCollection.insertAsync({\n"
                    "        text: 'My task', userId, createdAt: new Date(),\n"
                    "      });\n"
                    "      await TasksCollection.insertAsync({\n"
                    "        text: 'Other task', userId: otherUserId, createdAt: new Date(),\n"
                    "      });\n"
                    "    });\n"
                    "\n"
                    "    it('publishes only the current user tasks', async function () {\n"
                    "      const collector = new PublicationCollector({ userId });\n"
                    "\n"
                    "      const collections = await collector.collect('tasks.mine');\n"
                    "      const tasks = collections.tasks || [];\n"
                    "\n"
                    "      assert.equal(tasks.length, 1);\n"
                    "      assert.equal(tasks[0].text, 'My task');\n"
                    "      assert.equal(tasks[0].userId, userId);\n"
                    "    });\n"
                    "\n"
                    "    it('returns no data for unauthenticated users', async function () {\n"
                    "      const collector = new PublicationCollector({ userId: null });\n"
                    "\n"
                    "      const collections = await collector.collect('tasks.mine');\n"
                    "      const tasks = collections.tasks || [];\n"
                    "\n"
                    "      assert.equal(tasks.length, 0);\n"
                    "    });\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "PublicationCollector from johanbrook:publication-collector "
                    "captures the documents a publication would send to a client "
                    "without needing a real DDP connection. Its collect() method "
                    "returns a Promise of the published collections."
                ),
            },
            {
                "title": "Integration test with full-app mode",
                "code": (
                    "// Run: meteor test --full-app --driver-package meteortesting:mocha\n"
                    "\n"
                    "// tests/integration.test.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { assert } from 'chai';\n"
                    "\n"
                    "if (Meteor.isClient) {\n"
                    "  describe('Full-app integration', function () {\n"
                    "    it('can call a method end-to-end', async function () {\n"
                    "      this.timeout(10000);\n"
                    "\n"
                    "      // Log in first\n"
                    "      await Meteor.loginWithPassword('test@example.com', 'password');\n"
                    "      assert.isNotNull(Meteor.userId());\n"
                    "\n"
                    "      // Call a method through the full DDP stack\n"
                    "      const taskId = await Meteor.callAsync(\n"
                    "        'tasks.insert', 'Integration test task'\n"
                    "      );\n"
                    "      assert.isString(taskId);\n"
                    "\n"
                    "      // Clean up\n"
                    "      await Meteor.callAsync('tasks.remove', taskId);\n"
                    "      await Meteor.logout();\n"
                    "    });\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "Full-app tests run with the complete application stack. Use "
                    "'meteor test --full-app' to start the full server and client, "
                    "then run tests that exercise real DDP calls, subscriptions, "
                    "and client-server interactions."
                ),
            },
        ],
    },
    "deployment": {
        "title": "Deployment",
        "intro": (
            "Meteor apps can be deployed to Galaxy (Meteor's official hosting), "
            "any Node.js hosting via 'meteor build', or containerized with Docker. "
            "The build output is a standard Node.js application."
        ),
        "snippets": [
            {
                "title": "Build and deploy to a server",
                "code": (
                    "# Build a production bundle\n"
                    "meteor build ../output --architecture os.linux.x86_64\n"
                    "\n"
                    "# The output is a .tar.gz file. On the server:\n"
                    "tar -xzf output.tar.gz\n"
                    "cd bundle/programs/server\n"
                    "npm install\n"
                    "\n"
                    "# Set environment variables and start\n"
                    "export ROOT_URL=https://myapp.example.com\n"
                    "export MONGO_URL=mongodb://localhost:27017/myapp\n"
                    "export PORT=3000\n"
                    "export METEOR_SETTINGS=$(cat settings-production.json)\n"
                    "\n"
                    "node main.js"
                ),
                "description": (
                    "meteor build produces a Node.js bundle. On the target server, "
                    "install npm dependencies and set ROOT_URL, MONGO_URL, and PORT. "
                    "METEOR_SETTINGS should contain your settings.json content."
                ),
            },
            {
                "title": "Docker deployment",
                "code": (
                    "# Dockerfile\n"
                    "FROM geoffreybooth/meteor-base:3.4.0 AS builder\n"
                    "\n"
                    "WORKDIR /app\n"
                    "COPY . .\n"
                    "\n"
                    "RUN meteor npm install\n"
                    "RUN meteor build --directory /app/bundle --server-only\n"
                    "\n"
                    "FROM node:20-slim\n"
                    "\n"
                    "WORKDIR /app\n"
                    "COPY --from=builder /app/bundle/bundle .\n"
                    "\n"
                    "WORKDIR /app/programs/server\n"
                    "RUN npm install\n"
                    "\n"
                    "WORKDIR /app\n"
                    "\n"
                    "ENV PORT=3000\n"
                    "EXPOSE 3000\n"
                    "\n"
                    "CMD [\"node\", \"main.js\"]"
                ),
                "description": (
                    "A multi-stage Dockerfile builds the Meteor app in a Meteor-enabled "
                    "image and copies the output to a slim Node.js image. Set ROOT_URL, "
                    "MONGO_URL, and METEOR_SETTINGS via environment variables at runtime."
                ),
            },
            {
                "title": "Galaxy deployment",
                "code": (
                    "# Deploy to Meteor Galaxy\n"
                    "# First, set your deploy token or log in:\n"
                    "METEOR_SESSION_FILE=deploy-token.json meteor login\n"
                    "\n"
                    "# Deploy with settings\n"
                    "DEPLOY_HOSTNAME=us-east-1.galaxy-deploy.meteor.com \\\n"
                    "  meteor deploy myapp.meteorapp.com \\\n"
                    "  --settings settings-production.json\n"
                    "\n"
                    "# Galaxy environment variables are set via the dashboard\n"
                    "# or in your settings.json under the galaxy.env key:\n"
                    "# {\n"
                    "#   \"galaxy.env\": {\n"
                    "#     \"MONGO_URL\": \"mongodb+srv://...\",\n"
                    "#     \"ROOT_URL\": \"https://myapp.meteorapp.com\"\n"
                    "#   },\n"
                    "#   \"public\": { ... }\n"
                    "# }"
                ),
                "description": (
                    "Galaxy is Meteor's managed hosting platform. Deploy with "
                    "'meteor deploy' and provide settings via --settings. Galaxy "
                    "handles SSL, scaling, and monitoring. Environment variables "
                    "can be set through the Galaxy dashboard or in settings.json."
                ),
            },
        ],
    },
    "rest-api": {
        "title": "REST API Endpoints",
        "intro": (
            "Meteor's WebApp package (included by default) exposes the Connect "
            "HTTP server, allowing you to add REST endpoints alongside DDP. This "
            "is useful for webhooks, third-party integrations, and public APIs."
        ),
        "snippets": [
            {
                "title": "Basic REST endpoints with WebApp",
                "code": (
                    "// server/rest-api.js\n"
                    "import { WebApp } from 'meteor/webapp';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "// GET endpoint\n"
                    "WebApp.handlers.use('/api/tasks', async (req, res, next) => {\n"
                    "  if (req.method !== 'GET') {\n"
                    "    return next();\n"
                    "  }\n"
                    "\n"
                    "  try {\n"
                    "    const tasks = await TasksCollection.find(\n"
                    "      {},\n"
                    "      { sort: { createdAt: -1 }, limit: 50 }\n"
                    "    ).fetchAsync();\n"
                    "\n"
                    "    res.writeHead(200, { 'Content-Type': 'application/json' });\n"
                    "    res.end(JSON.stringify({ tasks }));\n"
                    "  } catch (error) {\n"
                    "    res.writeHead(500, { 'Content-Type': 'application/json' });\n"
                    "    res.end(JSON.stringify({ error: 'Internal server error' }));\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "WebApp.handlers is the Connect middleware stack. Use "
                    "req.method to route by HTTP verb. Call next() to pass "
                    "unhandled requests to the next middleware."
                ),
            },
            {
                "title": "POST endpoint with JSON body parsing",
                "code": (
                    "// server/rest-api.js\n"
                    "import { WebApp } from 'meteor/webapp';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "// Helper to parse JSON body\n"
                    "function parseBody(req) {\n"
                    "  return new Promise((resolve, reject) => {\n"
                    "    let body = '';\n"
                    "    req.on('data', (chunk) => {\n"
                    "      body += chunk.toString();\n"
                    "    });\n"
                    "    req.on('end', () => {\n"
                    "      try {\n"
                    "        resolve(JSON.parse(body));\n"
                    "      } catch (e) {\n"
                    "        reject(new Error('Invalid JSON'));\n"
                    "      }\n"
                    "    });\n"
                    "    req.on('error', reject);\n"
                    "  });\n"
                    "}\n"
                    "\n"
                    "// POST endpoint with auth via API key\n"
                    "WebApp.handlers.use('/api/tasks', async (req, res, next) => {\n"
                    "  if (req.method !== 'POST') {\n"
                    "    return next();\n"
                    "  }\n"
                    "\n"
                    "  const apiKey = req.headers['x-api-key'];\n"
                    "  if (apiKey !== Meteor.settings.apiKey) {\n"
                    "    res.writeHead(401, { 'Content-Type': 'application/json' });\n"
                    "    res.end(JSON.stringify({ error: 'Unauthorized' }));\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  try {\n"
                    "    const data = await parseBody(req);\n"
                    "    const taskId = await TasksCollection.insertAsync({\n"
                    "      text: data.text,\n"
                    "      createdAt: new Date(),\n"
                    "      source: 'api',\n"
                    "    });\n"
                    "\n"
                    "    res.writeHead(201, { 'Content-Type': 'application/json' });\n"
                    "    res.end(JSON.stringify({ taskId }));\n"
                    "  } catch (error) {\n"
                    "    res.writeHead(400, { 'Content-Type': 'application/json' });\n"
                    "    res.end(JSON.stringify({ error: error.message }));\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "For POST/PUT endpoints, parse the request body manually or "
                    "use a middleware like body-parser. Authenticate REST requests "
                    "using API keys in headers since DDP session tokens are not "
                    "available in HTTP middleware."
                ),
            },
            {
                "title": "Webhook endpoint with signature verification",
                "code": (
                    "// server/webhooks.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { WebApp } from 'meteor/webapp';\n"
                    "import crypto from 'crypto';\n"
                    "\n"
                    "function verifySignature(payload, signature, secret) {\n"
                    "  const hash = crypto\n"
                    "    .createHmac('sha256', secret)\n"
                    "    .update(payload)\n"
                    "    .digest('hex');\n"
                    "  const expected = `sha256=${hash}`;\n"
                    "  if (signature.length !== expected.length) {\n"
                    "    return false;\n"
                    "  }\n"
                    "  return crypto.timingSafeEqual(\n"
                    "    Buffer.from(signature),\n"
                    "    Buffer.from(expected)\n"
                    "  );\n"
                    "}\n"
                    "\n"
                    "WebApp.handlers.use('/webhooks/stripe', async (req, res) => {\n"
                    "  if (req.method !== 'POST') {\n"
                    "    res.writeHead(405);\n"
                    "    res.end();\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  let rawBody = '';\n"
                    "  for await (const chunk of req) {\n"
                    "    rawBody += chunk.toString();\n"
                    "  }\n"
                    "\n"
                    "  const signature = req.headers['stripe-signature'];\n"
                    "  const secret = Meteor.settings.stripe.webhookSecret;\n"
                    "\n"
                    "  if (!verifySignature(rawBody, signature, secret)) {\n"
                    "    res.writeHead(403);\n"
                    "    res.end('Invalid signature');\n"
                    "    return;\n"
                    "  }\n"
                    "\n"
                    "  const event = JSON.parse(rawBody);\n"
                    "  console.log('Webhook event:', event.type);\n"
                    "\n"
                    "  // Process the event...\n"
                    "\n"
                    "  res.writeHead(200);\n"
                    "  res.end('OK');\n"
                    "});"
                ),
                "description": (
                    "Webhook endpoints should verify request signatures using "
                    "HMAC to ensure the request is authentic. Use "
                    "crypto.timingSafeEqual to prevent timing attacks when "
                    "comparing signatures."
                ),
            },
        ],
    },
    "file-structure": {
        "title": "Recommended Project Structure",
        "intro": (
            "Meteor v3 uses ES modules and supports a flexible file structure. "
            "The recommended layout separates code into imports/ for explicit "
            "module loading, with client/, server/, and shared entry points."
        ),
        "snippets": [
            {
                "title": "Standard Meteor v3 project layout",
                "code": (
                    "my-meteor-app/\n"
                    "├── .meteor/\n"
                    "│   ├── packages          # Meteor packages list\n"
                    "│   ├── platforms          # Target platforms\n"
                    "│   └── release            # Meteor release version\n"
                    "├── client/\n"
                    "│   └── main.js            # Client entry point\n"
                    "├── server/\n"
                    "│   └── main.js            # Server entry point\n"
                    "├── imports/\n"
                    "│   ├── api/\n"
                    "│   │   ├── tasks/\n"
                    "│   │   │   ├── collection.js    # Mongo.Collection definition\n"
                    "│   │   │   ├── methods.js        # Meteor methods\n"
                    "│   │   │   ├── publications.js   # Server publications\n"
                    "│   │   │   └── schema.js          # Validation schemas\n"
                    "│   │   └── users/\n"
                    "│   │       ├── methods.js\n"
                    "│   │       └── publications.js\n"
                    "│   ├── startup/\n"
                    "│   │   ├── client/\n"
                    "│   │   │   ├── index.js          # Client startup imports\n"
                    "│   │   │   └── routes.js          # Route definitions\n"
                    "│   │   └── server/\n"
                    "│   │       ├── index.js           # Server startup imports\n"
                    "│   │       ├── accounts.js        # Accounts config\n"
                    "│   │       └── fixtures.js        # Seed data\n"
                    "│   └── ui/\n"
                    "│       ├── components/\n"
                    "│       │   ├── TaskItem.jsx\n"
                    "│       │   └── TaskList.jsx\n"
                    "│       ├── layouts/\n"
                    "│       │   └── MainLayout.jsx\n"
                    "│       ├── pages/\n"
                    "│       │   ├── Dashboard.jsx\n"
                    "│       │   └── LoginPage.jsx\n"
                    "│       └── App.jsx\n"
                    "├── public/                # Static assets served as-is\n"
                    "│   └── favicon.ico\n"
                    "├── private/               # Server-only assets (Assets API)\n"
                    "│   └── email-templates/\n"
                    "├── tests/\n"
                    "│   ├── methods.test.js\n"
                    "│   └── publications.test.js\n"
                    "├── package.json\n"
                    "└── settings.json          # Development settings"
                ),
                "description": (
                    "Files in imports/ are only loaded when explicitly imported. "
                    "Files in client/ and server/ auto-load on their respective "
                    "platforms. The public/ directory serves static assets and "
                    "private/ provides server-only assets via Assets.getText() "
                    "and Assets.getBinary()."
                ),
            },
            {
                "title": "Entry points that wire everything together",
                "code": (
                    "// client/main.js\n"
                    "import '/imports/startup/client';\n"
                    "import '/imports/api/tasks/methods';  // Load client stubs\n"
                    "\n"
                    "// server/main.js\n"
                    "import '/imports/startup/server';\n"
                    "import '/imports/api/tasks/methods';\n"
                    "import '/imports/api/tasks/publications';\n"
                    "import '/imports/api/users/methods';\n"
                    "import '/imports/api/users/publications';\n"
                    "\n"
                    "// imports/startup/client/index.js\n"
                    "import React from 'react';\n"
                    "import { createRoot } from 'react-dom/client';\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { App } from '/imports/ui/App';\n"
                    "\n"
                    "Meteor.startup(() => {\n"
                    "  const root = createRoot(document.getElementById('react-target'));\n"
                    "  root.render(<App />);\n"
                    "});\n"
                    "\n"
                    "// imports/startup/server/index.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import './accounts';\n"
                    "import './fixtures';\n"
                    "\n"
                    "Meteor.startup(async () => {\n"
                    "  console.log('Server started');\n"
                    "});"
                ),
                "description": (
                    "Entry points in client/main.js and server/main.js import "
                    "everything that needs to run. Method files are imported on both "
                    "sides for optimistic UI. Publications are imported only on "
                    "the server."
                ),
            },
        ],
    },
    "schema-validation": {
        "title": "Schema Validation with check() and Match",
        "intro": (
            "Meteor's built-in check package provides runtime type checking for "
            "method and publication arguments. The Match module offers pattern "
            "combinators for complex validation. Always validate all inputs in "
            "methods to prevent malformed or malicious data."
        ),
        "snippets": [
            {
                "title": "Basic input validation with check()",
                "code": (
                    "// imports/api/tasks/methods.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check, Match } from 'meteor/check';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async 'tasks.create'(data) {\n"
                    "    // Validate a complex object shape\n"
                    "    check(data, {\n"
                    "      text: String,\n"
                    "      priority: Match.OneOf('low', 'medium', 'high'),\n"
                    "      dueDate: Match.Maybe(Date),\n"
                    "      tags: Match.Maybe([String]),\n"
                    "      assigneeId: Match.Optional(String),\n"
                    "    });\n"
                    "\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "\n"
                    "    return await TasksCollection.insertAsync({\n"
                    "      ...data,\n"
                    "      createdAt: new Date(),\n"
                    "      userId: this.userId,\n"
                    "    });\n"
                    "  },\n"
                    "\n"
                    "  async 'tasks.updatePriority'(taskId, priority) {\n"
                    "    check(taskId, String);\n"
                    "    check(priority, Match.OneOf('low', 'medium', 'high'));\n"
                    "\n"
                    "    await TasksCollection.updateAsync(taskId, {\n"
                    "      $set: { priority },\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "check() throws a Match.Error if validation fails, which Meteor "
                    "converts to a sanitized error for the client. Use Match.Maybe "
                    "for nullable fields, Match.Optional for fields that can be "
                    "absent, and Match.OneOf for enumerated values."
                ),
            },
            {
                "title": "Advanced Match patterns and custom validators",
                "code": (
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check, Match } from 'meteor/check';\n"
                    "import { ContactsCollection } from '/imports/api/contacts';\n"
                    "\n"
                    "// Match.Where for custom validation logic\n"
                    "const NonEmptyString = Match.Where((value) => {\n"
                    "  check(value, String);\n"
                    "  return value.trim().length > 0;\n"
                    "});\n"
                    "\n"
                    "const PositiveInteger = Match.Where((value) => {\n"
                    "  check(value, Match.Integer);\n"
                    "  return value > 0;\n"
                    "});\n"
                    "\n"
                    "const EmailString = Match.Where((value) => {\n"
                    "  check(value, String);\n"
                    "  return /^[^@]+@[^@]+\\.[^@]+$/.test(value);\n"
                    "});\n"
                    "\n"
                    "// Using custom patterns in methods\n"
                    "Meteor.methods({\n"
                    "  async 'contacts.create'(contact) {\n"
                    "    check(contact, {\n"
                    "      name: NonEmptyString,\n"
                    "      email: EmailString,\n"
                    "      age: Match.Optional(PositiveInteger),\n"
                    "      address: Match.Optional({\n"
                    "        street: String,\n"
                    "        city: String,\n"
                    "        zip: Match.Where((z) => {\n"
                    "          check(z, String);\n"
                    "          return /^\\d{5}(-\\d{4})?$/.test(z);\n"
                    "        }),\n"
                    "      }),\n"
                    "    });\n"
                    "\n"
                    "    // If we reach here, all validation passed\n"
                    "    return await ContactsCollection.insertAsync(contact);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Match.Where accepts a function that returns true or false for "
                    "custom validation. Nest check() calls inside Where to also "
                    "enforce the base type. Custom patterns are reusable and "
                    "composable across methods."
                ),
            },
            {
                "title": "Validate publication arguments",
                "code": (
                    "// server/publications.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check, Match } from 'meteor/check';\n"
                    "import { TasksCollection } from '/imports/api/tasks';\n"
                    "\n"
                    "Meteor.publish('tasks.filtered', function (options) {\n"
                    "  check(options, {\n"
                    "    status: Match.Optional(Match.OneOf('active', 'completed', 'all')),\n"
                    "    limit: Match.Optional(Match.Where((n) => {\n"
                    "      check(n, Match.Integer);\n"
                    "      return n > 0 && n <= 100;\n"
                    "    })),\n"
                    "    sortBy: Match.Optional(Match.OneOf('createdAt', 'priority', 'dueDate')),\n"
                    "  });\n"
                    "\n"
                    "  if (!this.userId) {\n"
                    "    return this.ready();\n"
                    "  }\n"
                    "\n"
                    "  const filter = { userId: this.userId };\n"
                    "  if (options.status && options.status !== 'all') {\n"
                    "    filter.isChecked = options.status === 'completed';\n"
                    "  }\n"
                    "\n"
                    "  const sort = {};\n"
                    "  sort[options.sortBy || 'createdAt'] = -1;\n"
                    "\n"
                    "  return TasksCollection.find(filter, {\n"
                    "    sort,\n"
                    "    limit: options.limit || 20,\n"
                    "  });\n"
                    "});"
                ),
                "description": (
                    "Always validate publication arguments with check(). Restrict "
                    "limit values to prevent clients from requesting too much data. "
                    "Validate sort fields to prevent arbitrary field access."
                ),
            },
        ],
    },
    "email": {
        "title": "Sending Emails",
        "intro": (
            "Meteor's email package provides Email.sendAsync for sending emails "
            "via SMTP. Configure the MAIL_URL environment variable to point at "
            "your SMTP server. In development, emails are logged to the console "
            "if MAIL_URL is not set."
        ),
        "snippets": [
            {
                "title": "Send email with Email.sendAsync",
                "code": (
                    "// Install: meteor add email\n"
                    "\n"
                    "// server/email.js\n"
                    "import { Email } from 'meteor/email';\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check } from 'meteor/check';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async 'email.sendWelcome'(userId) {\n"
                    "    check(userId, String);\n"
                    "\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "\n"
                    "    const user = await Meteor.users.findOneAsync(userId);\n"
                    "    if (!user) {\n"
                    "      throw new Meteor.Error('user-not-found');\n"
                    "    }\n"
                    "\n"
                    "    const email = user.emails[0].address;\n"
                    "    const name = user.profile?.name || 'there';\n"
                    "\n"
                    "    await Email.sendAsync({\n"
                    "      to: email,\n"
                    "      from: 'no-reply@myapp.com',\n"
                    "      subject: 'Welcome to My App',\n"
                    "      text: `Hello ${name},\\n\\n`\n"
                    "        + 'Welcome to our app! Get started by creating your first task.\\n\\n'\n"
                    "        + 'Best regards,\\nThe Team',\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Email.sendAsync is the v3 async replacement for Email.send. "
                    "It accepts to, from, subject, text, and html fields. Configure "
                    "MAIL_URL as an environment variable, for example: "
                    "MAIL_URL=smtp://user:pass@smtp.example.com:587"
                ),
            },
            {
                "title": "HTML email with templates",
                "code": (
                    "// server/email-templates.js\n"
                    "import { Email } from 'meteor/email';\n"
                    "import { Assets } from 'meteor/assets';\n"
                    "\n"
                    "// Load an HTML template from private/ directory\n"
                    "async function renderTemplate(templateName, variables) {\n"
                    "  let html = await Assets.getTextAsync(\n"
                    "    `email-templates/${templateName}.html`\n"
                    "  );\n"
                    "\n"
                    "  // Simple variable replacement\n"
                    "  for (const [key, value] of Object.entries(variables)) {\n"
                    "    html = html.replace(\n"
                    "      new RegExp(`{{${key}}}`, 'g'),\n"
                    "      value\n"
                    "    );\n"
                    "  }\n"
                    "\n"
                    "  return html;\n"
                    "}\n"
                    "\n"
                    "async function sendOrderConfirmation(order, userEmail) {\n"
                    "  const html = await renderTemplate('order-confirmation', {\n"
                    "    orderId: order._id,\n"
                    "    total: order.total.toFixed(2),\n"
                    "    itemCount: String(order.items.length),\n"
                    "    appUrl: Meteor.absoluteUrl(),\n"
                    "  });\n"
                    "\n"
                    "  await Email.sendAsync({\n"
                    "    to: userEmail,\n"
                    "    from: 'orders@myapp.com',\n"
                    "    subject: `Order Confirmation #${order._id}`,\n"
                    "    html,\n"
                    "    // Plain text fallback\n"
                    "    text: `Order ${order._id} confirmed. `\n"
                    "      + `Total: $${order.total.toFixed(2)}`,\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "Store HTML email templates in the private/ directory and load "
                    "them with Assets.getTextAsync. Provide both html and text "
                    "fields for maximum email client compatibility."
                ),
            },
            {
                "title": "Configure SMTP and email defaults",
                "code": (
                    "// server/email-config.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "Meteor.startup(() => {\n"
                    "  // Option 1: Set MAIL_URL environment variable\n"
                    "  // export MAIL_URL=smtps://user:pass@smtp.mailgun.org:465\n"
                    "\n"
                    "  // Option 2: Set MAIL_URL programmatically from settings\n"
                    "  if (Meteor.settings.smtp) {\n"
                    "    const { user, password, host, port } = Meteor.settings.smtp;\n"
                    "    process.env.MAIL_URL = `smtps://${encodeURIComponent(user)}`\n"
                    "      + `:${encodeURIComponent(password)}`\n"
                    "      + `@${host}:${port}`;\n"
                    "  }\n"
                    "});\n"
                    "\n"
                    "// Customize accounts email defaults\n"
                    "import { Accounts } from 'meteor/accounts-base';\n"
                    "\n"
                    "Accounts.emailTemplates.siteName = 'My Meteor App';\n"
                    "Accounts.emailTemplates.from = 'My App <no-reply@myapp.com>';\n"
                    "\n"
                    "Accounts.emailTemplates.resetPassword = {\n"
                    "  subject() {\n"
                    "    return 'Reset Your Password';\n"
                    "  },\n"
                    "  text(user, url) {\n"
                    "    const name = user.profile?.name || 'User';\n"
                    "    return `Hello ${name},\\n\\n`\n"
                    "      + `Click the link below to reset your password:\\n${url}\\n\\n`\n"
                    "      + 'If you did not request this, ignore this email.\\n\\n'\n"
                    "      + 'Thanks,\\nThe Team';\n"
                    "  },\n"
                    "};"
                ),
                "description": (
                    "MAIL_URL supports smtp:// and smtps:// protocols. URL-encode "
                    "the username and password to handle special characters. In "
                    "development without MAIL_URL, Meteor logs the email content "
                    "to the server console."
                ),
            },
        ],
    },
    "environment": {
        "title": "Environment Configuration",
        "intro": (
            "Meteor uses Meteor.settings for app configuration and standard "
            "environment variables for infrastructure settings. Key environment "
            "variables include ROOT_URL, MONGO_URL, MAIL_URL, PORT, and "
            "METEOR_SETTINGS."
        ),
        "snippets": [
            {
                "title": "Using Meteor.settings for app configuration",
                "code": (
                    "// settings.json (development)\n"
                    "// {\n"
                    "//   \"private\": {\n"
                    "//     \"stripeSecretKey\": \"sk_test_...\",\n"
                    "//     \"awsAccessKeyId\": \"AKIA...\",\n"
                    "//     \"awsSecretKey\": \"secret...\"\n"
                    "//   },\n"
                    "//   \"smtp\": {\n"
                    "//     \"user\": \"postmaster@mg.myapp.com\",\n"
                    "//     \"password\": \"smtp-password\",\n"
                    "//     \"host\": \"smtp.mailgun.org\",\n"
                    "//     \"port\": 465\n"
                    "//   },\n"
                    "//   \"public\": {\n"
                    "//     \"appName\": \"My App\",\n"
                    "//     \"analyticsId\": \"UA-12345678-1\",\n"
                    "//     \"maxUploadSizeMb\": 10\n"
                    "//   }\n"
                    "// }\n"
                    "\n"
                    "// Run with: meteor run --settings settings.json\n"
                    "\n"
                    "// Server: access all settings\n"
                    "const stripeKey = Meteor.settings.private.stripeSecretKey;\n"
                    "const smtpHost = Meteor.settings.smtp.host;\n"
                    "\n"
                    "// Client: only public settings are available\n"
                    "const appName = Meteor.settings.public.appName;\n"
                    "const maxSize = Meteor.settings.public.maxUploadSizeMb;"
                ),
                "description": (
                    "Settings defined under 'public' are sent to the client. All "
                    "other top-level keys are server-only. Run the app with "
                    "--settings to load the file, or set METEOR_SETTINGS as an "
                    "environment variable in production."
                ),
            },
            {
                "title": "Environment variables for infrastructure",
                "code": (
                    "// Required environment variables for production:\n"
                    "\n"
                    "// ROOT_URL - The public URL of your app\n"
                    "// export ROOT_URL=https://myapp.example.com\n"
                    "\n"
                    "// MONGO_URL - MongoDB connection string\n"
                    "// export MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/myapp\n"
                    "\n"
                    "// MONGO_OPLOG_URL - Oplog tailing for real-time updates (optional)\n"
                    "// export MONGO_OPLOG_URL=mongodb+srv://oplog-user:pass@cluster.mongodb.net/local\n"
                    "\n"
                    "// PORT - HTTP port (default 3000)\n"
                    "// export PORT=8080\n"
                    "\n"
                    "// MAIL_URL - SMTP server for sending emails\n"
                    "// export MAIL_URL=smtps://user:pass@smtp.mailgun.org:465\n"
                    "\n"
                    "// METEOR_SETTINGS - JSON string of settings\n"
                    "// export METEOR_SETTINGS=$(cat settings-production.json)\n"
                    "\n"
                    "// Access environment variables in server code:\n"
                    "const mongoUrl = process.env.MONGO_URL;\n"
                    "const rootUrl = process.env.ROOT_URL;\n"
                    "const customVar = process.env.MY_CUSTOM_VAR;\n"
                    "\n"
                    "// Set custom env vars for your app\n"
                    "// export MY_CUSTOM_VAR=some-value\n"
                    "Meteor.startup(() => {\n"
                    "  if (!process.env.MY_CUSTOM_VAR) {\n"
                    "    console.warn('MY_CUSTOM_VAR is not set');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "ROOT_URL and MONGO_URL are required for production. "
                    "MONGO_OPLOG_URL enables oplog tailing for efficient real-time "
                    "updates. Access environment variables via process.env on the "
                    "server. Never expose process.env to the client."
                ),
            },
            {
                "title": "Per-environment settings pattern",
                "code": (
                    "// settings-development.json\n"
                    "// {\n"
                    "//   \"private\": {\n"
                    "//     \"stripe\": { \"secretKey\": \"sk_test_...\" }\n"
                    "//   },\n"
                    "//   \"public\": {\n"
                    "//     \"stripe\": { \"publishableKey\": \"pk_test_...\" },\n"
                    "//     \"environment\": \"development\"\n"
                    "//   }\n"
                    "// }\n"
                    "\n"
                    "// settings-production.json\n"
                    "// {\n"
                    "//   \"private\": {\n"
                    "//     \"stripe\": { \"secretKey\": \"sk_live_...\" }\n"
                    "//   },\n"
                    "//   \"public\": {\n"
                    "//     \"stripe\": { \"publishableKey\": \"pk_live_...\" },\n"
                    "//     \"environment\": \"production\"\n"
                    "//   }\n"
                    "// }\n"
                    "\n"
                    "// server/startup.js\n"
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "Meteor.startup(() => {\n"
                    "  const env = Meteor.settings.public.environment || 'development';\n"
                    "  console.log(`Running in ${env} mode`);\n"
                    "  console.log(`Meteor release: ${Meteor.release}`);\n"
                    "\n"
                    "  // Validate required settings exist\n"
                    "  const required = ['private.stripe.secretKey'];\n"
                    "  for (const path of required) {\n"
                    "    const keys = path.split('.');\n"
                    "    let value = Meteor.settings;\n"
                    "    for (const key of keys) {\n"
                    "      value = value?.[key];\n"
                    "    }\n"
                    "    if (value === undefined) {\n"
                    "      throw new Error(`Missing required setting: ${path}`);\n"
                    "    }\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Maintain separate settings files for each environment and load "
                    "the appropriate one at startup. Validate that required settings "
                    "exist early to catch misconfiguration before the app serves "
                    "requests."
                ),
            },
        ],
    },
}
