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

## Tips for Live Demo

- Pre-send all test emails before the session — show the replies are already waiting
- For slow demos, pre-record a 30-sec screen capture as fallback
- Keep one "surprise" scenario (attendee picks the topic) for the last 3 minutes
