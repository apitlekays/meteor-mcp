"""App configuration API entries for Meteor.js v3.4.0 mobile-config.js."""

APP_CONFIG = [
    {
        "name": "App.info",
        "module": "app_config",
        "signature": "App.info(options)",
        "description": (
            "Set metadata about your Meteor Cordova application in the "
            "mobile-config.js file. This information is used when building "
            "the mobile app and is reflected in the app store listing, "
            "the device home screen, and the system's application manager. "
            "The options object can include 'id' (the reverse-domain "
            "identifier such as 'com.example.myapp'), 'version' (the "
            "user-facing version string), 'name' (the display name), "
            "'description' (a short summary of the app), 'author' (the "
            "developer or organization name), 'email' (a contact "
            "email address), 'website' (a URL for the project), and "
            "'buildNumber' (the internal build number, distinct from "
            "the user-facing version). "
            "This function can only be called in "
            "mobile-config.js at the project root."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "An object with fields: id (String, reverse-domain "
                    "identifier), version (String, user-facing version), "
                    "name (String, display name), description (String, "
                    "short summary), author (String, developer name), "
                    "email (String, contact email), website (String, URL), "
                    "buildNumber (String, internal build number)."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "mobile-config.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Set basic app metadata",
                "code": (
                    "// mobile-config.js\n"
                    "\n"
                    "App.info({\n"
                    "  id: 'com.example.myapp',\n"
                    "  name: 'My Meteor App',\n"
                    "  version: '1.2.0',\n"
                    "  description: 'A real-time collaborative task manager',\n"
                    "  author: 'My Company',\n"
                    "  email: 'support@example.com',\n"
                    "  website: 'https://example.com',\n"
                    "});"
                ),
                "description": (
                    "Define the app's identity for app store submissions "
                    "and device display. The id field must be a unique "
                    "reverse-domain identifier that matches your app store "
                    "registration."
                ),
            },
        ],
        "tags": ["mobile", "cordova", "config", "metadata", "app-store"],
    },
    {
        "name": "App.setPreference",
        "module": "app_config",
        "signature": "App.setPreference(name, value, [platform])",
        "description": (
            "Set a Cordova preference in mobile-config.js. Preferences "
            "control various aspects of the mobile app's behavior and "
            "appearance, such as the status bar style, orientation lock, "
            "background color, and splash screen behavior. When the "
            "optional platform argument is provided, the preference is "
            "applied only to that platform ('ios' or 'android'). Without "
            "a platform, the preference applies globally. See the Apache "
            "Cordova documentation for the full list of supported "
            "preferences."
        ),
        "params": [
            {
                "name": "name",
                "type": "String",
                "description": "The Cordova preference name (e.g., 'BackgroundColor', 'Orientation').",
                "optional": False,
            },
            {
                "name": "value",
                "type": "String",
                "description": "The value for the preference.",
                "optional": False,
            },
            {
                "name": "platform",
                "type": "String",
                "description": (
                    "Optional platform to restrict the preference to. "
                    "Accepted values are 'ios' or 'android'."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "mobile-config.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Set global and platform-specific preferences",
                "code": (
                    "// mobile-config.js\n"
                    "\n"
                    "// Global preferences (apply to all platforms)\n"
                    "App.setPreference('BackgroundColor', '0xff0000ff');\n"
                    "App.setPreference('Orientation', 'portrait');\n"
                    "App.setPreference('DisallowOverscroll', 'true');\n"
                    "\n"
                    "// iOS-specific preferences\n"
                    "App.setPreference('StatusBarOverlaysWebView', 'false', 'ios');\n"
                    "App.setPreference('StatusBarBackgroundColor', '#000000', 'ios');\n"
                    "App.setPreference('StatusBarStyle', 'lightcontent', 'ios');\n"
                    "\n"
                    "// Android-specific preferences\n"
                    "App.setPreference('android-minSdkVersion', '24', 'android');\n"
                    "App.setPreference('android-targetSdkVersion', '33', 'android');\n"
                    "App.setPreference('AndroidWindowSoftInputMode', 'adjustResize', 'android');"
                ),
                "description": (
                    "Preferences without a platform argument are applied "
                    "globally. Provide 'ios' or 'android' as the third "
                    "argument to target a specific platform."
                ),
            },
        ],
        "tags": ["mobile", "cordova", "config", "preference", "ios", "android"],
    },
    {
        "name": "App.accessRule",
        "module": "app_config",
        "signature": "App.accessRule(pattern, [options])",
        "description": (
            "Define access rules in mobile-config.js to control which "
            "external URLs the Cordova app is allowed to access. By "
            "default, Cordova apps can only load content from the app's "
            "own origin. Use accessRule to whitelist domains for network "
            "requests, navigation, and intent launching. The pattern is "
            "a URL pattern with optional wildcards (e.g., 'https://*.example.com/*'). "
            "The options object supports 'type' which can be 'intent' "
            "(for Android intent URLs), 'navigation' (for in-app "
            "navigation), or left unset for general network access. "
            "Patterns without a scheme default to allowing both HTTP and HTTPS."
        ),
        "params": [
            {
                "name": "pattern",
                "type": "String",
                "description": (
                    "A URL pattern to allow access to. Supports wildcards "
                    "(e.g., 'https://*.example.com/*', 'tel:*', 'geo:*')."
                ),
                "optional": False,
            },
            {
                "name": "options",
                "type": "Object",
                "description": (
                    "Optional configuration. Supports 'type' field: "
                    "'intent' to allow Android intents, 'navigation' to "
                    "allow in-app navigation, or omit for general network "
                    "access."
                ),
                "optional": True,
            },
        ],
        "returns": "void",
        "environment": "mobile-config.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Configure access rules for API and external resources",
                "code": (
                    "// mobile-config.js\n"
                    "\n"
                    "// Allow network access to your API server\n"
                    "App.accessRule('https://api.example.com/*');\n"
                    "\n"
                    "// Allow loading images from a CDN\n"
                    "App.accessRule('https://cdn.example.com/*');\n"
                    "\n"
                    "// Allow all HTTPS traffic (less restrictive)\n"
                    "App.accessRule('https://*');\n"
                    "\n"
                    "// Allow tel: links to open the phone dialer\n"
                    "App.accessRule('tel:*', { type: 'intent' });\n"
                    "\n"
                    "// Allow mailto: links\n"
                    "App.accessRule('mailto:*', { type: 'intent' });\n"
                    "\n"
                    "// Allow navigation to an external OAuth provider\n"
                    "App.accessRule('https://accounts.google.com/*', {\n"
                    "  type: 'navigation',\n"
                    "});"
                ),
                "description": (
                    "Define which external resources the app can access. "
                    "Be as specific as possible with patterns to maintain "
                    "security. The 'intent' type is needed for Android to "
                    "handle special URL schemes."
                ),
            },
        ],
        "tags": ["mobile", "cordova", "config", "security", "whitelist", "access"],
    },
    {
        "name": "App.icons",
        "module": "app_config",
        "signature": "App.icons(icons)",
        "description": (
            "Define app icons for different platforms and screen densities "
            "in mobile-config.js. The icons argument is an object whose "
            "keys are platform-specific icon identifiers and values are "
            "file paths relative to the project root. Meteor supports "
            "icons for iOS (various sizes for iPhone, iPad, App Store) "
            "and Android (mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi densities). "
            "Icon files should be PNG format with no transparency for iOS "
            "or PNG with transparency for Android."
        ),
        "params": [
            {
                "name": "icons",
                "type": "Object",
                "description": (
                    "An object mapping platform icon identifiers to file "
                    "paths. Keys are identifiers like 'app_store' (1024x1024), "
                    "'iphone_2x' (120x120), 'iphone_3x' (180x180), "
                    "'ipad_2x' (152x152), 'android_mdpi' (48x48), "
                    "'android_hdpi' (72x72), 'android_xhdpi' (96x96), "
                    "'android_xxhdpi' (144x144), 'android_xxxhdpi' (192x192)."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "mobile-config.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Define app icons for iOS and Android",
                "code": (
                    "// mobile-config.js\n"
                    "\n"
                    "App.icons({\n"
                    "  // iOS icons\n"
                    "  app_store: 'resources/icons/ios/icon-1024.png',     // 1024x1024\n"
                    "  iphone_2x: 'resources/icons/ios/icon-120.png',     // 120x120\n"
                    "  iphone_3x: 'resources/icons/ios/icon-180.png',     // 180x180\n"
                    "  ipad_2x: 'resources/icons/ios/icon-152.png',       // 152x152\n"
                    "  ipad_pro: 'resources/icons/ios/icon-167.png',      // 167x167\n"
                    "  ios_settings_2x: 'resources/icons/ios/icon-58.png', // 58x58\n"
                    "  ios_spotlight_2x: 'resources/icons/ios/icon-80.png', // 80x80\n"
                    "\n"
                    "  // Android icons\n"
                    "  android_mdpi: 'resources/icons/android/icon-48.png',     // 48x48\n"
                    "  android_hdpi: 'resources/icons/android/icon-72.png',     // 72x72\n"
                    "  android_xhdpi: 'resources/icons/android/icon-96.png',    // 96x96\n"
                    "  android_xxhdpi: 'resources/icons/android/icon-144.png',  // 144x144\n"
                    "  android_xxxhdpi: 'resources/icons/android/icon-192.png', // 192x192\n"
                    "});"
                ),
                "description": (
                    "Provide icon files at the required sizes for each "
                    "platform. Missing sizes will be generated by scaling, "
                    "but providing exact sizes produces the best results."
                ),
            },
        ],
        "tags": ["mobile", "cordova", "config", "icons", "ios", "android", "assets"],
    },
    {
        "name": "App.launchScreens",
        "module": "app_config",
        "signature": "App.launchScreens(launchScreens)",
        "description": (
            "Define launch screen (splash screen) images for different "
            "platforms and screen sizes in mobile-config.js. The argument "
            "is an object whose keys are platform-specific screen "
            "identifiers and values are file paths relative to the "
            "project root. Launch screens are displayed while the app "
            "is loading. iOS uses storyboard-based launch screens in "
            "modern versions but still supports image-based screens. "
            "Android uses various density-based screen identifiers. "
            "Files should be PNG format."
        ),
        "params": [
            {
                "name": "launchScreens",
                "type": "Object",
                "description": (
                    "An object mapping platform screen identifiers to "
                    "file paths. Keys include iOS sizes like "
                    "'iphone5' (640x1136), 'iphone6' (750x1334), "
                    "'iphone6p_portrait' (1242x2208), "
                    "'iphoneX_portrait' (1125x2436), 'ipad_portrait_2x' "
                    "(1536x2048), and Android densities like "
                    "'android_mdpi_portrait' (320x480), "
                    "'android_hdpi_portrait' (480x800), "
                    "'android_xhdpi_portrait' (720x1280)."
                ),
                "optional": False,
            },
        ],
        "returns": "void",
        "environment": "mobile-config.js",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Define launch screens for iOS and Android",
                "code": (
                    "// mobile-config.js\n"
                    "\n"
                    "App.launchScreens({\n"
                    "  // iOS launch screens\n"
                    "  iphone5: 'resources/splash/ios/splash-640x1136.png',\n"
                    "  iphone6: 'resources/splash/ios/splash-750x1334.png',\n"
                    "  iphone6p_portrait: 'resources/splash/ios/splash-1242x2208.png',\n"
                    "  iphoneX_portrait: 'resources/splash/ios/splash-1125x2436.png',\n"
                    "  ipad_portrait_2x: 'resources/splash/ios/splash-1536x2048.png',\n"
                    "  ipad_landscape_2x: 'resources/splash/ios/splash-2048x1536.png',\n"
                    "\n"
                    "  // Android launch screens\n"
                    "  android_mdpi_portrait: 'resources/splash/android/splash-320x480.png',\n"
                    "  android_hdpi_portrait: 'resources/splash/android/splash-480x800.png',\n"
                    "  android_xhdpi_portrait: 'resources/splash/android/splash-720x1280.png',\n"
                    "  android_xxhdpi_portrait: 'resources/splash/android/splash-960x1600.png',\n"
                    "  android_xxxhdpi_portrait: 'resources/splash/android/splash-1280x1920.png',\n"
                    "});"
                ),
                "description": (
                    "Provide splash screen images at the required sizes "
                    "for each device. These are shown during app startup "
                    "before the web view has loaded."
                ),
            },
        ],
        "tags": ["mobile", "cordova", "config", "splash", "launch-screen", "ios", "android"],
    },
]
