# Credwork — Product Design Document
### Screen-by-Screen Reference | Full Product | v1.0

> **Purpose:** This document is the single source of truth for every screen in the Credwork app. It describes what each screen contains, what it communicates to the user, and why it exists. It does not describe layout or code — it describes meaning and content. Use this before prompting any design or frontend tool.
>
> **Colour Tokens (apply globally):**
> Primary `#111827` · Secondary `#2563EB` · Accent `#06B6D4` · Background `#F4F6FA`
>
> **Platforms:** Mobile (iOS + Android) and Web App
>
> **User Types:** Gig Worker · Domestic Worker · Household · Credwork Admin

---

## Table of Contents

### Universal Screens
- S-01 Splash Screen
- S-02 Language Select
- S-03 Role Select
- S-04 Phone + OTP Login
- S-05 Profile Setup

### Gig Worker Flow
- G-01 Home Dashboard
- G-02 Upload Bank Statement
- G-03 Processing / Scanning
- G-04 Verification Results
- G-05 Success — Income Summary
- G-06 Fraud / Error
- G-07 Certificate Preview
- G-08 Share / Export

### Domestic Worker Flow
- D-01 Home Dashboard
- D-02 Payment History
- D-03 Certificate Preview
- D-04 Share / Export

### Household Flow (ServiConnect)
- H-01 Home Dashboard
- H-02 Add Worker
- H-03 Make Payment
- H-04 Payment History (per worker)

### Global / Settings
- X-01 Notification Preferences
- X-02 Language Toggle
- X-03 Privacy + Data
- X-04 Help / FAQ

### Admin Panel
- A-01 Admin Dashboard

---

---

# UNIVERSAL SCREENS

---

## S-01 — Splash Screen

**What this screen is:**
The first thing a user sees when they open the app. It exists for two seconds maximum. It is a moment of brand trust — nothing interactive, nothing to read.

**What it contains:**
The Credwork logo, centred on the background colour. The logo should feel confident and minimal — this is not a loading screen with a progress bar, it is a brand moment. The tagline sits below the logo: *"Your work. Your proof. Your credit."* In Hindi: *"Aapka kaam. Aapka saboot. Aapka credit."* The tagline appears in whichever language was last used. On first install, it defaults to English.

**What it communicates:**
Credwork exists to give informal workers the same financial credibility as salaried employees. That is the entire emotional payload of this screen. It should feel like the app understands who the user is before they have said a single word.

**What happens after:**
Auto-advances to S-02 Language Select (first install) or directly to the user's home dashboard if they are already logged in.

**Design notes:**
No buttons. No animations that take more than 500ms. The background is off-white `#F4F6FA`. The logo uses charcoal black `#111827` for the wordmark and electric blue `#2563EB` as the accent mark or icon element. Do not make this screen feel like a loading screen.

---

## S-02 — Language Select

**What this screen is:**
A one-time preference screen shown only on first install, immediately after the splash. The user picks their preferred language for the entire app experience.

**What it contains:**
A simple, large-text choice between two options:

- **English**
- **हिंदी (Hindi)**

Each option is a large tappable card or button — not a dropdown, not a settings menu. The choice needs to be immediate and obvious for users who may not be comfortable with either language until they see both options side by side.

Above the options, a single line of text in both languages simultaneously: *"Choose your language / अपनी भाषा चुनें"* — this is the only place in the app where both languages appear in the same line. It exists so a Hindi-speaking user who cannot read the English instruction still understands what to do.

**What it communicates:**
Credwork was built for India's informal workforce, not for English-speaking urban professionals. Showing Hindi as a first-class option — not buried in settings — signals this immediately. The domestic worker from Bihar and the delivery rider from Lucknow should feel as welcome as anyone else.

**What happens after:**
Tapping either option sets the app language, saves the preference, and advances to S-03 Role Select. The language can be changed at any time from X-02 Language Toggle in settings.

**Design notes:**
Both cards are equal in visual weight. Neither should look like the "default" or "better" choice. The screen is intentionally sparse — two choices, a heading, and nothing else.

---

## S-03 — Role Select

**What this screen is:**
The screen where the user tells Credwork who they are. This selection determines which entire flow they enter and which home dashboard they see. It is permanent for a given account — a user cannot change their role after sign-up without creating a new account.

**What it contains:**
Three cards, each representing a user type:

**Card 1 — Gig Worker**
Icon: delivery bag or motorcycle (not a corporate icon)
Label: *"I'm a gig worker"* / *"Main gig worker hoon"*
Sub-label: *"Swiggy, Zomato, Rapido, Blinkit, Urban Company, and more"*
This sub-label exists specifically because the word "gig worker" may not be self-explanatory to the user. Seeing the names of apps they already work for resolves any ambiguity immediately.

**Card 2 — Domestic Worker**
Icon: a broom or household cleaning symbol (dignified, not demeaning)
Label: *"I'm a domestic worker"* / *"Main ghar mein kaam karta/karti hoon"*
Sub-label: *"Cook, cleaner, driver, caretaker"*
The icon and sub-label must be chosen with care. This user is often low-literacy and sometimes apprehensive about digital financial systems. The language must be plain, familiar, and non-bureaucratic.

**Card 3 — Household**
Icon: a house or family symbol
Label: *"I employ a domestic worker"* / *"Mere ghar mein koi kaam karta hai"*
Sub-label: *"Pay your worker and help them build their credit history"*
This sub-label is important — it reframes the household's act of using ServiConnect as something that directly benefits their worker, not just a convenience for the employer. This is a trust and adoption driver.

**What it communicates:**
This is not a generic app. It was built for exactly these three kinds of people. The role select screen should make every user feel like the app was made for them specifically.

**What happens after:**
Tapping a role saves the selection and advances to S-04 Phone + OTP Login. The selected role determines all subsequent flows.

