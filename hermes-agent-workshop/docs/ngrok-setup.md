# ngrok Setup Guide

ngrok creates a public HTTPS tunnel to your local Hermes instance so AgentMail can deliver emails to it.

## Step 1: Create Account

1. Go to [ngrok.com](https://ngrok.com) and sign up (free)
2. After login, go to **Your Authtoken** in the dashboard
3. Copy your token

## Step 2: Install ngrok

**Mac:**
```bash
brew install ngrok/ngrok/ngrok
```

**Linux:**
```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

**Windows:** Download installer from [ngrok.com/download](https://ngrok.com/download)

## Step 3: Authenticate

```bash
ngrok config add-authtoken <your-token>
```

## Step 4: Start Tunnel

Make sure Hermes is running first (`docker compose up -d`), then:

```bash
ngrok http 3001
```

You'll see output like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:3001
```

Copy the `https://...` URL.

## Step 5: Set Webhook in AgentMail

1. AgentMail dashboard → **Inboxes** → your inbox → **Settings**
2. Paste your ngrok URL + `/webhook/email`:
   ```
   https://abc123.ngrok-free.app/webhook/email
   ```
3. Save

## Step 6: Test

Send an email to your AgentMail inbox. Hermes should reply within ~10 seconds.

Check ngrok traffic at [http://localhost:4040](http://localhost:4040) — shows all requests/responses.

Check Hermes logs:
```bash
docker compose logs -f hermes
```

## Important Notes

- **Free tier ngrok URL changes every restart.** Update AgentMail webhook each time you restart ngrok.
- Keep the ngrok terminal open while testing — closing it kills the tunnel.
- Paid ngrok plans offer static domains (no URL changes).
