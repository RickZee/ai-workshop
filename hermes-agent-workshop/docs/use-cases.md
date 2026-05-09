# AgentMail Demo Scenarios

Run these during the 00:40–00:55 segment. Each takes ~3 minutes: send email, narrate what Hermes is doing, show the response.

---

## General & Multimedia

### 1. Image Analysis & Reply

**Setup:** Attach `assets/demo-image.jpg` (a product photo or diagram).

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: What do you see?
Body: Please describe this image and suggest how it could be used in a marketing email.
[Attach: demo-image.jpg]
```

**What Hermes does:**
1. Downloads attachment via AgentMail API
2. Passes image to Vision tool
3. Generates description + marketing copy
4. Sends reply

**Expected reply:** 2–3 paragraph description + email copy draft.

---

### 2. PDF Processing

**Setup:** Attach `assets/sample-invoice.pdf`.

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Invoice attached
Body: Can you extract the key details from this invoice and confirm receipt?
[Attach: sample-invoice.pdf]
```

**What Hermes does:**
1. Downloads PDF
2. Extracts: vendor, amount, due date, line items
3. Saves to `data/invoices/` via Filesystem MCP
4. Replies with structured summary

---

### 3. Voice Message Handling

**Setup:** Attach `assets/voice-note.mp3` (~30 sec audio).

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Voice note
Body: I recorded a quick note. Can you transcribe and summarize it?
[Attach: voice-note.mp3]
```

**What Hermes does:**
1. Downloads audio
2. Sends to transcription tool (Whisper-compatible)
3. Summarizes key points
4. Replies with transcript + summary

---

### 4. Screenshot Debugging

**Setup:** Attach `assets/error-screenshot.png` (a browser error or console log).

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Getting this error
Body: My app is throwing this error. What's wrong and how do I fix it?
[Attach: error-screenshot.png]
```

**Expected reply:** Error diagnosis + step-by-step fix.

---

### 5. Receipt & Expense Tracking

**Setup:** Attach `assets/receipt.jpg`.

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Expense receipt
Body: Please log this receipt to my expense tracker.
[Attach: receipt.jpg]
```

**What Hermes does:**
1. Extracts: vendor, date, amount, category
2. Appends to `data/expenses.csv`
3. Confirms with running monthly total

---

### 6. Video Summary

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Watch this and summarize
Body: https://www.youtube.com/watch?v=<demo-video-id>
Please summarize the key points in bullet form.
```

---

## Small & Medium Business Use Cases

### 7. Automated Customer Onboarding

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: New client signup
Body: Hi, we just signed up for your service. Our company is Acme Corp, 
we have 12 employees, and we're in the manufacturing sector. 
What do we do next?
```

**Expected:** Personalized onboarding steps, resource links, next-action checklist.

---

### 8. Invoice Processing & Follow-ups

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Invoice #2024-089 — still unpaid
Body: Following up on invoice #2024-089 sent 3 weeks ago for $4,200. 
No response from the client. What should I do?
```

**Expected:** Draft follow-up email + suggested escalation timeline.

---

### 9. Support Ticket Routing

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Can't login to my account
Body: I've been locked out since yesterday. 
I tried resetting my password but the email never arrived.
```

**What Hermes does:**
1. Classifies: account access issue → high priority
2. Creates ticket in `data/tickets/`
3. Auto-replies with ticket ID + ETA
4. (Optional) Notifies support channel via Slack MCP

---

### 10. Lead Response Automation

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Interested in your consulting services
Body: Hi, I'm the CTO at a 50-person SaaS startup. 
We're looking for AI integration consulting. 
What are your rates and availability?
```

**Expected:** Personalized reply with service overview, pricing bracket, calendar booking link.

---

### 11. Appointment Booking

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Can we schedule a call?
Body: I'd like to discuss your services. 
I'm available Tuesday or Thursday afternoon next week.
```

**What Hermes does:**
1. Checks Google Calendar (if configured)
2. Proposes 2–3 specific time slots
3. Sends calendar invite on confirmation

---

### 12. Review & Testimonial Requests

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Project complete — send review request
Body: The website project for Johnson & Sons wrapped up yesterday. 
They seemed really happy. Can you send them a review request?
```

**Expected:** Draft personalized review request email addressed to the client.

---

### 13. Supplier Communication

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Order delayed again
Body: Supplier XYZ has delayed our component order by 2 weeks for the third time. 
We need these parts by the 15th. What should I say to them?
```

**Expected:** Draft assertive but professional supplier escalation email with deadline, impact statement, and request for written commitment.

---

## Developer Tools

### 14. Error Triage

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Production error — needs investigation
Body: Getting this in our logs since the last deploy:

TypeError: Cannot read properties of undefined (reading 'userId')
    at authMiddleware (src/middleware/auth.js:42)
    at Layer.handle [as handle_request] (express/lib/router/layer.js:95)

Stack trace attached. What's wrong and what's the fix?
[Attach: error-screenshot.png]
```