**Design notes:**
Cards should be large enough to tap comfortably on budget Android devices with smaller screens. Avoid small text. Icons should be warm and approachable, not formal or corporate.

---

## S-04 — Phone + OTP Login

**What this screen is:**
The authentication screen. Credwork uses phone number + OTP as the only login method. No email, no password, no social login. This is a deliberate accessibility and simplicity choice — every Indian informal worker has a mobile number; far fewer have active email accounts they remember passwords to.

**What it contains:**

**Step 1 — Phone Entry:**
A single input field for a 10-digit Indian mobile number. A +91 prefix is shown but not editable — Credwork is India-only for this build. A large, clear "Send OTP" button. Below the button, a one-line reassurance: *"We'll send a 6-digit code to this number."* / *"Hum is number par ek 6-digit code bhejenge."*

**Step 2 — OTP Entry (same screen, replaces Step 1 after submission):**
Six individual input boxes for the OTP digits — not one field, six separate boxes. This is intentional: individual boxes make it easy to see which digit you're on, are easier for users with lower digital literacy, and auto-advance focus on each digit entry. A countdown timer: *"Resend in 00:30"* — after 30 seconds, a "Resend OTP" link becomes tappable. A "Change number" link below in case the user entered the wrong number.

**What it communicates:**
This login is fast, simple, and requires nothing the user doesn't already have. There is no friction around forgotten passwords. The OTP model is deeply familiar to Indian users — almost every app they use has trained them for it.

**What happens after:**
Successful OTP verification checks if this phone number has an existing account. If yes: goes directly to the user's role-appropriate home dashboard. If no: goes to S-05 Profile Setup.

**Design notes:**
The OTP boxes should be large — minimum 48x48px tap target each. Auto-read OTP from SMS on Android where permission is granted. Do not ask for the permission aggressively — request it after the OTP is sent, with a plain explanation of why.

---

## S-05 — Profile Setup

**What this screen is:**
A one-time setup screen shown only on first login, after OTP verification. Collects the minimum necessary information to personalise the experience and generate certificates. It is deliberately short — three fields only.

**What it contains:**

**Field 1 — Full Name:**
A text input. Label: *"Your full name"* / *"Aapka poora naam"*. This name will appear on income certificates, so the placeholder text should remind the user: *"As you'd like it on your certificate."* No validation beyond minimum length — do not require a specific format. Some users have single names; some have names that don't fit Western first/last name conventions.

**Field 2 — Profile Photo (optional):**
A circular image picker with a camera icon in the centre. Label: *"Add a photo (optional)"* / *"Photo lagaayein (optional)"*. The word "optional" must be visible and prominent — do not hide it. Many domestic workers and gig workers may be cautious about uploading a photo to a financial app they are using for the first time. If skipped, a default avatar using the first letter of their name is used throughout the app.

**Field 3 — City:**
A text input with autocomplete for Indian cities. Label: *"Your city"* / *"Aapka sheher"*. City is used for localisation of platform lists (e.g., Rapido is not available in all cities; this affects which VPAs are considered valid) and for certificate display. It is not used for anything the user would find intrusive.

**A "Continue" button** at the bottom. No "Skip all" option — name and city are required. Photo is the only optional field.

**What it communicates:**
Credwork needs to know who you are to issue a certificate in your name. The screen explains this implicitly through the placeholder text. It should not feel like a data collection exercise — it should feel like setting up a professional identity.

**What happens after:**
Tapping "Continue" with required fields filled saves the profile and navigates to the role-appropriate home dashboard for the first time. A brief celebratory micro-moment (a checkmark animation or a "You're all set" message) is shown before the dashboard loads. This is the user's first moment of being inside the product.

---

---

# GIG WORKER FLOW

---

## G-01 — Home Dashboard (Gig Worker)

**What this screen is:**
The central hub of the gig worker's experience in Credwork. Every session begins and ends here. It gives the worker a real-time view of their income credibility status without requiring them to do anything.

**What it contains:**

**Top Section — Identity Bar:**
The worker's name, profile photo (or initial avatar), and city. A small "Verified" badge if their identity has been confirmed via OTP. This is not a prominent hero element — it is a quiet reassurance that the app knows who they are.

**Primary Card — GigScore:**
The most visually prominent element on the screen. A circular ring/gauge showing the GigScore from 0 to 100. The ring fills clockwise, coloured in cyan `#06B6D4` for the filled portion and a light grey for the unfilled portion. Inside the ring: the numeric score in large bold type (e.g., "78") in charcoal black `#111827`. Below the number: the label (e.g., "Good") in electric blue `#2563EB`. Below the card: a single line — *"Based on 6 months of verified income"* or *"Based on X months of verified income"* depending on how much data exists. If no data yet: *"Upload your bank statement to generate your GigScore."*

**Secondary Card — Certificate Status:**
A card showing the status of the latest certificate. Three possible states:
- **Active:** Shows the certificate version number, the date it was issued, and a "View Certificate" button.
- **Pending:** Shows *"Your statement is being processed"* with a subtle loading indicator.
- **Not yet issued:** Shows *"No certificate yet — upload a bank statement to get started"* with an upload CTA.

**Income Snapshot:**
A compact horizontal row of monthly income bars — the last 6 months, each bar coloured in cyan `#06B6D4`, with the month label below (e.g., "Sep", "Oct"). If a month has zero income, the bar is present but empty (outlined only, not filled). This visual makes gaps immediately visible to the worker without requiring them to read text. No numbers are shown on this mini-chart — it is an at-a-glance pattern, not a data table. Tapping it does not go anywhere — it is informational only. The full income breakdown lives in the certificate.

