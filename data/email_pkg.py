"""Meteor.js Email package API data (meteor/email) for v3.4.0."""

EMAIL_PKG = [
    {
        "name": "Email.send",
        "module": "email_pkg",
        "signature": "Email.send(options)",
        "description": (
            "Synchronously sends an email message. The method connects to the mail server "
            "specified by the MAIL_URL environment variable. If MAIL_URL is not set, the "
            "email is written to standard output. In Meteor v3, Email.sendAsync is the "
            "preferred async alternative, but Email.send remains a fully supported API."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": "An object containing email parameters.",
                "optional": False,
            },
            {
                "name": "options.from",
                "type": "String",
                "optional": True,
                "description": (
                    "RFC 5322 'From' address. If not provided, uses the MAIL_FROM "
                    "environment variable or the application's default sender."
                ),
            },
            {
                "name": "options.to",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'To' address or array of addresses.",
            },
            {
                "name": "options.cc",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'Cc' address or array of addresses.",
            },
            {
                "name": "options.bcc",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'Bcc' address or array of addresses.",
            },
            {
                "name": "options.replyTo",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'Reply-To' address or array of addresses.",
            },
            {
                "name": "options.subject",
                "type": "String",
                "optional": True,
                "description": "The subject line of the email.",
            },
            {
                "name": "options.text",
                "type": "String",
                "optional": True,
                "description": "The plain-text body of the email.",
            },
            {
                "name": "options.html",
                "type": "String",
                "optional": True,
                "description": "The HTML body of the email.",
            },
            {
                "name": "options.headers",
                "type": "Object",
                "optional": True,
                "description": "Custom headers as key-value pairs to include in the email.",
            },
            {
                "name": "options.attachments",
                "type": "Object[]",
                "optional": True,
                "description": (
                    "Array of attachment objects following the Nodemailer attachment format. "
                    "Each object can include filename, content, path, contentType, and encoding."
                ),
            },
        ],
        "returns": "undefined",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Send a simple text email (sync API)",
                "code": (
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "// Email.sendAsync is the preferred async alternative\n"
                    "Email.send({\n"
                    "  from: 'no-reply@example.com',\n"
                    "  to: 'user@example.com',\n"
                    "  subject: 'Welcome!',\n"
                    "  text: 'Thanks for signing up.',\n"
                    "});"
                ),
                "description": (
                    "Sends a plain-text email synchronously. In Meteor v3, consider "
                    "using Email.sendAsync for non-blocking delivery."
                ),
            },
        ],
        "tags": ["email", "send", "mail", "smtp", "sync"],
    },
    {
        "name": "Email.sendAsync",
        "module": "email_pkg",
        "signature": "Email.sendAsync(options)",
        "description": (
            "Asynchronously sends an email message. Returns a Promise that resolves when "
            "the email has been handed off to the mail transport. This is the recommended "
            "way to send email in Meteor v3 and later, since fibers are no longer used. "
            "The method connects to the mail server specified by the MAIL_URL environment "
            "variable. If MAIL_URL is not set, the email content is written to standard "
            "output for development convenience."
        ),
        "params": [
            {
                "name": "options",
                "type": "Object",
                "description": "An object containing email parameters.",
                "optional": False,
            },
            {
                "name": "options.from",
                "type": "String",
                "optional": True,
                "description": (
                    "RFC 5322 'From' address. If not provided, uses the MAIL_FROM "
                    "environment variable or the application's default sender."
                ),
            },
            {
                "name": "options.to",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'To' address or array of addresses.",
            },
            {
                "name": "options.cc",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'Cc' address or array of addresses.",
            },
            {
                "name": "options.bcc",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'Bcc' address or array of addresses.",
            },
            {
                "name": "options.replyTo",
                "type": "String | String[]",
                "optional": True,
                "description": "RFC 5322 'Reply-To' address or array of addresses.",
            },
            {
                "name": "options.subject",
                "type": "String",
                "optional": True,
                "description": "The subject line of the email.",
            },
            {
                "name": "options.text",
                "type": "String",
                "optional": True,
                "description": "The plain-text body of the email.",
            },
            {
                "name": "options.html",
                "type": "String",
                "optional": True,
                "description": "The HTML body of the email.",
            },
            {
                "name": "options.headers",
                "type": "Object",
                "optional": True,
                "description": "Custom headers as key-value pairs to include in the email.",
            },
            {
                "name": "options.attachments",
                "type": "Object[]",
                "optional": True,
                "description": (
                    "Array of attachment objects following the Nodemailer attachment format. "
                    "Each object can include filename, content, path, contentType, and encoding."
                ),
            },
        ],
        "returns": "Promise<void>",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Send a plain-text email",
                "code": (
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "await Email.sendAsync({\n"
                    "  from: 'no-reply@example.com',\n"
                    "  to: 'user@example.com',\n"
                    "  subject: 'Welcome to Our App',\n"
                    "  text: 'Thanks for joining! We are glad to have you.',\n"
                    "});"
                ),
                "description": "Sends a plain-text email and awaits delivery confirmation.",
            },
            {
                "title": "Send an HTML email with attachments",
                "code": (
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "await Email.sendAsync({\n"
                    "  from: 'support@example.com',\n"
                    "  to: ['alice@example.com', 'bob@example.com'],\n"
                    "  cc: 'manager@example.com',\n"
                    "  subject: 'Monthly Report',\n"
                    "  html: '<h1>Report</h1><p>Please find the report attached.</p>',\n"
                    "  attachments: [\n"
                    "    {\n"
                    "      filename: 'report.pdf',\n"
                    "      path: '/tmp/report.pdf',\n"
                    "      contentType: 'application/pdf',\n"
                    "    },\n"
                    "  ],\n"
                    "});"
                ),
                "description": (
                    "Sends an HTML email to multiple recipients with a PDF attachment. "
                    "The attachments array follows the Nodemailer format."
                ),
            },
            {
                "title": "Send email inside a Meteor method",
                "code": (
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { check } from 'meteor/check';\n"
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "Meteor.methods({\n"
                    "  async sendInvitation(email, name) {\n"
                    "    // Validate inputs\n"
                    "    check(email, String);\n"
                    "    check(name, String);\n"
                    "\n"
                    "    if (!this.userId) {\n"
                    "      throw new Meteor.Error('not-authorized');\n"
                    "    }\n"
                    "\n"
                    "    await Email.sendAsync({\n"
                    "      from: 'invites@example.com',\n"
                    "      to: email,\n"
                    "      subject: `You've been invited by ${name}`,\n"
                    "      html: `<p>Hi! ${name} has invited you to join.</p>`,\n"
                    "    });\n"
                    "  },\n"
                    "});"
                ),
                "description": (
                    "Demonstrates sending an email from within a Meteor method with "
                    "authentication and input validation."
                ),
            },
        ],
        "tags": ["email", "send", "async", "mail", "smtp", "promise"],
    },
    {
        "name": "Email.hookSend",
        "module": "email_pkg",
        "signature": "Email.hookSend(hook)",
        "description": (
            "Registers a hook function that is called whenever an email is about to be "
            "sent via Email.send or Email.sendAsync. The hook receives the full email "
            "options object and can inspect, modify, or prevent the email from being sent. "
            "If the hook function returns false, the email is not sent through the default "
            "transport, allowing you to route emails through a custom provider or suppress "
            "them entirely. To allow normal sending to proceed, return the options object "
            "(possibly modified); returning true alone is not sufficient. If the hook "
            "returns undefined, normal sending proceeds unchanged. This is useful for "
            "logging outgoing emails, redirecting in development, or integrating "
            "third-party email services like SendGrid or Mailgun."
        ),
        "params": [
            {
                "name": "hook",
                "type": "Function",
                "description": (
                    "A function that receives the email options object. Return false to "
                    "prevent the default send behavior. Return the options object "
                    "(possibly modified) to allow sending to proceed. Returning "
                    "undefined also allows normal sending."
                ),
                "optional": False,
            },
        ],
        "returns": "undefined",
        "environment": "server",
        "is_reactive": False,
        "deprecated": False,
        "examples": [
            {
                "title": "Log all outgoing emails",
                "code": (
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "Email.hookSend((options) => {\n"
                    "  console.log(`Sending email to: ${options.to}`);\n"
                    "  console.log(`Subject: ${options.subject}`);\n"
                    "  // Return the options object to allow normal sending\n"
                    "  return options;\n"
                    "});"
                ),
                "description": (
                    "Logs recipient and subject for every outgoing email while still "
                    "allowing the default mail transport to deliver the message."
                ),
            },
            {
                "title": "Redirect emails in development",
                "code": (
                    "import { Meteor } from 'meteor/meteor';\n"
                    "import { Email } from 'meteor/email';\n"
                    "\n"
                    "if (Meteor.isDevelopment) {\n"
                    "  Email.hookSend((options) => {\n"
                    "    // Override the recipient so real users are not emailed\n"
                    "    options.to = 'dev-team@example.com';\n"
                    "    options.subject = `[DEV] ${options.subject}`;\n"
                    "    // Return the modified options to send via default transport\n"
                    "    return options;\n"
                    "  });\n"
                    "}"
                ),
                "description": (
                    "In development mode, redirects all outgoing email to a team inbox and "
                    "prefixes subjects with [DEV] to prevent accidental emails to real users."
                ),
            },
            {
                "title": "Use a custom email provider",
                "code": (
                    "import { Email } from 'meteor/email';\n"
                    "import sgMail from '@sendgrid/mail';\n"
                    "\n"
                    "sgMail.setApiKey(process.env.SENDGRID_API_KEY);\n"
                    "\n"
                    "Email.hookSend(async (options) => {\n"
                    "  // Route through SendGrid instead of the default SMTP transport\n"
                    "  await sgMail.send({\n"
                    "    to: options.to,\n"
                    "    from: options.from,\n"
                    "    subject: options.subject,\n"
                    "    text: options.text,\n"
                    "    html: options.html,\n"
                    "  });\n"
                    "  // Return false to prevent the default SMTP transport\n"
                    "  return false;\n"
                    "});"
                ),
                "description": (
                    "Intercepts all outgoing emails and routes them through SendGrid. "
                    "Returns false to suppress the default SMTP transport."
                ),
            },
        ],
        "tags": ["email", "hook", "intercept", "logging", "sendgrid", "mailgun", "override"],
    },
]
