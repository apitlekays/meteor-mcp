"""Meteor Accounts API entries for Meteor.js v3.4.0."""

ACCOUNTS = [
    {
        "name": "Meteor.user",
        "module": "accounts",
        "signature": "Meteor.user([options])",
        "description": (
            "Returns the current user's document from the Meteor.users "
            "collection, or null if no user is logged in. On the client, "
            "this is a reactive data source that triggers reruns of any "
            "reactive computation (such as Tracker.autorun or Blaze helpers) "
            "whenever the user document changes. The returned document "
            "includes the user's _id, username, emails array, and profile "
            "subdocument. On the server, this function is available inside "
            "Meteor methods and publications via this.userId, but calling "
            "Meteor.user() directly on the server is only supported inside "
            "a method or publication invocation context."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Optional. An object with a 'fields' key (Object) "
                    "specifying a field projection to limit which fields "
                    "of the user document are returned. On the client, "
                    "this can reduce reactivity to only the specified fields."
                ),
                "optional": True,
            },
        ],
        "returns": "Object | null",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Display the current user's name in a Blaze template",
                "code": (
                    "Template.navbar.helpers({\n"
                    "  currentUser() {\n"
                    "    const user = Meteor.user();\n"
                    "    if (user) {\n"
                    "      return user.username || user.emails[0].address;\n"
                    "    }\n"
                    "    return 'Guest';\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Meteor.user() is reactive on the client, so the helper "
                    "will rerun automatically when the user logs in or out."
                ),
            },
            {
                "title": "Access user data in a React component",
                "code": (
                    "import { useTracker } from 'meteor/react-meteor-data';\n"
                    "\n"
                    "function UserGreeting() {\n"
                    "  const user = useTracker(() => Meteor.user());\n"
                    "\n"
                    "  if (!user) {\n"
                    "    return <p>Please log in.</p>;\n"
                    "  }\n"
                    "\n"
                    "  return <p>Welcome, {user.username}!</p>;\n"
                    "}"
                ),
                "description": (
                    "In React, wrap Meteor.user() inside useTracker to "
                    "subscribe to reactive changes to the user document."
                ),
            },
        ],
        "tags": ["accounts", "user", "auth", "reactive"],
    },
    {
        "name": "Meteor.userAsync",
        "module": "accounts",
        "signature": "Meteor.userAsync()",
        "description": (
            "Asynchronous version of Meteor.user(). Returns a Promise that "
            "resolves to the current user's document from the Meteor.users "
            "collection, or null if no user is logged in. This is the "
            "recommended way to access the current user document in Meteor "
            "v3, especially on the server where Fibers have been removed. "
            "On the server, this must be called within a method or "
            "publication invocation context."
        ),
        "params": [],
        "returns": "Promise<Object | null>",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Fetch user data in an async Meteor method",
                "code": (
                    "Meteor.methods({\n"
                    "  async updateProfile(profileData) {\n"
                    "    check(profileData, Object);\n"
                    "\n"
                    "    const user = await Meteor.userAsync();\n"
                    "    if (!user) {\n"
                    "      throw new Meteor.Error('not-authorized', 'You must be logged in.');\n"
                    "    }\n"
                    "\n"
                    "    await Meteor.users.updateAsync(user._id, {\n"
                    "      $set: { profile: profileData },\n"
                    "    });\n"
                    "\n"
                    "    return { success: true };\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Meteor.userAsync() is the async-friendly replacement for "
                    "Meteor.user() in Meteor v3 server code."
                ),
            },
        ],
        "tags": ["accounts", "user", "auth", "async"],
    },
    {
        "name": "Meteor.userId",
        "module": "accounts",
        "signature": "Meteor.userId()",
        "description": (
            "Returns the ID of the currently logged-in user, or null if no "
            "user is logged in. On the client, this is a reactive data source. "
            "This is a lightweight alternative to Meteor.user() when you only "
            "need the user's _id and do not need the full user document. On "
            "the server, this function works inside Meteor methods and "
            "publications. It is equivalent to this.userId in a method or "
            "publication context. Note: Meteor.userId() is only reactive on "
            "the client. On the server in async methods, capture the userId "
            "before any await (or use this.userId) to avoid losing the "
            "invocation context."
        ),
        "params": [],
        "returns": "String | null",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Authorization check in a Meteor method",
                "code": (
                    "Meteor.methods({\n"
                    "  async deletePost(postId) {\n"
                    "    check(postId, String);\n"
                    "\n"
                    "    // Capture userId before any await to preserve context\n"
                    "    const userId = this.userId;\n"
                    "    if (!userId) {\n"
                    "      throw new Meteor.Error('not-authorized', 'You must be logged in.');\n"
                    "    }\n"
                    "\n"
                    "    const post = await Posts.findOneAsync(postId);\n"
                    "    if (post.authorId !== userId) {\n"
                    "      throw new Meteor.Error('not-authorized', 'You can only delete your own posts.');\n"
                    "    }\n"
                    "\n"
                    "    await Posts.removeAsync(postId);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Meteor.userId() is commonly used for authorization checks "
                    "inside methods and publications."
                ),
            },
            {
                "title": "Reactive user ID tracking on the client",
                "code": (
                    "Tracker.autorun(() => {\n"
                    "  const userId = Meteor.userId();\n"
                    "  if (userId) {\n"
                    "    console.log('User logged in:', userId);\n"
                    "  } else {\n"
                    "    console.log('No user logged in');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "On the client, Meteor.userId() is reactive and will "
                    "trigger the autorun whenever login state changes."
                ),
            },
        ],
        "tags": ["accounts", "user", "auth", "reactive"],
    },
    {
        "name": "Meteor.users",
        "module": "accounts",
        "signature": "Meteor.users",
        "description": (
            "A Mongo.Collection containing user documents. By default, the "
            "users collection stores documents with the following fields: "
            "_id, username, emails (an array of {address, verified} objects), "
            "createdAt, services (authentication provider data), and profile "
            "(a user-editable object). On the client, this collection "
            "contains only the currently logged-in user's document by default "
            "(unless additional users are published). Cursor queries on "
            "Meteor.users.find() are reactive data sources on the client. "
            "The users collection supports all standard Mongo.Collection "
            "operations such as find, findOne, insert, update, and remove, "
            "along with their async counterparts in Meteor v3."
        ),
        "params": [],
        "returns": "Mongo.Collection",
        "environment": "anywhere",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Publish and subscribe to user data",
                "code": (
                    "// Server: publish specific user fields\n"
                    "Meteor.publish('allUsers', function () {\n"
                    "  return Meteor.users.find({}, {\n"
                    "    fields: { username: 1, 'emails.address': 1, createdAt: 1 },\n"
                    "  });\n"
                    "});\n"
                    "\n"
                    "// Client: subscribe and query\n"
                    "Meteor.subscribe('allUsers');\n"
                    "const users = await Meteor.users.find({}).fetchAsync();"
                ),
                "description": (
                    "By default only the current user is published to the "
                    "client. To access other users' data, create a publication "
                    "that exposes only the necessary fields."
                ),
            },
            {
                "title": "Query users on the server",
                "code": (
                    "Meteor.methods({\n"
                    "  async getAdminUsers() {\n"
                    "    return await Meteor.users.find(\n"
                    "      { 'roles': 'admin' },\n"
                    "      { fields: { username: 1, emails: 1 } }\n"
                    "    ).fetchAsync();\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "On the server, Meteor.users provides full access to all "
                    "user documents. Use projection to limit returned fields."
                ),
            },
        ],
        "tags": ["accounts", "user", "collection", "mongo"],
    },
    {
        "name": "Meteor.loggingIn",
        "module": "accounts",
        "signature": "Meteor.loggingIn()",
        "description": (
            "Returns true if a login method (such as Meteor.loginWithPassword) "
            "is currently in progress. This is a reactive data source on the "
            "client. Use this to display loading indicators while "
            "authentication is being processed. This function is only "
            "available on the client."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Show a loading spinner during login",
                "code": (
                    "Template.loginForm.helpers({\n"
                    "  isLoggingIn() {\n"
                    "    return Meteor.loggingIn();\n"
                    "  },\n"
                    "});\n"
                    "\n"
                    "// In the template:\n"
                    "// {{#if isLoggingIn}}\n"
                    "//   <div class=\"spinner\">Logging in...</div>\n"
                    "// {{else}}\n"
                    "//   <button>Login</button>\n"
                    "// {{/if}}"
                ),
                "description": (
                    "Meteor.loggingIn() is reactive and updates the template "
                    "automatically as the login process starts and completes."
                ),
            },
            {
                "title": "React component with login state",
                "code": (
                    "import { useTracker } from 'meteor/react-meteor-data';\n"
                    "\n"
                    "function LoginButton() {\n"
                    "  const loggingIn = useTracker(() => Meteor.loggingIn());\n"
                    "\n"
                    "  if (loggingIn) {\n"
                    "    return <span>Authenticating...</span>;\n"
                    "  }\n"
                    "\n"
                    "  return <button onClick={handleLogin}>Log In</button>;\n"
                    "}"
                ),
                "description": (
                    "In React, use useTracker to reactively track the "
                    "loggingIn state and render a loading indicator."
                ),
            },
        ],
        "tags": ["accounts", "auth", "login", "reactive", "loading"],
    },
    {
        "name": "Meteor.loggingOut",
        "module": "accounts",
        "signature": "Meteor.loggingOut()",
        "description": (
            "Returns true if a logout is currently in progress (the server "
            "has been contacted but the client has not yet received the "
            "response). This is a reactive data source on the client. Use "
            "this to display loading indicators during the logout process. "
            "This function is only available on the client."
        ),
        "params": [],
        "returns": "Boolean",
        "environment": "client",
        "is_reactive": True,
        "deprecated": False,
        "examples": [
            {
                "title": "Disable UI during logout",
                "code": (
                    "Template.navbar.helpers({\n"
                    "  isLoggingOut() {\n"
                    "    return Meteor.loggingOut();\n"
                    "  },\n"
                    "});\n"
                    "\n"
                    "// In the template:\n"
                    "// <button {{#if isLoggingOut}}disabled{{/if}}>\n"
                    "//   {{#if isLoggingOut}}Logging out...{{else}}Logout{{/if}}\n"
                    "// </button>"
                ),
                "description": (
                    "Meteor.loggingOut() is reactive and can be used to "
                    "disable buttons or show a loading state during logout."
                ),
            },
        ],
        "tags": ["accounts", "auth", "logout", "reactive", "loading"],
    },
    {
        "name": "Meteor.logout",
        "module": "accounts",
        "signature": "Meteor.logout([callback])",
        "description": (
            "Log the user out of the current session. This invalidates the "
            "current login token on both the client and the server. The "
            "user's other sessions (on other browsers or devices) remain "
            "active. The optional callback is called with no arguments on "
            "success, or with a single Error argument on failure."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Optional callback. Called with no arguments on success, "
                    "or with a single Error argument on failure."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log out with error handling",
                "code": (
                    "Meteor.logout((error) => {\n"
                    "  if (error) {\n"
                    "    console.error('Logout failed:', error.reason);\n"
                    "  } else {\n"
                    "    console.log('Successfully logged out');\n"
                    "    Router.go('/login');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Meteor.logout() invalidates the current login token. "
                    "Use the callback to redirect the user after successful logout."
                ),
            },
            {
                "title": "Logout button in a React component",
                "code": (
                    "function LogoutButton() {\n"
                    "  function handleLogout() {\n"
                    "    Meteor.logout((error) => {\n"
                    "      if (error) {\n"
                    "        alert(`Logout failed: ${error.reason}`);\n"
                    "      }\n"
                    "    });\n"
                    "  }\n"
                    "\n"
                    "  return <button onClick={handleLogout}>Log Out</button>;\n"
                    "}"
                ),
                "description": (
                    "A simple React component that logs the user out when "
                    "the button is clicked."
                ),
            },
        ],
        "tags": ["accounts", "auth", "logout", "session"],
    },
    {
        "name": "Meteor.logoutOtherClients",
        "module": "accounts",
        "signature": "Meteor.logoutOtherClients([callback])",
        "description": (
            "Log out all other clients logged in as the current user, while "
            "keeping the current session active. This invalidates all login "
            "tokens for the current user except the one associated with the "
            "current connection. The callback receives no arguments on "
            "success, or a single Error argument on failure. This is useful "
            "for security features where a user wants to ensure no other "
            "sessions are active."
        ),
        "params": [
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Optional callback. Called with no arguments on success, "
                    "or with a single Error argument on failure."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log out all other sessions",
                "code": (
                    "// Security: terminate all other active sessions\n"
                    "Meteor.logoutOtherClients((error) => {\n"
                    "  if (error) {\n"
                    "    console.error('Failed to logout other clients:', error.reason);\n"
                    "  } else {\n"
                    "    console.log('All other sessions have been terminated.');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Use Meteor.logoutOtherClients() after a password change "
                    "or when a user wants to secure their account by ending "
                    "all other active sessions."
                ),
            },
        ],
        "tags": ["accounts", "auth", "logout", "session", "security"],
    },
    {
        "name": "Meteor.loginWithPassword",
        "module": "accounts",
        "signature": "Meteor.loginWithPassword(user, password, [callback])",
        "description": (
            "Log the user in using a password. The 'user' parameter can be "
            "a string (interpreted as a username), an object with an 'email' "
            "field, an object with a 'username' field, or an object with an "
            "'id' field. The password is the user's plaintext password, which "
            "is hashed with SHA-256 on the client before being sent to the "
            "server, so the plaintext password is never sent over the wire. "
            "On the server, the password is stored using bcrypt. "
            "The callback receives no arguments on "
            "success, or a single Error argument on failure."
        ),
        "params": [
            {
                "name": "user",
                "type": "String | Object",
                "description": (
                    "The user identifier. Pass a string to log in by username, "
                    "or an object with one of the following keys: 'email', "
                    "'username', or 'id'."
                ),
                "optional": False,
            },
            {
                "name": "password",
                "type": "String",
                "description": "The user's plaintext password. It is hashed before being sent to the server.",
                "optional": False,
            },
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Optional callback. Called with no arguments on success, "
                    "or with a single Error argument on failure."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Login with username and password",
                "code": (
                    "Meteor.loginWithPassword('johndoe', 'securePassword123', (error) => {\n"
                    "  if (error) {\n"
                    "    console.error('Login failed:', error.reason);\n"
                    "  } else {\n"
                    "    console.log('Login successful');\n"
                    "    Router.go('/dashboard');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Login using a username string. The password is hashed "
                    "with SHA-256 on the client before being sent to the server."
                ),
            },
            {
                "title": "Login with email address",
                "code": (
                    "Meteor.loginWithPassword(\n"
                    "  { email: 'john@example.com' },\n"
                    "  'securePassword123',\n"
                    "  (error) => {\n"
                    "    if (error) {\n"
                    "      if (error.reason === 'User not found') {\n"
                    "        alert('No account exists with that email address.');\n"
                    "      } else if (error.reason === 'Incorrect password') {\n"
                    "        alert('Incorrect password. Please try again.');\n"
                    "      } else {\n"
                    "        alert(`Login error: ${error.reason}`);\n"
                    "      }\n"
                    "    }\n"
                    "  }\n"
                    ");"
                ),
                "description": (
                    "Login using an email object. Handle specific error reasons "
                    "to provide useful feedback to the user."
                ),
            },
            {
                "title": "Login form handler in React",
                "code": (
                    "function LoginForm() {\n"
                    "  const [email, setEmail] = useState('');\n"
                    "  const [password, setPassword] = useState('');\n"
                    "  const [error, setError] = useState(null);\n"
                    "\n"
                    "  function handleSubmit(e) {\n"
                    "    e.preventDefault();\n"
                    "    Meteor.loginWithPassword({ email }, password, (err) => {\n"
                    "      if (err) {\n"
                    "        setError(err.reason);\n"
                    "      } else {\n"
                    "        setError(null);\n"
                    "      }\n"
                    "    });\n"
                    "  }\n"
                    "\n"
                    "  return (\n"
                    "    <form onSubmit={handleSubmit}>\n"
                    "      <input value={email} onChange={(e) => setEmail(e.target.value)} />\n"
                    "      <input type=\"password\" value={password}\n"
                    "        onChange={(e) => setPassword(e.target.value)} />\n"
                    "      {error && <p className=\"error\">{error}</p>}\n"
                    "      <button type=\"submit\">Log In</button>\n"
                    "    </form>\n"
                    "  );\n"
                    "}"
                ),
                "description": (
                    "A React login form using Meteor.loginWithPassword with "
                    "error state management."
                ),
            },
        ],
        "tags": ["accounts", "auth", "login", "password"],
    },
    {
        "name": "Accounts.createUser",
        "module": "accounts",
        "signature": "Accounts.createUser(options, [callback])",
        "description": (
            "Create a new user. On the client, this logs in as the newly "
            "created user on successful completion and returns void (results "
            "are delivered via the callback only). On the server in Meteor "
            "v3, use Accounts.createUserAsync instead, as the synchronous "
            "server path is no longer supported without Fibers. "
            "The options object must include at least one of 'username' or "
            "'email', and may include 'password' and 'profile'. The profile "
            "field is directly accessible on the user document at "
            "user.profile and is writable by the user by default. The "
            "callback on the client receives no arguments on success, or a "
            "single Error argument on failure."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "An object with the following optional fields: 'username' "
                    "(String), 'email' (String), 'password' (String), and "
                    "'profile' (Object). At least 'username' or 'email' must "
                    "be provided."
                ),
                "optional": False,
            },
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Client only. Called with no arguments on success, or "
                    "with a single Error argument on failure."
                ),
                "optional": True,
            },
        ],
        "returns": "void on the client (use Accounts.createUserAsync on the server)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Create a user on the client",
                "code": (
                    "Accounts.createUser({\n"
                    "  username: 'johndoe',\n"
                    "  email: 'john@example.com',\n"
                    "  password: 'securePassword123',\n"
                    "  profile: {\n"
                    "    firstName: 'John',\n"
                    "    lastName: 'Doe',\n"
                    "  },\n"
                    "}, (error) => {\n"
                    "  if (error) {\n"
                    "    console.error('Registration failed:', error.reason);\n"
                    "  } else {\n"
                    "    console.log('Account created and logged in');\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "On the client, Accounts.createUser creates the account "
                    "and automatically logs the user in upon success."
                ),
            },
            {
                "title": "Create a user on the server",
                "code": (
                    "// Server-side user creation (e.g., admin creating users)\n"
                    "const userId = await Accounts.createUserAsync({\n"
                    "  email: 'newuser@example.com',\n"
                    "  password: 'initialPassword',\n"
                    "  profile: { role: 'editor' },\n"
                    "});\n"
                    "\n"
                    "console.log('Created user with ID:', userId);\n"
                    "\n"
                    "// Optionally send an enrollment email\n"
                    "await Accounts.sendEnrollmentEmail(userId);"
                ),
                "description": (
                    "On the server, use Accounts.createUserAsync which "
                    "returns a Promise resolving to the new user's _id. "
                    "This is useful for admin scripts or seeding data."
                ),
            },
        ],
        "tags": ["accounts", "user", "auth", "registration", "create"],
    },
    {
        "name": "Accounts.createUserAsync",
        "module": "accounts",
        "signature": "Accounts.createUserAsync(options)",
        "description": (
            "Asynchronous version of Accounts.createUser. Returns a Promise "
            "that resolves to the newly created user's _id. This is the "
            "recommended way to create users on the server in Meteor v3, "
            "where Fibers have been removed. On the server, it does not "
            "log the user in. The options object has the same fields as "
            "Accounts.createUser: 'username', 'email', 'password', and "
            "'profile'."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "An object with the following optional fields: 'username' "
                    "(String), 'email' (String), 'password' (String), and "
                    "'profile' (Object). At least 'username' or 'email' must "
                    "be provided."
                ),
                "optional": False,
            },
        ],
        "returns": "Promise<String> (userId)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Create a user asynchronously on the server",
                "code": (
                    "Meteor.startup(async () => {\n"
                    "  const adminCount = await Meteor.users.find(\n"
                    "    { 'profile.role': 'admin' }\n"
                    "  ).countAsync();\n"
                    "\n"
                    "  if (adminCount === 0) {\n"
                    "    const adminId = await Accounts.createUserAsync({\n"
                    "      username: 'admin',\n"
                    "      email: 'admin@example.com',\n"
                    "      password: 'changeMeImmediately',\n"
                    "      profile: { role: 'admin' },\n"
                    "    });\n"
                    "\n"
                    "    console.log('Default admin created:', adminId);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Accounts.createUserAsync is the v3 async-friendly way to "
                    "create users in server startup code and async methods."
                ),
            },
            {
                "title": "Bulk user creation in a method",
                "code": (
                    "Meteor.methods({\n"
                    "  async importUsers(userList) {\n"
                    "    check(userList, [Object]);\n"
                    "\n"
                    "    const createdIds = [];\n"
                    "    for (const userData of userList) {\n"
                    "      const userId = await Accounts.createUserAsync({\n"
                    "        email: userData.email,\n"
                    "        password: userData.tempPassword,\n"
                    "        profile: { name: userData.name },\n"
                    "      });\n"
                    "      createdIds.push(userId);\n"
                    "    }\n"
                    "\n"
                    "    return createdIds;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Use Accounts.createUserAsync in async methods for bulk "
                    "user creation with proper await handling."
                ),
            },
        ],
        "tags": ["accounts", "user", "auth", "registration", "create", "async"],
    },
    {
        "name": "Accounts.setPassword",
        "module": "accounts",
        "signature": "Accounts.setPassword(userId, newPassword, [options])",
        "description": (
            "Deprecated in Meteor v3. Use Accounts.setPasswordAsync instead. "
            "Forcefully set the password for a user. This is a server-only "
            "function intended for administrative use. By default, this also "
            "logs out all existing sessions for the user (invalidates all "
            "login tokens). Set options.logout to false to keep existing "
            "sessions active. The new password is provided in plaintext and "
            "is hashed by the server before storage."
        ),
        "params": [
            {
                "name": "userId",
                "type": "String",
                "description": "The _id of the user whose password to set.",
                "optional": False,
            },
            {
                "name": "newPassword",
                "type": "String",
                "description": "The new plaintext password for the user.",
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "An options object. Supported field: 'logout' (Boolean, "
                    "default true). If true, all existing login tokens for "
                    "the user are invalidated, logging out all sessions."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": True,
        "examples": [
            {
                "title": "Admin password reset",
                "code": (
                    "Meteor.methods({\n"
                    "  async adminResetPassword(targetUserId) {\n"
                    "    check(targetUserId, String);\n"
                    "\n"
                    "    const currentUser = await Meteor.userAsync();\n"
                    "    if (!currentUser || currentUser.profile.role !== 'admin') {\n"
                    "      throw new Meteor.Error('not-authorized', 'Admin access required.');\n"
                    "    }\n"
                    "\n"
                    "    const tempPassword = Random.secret(12);\n"
                    "    await Accounts.setPasswordAsync(targetUserId, tempPassword);\n"
                    "\n"
                    "    return { tempPassword };\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Accounts.setPassword is used for admin-initiated password "
                    "resets. By default it invalidates all existing sessions."
                ),
            },
            {
                "title": "Set password without logging out other sessions",
                "code": (
                    "Accounts.setPassword(userId, 'newSecurePassword', {\n"
                    "  logout: false,\n"
                    "});"
                ),
                "description": (
                    "Pass { logout: false } to keep the user's existing "
                    "sessions active after the password change."
                ),
            },
        ],
        "tags": ["accounts", "password", "auth", "admin", "server", "deprecated"],
    },
    {
        "name": "Accounts.addEmail",
        "module": "accounts",
        "signature": "Accounts.addEmail(userId, newEmail, [verified])",
        "description": (
            "Add an email address to a user's account. The new email is "
            "added to the user's emails array. If the verified parameter is "
            "not provided or is false, the email is added as unverified. If "
            "the email address already belongs to another user, this "
            "function throws an error. This function is server-only."
        ),
        "params": [
            {
                "name": "userId",
                "type": "String",
                "description": "The _id of the user to add the email to.",
                "optional": False,
            },
            {
                "name": "newEmail",
                "type": "String",
                "description": "The new email address to add.",
                "optional": False,
            },
            {
                "name": "verified",
                "type": "Boolean",
                "description": (
                    "Whether to mark the new email as verified. Defaults to false."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Add a secondary email to a user's account",
                "code": (
                    "Meteor.methods({\n"
                    "  async addSecondaryEmail(newEmail) {\n"
                    "    check(newEmail, String);\n"
                    "\n"
                    "    const userId = this.userId;\n"
                    "    if (!userId) {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "\n"
                    "    await Accounts.addEmail(userId, newEmail);\n"
                    "    await Accounts.sendVerificationEmail(userId, newEmail);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Add an unverified email and immediately send a "
                    "verification email to confirm ownership."
                ),
            },
        ],
        "tags": ["accounts", "email", "user", "server"],
    },
    {
        "name": "Accounts.removeEmail",
        "module": "accounts",
        "signature": "Accounts.removeEmail(userId, email)",
        "description": (
            "Remove an email address from a user's account. The email is "
            "removed from the user's emails array. If the email is not "
            "found in the user's document, this function has no effect. "
            "This function is server-only."
        ),
        "params": [
            {
                "name": "userId",
                "type": "String",
                "description": "The _id of the user to remove the email from.",
                "optional": False,
            },
            {
                "name": "email",
                "type": "String",
                "description": "The email address to remove.",
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Remove an email address from a user's account",
                "code": (
                    "Meteor.methods({\n"
                    "  async removeMyEmail(emailToRemove) {\n"
                    "    check(emailToRemove, String);\n"
                    "\n"
                    "    const userId = this.userId;\n"
                    "    if (!userId) {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "\n"
                    "    const user = await Meteor.userAsync();\n"
                    "    if (user.emails.length <= 1) {\n"
                    "      throw new Meteor.Error(\n"
                    "        'last-email',\n"
                    "        'You must keep at least one email address.'\n"
                    "      );\n"
                    "    }\n"
                    "\n"
                    "    await Accounts.removeEmail(userId, emailToRemove);\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Remove a secondary email while ensuring the user always "
                    "retains at least one email address."
                ),
            },
        ],
        "tags": ["accounts", "email", "user", "server"],
    },
    {
        "name": "Accounts.verifyEmail",
        "module": "accounts",
        "signature": "Accounts.verifyEmail(token, [callback])",
        "description": (
            "Marks the email address associated with the given verification "
            "token as verified. This is a client-side function typically "
            "called when a user clicks a verification link in their email. "
            "The token is extracted from the verification URL. The callback "
            "receives no arguments on success, or a single Error argument "
            "on failure."
        ),
        "params": [
            {
                "name": "token",
                "type": "String",
                "description": "The email verification token from the verification URL.",
                "optional": False,
            },
            {
                "name": "callback",
                "type": "Function",
                "description": (
                    "Optional callback. Called with no arguments on success, "
                    "or with a single Error argument on failure."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Handle email verification from a URL",
                "code": (
                    "// Using Iron Router or Flow Router to capture the token\n"
                    "Accounts.onEmailVerificationLink((token, done) => {\n"
                    "  Accounts.verifyEmail(token, (error) => {\n"
                    "    if (error) {\n"
                    "      console.error('Verification failed:', error.reason);\n"
                    "      alert('Email verification failed. The link may have expired.');\n"
                    "    } else {\n"
                    "      console.log('Email verified successfully');\n"
                    "      alert('Your email has been verified!');\n"
                    "    }\n"
                    "    done();\n"
                    "  });\n"
                    "});"
                ),
                "description": (
                    "Use Accounts.onEmailVerificationLink to intercept "
                    "verification URLs and call Accounts.verifyEmail with "
                    "the extracted token."
                ),
            },
        ],
        "tags": ["accounts", "email", "verification", "auth"],
    },
    {
        "name": "Accounts.findUserByUsername",
        "module": "accounts",
        "signature": "Accounts.findUserByUsername(username, [options])",
        "description": (
            "Find a user by their username. Returns the full user document "
            "if found, or null if no user with the given username exists. "
            "The username comparison is case-insensitive. This is a "
            "server-only function."
        ),
        "params": [
            {
                "name": "username",
                "type": "String",
                "description": "The username to search for (case-insensitive).",
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Optional. An object with a 'fields' key (Object) "
                    "specifying which fields to include or exclude from "
                    "the returned user document."
                ),
                "optional": True,
            },
        ],
        "returns": "Object | null",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Check if a username is already taken",
                "code": (
                    "Meteor.methods({\n"
                    "  async isUsernameTaken(username) {\n"
                    "    check(username, String);\n"
                    "    const existingUser = await Accounts.findUserByUsername(username);\n"
                    "    return existingUser !== null;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Use Accounts.findUserByUsername to check username "
                    "availability before registration."
                ),
            },
            {
                "title": "Look up a user for administrative purposes",
                "code": (
                    "const user = Accounts.findUserByUsername('johndoe');\n"
                    "if (user) {\n"
                    "  console.log('Found user:', user._id, user.emails);\n"
                    "} else {\n"
                    "  console.log('User not found');\n"
                    "}"
                ),
                "description": (
                    "Retrieve the full user document by username for admin "
                    "tools or server-side logic."
                ),
            },
        ],
        "tags": ["accounts", "user", "lookup", "server", "username"],
    },
    {
        "name": "Accounts.findUserByEmail",
        "module": "accounts",
        "signature": "Accounts.findUserByEmail(email, [options])",
        "description": (
            "Find a user by their email address. Returns the full user "
            "document if found, or null if no user with the given email "
            "exists. The email comparison is case-insensitive. This is a "
            "server-only function."
        ),
        "params": [
            {
                "name": "email",
                "type": "String",
                "description": "The email address to search for (case-insensitive).",
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Optional. An object with a 'fields' key (Object) "
                    "specifying which fields to include or exclude from "
                    "the returned user document."
                ),
                "optional": True,
            },
        ],
        "returns": "Object | null",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Find a user by email for password reset",
                "code": (
                    "Meteor.methods({\n"
                    "  async requestPasswordReset(email) {\n"
                    "    check(email, String);\n"
                    "\n"
                    "    const user = await Accounts.findUserByEmail(email);\n"
                    "    if (user) {\n"
                    "      await Accounts.sendResetPasswordEmail(user._id, email);\n"
                    "    }\n"
                    "\n"
                    "    // Always return success to avoid leaking whether\n"
                    "    // the email exists in the system.\n"
                    "    return { success: true };\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Look up a user by email to trigger a password reset flow. "
                    "Always return a generic success response to prevent email "
                    "enumeration attacks."
                ),
            },
        ],
        "tags": ["accounts", "user", "lookup", "server", "email"],
    },
    {
        "name": "Accounts.sendResetPasswordEmail",
        "module": "accounts",
        "signature": "Accounts.sendResetPasswordEmail(userId, [email], [extraTokenData], [extraParams])",
        "description": (
            "Send an email with a link the user can use to reset their "
            "password. The email contains a URL with a secure token. When "
            "the user clicks the link, the Accounts.onResetPasswordLink "
            "callback fires on the client. If the 'email' parameter is "
            "provided, the reset email is sent to that specific address "
            "(which must be in the user's emails array). Otherwise, it is "
            "sent to the user's first email address. This is server-only."
        ),
        "params": [
            {
                "name": "userId",
                "type": "String",
                "description": "The _id of the user to send the reset email to.",
                "optional": False,
            },
            {
                "name": "email",
                "type": "String",
                "description": (
                    "The specific email address to send the reset link to. "
                    "Must be one of the user's registered emails. Defaults "
                    "to the user's first email if not specified."
                ),
                "optional": True,
            },
            {
                "name": "extraTokenData",
                "type": "Object",
                "description": (
                    "Additional data to include in the password reset token. "
                    "This data is available in the Accounts.onResetPasswordLink "
                    "callback."
                ),
                "optional": True,
            },
            {
                "name": "extraParams",
                "type": "Object",
                "description": (
                    "Additional URL parameters to append to the reset password link."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Send a password reset email",
                "code": (
                    "Meteor.methods({\n"
                    "  async forgotPassword(email) {\n"
                    "    check(email, String);\n"
                    "\n"
                    "    const user = await Accounts.findUserByEmail(email);\n"
                    "    if (user) {\n"
                    "      await Accounts.sendResetPasswordEmail(user._id, email);\n"
                    "    }\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Send a password reset email to the specified address. "
                    "The email contains a link with a secure one-time token."
                ),
            },
            {
                "title": "Reset email with extra token data",
                "code": (
                    "Accounts.sendResetPasswordEmail(\n"
                    "  userId,\n"
                    "  'user@example.com',\n"
                    "  { reason: 'admin-initiated' },\n"
                    "  { redirect: '/settings' }\n"
                    ");"
                ),
                "description": (
                    "Include extra data in the token and additional URL "
                    "parameters for custom reset flows."
                ),
            },
        ],
        "tags": ["accounts", "password", "email", "reset", "server"],
    },
    {
        "name": "Accounts.sendVerificationEmail",
        "module": "accounts",
        "signature": "Accounts.sendVerificationEmail(userId, [email], [extraTokenData], [extraParams])",
        "description": (
            "Send an email with a link the user can use to verify their "
            "email address. The email contains a URL with a secure token. "
            "When the user clicks the link, the "
            "Accounts.onEmailVerificationLink callback fires on the client. "
            "If the 'email' parameter is provided, the verification email "
            "is sent to that specific address. Otherwise, it is sent to "
            "the user's first unverified email address. This is server-only."
        ),
        "params": [
            {
                "name": "userId",
                "type": "String",
                "description": "The _id of the user to send the verification email to.",
                "optional": False,
            },
            {
                "name": "email",
                "type": "String",
                "description": (
                    "The specific email address to verify. Must be one of "
                    "the user's registered emails. Defaults to the first "
                    "unverified email if not specified."
                ),
                "optional": True,
            },
            {
                "name": "extraTokenData",
                "type": "Object",
                "description": (
                    "Additional data to include in the verification token."
                ),
                "optional": True,
            },
            {
                "name": "extraParams",
                "type": "Object",
                "description": (
                    "Additional URL parameters to append to the verification link."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Send verification email after user creation",
                "code": (
                    "Accounts.onCreateUser((options, user) => {\n"
                    "  if (options.profile) {\n"
                    "    user.profile = options.profile;\n"
                    "  }\n"
                    "  return user;\n"
                    "});\n"
                    "\n"
                    "// After user is created, send verification\n"
                    "Accounts.onLogin(({ user }) => {\n"
                    "  const unverifiedEmail = user.emails?.find(e => !e.verified);\n"
                    "  if (unverifiedEmail) {\n"
                    "    Accounts.sendVerificationEmail(user._id, unverifiedEmail.address);\n"
                    "  }\n"
                    "});"
                ),
                "description": (
                    "Automatically send a verification email when a user "
                    "logs in and has an unverified email address."
                ),
            },
        ],
        "tags": ["accounts", "email", "verification", "server"],
    },
    {
        "name": "Accounts.sendEnrollmentEmail",
        "module": "accounts",
        "signature": "Accounts.sendEnrollmentEmail(userId, [email], [extraTokenData], [extraParams])",
        "description": (
            "Send an email with a link the user can use to set their "
            "initial password. This is typically used when an admin creates "
            "an account for a user without setting a password. The email "
            "contains a URL with a secure token. When the user clicks the "
            "link, the Accounts.onEnrollmentLink callback fires on the "
            "client. If the 'email' parameter is provided, the enrollment "
            "email is sent to that specific address. Otherwise, it is sent "
            "to the user's first email address. This is server-only."
        ),
        "params": [
            {
                "name": "userId",
                "type": "String",
                "description": "The _id of the user to send the enrollment email to.",
                "optional": False,
            },
            {
                "name": "email",
                "type": "String",
                "description": (
                    "The specific email address to send the enrollment link to. "
                    "Must be one of the user's registered emails. Defaults "
                    "to the first email if not specified."
                ),
                "optional": True,
            },
            {
                "name": "extraTokenData",
                "type": "Object",
                "description": (
                    "Additional data to include in the enrollment token."
                ),
                "optional": True,
            },
            {
                "name": "extraParams",
                "type": "Object",
                "description": (
                    "Additional URL parameters to append to the enrollment link."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Admin creates a user and sends an enrollment email",
                "code": (
                    "Meteor.methods({\n"
                    "  async inviteUser(email, name) {\n"
                    "    check(email, String);\n"
                    "    check(name, String);\n"
                    "\n"
                    "    const currentUser = await Meteor.userAsync();\n"
                    "    if (!currentUser || currentUser.profile.role !== 'admin') {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "\n"
                    "    const userId = await Accounts.createUserAsync({\n"
                    "      email,\n"
                    "      profile: { name, role: 'member' },\n"
                    "    });\n"
                    "\n"
                    "    await Accounts.sendEnrollmentEmail(userId, email);\n"
                    "    return userId;\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Create a user without a password and send an enrollment "
                    "email so they can set their own password."
                ),
            },
        ],
        "tags": ["accounts", "email", "enrollment", "invitation", "server"],
    },
    {
        "name": "Accounts.onCreateUser",
        "module": "accounts",
        "signature": "Accounts.onCreateUser(func)",
        "description": (
            "Customize the user document created by Accounts.createUser. "
            "The callback function receives two arguments: 'options' (the "
            "options object passed to createUser) and 'user' (the default "
            "user document that Meteor would create). The callback must "
            "return the user document to be inserted into the database. "
            "Use this to add custom fields, validate user data, or modify "
            "the default user structure. Only one onCreateUser callback "
            "can be registered. This is server-only."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A function that takes (options, user) and returns the "
                    "user document to insert. The 'options' parameter is the "
                    "object passed to Accounts.createUser. The 'user' "
                    "parameter is the default user document."
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
                "title": "Add custom fields to new user documents",
                "code": (
                    "Accounts.onCreateUser((options, user) => {\n"
                    "  // Copy profile from options if provided\n"
                    "  if (options.profile) {\n"
                    "    user.profile = options.profile;\n"
                    "  }\n"
                    "\n"
                    "  // Add custom fields\n"
                    "  user.createdAt = new Date();\n"
                    "  user.roles = ['member'];\n"
                    "  user.settings = {\n"
                    "    notifications: true,\n"
                    "    theme: 'light',\n"
                    "  };\n"
                    "\n"
                    "  return user;\n"
                    "});"
                ),
                "description": (
                    "Accounts.onCreateUser lets you customize the user "
                    "document before it is inserted. You must return the "
                    "modified user document."
                ),
            },
            {
                "title": "Capture OAuth profile data",
                "code": (
                    "Accounts.onCreateUser((options, user) => {\n"
                    "  if (user.services.google) {\n"
                    "    user.profile = {\n"
                    "      name: user.services.google.name,\n"
                    "      avatar: user.services.google.picture,\n"
                    "    };\n"
                    "  } else if (user.services.github) {\n"
                    "    user.profile = {\n"
                    "      name: user.services.github.username,\n"
                    "      avatar: user.services.github.avatar_url,\n"
                    "    };\n"
                    "  } else if (options.profile) {\n"
                    "    user.profile = options.profile;\n"
                    "  }\n"
                    "\n"
                    "  return user;\n"
                    "});"
                ),
                "description": (
                    "Extract profile information from OAuth service data "
                    "and store it on the user document during creation."
                ),
            },
        ],
        "tags": ["accounts", "user", "hook", "creation", "server"],
    },
    {
        "name": "Accounts.validateNewUser",
        "module": "accounts",
        "signature": "Accounts.validateNewUser(func)",
        "description": (
            "Register a callback to validate new users before they are "
            "created. The callback receives the user document that is about "
            "to be inserted and must return true to allow creation or throw "
            "an error (or return false) to reject it. Multiple callbacks "
            "can be registered and all must pass for the user to be created. "
            "This runs before Accounts.onCreateUser — validation callbacks "
            "must pass before the user document is constructed. "
            "This is server-only."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A function that receives the proposed user document and "
                    "returns true to allow creation or throws a "
                    "Meteor.Error to reject it."
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
                "title": "Restrict registration to specific email domains",
                "code": (
                    "Accounts.validateNewUser((user) => {\n"
                    "  const email = user.emails?.[0]?.address;\n"
                    "  if (!email) {\n"
                    "    throw new Meteor.Error(\n"
                    "      'email-required',\n"
                    "      'An email address is required to register.'\n"
                    "    );\n"
                    "  }\n"
                    "\n"
                    "  const domain = email.split('@')[1];\n"
                    "  if (domain !== 'mycompany.com') {\n"
                    "    throw new Meteor.Error(\n"
                    "      'invalid-email-domain',\n"
                    "      'Registration is restricted to @mycompany.com email addresses.'\n"
                    "    );\n"
                    "  }\n"
                    "\n"
                    "  return true;\n"
                    "});"
                ),
                "description": (
                    "Reject user creation if the email domain does not match "
                    "the company domain. The error message is sent back to "
                    "the client."
                ),
            },
            {
                "title": "Validate username format",
                "code": (
                    "Accounts.validateNewUser((user) => {\n"
                    "  if (user.username && !/^[a-zA-Z0-9_]{3,20}$/.test(user.username)) {\n"
                    "    throw new Meteor.Error(\n"
                    "      'invalid-username',\n"
                    "      'Username must be 3-20 characters and contain only letters, numbers, and underscores.'\n"
                    "    );\n"
                    "  }\n"
                    "\n"
                    "  return true;\n"
                    "});"
                ),
                "description": (
                    "Multiple validateNewUser callbacks can be registered. "
                    "All must return true for the user to be created."
                ),
            },
        ],
        "tags": ["accounts", "user", "validation", "server", "security"],
    },
    {
        "name": "Accounts.validateLoginAttempt",
        "module": "accounts",
        "signature": "Accounts.validateLoginAttempt(func)",
        "description": (
            "Register a callback to validate login attempts. The callback "
            "receives an object with information about the login attempt "
            "including: type (the login service name), allowed (whether "
            "other validators passed), error (any error from previous "
            "validators), user (the user document), connection (the DDP "
            "connection), methodName, and methodArguments (Array). The "
            "callback must return true to allow the login or throw an "
            "error (or return false) to reject it. Multiple callbacks can "
            "be registered. This is server-only."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A function that receives an attempt info object and "
                    "returns true to allow login or throws an error to "
                    "reject it. The attempt object contains: type, allowed, "
                    "error, user, connection, methodName, and "
                    "methodArguments (Array)."
                ),
                "optional": False,
            },
        ],
        "returns": "Object (with stop() method)",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Require email verification before login",
                "code": (
                    "Accounts.validateLoginAttempt((attempt) => {\n"
                    "  if (!attempt.allowed) {\n"
                    "    return false;\n"
                    "  }\n"
                    "\n"
                    "  const user = attempt.user;\n"
                    "  const hasVerifiedEmail = user.emails?.some(e => e.verified);\n"
                    "\n"
                    "  if (!hasVerifiedEmail) {\n"
                    "    throw new Meteor.Error(\n"
                    "      'email-not-verified',\n"
                    "      'Please verify your email address before logging in.'\n"
                    "    );\n"
                    "  }\n"
                    "\n"
                    "  return true;\n"
                    "});"
                ),
                "description": (
                    "Prevent users from logging in until they have verified "
                    "at least one email address."
                ),
            },
            {
                "title": "Block suspended accounts from logging in",
                "code": (
                    "Accounts.validateLoginAttempt((attempt) => {\n"
                    "  if (!attempt.allowed) {\n"
                    "    return false;\n"
                    "  }\n"
                    "\n"
                    "  if (attempt.user?.suspended) {\n"
                    "    throw new Meteor.Error(\n"
                    "      'account-suspended',\n"
                    "      'Your account has been suspended. Contact support.'\n"
                    "    );\n"
                    "  }\n"
                    "\n"
                    "  return true;\n"
                    "});"
                ),
                "description": (
                    "Check custom user fields during login validation to "
                    "block suspended or banned accounts."
                ),
            },
        ],
        "tags": ["accounts", "auth", "login", "validation", "server", "security"],
    },
    {
        "name": "Accounts.onLogin",
        "module": "accounts",
        "signature": "Accounts.onLogin(func)",
        "description": (
            "Register a callback to be called after a successful login. "
            "The callback receives an object with information about the "
            "login including: type (the login service name), user (the "
            "user document), connection (the DDP connection), and "
            "methodName. On the client, the callback receives a simpler "
            "object. Multiple callbacks can be registered and are called "
            "in the order they were added. Returns an object with a stop() "
            "method to unregister the callback."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A function called after a successful login. On the "
                    "server, it receives an object with type, user, "
                    "connection, and methodName. On the client, it receives "
                    "a simpler login info object."
                ),
                "optional": False,
            },
        ],
        "returns": "Object (with stop() method)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Track last login time on the server",
                "code": (
                    "Accounts.onLogin(async ({ user }) => {\n"
                    "  await Meteor.users.updateAsync(user._id, {\n"
                    "    $set: { lastLoginAt: new Date() },\n"
                    "  });\n"
                    "});"
                ),
                "description": (
                    "Update a lastLoginAt timestamp each time a user "
                    "successfully logs in."
                ),
            },
            {
                "title": "Client-side post-login redirect",
                "code": (
                    "Accounts.onLogin(() => {\n"
                    "  const redirect = Session.get('loginRedirect') || '/dashboard';\n"
                    "  Session.set('loginRedirect', null);\n"
                    "  Router.go(redirect);\n"
                    "});"
                ),
                "description": (
                    "On the client, redirect the user to their intended "
                    "destination after a successful login."
                ),
            },
        ],
        "tags": ["accounts", "auth", "login", "hook", "event"],
    },
    {
        "name": "Accounts.onLogout",
        "module": "accounts",
        "signature": "Accounts.onLogout(func)",
        "description": (
            "Register a callback to be called after a logout. On the "
            "server, the callback receives an object with the 'user' "
            "field (the user document of the user who logged out) and "
            "'connection' (the DDP connection). On the client, the "
            "callback receives no arguments. Multiple callbacks can be "
            "registered. Returns an object with a stop() method."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A function called after a logout. On the server, "
                    "receives an object with user and connection. On the "
                    "client, receives no arguments."
                ),
                "optional": False,
            },
        ],
        "returns": "Object (with stop() method)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log user logouts on the server",
                "code": (
                    "Accounts.onLogout(({ user, connection }) => {\n"
                    "  console.log(\n"
                    "    `User ${user?.username || user?._id} logged out ` +\n"
                    "    `from IP ${connection?.clientAddress}`\n"
                    "  );\n"
                    "});"
                ),
                "description": (
                    "Track logout events on the server for audit logging "
                    "or analytics."
                ),
            },
            {
                "title": "Client-side cleanup on logout",
                "code": (
                    "Accounts.onLogout(() => {\n"
                    "  // Clear client-side state\n"
                    "  Session.clear();\n"
                    "  Router.go('/login');\n"
                    "});"
                ),
                "description": (
                    "On the client, use Accounts.onLogout to clear session "
                    "data and redirect to the login page."
                ),
            },
        ],
        "tags": ["accounts", "auth", "logout", "hook", "event"],
    },
    {
        "name": "Accounts.onLoginFailure",
        "module": "accounts",
        "signature": "Accounts.onLoginFailure(func)",
        "description": (
            "Register a callback to be called after a failed login attempt. "
            "The callback receives an object with information about the "
            "failed attempt including: type (the login service name), "
            "error (the Error that caused the failure), user (the user "
            "document if the user was found), connection (the DDP "
            "connection), and methodName. Multiple callbacks can be "
            "registered. Returns an object with a stop() method."
        ),
        "params": [
            {
                "name": "func",
                "type": "Function",
                "description": (
                    "A function called after a failed login attempt. "
                    "Receives an object with type, error, user (if found), "
                    "connection, and methodName."
                ),
                "optional": False,
            },
        ],
        "returns": "Object (with stop() method)",
        "environment": "anywhere",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Rate-limit failed login attempts",
                "code": (
                    "const failedAttempts = new Map();\n"
                    "\n"
                    "Accounts.onLoginFailure(({ connection, user, error }) => {\n"
                    "  const ip = connection?.clientAddress;\n"
                    "  if (!ip) return;\n"
                    "\n"
                    "  const attempts = failedAttempts.get(ip) || 0;\n"
                    "  failedAttempts.set(ip, attempts + 1);\n"
                    "\n"
                    "  console.warn(\n"
                    "    `Failed login attempt #${attempts + 1} from IP ${ip}: ` +\n"
                    "    `${error.reason}`\n"
                    "  );\n"
                    "\n"
                    "  // Clear after 15 minutes\n"
                    "  Meteor.setTimeout(() => {\n"
                    "    failedAttempts.delete(ip);\n"
                    "  }, 15 * 60 * 1000);\n"
                    "});"
                ),
                "description": (
                    "Track failed login attempts by IP address for security "
                    "monitoring and rate-limiting."
                ),
            },
            {
                "title": "Notify user of failed login on the client",
                "code": (
                    "Accounts.onLoginFailure(({ error }) => {\n"
                    "  console.error('Login failed:', error?.reason || 'Unknown error');\n"
                    "});"
                ),
                "description": (
                    "On the client, onLoginFailure can be used to show "
                    "notifications or log analytics events."
                ),
            },
        ],
        "tags": ["accounts", "auth", "login", "failure", "hook", "security"],
    },
    {
        "name": "Accounts.config",
        "module": "accounts",
        "signature": "Accounts.config(options)",
        "description": (
            "Set global accounts configuration options. This function must "
            "be called on both the client and the server. Options include: "
            "'sendVerificationEmail' (Boolean, automatically send a "
            "verification email on new account creation), "
            "'forbidClientAccountCreation' (Boolean, prevent "
            "Accounts.createUser from being called on the client), "
            "'restrictCreationByEmailDomain' (String or Function, restrict "
            "registration to specific email domains), "
            "'loginExpirationInDays' (Number, how long login tokens are "
            "valid, default 90 days), "
            "'oauthSecretKey' (String, encryption key for OAuth secrets in "
            "the database), "
            "'passwordResetTokenExpirationInDays' (Number, how long "
            "password reset tokens are valid, default 3 days), and "
            "'passwordEnrollTokenExpirationInDays' (Number, how long "
            "enrollment tokens are valid, default 30 days). "
            "Accounts.config is typically called once during application "
            "startup on both client and server."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Configuration object with optional fields: "
                    "'sendVerificationEmail' (Boolean), "
                    "'forbidClientAccountCreation' (Boolean), "
                    "'restrictCreationByEmailDomain' (String or Function), "
                    "'loginExpirationInDays' (Number, default 90), "
                    "'oauthSecretKey' (String), "
                    "'passwordResetTokenExpirationInDays' (Number, default 3), "
                    "'passwordEnrollTokenExpirationInDays' (Number, default 30), "
                    "'ambiguousErrorMessages' (Boolean), "
                    "'defaultFieldSelector' (Object)."
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
                "title": "Basic accounts configuration",
                "code": (
                    "Accounts.config({\n"
                    "  sendVerificationEmail: true,\n"
                    "  forbidClientAccountCreation: false,\n"
                    "  loginExpirationInDays: 30,\n"
                    "  passwordResetTokenExpirationInDays: 1,\n"
                    "  passwordEnrollTokenExpirationInDays: 14,\n"
                    "});"
                ),
                "description": (
                    "Configure Accounts to automatically send verification "
                    "emails, set login tokens to expire after 30 days, and "
                    "password reset tokens to expire after 1 day."
                ),
            },
            {
                "title": "Restrict registration by email domain",
                "code": (
                    "// Use a string for a single domain, or a function for\n"
                    "// multiple domains / custom validation logic.\n"
                    "Accounts.config({\n"
                    "  restrictCreationByEmailDomain: (email) => {\n"
                    "    const allowedDomains = ['mycompany.com', 'partner.com'];\n"
                    "    const domain = email.split('@')[1];\n"
                    "    return allowedDomains.includes(domain);\n"
                    "  },\n"
                    "  forbidClientAccountCreation: false,\n"
                    "  ambiguousErrorMessages: true,\n"
                    "});"
                ),
                "description": (
                    "Restrict account creation to specific email domains. "
                    "Pass a string (e.g., 'mycompany.com') for a single domain "
                    "or a function for custom validation logic. "
                    "Setting ambiguousErrorMessages to true prevents leaking "
                    "whether an email exists."
                ),
            },
            {
                "title": "Production security configuration",
                "code": (
                    "Accounts.config({\n"
                    "  sendVerificationEmail: true,\n"
                    "  forbidClientAccountCreation: true,\n"
                    "  loginExpirationInDays: 7,\n"
                    "  ambiguousErrorMessages: true,\n"
                    "  defaultFieldSelector: {\n"
                    "    username: 1,\n"
                    "    emails: 1,\n"
                    "    profile: 1,\n"
                    "    createdAt: 1,\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "A production-hardened configuration that prevents client "
                    "account creation, uses short login expiration, hides "
                    "user existence in error messages, and limits default "
                    "user fields exposed to Meteor.user()."
                ),
            },
        ],
        "tags": ["accounts", "configuration", "security", "setup"],
    },
    {
        "name": "Accounts.changePassword",
        "module": "accounts",
        "signature": "Accounts.changePassword(oldPassword, newPassword, [callback])",
        "description": (
            "Change the current user's password. Must be called on the client "
            "while a user is logged in. The old password is verified before "
            "setting the new one. The callback receives no arguments on "
            "success, or a single Error argument on failure."
        ),
        "params": [
            {"name": "oldPassword", "type": "String", "description": "The user's current password.", "optional": False},
            {"name": "newPassword", "type": "String", "description": "The new password to set.", "optional": False},
            {"name": "callback", "type": "Function", "description": "Optional callback. Called with no arguments on success, or with a single Error argument on failure.", "optional": True},
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Change password with error handling",
                "code": (
                    "Accounts.changePassword(currentPassword, newPassword, (error) => {\n"
                    "  if (error) {\n"
                    "    console.error('Password change failed:', error.reason);\n"
                    "  } else {\n"
                    "    console.log('Password changed successfully');\n"
                    "  }\n"
                    "});"
                ),
                "description": "Verifies the old password and sets the new one.",
            },
        ],
        "tags": ["accounts", "password", "auth", "client"],
    },
    {
        "name": "Accounts.forgotPassword",
        "module": "accounts",
        "signature": "Accounts.forgotPassword(options, [callback])",
        "description": (
            "Request a password reset email for the specified email address. "
            "This is a client-side method that sends a request to the server "
            "to generate a reset token and email it to the user. The options "
            "object must contain an 'email' field."
        ),
        "params": [
            {"name": "options", "type": "Object", "description": "An object with an 'email' (String) field specifying the email address to send the reset link to.", "optional": False},
            {"name": "callback", "type": "Function", "description": "Optional callback. Called with no arguments on success, or with a single Error argument on failure.", "optional": True},
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Request a password reset email",
                "code": (
                    "Accounts.forgotPassword({ email: 'user@example.com' }, (error) => {\n"
                    "  if (error) {\n"
                    "    console.error('Error:', error.reason);\n"
                    "  } else {\n"
                    "    alert('Check your email for a reset link.');\n"
                    "  }\n"
                    "});"
                ),
                "description": "Sends a password reset email to the specified address.",
            },
        ],
        "tags": ["accounts", "password", "reset", "email", "client"],
    },
    {
        "name": "Accounts.resetPassword",
        "module": "accounts",
        "signature": "Accounts.resetPassword(token, newPassword, [callback])",
        "description": (
            "Reset the user's password using a token received via email. This "
            "completes the password reset flow started by "
            "Accounts.forgotPassword or Accounts.sendResetPasswordEmail. "
            "Logs the user in on success. The callback receives no arguments "
            "on success, or a single Error argument on failure."
        ),
        "params": [
            {"name": "token", "type": "String", "description": "The password reset token from the reset URL.", "optional": False},
            {"name": "newPassword", "type": "String", "description": "The new password to set.", "optional": False},
            {"name": "callback", "type": "Function", "description": "Optional callback. Called with no arguments on success, or with a single Error argument on failure.", "optional": True},
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Reset password from a token URL",
                "code": (
                    "Accounts.onResetPasswordLink((token, done) => {\n"
                    "  // Show reset password UI, then:\n"
                    "  Accounts.resetPassword(token, newPassword, (error) => {\n"
                    "    if (error) {\n"
                    "      console.error('Reset failed:', error.reason);\n"
                    "    } else {\n"
                    "      console.log('Password reset and logged in');\n"
                    "    }\n"
                    "    done();\n"
                    "  });\n"
                    "});"
                ),
                "description": "Completes the password reset flow by setting a new password.",
            },
        ],
        "tags": ["accounts", "password", "reset", "auth", "client"],
    },
    {
        "name": "Accounts.onResetPasswordLink",
        "module": "accounts",
        "signature": "Accounts.onResetPasswordLink(callback)",
        "description": (
            "Register a callback to be called when the user arrives at the "
            "app via a password reset link. The callback receives two "
            "arguments: the reset token (String) and a done function that "
            "must be called when the reset UI is finished. This prevents "
            "the default Accounts UI behavior from handling the link."
        ),
        "params": [
            {"name": "callback", "type": "Function", "description": "A function(token, done) called when a password reset link is clicked. Call done() when finished.", "optional": False},
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Handle password reset links",
                "code": (
                    "Accounts.onResetPasswordLink((token, done) => {\n"
                    "  // Show a password reset form to the user\n"
                    "  Session.set('resetPasswordToken', token);\n"
                    "  // Call done() after the user submits the form\n"
                    "});"
                ),
                "description": "Intercept password reset URLs and show a custom reset UI.",
            },
        ],
        "tags": ["accounts", "password", "reset", "link", "client"],
    },
    {
        "name": "Accounts.onEnrollmentLink",
        "module": "accounts",
        "signature": "Accounts.onEnrollmentLink(callback)",
        "description": (
            "Register a callback to be called when the user arrives at the "
            "app via an enrollment link (sent by "
            "Accounts.sendEnrollmentEmail). The callback receives two "
            "arguments: the enrollment token (String) and a done function "
            "that must be called when the enrollment UI is finished."
        ),
        "params": [
            {"name": "callback", "type": "Function", "description": "A function(token, done) called when an enrollment link is clicked. Call done() when finished.", "optional": False},
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Handle enrollment links",
                "code": (
                    "Accounts.onEnrollmentLink((token, done) => {\n"
                    "  // Show initial password setup form\n"
                    "  Session.set('enrollmentToken', token);\n"
                    "  // After user sets password, call:\n"
                    "  // Accounts.resetPassword(token, password, callback);\n"
                    "  // then done();\n"
                    "});"
                ),
                "description": "Intercept enrollment URLs and show a custom password setup UI.",
            },
        ],
        "tags": ["accounts", "enrollment", "link", "client"],
    },
    {
        "name": "Accounts.onEmailVerificationLink",
        "module": "accounts",
        "signature": "Accounts.onEmailVerificationLink(callback)",
        "description": (
            "Register a callback to be called when the user arrives at the "
            "app via an email verification link (sent by "
            "Accounts.sendVerificationEmail). The callback receives two "
            "arguments: the verification token (String) and a done function "
            "that must be called when the verification UI is finished."
        ),
        "params": [
            {"name": "callback", "type": "Function", "description": "A function(token, done) called when an email verification link is clicked. Call done() when finished.", "optional": False},
        ],
        "returns": "void",
        "environment": "client",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Handle email verification links",
                "code": (
                    "Accounts.onEmailVerificationLink((token, done) => {\n"
                    "  Accounts.verifyEmail(token, (error) => {\n"
                    "    if (error) {\n"
                    "      alert('Verification failed: ' + error.reason);\n"
                    "    } else {\n"
                    "      alert('Email verified!');\n"
                    "    }\n"
                    "    done();\n"
                    "  });\n"
                    "});"
                ),
                "description": "Intercept email verification URLs and verify the email automatically.",
            },
        ],
        "tags": ["accounts", "email", "verification", "link", "client"],
    },
    {
        "name": "Accounts.setPasswordAsync",
        "module": "accounts",
        "signature": "Accounts.setPasswordAsync(userId, newPassword, [options])",
        "description": (
            "Asynchronous version of Accounts.setPassword. Forcefully set "
            "the password for a user and returns a Promise. This is the "
            "async-first replacement for the deprecated synchronous "
            "Accounts.setPassword in Meteor v3. Server-only."
        ),
        "params": [
            {"name": "userId", "type": "String", "description": "The _id of the user whose password to set.", "optional": False},
            {"name": "newPassword", "type": "String", "description": "The new plaintext password for the user.", "optional": False},
            {"name": "options", "type": "Object", "description": "Options. 'logout' (Boolean, default true) - if true, invalidates all login tokens.", "optional": True},
        ],
        "returns": "Promise<void>",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Async password reset by admin",
                "code": (
                    "await Accounts.setPasswordAsync(userId, 'newSecurePassword');"
                ),
                "description": "Asynchronously sets a user's password and invalidates their login tokens.",
            },
        ],
        "tags": ["accounts", "password", "auth", "admin", "server", "async"],
    },
    {
        "name": "Accounts.emailTemplates",
        "module": "accounts",
        "signature": "Accounts.emailTemplates",
        "description": (
            "An object with fields that customize the emails sent by "
            "Accounts.sendResetPasswordEmail, Accounts.sendEnrollmentEmail, "
            "and Accounts.sendVerificationEmail. Customizable fields include: "
            "'from' (String - the sender address), 'siteName' (String - the "
            "application name used in the subject), 'resetPassword' (Object "
            "with 'from', 'subject', 'text', and 'html' functions), "
            "'enrollAccount' (Object with 'from', 'subject', 'text', and "
            "'html' functions), and 'verifyEmail' (Object with 'from', "
            "'subject', 'text', and 'html' functions). Each template's "
            "'subject' function receives the user document. Each template's "
            "'text' and 'html' functions receive the user document and the "
            "URL the user must visit."
        ),
        "params": [],
        "returns": "Object",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Customize email templates",
                "code": (
                    "Accounts.emailTemplates.siteName = 'My App';\n"
                    "Accounts.emailTemplates.from = 'My App <no-reply@myapp.com>';\n"
                    "\n"
                    "Accounts.emailTemplates.resetPassword = {\n"
                    "  subject(user) {\n"
                    "    return `Password Reset for ${user.username}`;\n"
                    "  },\n"
                    "  text(user, url) {\n"
                    "    return `Hello ${user.username},\\n\\n`\n"
                    "      + `Click the link below to reset your password:\\n\\n`\n"
                    "      + `${url}\\n\\n`\n"
                    "      + `If you did not request this, please ignore this email.`;\n"
                    "  },\n"
                    "};"
                ),
                "description": (
                    "Customize the sender address, site name, and password "
                    "reset email template content."
                ),
            },
            {
                "title": "HTML email template for verification",
                "code": (
                    "Accounts.emailTemplates.verifyEmail = {\n"
                    "  subject(user) {\n"
                    "    return 'Verify Your Email Address';\n"
                    "  },\n"
                    "  html(user, url) {\n"
                    "    return `<h2>Welcome, ${user.username}!</h2>`\n"
                    "      + `<p>Click <a href=\"${url}\">here</a> to verify your email.</p>`;\n"
                    "  },\n"
                    "};"
                ),
                "description": (
                    "Provide an HTML template for verification emails. If "
                    "both text and html are provided, most email clients "
                    "will prefer the HTML version."
                ),
            },
        ],
        "tags": ["accounts", "email", "templates", "server", "customization"],
    },
]