**Quick Actions Row:**
Three icon-buttons in a horizontal row:
- Upload Statement (upload icon)
- View Certificate (document icon)
- Share Certificate (share icon)
Each has a label below. These are the three most common actions a gig worker takes in the app.

**Bottom Navigation Bar:**
Home (active) · Certificate · Settings

**What it communicates:**
The gig worker should be able to open the app, see their GigScore, understand their income credibility at a glance, and close it in under 10 seconds. The dashboard is a confidence screen. It should make the worker feel proud of what they have built, not confused by financial jargon.

**Design notes:**
The GigScore ring is the hero. Everything else supports it. Do not crowd the screen — if information does not serve the worker in the next 10 seconds, it does not belong on this screen. The monthly bars are a visual treat, not a financial analysis tool.

---

## G-02 — Upload Bank Statement

**What this screen is:**
The screen where the gig worker provides the raw data that Credwork uses to calculate income and issue a certificate. It is the most important functional screen in the gig worker flow.

**What it contains:**

**Header:**
*"Upload your bank statement"* / *"Apna bank statement upload karein"*
A one-line explanation below: *"We read your UPI payment history to verify your gig income. Your statement is never stored after processing."*
This reassurance line is non-negotiable. Many informal workers are deeply suspicious of apps that ask for bank documents. Being explicit that the document is not stored builds the trust required for them to proceed.

**Upload Zone:**
A large dashed-border rectangle in the centre of the screen. Inside: a cloud-upload icon, and the text *"Tap to select your PDF"* / *"PDF select karne ke liye tap karein"*. Below the zone: *"Accepted format: PDF only. Max size: 10MB."*

When a file is selected, the upload zone transforms: it shows the file name, file size, and a green checkmark. A "Remove" link appears in case the user wants to swap the file.

**Supported Banks Section:**
A collapsed accordion or a small scrollable chip row showing logos or names of supported banks: SBI, HDFC, ICICI, Axis, Kotak, Yes Bank, Bank of Baroda, Canara, and others. This section exists to answer the question the user will definitely have: *"Will my bank work?"* Label: *"We support statements from these banks."* A small note: *"Statement must cover at least 3 months of transactions."*

**How to get your PDF section:**
A collapsed "?" or "Help" toggle. When expanded, it shows 3 steps specific to the most common banks: how to download a statement PDF from the mobile banking app. This is critical — many gig workers have never downloaded their bank statement before. Step-by-step instructions in plain language (and Hindi) reduce abandonment at this step dramatically.

**A prominent "Start Scan" button** at the bottom, disabled until a file is selected.

**What it communicates:**
This screen needs to do two things simultaneously: make the upload feel easy and make it feel safe. The reassurance copy and the supported-banks list address both. The help section removes the "I don't know how to get a PDF" blocker.

**What happens after:**
Tapping "Start Scan" navigates to G-03 Processing / Scanning with the uploaded file.

---

## G-03 — Processing / Scanning

**What this screen is:**
The screen shown while Credwork's backend is running the fraud stack, VPA extraction, monthly aggregation, and GigScore calculation. It is a waiting screen, but it should not feel passive — it should feel like something important is happening on the user's behalf.

**What it contains:**

**Animated Header:**
A subtle pulsing animation — the Credwork logo or a document-scan visual. Not a generic spinner. The animation should feel purposeful, like a scanner moving across a document.

**Live Checklist:**
A vertical list of processing steps, each with an icon and a label. Steps complete one by one as the backend processes them. Completed steps show a filled cyan checkmark. The current step shows a spinning cyan indicator. Pending steps are greyed out.

The steps, in order:
1. *"Checking document authenticity"* — fraud metadata check
2. *"Reading your transactions"* — PDF parsing
3. *"Finding your gig payments"* — VPA extraction
4. *"Calculating monthly income"* — aggregation
5. *"Computing your GigScore"* — stability scoring
6. *"Generating your certificate"* — certificate creation

Each step has a plain-language sub-label below it. For example, step 1 sub-label: *"Making sure this statement hasn't been altered."* Step 3 sub-label: *"Looking for payments from Swiggy, Zomato, Rapido, and other platforms."*

**Time Estimate:**
Below the checklist: *"This usually takes 20–40 seconds."* This sets expectation and reduces anxiety. If processing takes longer than 60 seconds, the message updates to: *"Taking a bit longer than usual — almost there."*

**What it communicates:**
The worker has just handed over their bank statement. They are in a moment of vulnerability and uncertainty. This screen must communicate that something real and useful is happening, that the app has not frozen, and that the wait is worthwhile. The live checklist turns a passive wait into an active, legible process.

**What happens after:**
On success: navigates to G-04 Verification Results.
On fraud detection: navigates to G-06 Fraud / Error.
On system error: navigates to G-06 Fraud / Error with an error-specific message.

**Design notes:**
Do not use a generic loading spinner. Do not say "Please wait." The checklist animation is the entire emotional design of this screen. Each step completing is a small moment of progress.

---

## G-04 — Verification Results

**What this screen is:**
The screen shown immediately after processing completes. It tells the worker exactly what was found and what was flagged before committing to certificate generation. This screen exists to be honest — even when the results are complicated.

**What it contains:**

**Summary Banner:**
A coloured banner at the top — green if everything passed, amber if some items need attention, red if the document was rejected. Text inside the banner is direct: *"Everything looks good"* / *"Some items need your attention"* / *"We couldn't verify this statement."*

**Passed Items Section:**
A list of what verified successfully. Each item has a green checkmark icon, a label, and a value. Examples:
- *Statement period:* October 2024 – March 2025
- *Platforms detected:* Swiggy, Zomato, Blinkit
- *Months with income:* 5 of 6
- *Document authenticity:* Passed

