# AgentMail Setup Guide

How to create an AgentMail account and configure an inbox for Hermes.

## Step 1: Create Account

1. Go to [agentmail.to](https://agentmail.to)
2. Sign up with email or GitHub
3. Verify email address

## Step 2: Create an Inbox

1. Dashboard → **Inboxes** → **New Inbox**
2. Choose subdomain: `hermes` (gives you `hermes@yourdomain.agentmail.to`)
3. Click **Create**

Copy the full inbox address — you'll need it for `.env`:
```
AGENTMAIL_INBOX=hermes@yourdomain.agentmail.to
```

## Step 3: Get API Key

1. Dashboard → **Settings** → **API Keys**
2. Click **Generate New Key**
3. Copy the key (shown once)

Add to `.env`:
```
AGENTMAIL_API_KEY=am_...
```

## Step 4: Configure Webhook

AgentMail calls your webhook when email arrives.

1. Dashboard → **Inboxes** → your inbox → **Settings**
2. **Webhook URL** field → enter your Hermes endpoint:
   ```
   http://<your-host>:3000/webhook/email
   ```

### Local development (ngrok)

If running locally, expose port 3000:
```bash
ngrok http 3000
```

Copy the HTTPS URL (e.g. `https://abc123.ngrok.io`) and use:
```
https://abc123.ngrok.io/webhook/email
```

Paste into AgentMail webhook field → **Save**.

## Step 5: Verify

Send a test email to your inbox address. AgentMail dashboard → **Logs** should show the incoming message and webhook delivery.

## Troubleshooting

**Webhook shows "failed" in logs**
- Check ngrok is running and URL matches
- Verify Hermes container is up: `docker-compose ps`
- Check Hermes logs: `docker-compose logs -f hermes`

**"Invalid API key" errors**
- Re-copy key from dashboard (no extra spaces)
- Confirm key is in `.env` and container was restarted after edit

**Emails not appearing in inbox**
- Check spam folder of sender
- Confirm inbox address is typed correctly