**What Hermes does:**
1. Reads stack trace + screenshot
2. Identifies root cause: undefined object access before null check
3. Replies with diagnosis, specific line fix, and suggested defensive pattern

**Expected reply:** Root cause explanation + before/after code snippet + recommendation to add null guard.

---

### 15. PR Summary Request

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Summarize this PR for the team
Body: Can you write a plain-English summary of this pull request for our non-technical stakeholders?

PR title: Migrate auth from JWT to session cookies
Changes: removed jsonwebtoken dependency, added express-session, updated all auth middleware, added Redis session store, updated 14 route handlers.
```

**Expected:** 3–4 sentence summary suitable for a Slack announcement — what changed, why, what users notice (nothing, it's transparent).

---

### 16. Deploy Notification Digest

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Deploy log — summarize for standup
Body: Here's our CI/CD output from today. Please summarize what shipped, what failed, and any action items.

[paste or attach a deploy log with 3–4 builds: 2 green, 1 failed, 1 rolled back]
```

**What Hermes does:**
1. Parses build statuses
2. Identifies failures and rollback reason
3. Drafts a standup-ready bullet summary

**Expected:** ✅/❌ per deploy, one-line failure reason, suggested owner for follow-up.

---

### 17. Dependency Vulnerability Alert

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: npm audit flagged critical CVE
Body: npm audit output:

lodash  <4.17.21
Severity: critical
Prototype Pollution — https://npmjs.com/advisories/1065
Fix available: npm audit fix

We're on lodash 4.17.4. How urgent is this and what do we do?
```

**Expected:** Severity assessment, exploit risk in plain terms, exact fix command, note on whether `audit fix` is safe or requires manual review.

---

### 18. On-Call Incident Summary

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Incident report — last night's outage
Body: We had a 47-minute outage last night. Here's the timeline:

02:14 — alert fired, p99 latency > 10s
02:19 — on-call acknowledged
02:31 — identified DB connection pool exhaustion
02:41 — scaled pool size from 10 to 50
03:01 — traffic normalized

Can you write a post-mortem summary and suggest 3 action items?
```

**Expected:** Executive summary (2–3 sentences), root cause, timeline recap, 3 concrete action items (e.g. add pool exhaustion alert, automate scaling, add load test to CI).

---

## Personal Assistant

### 19. Newsletter Digest

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Morning digest
Body: Here are 5 newsletters I received this morning. Please summarize each in 2 sentences and flag anything I should actually read in full.

[paste newsletter text or forward multiple emails as body]
```

**Expected:** Numbered list, 2-sentence summary per newsletter, 1–2 flagged as "worth reading" with reason.

---

### 20. Bill & Subscription Reminder

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Help me audit my subscriptions
Body: Here's a list of recurring charges from my bank statement this month:

Netflix $15.99
Spotify $9.99
Adobe CC $54.99
Notion $16
Linear $18
Figma $45
Loom $12.50
GitHub $21
AWS $134.22
Heroku $25
Vercel $20

I want to cut $100/month. Which should I consider cancelling?
```

**Expected:** Categorized list (essential vs. optional), specific cancellation candidates with reasoning, estimated savings.

---

### 21. Travel Itinerary Builder

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Help plan my trip to Lisbon
Body: I'll be in Lisbon for 4 days in June, solo travel. I like: walkable neighborhoods, local food (not tourist traps), contemporary art, and good coffee. Budget is mid-range. Can you build a day-by-day itinerary?
```

**Expected:** 4-day plan with morning/afternoon/evening structure, specific neighborhood recommendations, 2–3 restaurant suggestions per day, 1 art/culture stop per day.

---

### 22. Email Drafting Assistant

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Help me write a difficult email
Body: I need to tell a freelancer we're not continuing their contract. They've been working with us for 8 months, the work quality has been inconsistent, and we're going in a different direction. I want to be honest but kind. Can you draft this for me?
```

**Expected:** Professional, empathetic draft. Acknowledges contributions, gives a clear reason without being harsh, clean ending. Ready to send with minimal edits.

---

### 23. Weekly Review Summarizer

**Send:**
```
To: hermes@yourdomain.agentmail.to
Subject: Weekly review — help me reflect
Body: Here's everything I worked on this week:

Mon: finished auth refactor, 3 PR reviews, team sync
Tue: debugging session (6h on payment bug), 1:1 with manager
Wed: payment bug fixed and deployed, wrote post-mortem
Thu: started new feature (user notifications), design review
Fri: half day, wrapped up notification spike, weekly retro

What were my wins, where did I lose time, and what should I prioritize next week?
```

**Expected:** 3 wins, 1–2 time sinks with observation, 3 prioritized suggestions for next week.

---

## Tips for Live Demo

- Pre-send all test emails before the session — show the replies are already waiting
- For slow demos, pre-record a 30-sec screen capture as fallback
- Keep one "surprise" scenario (attendee picks the topic) for the last 3 minutes