**Flagged Items Section (if any):**
Only shown if there are flags. Each flagged item has an amber warning icon and a plain-language explanation of what was flagged and what it means. Examples:
- *"March 2025 had no gig income detected. This month will be counted as zero."*
- *"We noticed income that may be from multiple earners on this account. A manual review will be requested."*
- *"One month's income was significantly higher than your average. This has been noted in your record."*

Flags do not block certificate generation unless they represent a hard fraud failure. The purpose of this screen is to be transparent, not to gatekeep.

**Gap Notice (if applicable):**
If the statement reveals a gap in the worker's history (e.g., a missing month in the middle of their record), a specific callout box appears: *"We noticed a gap in [Month]. If you have a statement covering this period, uploading it will strengthen your GigScore."* This is not a blocker — it is an opportunity.

**A "Generate My Certificate" button** at the bottom, in electric blue. This is a confirmation action — the worker is choosing to proceed with the data as shown.

**A "Cancel" or "Start Over" link** below the button, in case the worker wants to upload a different document.

**What it communicates:**
Honesty and transparency. The worker sees exactly what Credwork found and exactly what is being used to build their certificate. Nothing is hidden. Gaps and flags are explained in plain language, not technical error messages. This screen is a trust-builder — even when the results are imperfect.

**What happens after:**
Tapping "Generate My Certificate" navigates to G-05 Success. Tapping "Cancel" returns to G-02 Upload.

---

## G-05 — Success — Income Summary

**What this screen is:**
The reward screen. The certificate has been generated. This is the moment Credwork was built for — a gig worker holding a verified proof of income that they can take to any lender.

**What it contains:**

**Celebratory Moment:**
A brief animation — a checkmark drawing itself, or a certificate icon appearing with a subtle scale-up. The word *"Verified!"* in large type, in electric blue `#2563EB`. Below it: *"Your income certificate is ready."*

**Income Summary Card:**
A prominent card showing:
- **Average monthly income:** e.g., ₹18,500/month — in large bold type
- **GigScore:** The ring/gauge, same visual as the home dashboard, showing the updated score
- **GigScore label:** e.g., "Good"
- **Certificate period:** e.g., October 2024 – March 2025
- **Platforms verified:** Swiggy · Zomato · Blinkit (shown as small chips/tags)
- **Certificate version:** v2 (if this is an update to a previous certificate)

If the GigScore improved from the previous certificate, a small delta indicator appears: *"Up from 71 — your consistency is improving."* This is a motivational moment that rewards workers who upload regularly.

**What this certificate means — one line:**
*"You can show this to any bank or lender as proof of your income."* / *"Koi bhi bank ya lender ko ye income proof dikha sakte hain."*

This single line is critical. Many gig workers have never had a document that a formal institution would accept as income proof. This is the first time they are being told explicitly that they now have one.

**Two primary action buttons:**
- *"View Full Certificate"* — navigates to G-07 Certificate Preview
- *"Share Certificate"* — navigates to G-08 Share / Export

**A secondary link:** *"Back to Home"* — returns to G-01 without viewing or sharing the certificate.

**What it communicates:**
Pride. Empowerment. Clarity. The worker has done something real and valuable. The screen should feel like a moment of arrival. The income summary is presented as an achievement, not a bureaucratic output.

**Design notes:**
This is the highest-emotion screen in the app. The animation, the GigScore ring, and the income number together should feel like a certificate ceremony. Do not underdesign this screen.

---

## G-06 — Fraud / Error

**What this screen is:**
The screen shown when processing fails — either because the fraud stack detected a problem with the document, or because a system error occurred. It is the most delicate screen in the app to design, because the user's reaction to this screen will determine whether they trust Credwork or abandon it.

**What it contains:**

**Two distinct versions of this screen, based on failure type:**

---

**Version A — Document Issue (Fraud Flag or Unreadable PDF)**

Header: *"We couldn't verify this statement"* — in charcoal, not red. Avoid alarmist colour choices on this screen.

A plain-language explanation of what happened, specific to the failure type. The language must be non-accusatory. Examples:

- *"This PDF appears to have been edited after it was generated by your bank. Please download a fresh statement directly from your bank app and upload it again."*
- *"We weren't able to read this PDF clearly. It may be a scanned image rather than a digital statement. Please try downloading a fresh PDF from your bank app."*
- *"This statement doesn't seem to contain transactions from any recognised gig platforms. Make sure you're uploading your primary bank account — the one your gig payments arrive in."*

Below the explanation: a *"What to do next"* section — 2 to 3 numbered steps guiding the user to resolve the specific issue. These steps are different for each failure type and must be written in plain language.

A *"Try Again"* button (primary) and a *"Contact Support"* link (secondary).

---

**Version B — System Error**

Header: *"Something went wrong on our end"*
Body: *"This isn't because of your document — we had a technical issue. Your file has not been stored. Please try uploading again in a few minutes."*
A *"Try Again"* button and a timestamp of when to try again if applicable.

---

**What it communicates:**
The most important thing this screen communicates is: *this is not your fault, and here is exactly what to do.* A gig worker who uploads a document and sees an error message they don't understand will leave and never come back. A gig worker who sees a clear explanation and a clear next step will try again. Every word on this screen must be chosen to preserve the user's dignity and confidence.

**Design notes:**
Do not use red as the dominant colour on this screen. Use amber for warnings, and use charcoal for informational failures. Reserve red only for cases where the document has been rejected due to confirmed tampering — and even then, the copy must remain non-accusatory and give the user a path forward.

---

## G-07 — Certificate Preview

**What this screen is:**
A full in-app view of the income certificate. The worker can read their certificate exactly as a lender would see it. This screen is both functional (reviewing the document) and emotional (seeing your official credential).

**What it contains:**

**A rendered certificate view** — not a raw PDF viewer, but a styled in-app rendering of the certificate content. The certificate is rendered using Credwork's design system colours and typography. It contains:

