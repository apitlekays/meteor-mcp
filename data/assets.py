"""Meteor.js Assets API data for v3.4.0."""

ASSETS = [
    {
        "name": "Assets.getText",
        "module": "assets",
        "signature": "Assets.getText(assetPath)",
        "description": (
            "Synchronously retrieves the contents of a static server asset as a UTF-8 "
            "encoded string. Static assets are files placed in the 'private' directory of "
            "a Meteor application. In Meteor v3, fibers have been removed, making this "
            "synchronous API deprecated. Use Assets.getTextAsync instead for non-blocking "
            "asset retrieval."
        ),
        "params": [
            {
                "name": "assetPath",
                "type": "String",
                "description": (
                    "The path of the asset relative to the application's 'private' "
                    "directory. For example, 'templates/welcome.txt' reads the file at "
                    "'private/templates/welcome.txt'."
                ),
                "optional": False,
            },
        ],
        "returns": "String - The contents of the asset file as a UTF-8 string.",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Read a text asset (deprecated sync API)",
                "code": (
                    "// Deprecated in Meteor v3 -- use Assets.getTextAsync instead\n"
                    "const template = Assets.getText('email-templates/welcome.txt');\n"
                    "console.log(template);"
                ),
                "description": (
                    "Reads a text file from private/email-templates/welcome.txt "
                    "synchronously. Deprecated in Meteor v3; migrate to getTextAsync."
                ),
            },
        ],
        "tags": ["assets", "text", "file", "read", "private", "deprecated", "sync"],
    },
    {
        "name": "Assets.getTextAsync",
        "module": "assets",
        "signature": "Assets.getTextAsync(assetPath)",
        "description": (
            "Asynchronously retrieves the contents of a static server asset as a UTF-8 "
            "encoded string. Returns a Promise that resolves with the file contents. "
            "Static assets are files placed in the 'private' directory of a Meteor "
            "application. This is the recommended way to read text assets in Meteor v3 "
            "and later."
        ),
        "params": [
            {
                "name": "assetPath",
                "type": "String",
                "description": (
                    "The path of the asset relative to the application's 'private' "
                    "directory. For example, 'data/config.json' reads the file at "
                    "'private/data/config.json'."
                ),
                "optional": False,
            },
        ],
        "returns": "Promise<String> - Resolves with the contents of the asset as a UTF-8 string.",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Read a JSON configuration file",
                "code": (
                    "const raw = await Assets.getTextAsync('config/settings.json');\n"
                    "const settings = JSON.parse(raw);\n"
                    "console.log('App settings:', settings);"
                ),
                "description": (
                    "Reads a JSON file from private/config/settings.json and parses it "
                    "into a JavaScript object."
                ),
            },
            {
                "title": "Load an email template",
                "code": (
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "async function sendWelcomeEmail(user) {\n"
                    "  const htmlTemplate = await Assets.getTextAsync(\n"
                    "    'email-templates/welcome.html'\n"
                    "  );\n"
                    "  const personalizedHtml = htmlTemplate.replace(\n"
                    "    '{{name}}',\n"
                    "    user.profile.name\n"
                    "  );\n"
                    "\n"
                    "  await Email.sendAsync({\n"
                    "    from: 'no-reply@example.com',\n"
                    "    to: user.emails[0].address,\n"
                    "    subject: 'Welcome!',\n"
                    "    html: personalizedHtml,\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "Loads an HTML email template from the private directory, performs "
                    "simple placeholder replacement, and sends the personalized email."
                ),
            },
            {
                "title": "Read a CSV data file inside a Meteor method",
                "code": (
                    "import { Meteor } from 'meteor/meteor';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async importSeedData() {\n"
                    "    const csv = await Assets.getTextAsync('seed/products.csv');\n"
                    "    const lines = csv.split('\\n').filter(Boolean);\n"
                    "    const headers = lines[0].split(',');\n"
                    "\n"
                    "    for (const line of lines.slice(1)) {\n"
                    "      const values = line.split(',');\n"
                    "      const doc = Object.fromEntries(\n"
                    "        headers.map((h, i) => [h.trim(), values[i]?.trim()])\n"
                    "      );\n"
                    "      await Products.insertAsync(doc);\n"
                    "    }\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Reads a CSV file from private/seed/products.csv and inserts each row "
                    "as a document into a MongoDB collection."
                ),
            },
        ],
        "tags": ["assets", "text", "file", "read", "private", "async", "promise"],
    },
    {
        "name": "Assets.getBinary",
        "module": "assets",
        "signature": "Assets.getBinary(assetPath)",
        "description": (
            "Synchronously retrieves the contents of a static server asset as an EJSON "
            "Binary (Uint8Array). Static assets are files placed in the 'private' "
            "directory of a Meteor application. In Meteor v3, fibers have been removed, "
            "making this synchronous API deprecated. Use Assets.getBinaryAsync instead."
        ),
        "params": [
            {
                "name": "assetPath",
                "type": "String",
                "description": (
                    "The path of the asset relative to the application's 'private' "
                    "directory."
                ),
                "optional": False,
            },
        ],
        "returns": "EJSON.Binary (Uint8Array) - The raw binary contents of the asset file.",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Read a binary file (deprecated sync API)",
                "code": (
                    "// Deprecated in Meteor v3 -- use Assets.getBinaryAsync instead\n"
                    "const imageData = Assets.getBinary('images/logo.png');\n"
                    "console.log('Size:', imageData.length, 'bytes');"
                ),
                "description": (
                    "Reads a binary file from private/images/logo.png synchronously. "
                    "Deprecated in Meteor v3; migrate to getBinaryAsync."
                ),
            },
        ],
        "tags": ["assets", "binary", "file", "read", "private", "deprecated", "sync", "buffer"],
    },
    {
        "name": "Assets.getBinaryAsync",
        "module": "assets",
        "signature": "Assets.getBinaryAsync(assetPath)",
        "description": (
            "Asynchronously retrieves the contents of a static server asset as an EJSON Binary (Uint8Array). "
            "Returns a Promise that resolves with the raw binary data. Static assets are "
            "files placed in the 'private' directory of a Meteor application. This is the "
            "recommended way to read binary assets in Meteor v3 and later."
        ),
        "params": [
            {
                "name": "assetPath",
                "type": "String",
                "description": (
                    "The path of the asset relative to the application's 'private' "
                    "directory."
                ),
                "optional": False,
            },
        ],
        "returns": "Promise<EJSON.Binary>",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Read and serve a binary asset",
                "code": (
                    "import { WebApp } from 'meteor/webapp';\n"
                    "\n"
                    "WebApp.connectHandlers.use('/api/logo', async (req, res) => {\n"
                    "  const imageBuffer = await Assets.getBinaryAsync('images/logo.png');\n"
                    "  res.writeHead(200, {\n"
                    "    'Content-Type': 'image/png',\n"
                    "    'Content-Length': imageBuffer.length,\n"
                    "  });\n"
                    "  res.end(imageBuffer);\n"
                    "});"
                ),
                "description": (
                    "Reads a PNG image from the private directory and serves it via a "
                    "custom HTTP endpoint using WebApp."
                ),
            },
            {
                "title": "Compute a hash of a binary asset",
                "code": (
                    "import { createHash } from 'crypto';\n"
                    "\n"
                    "async function getAssetChecksum(assetPath) {\n"
                    "  const buffer = await Assets.getBinaryAsync(assetPath);\n"
                    "  const hash = createHash('sha256').update(buffer).digest('hex');\n"
                    "  return hash;\n"
                    "}\n"
                    "\n"
                    "// Usage\n"
                    "const checksum = await getAssetChecksum('firmware/v2.bin');\n"
                    "console.log('SHA-256:', checksum);"
                ),
                "description": (
                    "Reads a binary asset and computes its SHA-256 checksum for integrity "
                    "verification."
                ),
            },
        ],
        "tags": ["assets", "binary", "file", "read", "private", "async", "promise", "buffer"],
    },
    {
        "name": "Assets.absoluteFilePath",
        "module": "assets",
        "signature": "Assets.absoluteFilePath(assetPath)",
        "description": (
            "Returns the absolute filesystem path to a static server asset on disk. This "
            "is useful when you need to pass a file path to a third-party library that "
            "requires a filesystem path rather than file contents. Static assets are files "
            "placed in the 'private' directory of a Meteor application. Note that in some "
            "deployment environments the absolute path may differ from development."
        ),
        "params": [
            {
                "name": "assetPath",
                "type": "String",
                "description": (
                    "The path of the asset relative to the application's 'private' "
                    "directory."
                ),
                "optional": False,
            },
        ],
        "returns": "String - The absolute filesystem path to the asset.",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Get the absolute path to a font file",
                "code": (
                    "const fontPath = Assets.absoluteFilePath('fonts/custom.ttf');\n"
                    "console.log('Font located at:', fontPath);\n"
                    "// e.g. /app/bundle/programs/server/assets/app/fonts/custom.ttf"
                ),
                "description": (
                    "Resolves the absolute path of a font file stored in the private "
                    "directory. Useful for passing to libraries that require a file path."
                ),
            },
            {
                "title": "Use absolute path with a PDF generation library",
                "code": (
                    "import PDFDocument from 'pdfkit';\n"
                    "import fs from 'fs';\n"
                    "\n"
                    "function generateReport() {\n"
                    "  const logoPath = Assets.absoluteFilePath('images/logo.png');\n"
                    "  const fontPath = Assets.absoluteFilePath('fonts/Roboto.ttf');\n"
                    "\n"
                    "  const doc = new PDFDocument();\n"
                    "  doc.pipe(fs.createWriteStream('/tmp/report.pdf'));\n"
                    "  doc.font(fontPath);\n"
                    "  doc.image(logoPath, 50, 50, { width: 100 });\n"
                    "  doc.text('Monthly Report', 160, 70);\n"
                    "  doc.end();\n"
                    "}"
                ),
                "description": (
                    "Uses absoluteFilePath to resolve asset paths for a PDF generation "
                    "library that needs filesystem paths for fonts and images."
                ),
            },
        ],
        "tags": ["assets", "path", "file", "private", "filesystem", "absolute"],
    },
]