- Credwork logo and "Income Verification Certificate" header
- Worker name and profile photo (or initial avatar)
- Certificate issue date and version number (e.g., "v2 — Issued 1 April 2025")
- Certificate period (e.g., "Income period: October 2024 – March 2025")
- Average monthly income (large, prominent)
- Monthly income breakdown — a table or list: Month | Platform(s) | Amount
- Platforms verified (with platform names listed)
- GigScore: the numeric value, the label, and a brief explanation of what the score means
- A verification statement: *"This certificate was generated by Credwork based on verified bank statement data. Income figures reflect actual UPI credit transactions from recognised gig platforms."*
- A unique certificate ID (e.g., CW-2025-00847) for lender verification

**Below the rendered certificate:**
A *"Download PDF"* button and a *"Share"* button. Both navigate to G-08 Share / Export.

**A "Certificate History" link** — shows all previously issued certificates for this worker, with version numbers and dates. Each historical certificate can be viewed in this same preview screen.

**What it communicates:**
This is what a lender will see. The worker needs to feel confident that this document looks professional and credible. The certificate preview should feel like a real financial document — not a screenshot, not a basic summary card.

**Design notes:**
The certificate rendering must look polished. It will be the image a worker shares on WhatsApp with a bank manager. Every element — typography, spacing, colour — must convey legitimacy. The certificate ID is important — it allows a lender to call Credwork and verify the document is real.

---

## G-08 — Share / Export

**What this screen is:**
The screen from which the worker distributes their certificate to lenders, employers, or anyone else they need to prove their income to.

**What it contains:**

**Header:** *"Share your certificate"* / *"Apna certificate share karein"*

**Share Options — presented as large, tappable cards:**

- **WhatsApp** — the most important option for India. Label: *"Send via WhatsApp"*. Tapping this opens WhatsApp's native share sheet with the certificate PDF pre-attached. This is the primary use case — a gig worker sending their certificate to a bank manager or an NBFC agent over WhatsApp.
- **Download PDF** — saves the certificate PDF to the device's local storage / downloads folder. Label: *"Save to phone"* / *"Phone mein save karein"*.
- **Email** — opens the device's email app with the certificate attached. Label: *"Send by email"*.
- **Copy link** — copies a unique, shareable Credwork verification link to the clipboard. Label: *"Copy verification link"*. When a lender opens this link, they see the certificate on a Credwork-hosted page and can verify its authenticity.

**Certificate Preview Thumbnail:**
A small thumbnail of the certificate is shown at the top of this screen so the worker can confirm they are sharing the right document before sending it.

**A note below the share options:**
*"Your certificate contains your verified income data. Only share it with people you trust."* / *"Yeh certificate sirf bharosemand logon ke saath share karein."*

**What it communicates:**
This screen is the product fulfilling its promise. The worker has worked, the income has been verified, and now they can prove it to the world. The WhatsApp option being first and largest reflects where this action will happen in the real world — not in email threads, but in WhatsApp chats.

**Design notes:**
WhatsApp must be the visually dominant option. Its brand green can be used on the button icon only (not as a full button background). Every other option is secondary. The copy-link option is for digitally confident users — it should be present but not pushed.

---

---

# DOMESTIC WORKER FLOW

---

## D-01 — Home Dashboard (Domestic Worker)

**What this screen is:**
The domestic worker's central hub. Unlike the gig worker who uploads documents, the domestic worker's income record is built entirely from payments made by their household through ServiConnect. Their dashboard reflects this: they are a recipient and a credential-holder, not a document uploader.

**What it contains:**

**Top Section — Identity Bar:**
Name, photo (or initial avatar), and a "Verified Worker" badge if their OTP has been confirmed. This badge is meaningful for domestic workers — it signals that Credwork has confirmed they are a real, identifiable person, which strengthens the certificate's credibility.

**Primary Card — GigScore:**
Identical visual treatment to the gig worker's GigScore card — circular ring, numeric score, label, and data source note. For domestic workers, the data source note reads: *"Based on X months of verified payments from your employer(s)."* If no payments have been received yet, the card shows: *"Your employer needs to register and make your first payment on Credwork to start building your record."* This is an important message — it tells the domestic worker what they need to do (ask their household to sign up) in plain terms.

**Current Household Section:**
A card showing the household currently linked to the worker — household name (or address), start date, and current monthly salary. If the worker has multiple households (e.g., works for two families), each is shown as a separate card in a scrollable row.

**Payment Status:**
A line showing: *"Last payment: ₹3,500 on 1 March 2025 — Verified"* or *"This month's payment: Pending"*. The worker can see at a glance whether they have been paid for the current month through the platform.

**Certificate Status Card:**
Same logic as the gig worker dashboard — active, pending, or not yet issued.

**Quick Actions:**
- View Certificate
- Share Certificate
- Payment History

**Bottom Navigation:** Home · Certificate · Settings

**What it communicates:**
The domestic worker's dashboard is about confirmation and confidence. They cannot take action to add income data themselves — their data comes from their employer. So the dashboard is about showing them what exists, how their record is building, and what their GigScore means. The "Pending payment" signal is particularly important — it lets the worker know if they should follow up with their household.

---

## D-02 — Payment History (Domestic Worker)

**What this screen is:**
A chronological log of all payments the domestic worker has received through Credwork, from all households. It is the domestic worker's equivalent of a payslip history.

**What it contains:**

**Filter Row at the top:** Filter by household (if multiple), filter by payment type (salary / bonus / advance), filter by date range.

**Payment List:**
Each payment is a list item showing:
- Date
- Amount (e.g., ₹3,500)
- Payment type badge: "Salary" / "Bonus" / "Advance" — each in a different colour chip (cyan for salary, blue for bonus, amber for advance)
- Household name or identifier
- Status: "Verified" (green) — all payments processed through Razorpay are auto-verified. There is no "unverified" state for ServiConnect payments unless the webhook simulation failed.

**Monthly Totals:**
Payments are grouped by month. Each month has a subtle header showing the month and the total received that month. This lets the worker see their monthly income at a glance without having to do mental arithmetic.

**Gap Indicator:**
If a month has no payments, it appears in the list with a grey "No payment recorded" label and a note: *"If you were paid in cash this month, ask your employer to record it on Credwork."* This is the worker-facing version of the gap notification — it tells them about the gap without accusing anyone.

**What it communicates:**
This is the domestic worker's financial record. Many of them have never had a documented history of what they were paid and when. Seeing every payment listed, verified, and dated is a new and meaningful experience. The screen should feel like a dignified financial record — clean, clear, and trustworthy.

---

## D-03 — Certificate Preview (Domestic Worker)

**What this screen is:**
Identical in function and visual structure to G-07 Certificate Preview, adapted for domestic worker data.

**Key differences from the gig worker certificate:**

The income source is described as *"Verified household payments via ServiConnect"* rather than *"Verified UPI transactions from gig platforms."*

The platform logos are replaced by household identifiers (household name + city).

The income verification statement reads: *"This certificate was generated by Credwork based on verified Razorpay payment records from registered households. Payment amounts reflect actual salary, bonus, and advance transactions."*

**Demo note (internal):** For the hackathon, payments are confirmed via a simulated Razorpay webhook. The certificate language reflects what the live system will say — no "simulated" language appears anywhere in the user-facing certificate.

Everything else — the certificate ID, the GigScore ring, the version history, the download and share options — is identical to the gig worker certificate.

---

## D-04 — Share / Export (Domestic Worker)

**What this screen is:**
Identical to G-08 Share / Export in every way. The certificate content is different (ServiConnect-sourced) but the sharing mechanics, options, and visual design are the same.

The WhatsApp option remains the primary action. The copy-link option is available. The reassurance copy about only sharing with trusted parties is present.

---

---

# HOUSEHOLD FLOW (SERVICONNECT)

---

## H-01 — Home Dashboard (Household)

**What this screen is:**
The household employer's central screen. Their job in Credwork is simple: register their worker, make payments on time, and help the worker build a verified income record. The dashboard reflects this role.

**What it contains:**

**Header:**
Household name (e.g., "Sharma Household" or the user's name) and city. No GigScore — households are not income earners, they are income issuers.

**Worker Cards:**
A scrollable list of domestic workers linked to this household. Each worker card shows:
- Worker name and photo (or initial avatar)
- Role (cook, cleaner, driver, etc. — entered during the Add Worker flow)
- Current monthly salary: ₹X,XXX/month
- Last payment date and status
- A *"Pay Now"* button — a direct CTA to initiate this month's payment for that worker

The "Pay Now" button is the primary action on this screen. It should be prominent and unmissable. For a household with two workers, there will be two "Pay Now" buttons — one per worker.

**Payment Reminder Banner (conditional):**
If the current date is within 5 days of the worker's typical payment date and payment hasn't been made, a banner appears at the top of the screen: *"[Worker name]'s salary is due in X days."* This is a nudge, not a notification — it lives on the screen itself to catch the household's attention when they open the app.

**Quick Actions:**
- Add New Worker
- Payment History (all workers)

**Bottom Navigation:** Home · Workers · Settings

**What it communicates:**
The household's role is to be a reliable, documented employer. The dashboard makes it easy to see which workers are due for payment and to act on it immediately. The UX philosophy here is: make the right thing (paying on time, on-platform) the easiest thing.

---

## H-02 — Add Worker

**What this screen is:**
The screen where a household links a new domestic worker to their Credwork account. This is the handshake that connects the worker's identity to the household's payment record.

**What it contains:**

**Field 1 — Worker's Phone Number:**
*"Enter your worker's mobile number"* / *"Worker ka mobile number daalen."* This is how Credwork links the household to an existing worker account. If the worker already has a Credwork account, their profile is pulled and shown for confirmation. If they don't have an account yet, the system sends them an SMS invitation: *"[Household name] has added you as their worker on Credwork. Download the app to receive your payments and build your income record."*

**Field 2 — Worker's Role:**
A dropdown or chip selector: Cook · Cleaner · Driver · Caretaker · Full-time help · Other. If "Other" is selected, a free-text field appears.

**Field 3 — Monthly Salary:**
A number input for the agreed monthly salary in INR. Label: *"Monthly salary (₹)"*. A note below: *"This is the amount that will be sent to your worker each month. You can update it later."*

**Field 4 — Payment Date:**
A date picker (1st to 28th of the month) for the typical payment date. This feeds the payment reminder logic on the household dashboard.

**A "Confirm and Add Worker" button.** Before saving, a summary card shows the household a preview of what they have entered — worker name (if account found), role, salary, payment date — so they can review before confirming.

**What it communicates:**
Adding a worker is a commitment — a household is agreeing to make recorded, on-platform payments. The confirmation summary makes this feel deliberate, not accidental. The SMS invitation to unregistered workers is a growth mechanic built into a functional flow.

---

## H-03 — Make Payment

**What this screen is:**
The screen where the household initiates a salary payment to their domestic worker. This is the core transactional moment of ServiConnect — the payment that creates the worker's income record.

**What it contains:**

**Payment Summary Card at the top:**
- Worker name and photo
- Payment type — pre-selected as "Salary" but changeable to "Bonus" or "Advance" via a segmented control
- Amount — pre-filled with the worker's monthly salary amount. Editable for bonus/advance payments. For salary, the amount should be the agreed monthly figure — changing it triggers a confirmation: *"This is different from [Worker]'s usual salary of ₹X,XXX. Are you sure?"*
- Month — pre-filled with the current month. For salary payments, this is not editable. Backdating is handled separately.

**Payment Method:**
A line showing: *"Payment via Razorpay UPI"* with the household's linked UPI ID or bank account. A *"Change payment method"* link if they need to update it.

**Worker receives:**
A summary of what the worker will see: *"[Worker name] will receive ₹3,500 and a payment confirmation on Credwork."*

**A "Pay ₹X,XXX" button** — large, in electric blue. This is the confirmation action. The button text includes the amount to prevent accidental payments.

**What it communicates:**
This payment does two things: it pays the worker, and it creates a verified income record. The screen frames both. The worker receiving a confirmation is mentioned explicitly — this reinforces that the payment is being tracked and documented, not just transferred.

**What happens after:**
On successful payment (simulated Razorpay webhook in demo): navigates to a brief success state showing *"Payment sent! [Worker name]'s record has been updated."* Then returns to H-01 Home Dashboard. On failure: shows a payment failure message with a retry option.

**Demo note (internal):** The Razorpay payout is simulated via a webhook in the demo build. The UI behaves identically to the live implementation.

---

## H-04 — Payment History (Household View)

**What this screen is:**
A log of all payments made by this household to all their workers. The household's equivalent of an expense ledger for domestic worker payments.

**What it contains:**

**Filter Row:** Filter by worker, payment type, date range.

**Payment List:**
Each entry shows date, worker name, amount, payment type badge, and status (Verified / Failed). Grouped by month with monthly totals.

**Total paid this month** — a summary line at the top showing total outgoing payments in the current month across all workers.

**Export option:** A *"Download full history"* link that generates a PDF summary of all payments — useful for household tax records or if the household ever needs to verify employment history.

**What it communicates:**
The household is running a small, informal employer operation. Giving them a clean, exportable payment history treats them accordingly — like a responsible employer who keeps records. This also builds their confidence that Credwork is a legitimate financial record-keeping tool, not just an app.

---

---

# GLOBAL / SETTINGS SCREENS

---

## X-01 — Notification Preferences

**What this screen is:**
The screen where all user types manage what Credwork is allowed to notify them about.

**What it contains:**

A list of notification categories, each with an on/off toggle:

**For Gig Workers:**
- *"Certificate updated"* — when a new certificate version is generated
- *"GigScore changed"* — when the score moves by more than 5 points
- *"Upload reminder"* — monthly reminder to upload a new bank statement
- *"Processing complete"* — when an uploaded document has finished scanning

**For Domestic Workers:**
- *"Payment received"* — when a household payment is confirmed
- *"Certificate updated"* — when a new certificate version is generated
- *"Payment due reminder"* — when this month's payment hasn't arrived yet

**For Households:**
- *"Payment due reminder"* — reminder before a worker's payment date
- *"Worker joined Credwork"* — when an invited worker creates their account
- *"Payment confirmed"* — confirmation that a payment was successfully processed

Below the toggles, a one-line note: *"We will never send promotional notifications. All notifications are about your account activity only."*

**What it communicates:**
Credwork respects the user's attention. Informal workers and households are not the target of a growth marketing funnel — they are using a financial tool. Notifications are limited to genuinely useful account events. The reassurance line makes this explicit.

---

## X-02 — Language Toggle

**What this screen is:**
A persistent, accessible settings screen where the user can switch the app language at any time. Not a modal, not a popup — a real settings screen they can navigate to whenever they want.

**What it contains:**

Two options, identical in visual treatment to S-02 Language Select:
- **English**
- **हिंदी (Hindi)**

The currently active language has a filled checkmark. Tapping the other option switches the entire app immediately and live — no restart required, no confirmation dialog. The switch is instant.

A note below: *"Your language preference is saved to your account and will apply on all devices."*

**What it communicates:**
Language is not a one-time setup choice. A domestic worker who chose English at setup because they didn't understand the Hindi option on a shared phone should be able to switch without any friction. The live switch (no restart) is an important usability detail.

---

## X-03 — Privacy + Data

**What this screen is:**
The screen that tells the user exactly what data Credwork holds about them, how it is used, and what they can do about it. This screen exists to comply with India's Digital Personal Data Protection (DPDP) Act and to build user trust.

**What it contains:**

**What we store — a plain-language list:**
- Your name, phone number, and city
- Your profile photo (if provided)
- Your monthly income entries (derived from your bank statement — not the statement itself)
- Your certificates (all versions, permanently)
- Your payment history (domestic workers and households)

**What we don't store:**
- Your full bank statement PDF (it is processed and discarded)
- Your bank account number
- Your UPI PIN or password

**How your data is used:**
A short paragraph: *"Your income data is used only to generate your income certificate. We do not sell your data to lenders, advertisers, or any third party. Certificates shared with lenders are shared by you, not by us."*

**Delete my account:**
A *"Request account deletion"* button. When tapped, a confirmation dialog explains: *"Deleting your account will remove your profile and income data from Credwork. Certificates already shared with lenders cannot be recalled from their systems. Are you sure?"* If confirmed, the deletion is processed and the user is logged out.

**Download my data:**
A *"Download all my data"* button that generates a JSON or PDF export of everything Credwork holds on the user. This is a DPDP compliance requirement.

**What it communicates:**
Informal workers are often wary of apps that want their financial data. This screen addresses that wariness directly and honestly. The explicit statement that the bank statement PDF is not stored is one of the most important trust signals in the entire app. Put it at the top.

---

## X-04 — Help / FAQ

**What this screen is:**
The in-app support and help resource. Especially important for domestic workers and low-literacy users who may not be comfortable calling a support number or navigating an external website.

**What it contains:**

**Search bar at the top:** *"What do you need help with?"* / *"Kya jaanna chahte hain?"* — a live-search filter across all FAQ content.

**FAQ Categories — collapsible sections:**

**For Gig Workers:**
- How do I download a bank statement PDF?
- Which banks are supported?
- Why was my document flagged?
- What is GigScore and how is it calculated?
- How do I share my certificate with a bank?
- Can I upload statements from multiple banks?

**For Domestic Workers:**
- How do I get my employer to register on Credwork?
- What if my employer paid me in cash?
- How do I view my payment history?
- How do I share my certificate with a lender?

**For Households:**
- How do I add a worker?
- How do I change my worker's salary?
- What if I paid in cash and forgot to use the app?
- Can I add more than one worker?

**Contact Support:**
At the bottom: a *"Talk to us"* button that opens WhatsApp with a pre-filled message: *"Hi Credwork, I need help with [topic]."* This is the support channel — not email, not a ticket form. WhatsApp is where the users are.

**What it communicates:**
Help is available, immediate, and in the user's language. The WhatsApp support channel is consistent with how the target user communicates. FAQ answers should be written in the simplest possible language — assume the reader has never used a financial app before. Assume they may have someone else read the answer to them.

**Design notes:**
Every FAQ answer should be 3 lines or fewer. Use numbered steps when instructions are required. Avoid all financial or technical jargon. Test every answer by reading it aloud — if it sounds like a legal document, rewrite it.

---

---

# ADMIN PANEL

---

## A-01 — Admin Dashboard

**What this screen is:**
A web-only screen accessible only to Credwork team members with admin credentials. It exists for the hackathon demo to give the team real-time visibility into system health, upload processing, and data integrity. It is not a user-facing product screen.

**What it contains:**

**System Health — top row of stat cards:**
- Total accounts created (broken down: gig workers / domestic workers / households)
- Uploads processed in the last 24 hours
- Certificates issued (total and in the last 24 hours)
- Fraud flags triggered (total and in the last 24 hours)
- Processing errors (total and in the last 24 hours)

Each stat card shows the current count and a delta from the previous 24-hour period (up or down arrow with the change number).

**Recent Uploads Table:**
A live-updating table of the most recent 20 uploads, showing: timestamp, worker ID (anonymised in production, visible in admin), upload status (Processing / Passed / Flagged / Failed), fraud check result, and GigScore generated (if applicable). Clicking a row expands it to show the full processing log for that upload.

**Fraud Flags Queue:**
A list of uploads that passed the automated fraud check but were flagged for manual review (e.g., income difference > 15% between two uploads of the same period). Each row shows: worker ID, flag reason, date, and a *"Review"* button. The review screen (not a separate screen for the hackathon — inline expansion) shows the before/after figures and allows an admin to approve or reject the upload with a note.

**Certificate Version Log:**
A list of the most recently generated certificates with version numbers, worker IDs, and generation timestamps. Useful for verifying that the versioning system is working correctly during demo.

**ServiConnect Payment Log:**
A list of the most recent simulated Razorpay webhook events — payment amount, household ID, worker ID, timestamp, and webhook status (Received / Processed / Failed). This confirms the simulated payment pipeline is functioning end-to-end.

**What it communicates:**
The admin panel communicates to judges and the team that Credwork is not a prototype with hardcoded data — it is a working system processing real uploads in real time. The fraud flags queue and the certificate version log demonstrate that the business logic described in the framework document is actually implemented and running.

**Design notes:**
The admin panel uses the same colour system as the rest of the app (charcoal, blue, cyan, off-white) but is information-dense in a way the user-facing screens are not. Tables, numbers, and status badges dominate. This is acceptable for an admin tool — the audience is the Credwork team, not informal workers.

---

---

## Appendix — Screen Inventory Summary

| Screen ID | Screen Name | User Type | Platform |
|---|---|---|---|
| S-01 | Splash Screen | All | Mobile + Web |
| S-02 | Language Select | All | Mobile + Web |
| S-03 | Role Select | All | Mobile + Web |
| S-04 | Phone + OTP Login | All | Mobile + Web |
| S-05 | Profile Setup | All | Mobile + Web |
| G-01 | Home Dashboard | Gig Worker | Mobile + Web |
| G-02 | Upload Bank Statement | Gig Worker | Mobile + Web |
| G-03 | Processing / Scanning | Gig Worker | Mobile + Web |
| G-04 | Verification Results | Gig Worker | Mobile + Web |
| G-05 | Success — Income Summary | Gig Worker | Mobile + Web |
| G-06 | Fraud / Error | Gig Worker | Mobile + Web |
| G-07 | Certificate Preview | Gig Worker | Mobile + Web |
| G-08 | Share / Export | Gig Worker | Mobile + Web |
| D-01 | Home Dashboard | Domestic Worker | Mobile + Web |
| D-02 | Payment History | Domestic Worker | Mobile + Web |
| D-03 | Certificate Preview | Domestic Worker | Mobile + Web |
| D-04 | Share / Export | Domestic Worker | Mobile + Web |
| H-01 | Home Dashboard | Household | Mobile + Web |
| H-02 | Add Worker | Household | Mobile + Web |
| H-03 | Make Payment | Household | Mobile + Web |
| H-04 | Payment History | Household | Mobile + Web |
| X-01 | Notification Preferences | All | Mobile + Web |
| X-02 | Language Toggle | All | Mobile + Web |
| X-03 | Privacy + Data | All | Mobile + Web |
| X-04 | Help / FAQ | All | Mobile + Web |
| A-01 | Admin Dashboard | Credwork Admin | Web Only |

**Total screens: 26**

---

*This document is the complete design source of truth for Credwork v1.0. Every screen, every content element, and every copy decision documented here was made with one user in mind: an Indian informal worker who has never had a document that a bank would accept. Build for them.*
