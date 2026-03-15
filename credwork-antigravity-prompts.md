# Credwork — Antigravity + Stitch Prompt Reference
### Remaining Screens: Domestic Worker · Household · Settings · Admin
### (D-01, D-02, D-03, D-04, H-01, H-02, H-03, H-04, X-01, X-02, X-03, X-04, A-01)

---

## HOW TO USE THIS FILE

1. At the start of every Antigravity session, paste the MASTER CONTEXT BLOCK first.
2. Then paste the prompt for the screen you are generating — one screen at a time.
3. If Antigravity forgets context mid-session, paste the Master Context Block again.
4. Do not skip the Master Context Block. Every screen depends on it.
5. Generate in this order:
   H-01 → H-02 → H-03 → H-04 → D-01 → D-02 → D-03 → D-04 → X-01 → X-02 → X-03 → X-04 → A-01

---

---

# MASTER CONTEXT BLOCK
### Paste this at the start of every session, before any screen prompt.

---

```
You are designing screens for Credwork — a mobile and web app that gives India's informal 
workforce (gig workers and domestic workers) a verified income certificate they can take to 
any bank or lender, exactly like a salaried employee would. The app also serves households 
who employ domestic workers and allows them to make recorded salary payments that build the 
worker's income history.

The three user types are:
- Gig Worker: delivery riders, platform workers (Swiggy, Zomato, Rapido, Blinkit, Urban Company)
- Domestic Worker: cooks, cleaners, drivers, caretakers
- Household: families who employ domestic workers

LANGUAGE: All screens are in English only. Do not add Hindi copy to any screen 
unless explicitly instructed. Language selection happens at onboarding — the app 
renders the chosen language at runtime. Design in English.

COLOUR SYSTEM — use only these four tokens. No other colours permitted:
- Primary (text, headings, borders at rest):          #111827  Charcoal Black
- Secondary (buttons, links, CTAs, active states):    #2563EB  Electric Blue
- Accent (GigScore ring, data indicators, badges):    #06B6D4  Cyan
- Background (all screen backgrounds, card fills):    #F4F6FA  Off-White

Disabled states only: #111827 at 30% opacity for text, #E5E7EB for backgrounds.
No pure black (#000000). No pure white (#FFFFFF). No other colours.

TYPOGRAPHY RULES:
- All headings: bold, #111827
- All body text: regular weight, #111827
- All CTAs and primary action buttons: #2563EB background, white text
- All data indicators, badges, accent labels: #06B6D4
- All links and secondary actions: #2563EB, no underline

LOGO ASSETS — three files are in the /logo folder. Use them exactly as provided.
Do not recreate, redraw, or reinterpret any part of the logo:
- logo/credwork-logo-full.png   → full lockup, icon + wordmark (splash, login)
- logo/credwork-wordmark.png    → wordmark only (screen headers, nav bars)
- logo/credwork-icon.png        → icon only (app icon, compact spaces)

TONE:
- Plain language. Never bureaucratic. Never corporate.
- Warm but professional. Financial credential tool, not a consumer game.
- Every word should be understandable by someone who primarily uses WhatsApp and UPI.

GIGSCORE: Credwork's proprietary income stability score, 0–100.
Always displayed as three elements together: circular ring in #06B6D4 + numeric 
score + label (Excellent / Good / Moderate / Low).
Never show GigScore as just a number or just a label. Always all three together.

PLATFORM: Mobile (iOS + Android) primary. Web responsive secondary.
Minimum tap target size: 48x48px on all interactive elements.
Design for budget Android devices with smaller screens first.

NAVIGATION:
- Gig Worker and Domestic Worker bottom nav: Home · Certificate · Settings
- Household bottom nav: Home · Workers · Settings
- Active item: #2563EB icon + label. Inactive: #111827 at 50% opacity.
- Admin panel: web only, no bottom nav — use a left sidebar instead.

PAYMENT BADGE COLOURS (for payment type chips):
- Salary: #06B6D4 background at 15% opacity, #06B6D4 text
- Bonus: #2563EB background at 15% opacity, #2563EB text
- Advance: amber — #F59E0B background at 15% opacity, #F59E0B text
Note: amber is the only permitted colour outside the core four tokens, 
used exclusively for Advance payment badges.

SIMULATED RAZORPAY NOTE (internal, never shown to users):
The Razorpay payout in the Household flow is simulated via a backend webhook 
for the hackathon demo. The UI behaves identically to the live implementation. 
No "simulated" or "demo" language appears anywhere in the user-facing screens.
```

---

---

# SCREEN PROMPTS — HOUSEHOLD FLOW

---

## H-01 — Home Dashboard (Household)
### Generate this screen first.

---

```
SCREEN: H-01 — Home Dashboard (Household)
PURPOSE: The household employer's central hub. Their entire job in Credwork is 
to pay their domestic worker on time, on platform. The dashboard should make 
"Pay Now" the most obvious thing to do when they open the app. Everything else 
is secondary to that one action.

This screen has ONE STATE. Scrollable if content exceeds screen height.

---

HEADER BAR:
  Left: logo/credwork-wordmark.png — small, approximately 30% screen width
  Right: circular profile avatar (initial-based if no photo)
  Background: #F4F6FA, no border or shadow

IDENTITY ROW (below header):
  Household name in bold: "Sharma Household"
  Below: city — "New Delhi"
  No badge — households are not "verified" in the same way workers are
  This row is not interactive

---

PAYMENT REMINDER BANNER (conditional — shown when payment is due within 5 days):
  A full-width banner, background #2563EB at 8% opacity, border-left 3px #2563EB
  Left: a bell icon in #2563EB
  Text: "Priya's salary is due in 3 days."
  Bold, #111827
  Right: a small "Pay Now" link in #2563EB
  This banner sits below the identity row, above the worker cards
  It is a nudge — not an alarm. Calm colour treatment, not red.

---

WORKER CARDS SECTION:
  Label above: "Your workers" — small, bold, #111827

  Each worker is a full-width card, border 1.5px #111827, rounded corners, #F4F6FA background
  Show TWO worker cards as demo data

  WORKER CARD STRUCTURE:
    Top row of card:
      Left: circular worker avatar (initial-based) — 40px
      Next to avatar: worker name in bold — "Priya Devi"
      Below name: role in small regular — "Cook · Full-time"
      Right side of top row: payment status pill
        If paid this month: "Paid ✓" — #06B6D4 background at 15%, #06B6D4 text
        If unpaid: "Due" — #F59E0B background at 15%, #F59E0B text

    Divider: 1px #E5E7EB

    Bottom row of card:
      Left side:
        Label: "Monthly salary" — very small, #111827 at 60% opacity
        Value: "₹3,500 / month" — small, bold, #111827
      Centre:
        Label: "Last payment" — very small, #111827 at 60% opacity
        Value: "1 Mar 2025" — small, regular, #111827
      Right side:
        A "Pay Now" button — pill shape, #2563EB background, white text, small bold
        This button is the primary CTA of the entire screen
        Navigates to H-03 Make Payment for this specific worker

  DEMO WORKER CARD 1:
    Name: Priya Devi · Role: Cook · Full-time
    Status: Due (unpaid this month)
    Salary: ₹3,500/month · Last payment: 1 Feb 2025

  DEMO WORKER CARD 2:
    Name: Ramesh Singh · Role: Driver
    Status: Paid ✓ (paid this month)
    Salary: ₹8,000/month · Last payment: 1 Mar 2025
    "Pay Now" button is greyed/disabled for this card since month is already paid

---

QUICK ACTIONS ROW (below worker cards):
  Two equal-width icon-buttons in a horizontal row
  Background: #F4F6FA, border 1.5px #111827, rounded corners

  Action 1: Plus icon — label "Add Worker"
    Navigates to H-02 Add Worker
  Action 2: History/clock icon — label "Payment History"
    Navigates to H-04 Payment History

  Icons: #2563EB. Labels: #111827, small.

---

BOTTOM NAVIGATION BAR:
  Three items: Home · Workers · Settings
  Home is active — #2563EB
  Workers and Settings inactive — #111827 at 50% opacity

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No GigScore display — households are not income earners
- No certificate section — certificates belong to workers, not households
- No payment amount summary or expense tracker as a hero element
- No notifications feed

BACKGROUND: #F4F6FA
The "Pay Now" button on each worker card is the undisputed primary action.
Make it impossible to miss.
```

---

---

## H-02 — Add Worker
### Generate this screen second.

---

```
SCREEN: H-02 — Add Worker
PURPOSE: The household links a new domestic worker to their account by entering 
the worker's phone number. This is the handshake that connects the worker's 
identity to the household's payment record. If the worker already has a Credwork 
account, their profile is pulled automatically. If not, they receive an SMS invite.

This screen has TWO STATES: Search state and Confirmation state.

---

HEADER:
  Back arrow (left) — returns to H-01
  Centre title: "Add a worker" — bold, #111827
  No right element

---

STATE 1 — PHONE SEARCH:

SCREEN SUB-HEADING:
  "Enter your worker's mobile number to link them to your account."
  Regular, #111827 at 70% opacity, below the header

FIELD 1 — WORKER PHONE NUMBER:
  Label: "Worker's mobile number"
  Input field with +91 prefix (same treatment as login screen)
  Placeholder: "98765 43210"
  Below field, small helper text: 
  "If they're already on Credwork, their profile will appear automatically."
  Helper text: #111827 at 50% opacity

FIELD 2 — WORKER ROLE:
  Label: "Their role in your home"
  A horizontal scrollable chip selector — not a dropdown
  Chips: Cook · Cleaner · Driver · Caretaker · Full-time help · Other
  Default: none selected
  Selected chip: #2563EB background, white text
  Unselected chip: #F4F6FA background, border 1.5px #111827, #111827 text
  If "Other" is selected, a text input appears below the chips: "Describe their role"

FIELD 3 — MONTHLY SALARY:
  Label: "Monthly salary (₹)"
  Number input, placeholder: "3500"
  Below field: "This is the amount sent to your worker each month. You can update it later."
  Small, #111827 at 50% opacity

FIELD 4 — PAYMENT DATE:
  Label: "Usual payment date"
  A horizontal row of date chips — 1st through 28th, scrollable
  Show dates 1, 5, 7, 10, 15, 20, 25, 28 as quick options
  Selected date chip: #2563EB background, white text
  Below chips: "We'll remind you before this date each month."
  Small, #111827 at 50% opacity

SEARCH BUTTON:
  Full width, "Find Worker" — #2563EB background, white text
  Disabled until phone number is 10 digits AND role is selected

---

STATE 2 — WORKER FOUND / CONFIRMATION:
(Shown after a valid phone number is entered and matched to an existing account)

A worker profile card slides in below the phone field:
  Border 1.5px #06B6D4 (cyan border — signals a live Credwork account found)
  Background: #F4F6FA
  Left: circular avatar with worker's initial
  Centre:
    Worker name in bold: "Priya Devi"
    "Active Credwork account" in small #06B6D4
  Right: a green checkmark icon in #06B6D4

Below the card: all four fields remain filled as entered
A summary preview below the fields:
  "You are about to add:"
  Worker: Priya Devi
  Role: Cook
  Salary: ₹3,500/month
  Payment date: 1st of every month
  Each line small, #111827, label at 60% opacity / value bold

CONFIRM BUTTON:
  Full width, "Confirm and Add Worker" — #2563EB background, white text

If worker NOT found (no existing Credwork account):
  The profile card shows:
  "No Credwork account found"
  "We'll send Priya Devi an SMS invite to join Credwork."
  Small, #111827 at 60% opacity
  The confirm button changes to: "Add Worker + Send Invite"
  Same #2563EB treatment

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No option to add a worker by name only (phone is required for identity)
- No photo upload for the worker (worker manages their own photo)
- No salary history or previous records on this screen

BACKGROUND: #F4F6FA
```

---

---

## H-03 — Make Payment
### Generate this screen third.

---

```
SCREEN: H-03 — Make Payment
PURPOSE: The household initiates a salary payment to their domestic worker.
This is the core transactional moment of ServiConnect. The payment creates 
the worker's income record. The screen must feel deliberate — the household 
is making a financial commitment, not a casual tap.

This screen has ONE STATE with a success micro-state after payment.

---

HEADER:
  Back arrow (left) — returns to H-01
  Centre title: "Make Payment" — bold, #111827
  No right element

---

WORKER IDENTITY CARD (top of screen, below header):
  A compact card showing who is being paid
  Left: circular worker avatar — "PD" initials
  Centre:
    Worker name: "Priya Devi" — bold, #111827
    Role: "Cook · Full-time" — small, regular, #111827 at 60% opacity
  Right: nothing — this is identity only, not interactive
  Border: 1.5px #111827, rounded corners, #F4F6FA background

---

PAYMENT TYPE SELECTOR:
  Label above: "Payment type"
  A segmented control with three options: Salary · Bonus · Advance
  Default selected: Salary
  Selected segment: #2563EB background, white text
  Unselected: #F4F6FA background, #111827 text, border 1px #E5E7EB
  The entire segmented control has a border 1.5px #111827, rounded corners

---

PAYMENT AMOUNT:
  Label: "Amount"
  A large number input showing the pre-filled salary amount
  Value: "3,500" — large, bold, #111827 inside the field
  ₹ symbol left-aligned inside the field, #111827 at 60% opacity
  
  For Salary type: the field is pre-filled with ₹3,500 (the agreed monthly salary)
  A note below the field for Salary type:
  "This is Priya's agreed monthly salary. Changing it will prompt a confirmation."
  Small, #111827 at 50% opacity
  
  For Bonus/Advance: the field is empty with placeholder "Enter amount"
  No note shown for Bonus/Advance

---

PAYMENT PERIOD:
  Label: "For the month of"
  A read-only pill showing the current month: "March 2025"
  Background: #F4F6FA, border 1.5px #111827, rounded corners
  Not editable (backdating is restricted per system rules — not exposed here)
  Small note: "Payments are recorded for the current month."
  Small, #111827 at 50% opacity

---

PAYMENT METHOD:
  Label: "Paying via"
  A read-only row showing:
  Left: UPI icon (generic UPI logo mark)
  Centre: "Razorpay UPI" — bold, #111827
  Below: household's UPI ID (masked): "sharma****@okicici" — small, #111827 at 60%
  Right: "Change" link in #2563EB
  Border 1.5px #E5E7EB, rounded corners, #F4F6FA background

---

WORKER RECEIVES SUMMARY (above the pay button):
  A highlighted summary box, background #2563EB at 6% opacity, 
  border-left 3px #2563EB, rounded corners
  Text: "Priya Devi will receive ₹3,500 and a payment confirmation on Credwork."
  Small, bold, #111827
  This line is important — it confirms the payment is being documented, not just transferred

---

PAY BUTTON:
  Full width, large
  Text: "Pay ₹3,500" — the amount is in the button text, not just "Pay"
  #2563EB background, white text, bold
  This specificity ("Pay ₹3,500" not just "Pay") prevents accidental payments

---

SUCCESS MICRO-STATE (replaces the screen content after payment is confirmed):
  A centred success moment — same visual treatment as G-05 but smaller:
  A cyan checkmark (draws itself, 400ms)
  Bold text: "Payment sent!"
  Below: "Priya Devi's record has been updated."
  Regular, #111827
  Below that: "₹3,500 · March 2025 · Salary" — small chips
  
  After 2 seconds, auto-navigates back to H-01 Home Dashboard
  No button needed — the auto-navigation handles it

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No option to pay multiple workers simultaneously
- No recurring payment setup on this screen
- No payment notes or memo field
- No "split payment" option

BACKGROUND: #F4F6FA
```

---

---

## H-04 — Payment History (Household)
### Generate this screen fourth.

---

```
SCREEN: H-04 — Payment History (Household)
PURPOSE: A full log of all payments made by this household to all their workers.
The household's equivalent of an expense ledger for domestic worker payments.
Clean, scannable, exportable.

This screen has ONE STATE. Scrollable.

---

HEADER:
  Back arrow (left) — returns to H-01
  Centre title: "Payment History" — bold, #111827
  Right: a download icon in #2563EB — tapping generates a PDF export of all payments

---

SUMMARY ROW (below header):
  Two stat pills side by side, full width:
  
  Pill 1: "This month"
    Value: "₹11,500" — bold, large, #111827
    Label below: "Total paid in March 2025" — small, #111827 at 60%
  
  Pill 2: "All time"
    Value: "₹1,38,000" — bold, large, #111827
    Label below: "Since January 2024" — small, #111827 at 60%
  
  Both pills: #F4F6FA background, border 1.5px #E5E7EB, rounded corners

---

FILTER ROW (below summary):
  Three filter chips in a horizontal scrollable row:
  
  "All workers" (default selected) · "Priya Devi" · "Ramesh Singh"
  Selected: #2563EB background, white text
  Unselected: #F4F6FA background, border 1.5px #111827, #111827 text
  
  A second filter row below:
  "All types" · "Salary" · "Bonus" · "Advance"
  Same chip styling

---

PAYMENT LIST (grouped by month, newest first):

  MONTH GROUP HEADER:
    "March 2025" — small, bold, #111827
    Right aligned: "₹11,500 total" — small, #111827 at 60%
    A subtle 1px #E5E7EB full-width line below the header

  PAYMENT ROWS (inside each month group):
    Each row is a list item with:
    Left: a coloured icon based on payment type
      Salary: document icon in #06B6D4
      Bonus: star icon in #2563EB
      Advance: clock icon in #F59E0B
    Centre:
      Worker name: "Priya Devi" — small, bold, #111827
      Below name: payment type + date — "Salary · 1 Mar 2025" — very small, #111827 at 60%
    Right:
      Amount: "₹3,500" — small, bold, #111827
      Below amount: "Verified ✓" — very small, #06B6D4

  DEMO DATA — show these rows:

  March 2025 (₹11,500 total):
    Ramesh Singh · Salary · 1 Mar 2025 · ₹8,000 · Verified
    Priya Devi · Bonus · 12 Mar 2025 · ₹500 · Verified

  February 2025 (₹11,500 total):
    Ramesh Singh · Salary · 1 Feb 2025 · ₹8,000 · Verified
    Priya Devi · Salary · 1 Feb 2025 · ₹3,500 · Verified

  January 2025 (₹11,500 total):
    Ramesh Singh · Salary · 1 Jan 2025 · ₹8,000 · Verified
    Priya Devi · Salary · 1 Jan 2025 · ₹3,500 · Verified

---

EXPORT NOTE (bottom of screen, above navigation):
  Small, centred, #111827 at 50% opacity:
  "Tap ↓ above to download your full payment history as PDF."

---

BOTTOM NAVIGATION BAR:
  Workers tab is active on this screen — #2563EB
  Home and Settings inactive

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No edit or delete buttons on payment rows — records are permanent
- No payment amount totals per worker (only per month totals)
- No graphs or charts — this is a log, not an analytics screen

BACKGROUND: #F4F6FA
```

---

---

# SCREEN PROMPTS — DOMESTIC WORKER FLOW

---

## D-01 — Home Dashboard (Domestic Worker)
### Generate this screen fifth.

---

```
SCREEN: D-01 — Home Dashboard (Domestic Worker)
PURPOSE: The domestic worker's central hub. Unlike the gig worker who uploads documents, 
the domestic worker's record is built entirely from payments made by their household.
Their dashboard shows them what exists, how their record is building, and what their 
GigScore means. It should feel like ownership — this is their financial identity, 
even though they didn't build it themselves by uploading anything.

This screen has ONE STATE. Scrollable.

---

HEADER BAR:
  Left: logo/credwork-wordmark.png — small
  Right: circular profile avatar — "PD" initials
  Background: #F4F6FA

IDENTITY ROW:
  Worker name: "Priya Devi" — bold, #111827
  Below: "Domestic Worker · New Delhi" — small, regular, #111827 at 60%
  A "Verified" badge inline — #06B6D4 background, white text
  This badge means their phone OTP has been confirmed

---

PRIMARY CARD — GIGSCORE:
  Identical visual treatment to G-01 gig worker GigScore card
  Same ring, same size (160px), same colour (#06B6D4), same three-element display

  Demo value: GigScore 71, label "Good"
  
  Below the ring, inside the card:
  "Based on 5 months of verified payments from your employer"
  Small, #111827 at 70% opacity, centred
  
  Note: the data source description differs from gig worker — 
  "payments from your employer" not "verified bank statement data"

---

CURRENT HOUSEHOLD CARD:
  A card below the GigScore card
  Left border accent: 3px #06B6D4 (same as certificate status card on G-01)
  
  Left side:
    Label: "Current employer" — small, #111827 at 60%
    Below: "Sharma Household" — bold, #111827
    Below: "New Delhi · Since October 2024" — small, #111827 at 60%
  
  Right side:
    Payment status for this month:
    If paid: "March paid ✓" — small pill, #06B6D4 background at 15%, #06B6D4 text
    If unpaid: "March pending" — small pill, #F59E0B background at 15%, #F59E0B text
    Use "March paid ✓" for demo

---

CERTIFICATE STATUS CARD:
  Identical structure to G-01 certificate status card
  Left border accent: 3px #06B6D4
  
  Left:
    Label: "Latest Certificate" — small, #111827 at 60%
    "v1 — Active" — bold, #111827
    "Issued 15 February 2025" — small, #111827 at 60%
  
  Right:
    "View" button — #2563EB pill button, white text
    Navigates to D-03 Certificate Preview

---

PENDING PAYMENT NOTICE (conditional — shown when this month's payment hasn't arrived):
  Only shown if current month is unpaid
  A soft info banner: background #F59E0B at 8%, border-left 3px #F59E0B
  Text: "Your March payment hasn't been recorded yet."
  Below: "Ask your employer to make this month's payment on Credwork."
  Small, #111827
  This is informational — not an alarm. Do not use red.
  Hide this banner in the demo (March is paid).

---

QUICK ACTIONS ROW:
  Three equal-width icon-buttons

  Action 1: Document icon — "My Certificate" → D-03
  Action 2: History icon — "Payment History" → D-02
  Action 3: Share icon — "Share" → D-04

  Icons: #2563EB. Labels: #111827, small.

---

BOTTOM NAVIGATION BAR:
  Home · Certificate · Settings
  Home active — #2563EB

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No upload button — domestic workers do not upload bank statements
- No "Add income" button — income comes from household payments only
- No GigScore explanation tooltip on this screen (that belongs in Help/FAQ)

BACKGROUND: #F4F6FA
```

---

---

## D-02 — Payment History (Domestic Worker)
### Generate this screen sixth.

---

```
SCREEN: D-02 — Payment History (Domestic Worker)
PURPOSE: A chronological log of all payments the domestic worker has received through 
Credwork. This is the domestic worker's equivalent of a payslip history. Many domestic 
workers have never had documented proof of what they were paid and when. 
This screen should feel like a dignified, trustworthy financial record.

This screen has ONE STATE. Scrollable.

---

HEADER:
  Back arrow (left) — returns to D-01
  Centre title: "Payment History" — bold, #111827
  No right element

---

TOTAL EARNINGS CARD (below header):
  A prominent card, full width
  Background: #F4F6FA, border 1.5px #111827, rounded corners
  Top border accent: 3px #06B6D4
  
  Inside:
    Label: "Total verified earnings" — small, bold, #111827
    Value: "₹17,500" — large, bold, #111827
    Below: "October 2024 – February 2025 · 5 months" — small, #111827 at 60%

---

FILTER ROW:
  Horizontal scrollable chips:
  "All" (default selected) · "Salary" · "Bonus" · "Advance"
  Selected: #2563EB background, white text
  Unselected: #F4F6FA, border 1.5px #111827

---

PAYMENT LIST (grouped by month, newest first):

  MONTH GROUP HEADER:
    Month name: "February 2025" — small, bold, #111827
    Right: month total — "₹3,500" — small, #111827 at 60%
    1px #E5E7EB divider below

  PAYMENT ROW STRUCTURE:
    Left: payment type icon
      Salary: document icon in #06B6D4
      Bonus: star icon in #2563EB
      Advance: clock icon in #F59E0B
    Centre:
      "Sharma Household" — small, bold, #111827
      Payment type badge + date below:
        "Salary · 1 Feb 2025" — very small, #111827 at 60%
    Right:
      Amount: "₹3,500" — small, bold, #111827
      "Verified ✓" — very small, #06B6D4 below amount

  DEMO DATA:

  February 2025 (₹3,500):
    Sharma Household · Salary · 1 Feb 2025 · ₹3,500 · Verified

  January 2025 (₹3,500):
    Sharma Household · Salary · 1 Jan 2025 · ₹3,500 · Verified

  December 2024 (₹4,000):
    Sharma Household · Salary · 1 Dec 2024 · ₹3,500 · Verified
    Sharma Household · Bonus · 20 Dec 2024 · ₹500 · Verified

  November 2024 (₹3,500):
    Sharma Household · Salary · 1 Nov 2024 · ₹3,500 · Verified

  October 2024 (₹3,000):
    Sharma Household · Salary · 1 Oct 2024 · ₹3,000 · Verified
    Note: ₹3,000 because salary was lower before the raise in November

---

GAP NOTICE (shown between months if a gap exists in the record):
  A gap row between months — styled differently from payment rows:
  Background: #F59E0B at 6% opacity, dashed border 1px #F59E0B, rounded
  Text: "No payment recorded for [Month]"
  Below: "If you were paid in cash, ask your employer to record it on Credwork."
  Small, #111827
  No gap in demo data — do not show this row in the demo design

---

BOTTOM NAVIGATION BAR:
  Certificate tab is active here — #2563EB
  (Payment History is accessed from the Certificate tab context)

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No edit or delete buttons on any row — records are permanent
- No "Add payment manually" button — workers cannot self-report payments
- No total earnings chart or graph on this screen

BACKGROUND: #F4F6FA
```

---

---

## D-03 — Certificate Preview (Domestic Worker)
### Generate this screen seventh.

---

```
SCREEN: D-03 — Certificate Preview (Domestic Worker)
PURPOSE: Full in-app view of the domestic worker's income certificate. 
Structurally identical to G-07 (gig worker certificate) but the income 
source, platform information, and verification statement are different.
The certificate must look equally professional — this worker deserves the 
same quality of credential as a gig worker.

This screen has ONE STATE. Scrollable.

---

HEADER BAR:
  Back arrow (left)
  Centre title: "Certificate" — bold, #111827
  Right: share icon in #2563EB → navigates to D-04

---

CERTIFICATE DOCUMENT (styled in-app card — NOT a PDF viewer):
  Full width, border 2px #111827, rounded corners, #F4F6FA background
  Generous internal padding

  CERTIFICATE HEADER:
    logo/credwork-logo-full.png — left aligned, small
    Right aligned:
      "INCOME VERIFICATION CERTIFICATE" — small caps, bold, #111827
      Certificate ID: "CW-2025-01203" — small, monospace, #111827 at 60%
    Full-width divider 2px #111827 below header

  WORKER IDENTITY:
    Name: "Priya Devi" — large, bold, #111827
    "New Delhi, Delhi"
    "Member since October 2024"
    "Verified" badge — #06B6D4 background, white text, pill

  CERTIFICATE PERIOD:
    Label: "Income Period"
    Value: "October 2024 – February 2025 (5 months)"

  AVERAGE MONTHLY INCOME:
    Label: "Verified Average Monthly Income"
    Value: "₹3,500" — very large, bold, #111827
    This is the hero number — largest text on the document

  GIGSCORE:
    Three-element display: ring (48px, filled to 71%) + "71" + "Good"
    Below: "Income consistency measured over 5 months of verified payments"
    Small, #111827 at 60%

  MONTHLY PAYMENT BREAKDOWN TABLE:
    Label: "Monthly Breakdown"
    Columns: Month | Employer | Amount
    Five rows:
      October 2024   | Sharma Household | ₹3,000
      November 2024  | Sharma Household | ₹3,500
      December 2024  | Sharma Household | ₹4,000
      January 2025   | Sharma Household | ₹3,500
      February 2025  | Sharma Household | ₹3,500
    
    Note: December is higher due to the bonus payment
    Column headers: small, bold, #111827
    Row values: small, regular, #111827. Amount values: small, bold, #111827
    Row dividers: subtle 1px #E5E7EB

  EMPLOYER SECTION (replaces "Platforms Verified" from gig worker cert):
    Label: "Verified Employer"
    A single chip: "Sharma Household · New Delhi"
    Chip: #06B6D4 background at 15%, #06B6D4 text

  VERIFICATION STATEMENT:
    Smaller text, #111827 at 70%, regular:
    "This certificate was generated by Credwork based on verified payment records 
    from a registered household employer. Payment amounts reflect actual salary, 
    bonus, and advance transactions processed through ServiConnect."
    Full-width divider above this statement

  CERTIFICATE FOOTER:
    Left: "Issued: 15 February 2025"
    Right: "Version 1"
    Both small, #111827 at 60%

---

CERTIFICATE HISTORY (below the certificate card):
  Label: "Certificate History"
  One row (demo — only one version exists):
    "v1 — 15 February 2025" · "Active" badge in #06B6D4

---

BOTTOM ACTION BAR (fixed, above nav):
  "Download / Share" button — #2563EB, white text, full width
  → D-04 Share / Export

BOTTOM NAVIGATION BAR:
  Certificate tab active — #2563EB

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No "platforms verified" section (irrelevant for domestic workers)
- No bank statement reference
- No edit button

BACKGROUND: #F4F6FA
```

---

---

## D-04 — Share / Export (Domestic Worker)
### Generate this screen eighth.

---

```
SCREEN: D-04 — Share / Export (Domestic Worker)
PURPOSE: Identical in function and visual structure to G-08 (gig worker share screen).
The certificate content is different (ServiConnect-sourced) but the sharing mechanics, 
options, and visual design are the same. Do not redesign — replicate G-08 exactly 
with these content differences only.

This screen is a BOTTOM SHEET — same treatment as G-08.

---

DIFFERENCES FROM G-08:

CERTIFICATE THUMBNAIL (top of bottom sheet):
  Shows: Credwork logo + "Priya Devi" + "₹3,500 / month" + GigScore ring (71)
  Everything else in the thumbnail is identical to G-08

HEADING:
  "Share your certificate" — identical to G-08

SHARE OPTIONS:
  All four options are identical to G-08:
  1. Send via WhatsApp (primary, cyan left border accent)
  2. Save to phone
  3. Send by email
  4. Copy verification link

SAFETY NOTE:
  Identical: "Only share with people you trust."

---

WHAT IS IDENTICAL TO G-08:
- Bottom sheet structure and drag handle
- All four share option rows, icons, labels, sub-labels
- WhatsApp as the visually dominant primary option
- Cyan left border accent on WhatsApp row only
- Safety note at the bottom
- The dimmed screen behind the sheet

BACKGROUND: #F4F6FA for the sheet itself
```

---

---

# SCREEN PROMPTS — GLOBAL / SETTINGS

---

## X-01 — Notification Preferences
### Generate this screen ninth.

---

```
SCREEN: X-01 — Notification Preferences
PURPOSE: The user manages what Credwork is allowed to notify them about.
Clean toggle list. No promotional options. Only account-relevant events.
The screen adapts based on user role — show the gig worker version for design.

This screen has ONE STATE.

---

HEADER:
  Back arrow (left) — returns to Settings
  Centre title: "Notifications" — bold, #111827

---

INTRO LINE (below header):
  "We only send notifications about your account. Never promotional."
  Small, regular, #111827 at 60%

---

NOTIFICATION TOGGLES (for Gig Worker role):

Each toggle row:
  Left: a small icon in #2563EB
  Centre: 
    Primary label — bold, #111827
    Sub-label below — small, regular, #111827 at 60%
  Right: a toggle switch
    On state: #2563EB background, white circle
    Off state: #E5E7EB background, white circle

TOGGLE 1 — Certificate updated
  Icon: certificate/document icon
  Label: "Certificate updated"
  Sub-label: "When a new version of your certificate is generated"
  Default: ON

TOGGLE 2 — GigScore changed
  Icon: chart/score icon
  Label: "GigScore changed"
  Sub-label: "When your score moves by more than 5 points"
  Default: ON

TOGGLE 3 — Upload reminder
  Icon: calendar/reminder icon
  Label: "Monthly upload reminder"
  Sub-label: "Reminder to upload a new bank statement each month"
  Default: ON

TOGGLE 4 — Processing complete
  Icon: checkmark icon
  Label: "Processing complete"
  Sub-label: "When your uploaded document has finished scanning"
  Default: ON

---

A subtle section divider with label: "What we never send"
Below the divider, three lines with a ✗ icon each in #111827 at 40%:
  "Promotional offers"
  "Partner advertisements"  
  "Marketing messages"
Each line: small, #111827 at 50%

This section builds trust — making explicit what Credwork will NOT notify about.

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No "select all" or "deselect all" button
- No notification frequency settings
- No email notification options (app notifications only)

BACKGROUND: #F4F6FA
```

---

---

## X-02 — Language Toggle
### Generate this screen tenth.

---

```
SCREEN: X-02 — Language Toggle
PURPOSE: The user switches the app language. Switching is instant — no restart, 
no confirmation dialog. The screen is minimal and functional.

This screen has ONE STATE.

---

HEADER:
  Back arrow (left) — returns to Settings
  Centre title: "Language" — bold, #111827

---

INTRO LINE:
  "Your language preference is saved to your account."
  Small, #111827 at 60%

---

TWO LANGUAGE CARDS:
  Stacked vertically, full width, equal visual weight
  Same card treatment as S-02 Language Select — but one card shows the active state

  CARD 1 — ENGLISH (currently active):
    Large text: "English"
    Sub-text: "Continue in English"
    Right side: a filled checkmark in #2563EB — signals current selection
    Border: 1.5px #2563EB (active state border)
    Background: #2563EB at 5% opacity (very subtle active tint)

  CARD 2 — HINDI:
    Large text: "हिंदी"
    Sub-text: "हिंदी में जारी रखें"
    No checkmark
    Border: 1.5px #111827 (inactive)
    Background: #F4F6FA

  Tapping the inactive card:
  Immediately switches the app language
  The tapped card becomes active (checkmark appears, border becomes #2563EB)
  A brief toast: "Language updated" — 2 seconds, then disappears
  No reload. No confirmation. Instant.

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No "Apply" or "Save" button — the tap IS the save
- No other language options beyond English and Hindi
- No restart prompt

BACKGROUND: #F4F6FA
```

---

---

## X-03 — Privacy + Data
### Generate this screen eleventh.

---

```
SCREEN: X-03 — Privacy + Data
PURPOSE: Tells the user exactly what data Credwork holds, how it's used, and what 
they can do about it. DPDP Act compliance. The most important trust-building screen 
in settings. Must be honest, plain-language, and not feel like a legal document.

This screen has ONE STATE. Scrollable.

---

HEADER:
  Back arrow (left) — returns to Settings
  Centre title: "Privacy & Data" — bold, #111827

---

SECTION 1 — WHAT WE STORE:
  Label: "What we store" — small, bold, #111827
  
  Five rows, each with a small document/data icon in #2563EB:
  - "Your name, phone number, and city"
  - "Your profile photo (if provided)"
  - "Your monthly income entries (derived from your bank statement)"
  - "Your certificates — all versions, permanently"
  - "Your payment history (for ServiConnect users)"
  
  Each row: small, regular, #111827

---

SECTION 2 — WHAT WE DON'T STORE:
  Label: "What we don't store" — small, bold, #111827
  
  Three rows, each with a ✗ icon in #06B6D4:
  - "Your bank statement PDF (processed and deleted immediately)"
  - "Your bank account number"
  - "Your UPI PIN or password"
  
  The first item — about the bank statement PDF not being stored — must be visually 
  prominent. This is the most important trust signal in the entire screen.
  Make the first row slightly larger text or give it a subtle #06B6D4 background tint.

---

SECTION 3 — HOW YOUR DATA IS USED:
  Label: "How your data is used" — small, bold, #111827
  
  A short paragraph (not a list):
  "Your income data is used only to generate your income certificate. 
  We do not sell your data to lenders, advertisers, or any third party. 
  Certificates you share with lenders are shared by you — not by us."
  
  Small, regular, #111827 at 80%

---

SECTION 4 — YOUR RIGHTS (two action rows):

  ROW 1 — DOWNLOAD MY DATA:
    Left: download icon in #2563EB
    Centre:
      Label: "Download all my data" — bold, #111827
      Sub-label: "Get a copy of everything Credwork holds about you" — small, #111827 at 60%
    Right: chevron in #111827 at 40%
    Tapping generates and downloads a data export

  ROW 2 — DELETE ACCOUNT:
    Left: trash icon in a muted red — use #EF4444 for this icon only
    Centre:
      Label: "Delete my account" — bold, #EF4444
      Sub-label: "Permanently remove your profile and income data" — small, #111827 at 60%
    Right: chevron in #111827 at 40%
    
    Note: #EF4444 red is used ONLY for the delete account icon and label.
    This is the one permitted exception to the four-colour rule — delete is 
    a destructive action and must be visually distinct.
    
    Tapping shows a confirmation dialog (not a separate screen):
      Dialog heading: "Delete your account?"
      Body: "This will remove your profile from Credwork. Certificates already 
      shared with lenders cannot be recalled from their systems."
      Two buttons: "Cancel" (secondary) · "Yes, delete" (red, #EF4444 background)

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No legalese or terms-of-service language
- No "third party partners" list
- No cookie settings (this is a mobile app)

BACKGROUND: #F4F6FA
```

---

---

## X-04 — Help / FAQ
### Generate this screen twelfth.

---

```
SCREEN: X-04 — Help / FAQ
PURPOSE: In-app support and help. Especially important for low-literacy users.
Every answer must be readable in 3 lines or fewer. Plain language only.
WhatsApp is the support channel — not email, not a ticket form.

This screen has ONE STATE. Scrollable.

---

HEADER:
  Back arrow (left) — returns to Settings
  Centre title: "Help & FAQ" — bold, #111827

---

SEARCH BAR (below header):
  Full-width search input
  Left icon: magnifying glass in #111827 at 40%
  Placeholder: "Search help topics..."
  Border: 1.5px #111827, rounded corners, #F4F6FA background
  Live filters the FAQ items below as user types
  No search button — filters on keystroke

---

FAQ SECTIONS (collapsible accordions):

Each section has a section header (bold, #111827) and question rows inside.
Each question row:
  Left: a small question mark icon in #2563EB
  Question text: regular, #111827
  Right: a chevron — points down when collapsed, up when expanded
  When expanded: answer text appears below the question in a slightly indented block
  Answer text: small, regular, #111827 at 80%

---

SECTION — FOR GIG WORKERS:
  Label: "Gig Workers" — small, bold, #06B6D4 (cyan section label)

  Q: "How do I download my bank statement PDF?"
  A: "Open your bank app → go to Statements or Account Summary → 
  select the last 6 months → download as PDF."

  Q: "Which banks are supported?"
  A: "SBI, HDFC, ICICI, Axis, Kotak, Yes Bank, Bank of Baroda, Canara, and PNB."

  Q: "Why was my document flagged?"
  A: "Usually because the PDF was downloaded from a browser instead of your bank app. 
  Download a fresh statement directly from your bank's official app and try again."

  Q: "What is GigScore and how is it calculated?"
  A: "GigScore measures how consistent your income is over 6 months — not just the 
  average, but how reliable it is month to month. Higher consistency = higher score."

  Q: "How do I share my certificate with a bank?"
  A: "Tap Share on your certificate and choose WhatsApp. Send the PDF to your 
  bank manager or loan officer directly."

---

SECTION — FOR DOMESTIC WORKERS:
  Label: "Domestic Workers" — small, bold, #06B6D4

  Q: "How do I get my employer to register on Credwork?"
  A: "Show them the app and ask them to sign up as a Household. Once they add your 
  phone number, you'll be linked automatically."

  Q: "What if my employer paid me in cash?"
  A: "Ask your employer to record the cash payment in the app within 30 days. 
  After 30 days, the month shows as a gap in your record."

  Q: "How do I view my payment history?"
  A: "Tap Payment History from your home screen. You'll see every payment ever 
  recorded for you on Credwork."

---

SECTION — FOR HOUSEHOLDS:
  Label: "Households" — small, bold, #06B6D4

  Q: "How do I add a worker?"
  A: "Tap Add Worker on your home screen and enter their mobile number. 
  If they're on Credwork, they'll be linked instantly."

  Q: "What if I paid in cash and forgot to use the app?"
  A: "You can record a cash payment within 30 days of the payment date. 
  Go to your worker's card and tap Record Payment."

  Q: "Can I add more than one worker?"
  A: "Yes. Tap Add Worker as many times as you need. Each worker gets their 
  own payment record."

---

CONTACT SUPPORT SECTION (bottom of screen):
  A full-width card, border 1.5px #2563EB, background #2563EB at 5% opacity
  Left: WhatsApp icon (green)
  Centre:
    "Still need help?" — bold, #111827
    "Chat with us on WhatsApp" — small, #111827 at 60%
  Right: a chevron in #2563EB
  
  Tapping opens WhatsApp with pre-filled message:
  "Hi Credwork, I need help with [topic]"
  
  Below the card, very small centred text:
  "We usually reply within a few hours."
  #111827 at 40%

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No ticket submission form
- No email support option
- No phone call option
- No chatbot or AI chat widget
- No FAQ answers longer than 3 lines

BACKGROUND: #F4F6FA
```

---

---

# SCREEN PROMPTS — ADMIN PANEL

---

## A-01 — Admin Dashboard
### Generate this screen last. Web only — not a mobile screen.

---

```
SCREEN: A-01 — Admin Dashboard
PURPOSE: Web-only screen for the Credwork team. Provides real-time visibility into 
system health, upload processing, and data integrity during the hackathon demo.
This screen proves to judges that the system is real and running — not a prototype 
with hardcoded data. It is information-dense by design — the audience is the 
Credwork team, not informal workers.

This is a WEB DASHBOARD — not a mobile screen. Design for a 1280px wide browser window.
Use a left sidebar for navigation — no bottom nav bar.

---

LAYOUT:
  Left sidebar — 240px wide, #111827 background (dark sidebar)
  Main content area — remaining width, #F4F6FA background

LEFT SIDEBAR:
  Top: logo/credwork-wordmark.png — but inverted for dark background
    "Cred" in white, "work" in #06B6D4 (cyan) — adaptation for dark bg only
  Below logo: "Admin Panel" label — small, #F4F6FA at 50%
  
  Navigation items (vertical list):
    Dashboard (active) — #F4F6FA text, left border 3px #2563EB
    Uploads — #F4F6FA at 60% text
    Fraud Flags — #F4F6FA at 60% text
    Certificates — #F4F6FA at 60% text
    Payments — #F4F6FA at 60% text
  
  Each nav item: left icon + label, 48px height, hover state #F4F6FA at 8% background
  Bottom of sidebar: "Logged in as Admin" — very small, #F4F6FA at 40%

---

MAIN CONTENT — TOP ROW: SYSTEM HEALTH STAT CARDS

Five cards in a horizontal row, equal width
Each card: #F4F6FA background, border 1.5px #E5E7EB, rounded corners, padding 20px

  CARD 1 — TOTAL ACCOUNTS:
    Label: "Total Accounts" — small, #111827 at 60%
    Value: "1,247" — large, bold, #111827
    Below: breakdown in small chips:
      "892 Gig" · "203 Domestic" · "152 Household"
      Each chip: #F4F6FA, border 1px #E5E7EB, tiny text
    Delta: "↑ 23 today" — small, #06B6D4

  CARD 2 — UPLOADS (24H):
    Label: "Uploads (24h)" — small, #111827 at 60%
    Value: "47" — large, bold, #111827
    Delta: "↑ 12 from yesterday" — small, #06B6D4

  CARD 3 — CERTIFICATES ISSUED:
    Label: "Certificates Issued" — small, #111827 at 60%
    Value: "1,089" — large, bold, #111827
    Delta: "↑ 31 today" — small, #06B6D4

  CARD 4 — FRAUD FLAGS:
    Label: "Fraud Flags" — small, #111827 at 60%
    Value: "8" — large, bold, #111827
    Delta: "3 pending review" — small, #F59E0B (amber — indicates attention needed)

  CARD 5 — PROCESSING ERRORS:
    Label: "Processing Errors" — small, #111827 at 60%
    Value: "2" — large, bold, #111827
    Delta: "Both resolved" — small, #06B6D4

---

MAIN CONTENT — SECOND ROW: TWO PANELS SIDE BY SIDE

LEFT PANEL (60% width) — RECENT UPLOADS TABLE:
  Panel heading: "Recent Uploads" — bold, #111827
  Right of heading: "Live" badge — #06B6D4 background, white text, small pill
  
  A table with columns:
  Time | Worker ID | Status | Fraud Check | GigScore
  
  10 rows of demo data:
  
  Row format:
    Time: "14:32" — small, #111827 at 60%
    Worker ID: "GW-0892" — small, monospace, #111827
    Status: a badge pill
      "Passed" — #06B6D4 background at 15%, #06B6D4 text
      "Processing" — #2563EB background at 15%, #2563EB text
      "Flagged" — #F59E0B background at 15%, #F59E0B text
      "Failed" — #EF4444 background at 15%, #EF4444 text
    Fraud Check: "Passed" or "Flagged" — same colour logic
    GigScore: numeric value or "—" if not yet generated

  DEMO ROWS (10 rows):
    14:32 | GW-0892 | Passed    | Passed  | 81
    14:28 | GW-0891 | Passed    | Passed  | 67
    14:15 | GW-0890 | Flagged   | Flagged | —
    13:58 | GW-0889 | Passed    | Passed  | 74
    13:44 | GW-0888 | Processing| —       | —
    13:31 | GW-0887 | Passed    | Passed  | 88
    13:20 | GW-0886 | Failed    | Passed  | —
    13:08 | GW-0885 | Passed    | Passed  | 72
    12:55 | GW-0884 | Passed    | Passed  | 79
    12:40 | GW-0883 | Flagged   | Flagged | —

  Table header row: #F4F6FA background, bold column labels
  Alternating row background: rows 2, 4, 6, 8, 10 get #111827 at 2% tint

RIGHT PANEL (40% width) — FRAUD FLAGS QUEUE:
  Panel heading: "Fraud Flags — Pending Review" — bold, #111827
  A count badge: "3" — #F59E0B background, white text, small circle
  
  Three flag items stacked vertically:
  Each item is a card: border-left 3px #F59E0B, #F4F6FA background, rounded
  
  FLAG ITEM STRUCTURE:
    Top row: Worker ID (bold) + timestamp (small, right)
    Middle row: Flag reason in plain language
    Bottom row: "Review" button — small, #2563EB border, #2563EB text, pill shape
  
  DEMO FLAG ITEMS:
  
  Item 1:
    Worker ID: GW-0890 · 14:15
    Reason: "Income differs by 23% between two uploads of the same period (Oct 2024)"
    Review button

  Item 2:
    Worker ID: GW-0876 · 11:20
    Reason: "Income volume may reflect multiple earners on shared bank account"
    Review button

  Item 3:
    Worker ID: GW-0863 · 09:45
    Reason: "Same period uploaded twice. Figures differ by 18%."
    Review button

---

MAIN CONTENT — THIRD ROW: TWO PANELS SIDE BY SIDE

LEFT PANEL (50% width) — CERTIFICATE VERSION LOG:
  Panel heading: "Recent Certificates" — bold, #111827
  
  A list of 6 most recent certificates:
  Each row: Cert ID | Worker | Version | Issued | Status
  
  DEMO ROWS:
    CW-2025-01203 | PD-0203 | v1 | 15 Mar 2025 | Active
    CW-2025-00847 | GW-0847 | v2 | 1 Mar 2025  | Active
    CW-2025-00846 | GW-0846 | v1 | 28 Feb 2025 | Active
    CW-2025-00845 | GW-0845 | v3 | 27 Feb 2025 | Active
    CW-2025-00844 | GW-0844 | v1 | 26 Feb 2025 | Active
    CW-2025-00843 | GW-0843 | v2 | 25 Feb 2025 | Superseded

  Version badges: "v1", "v2", "v3" — small, #2563EB background at 15%, #2563EB text
  Status "Active": #06B6D4 text · "Superseded": #111827 at 40% text

RIGHT PANEL (50% width) — SERVICONNECT PAYMENT LOG:
  Panel heading: "ServiConnect Payments" — bold, #111827
  "Live" badge — #06B6D4 background, white text
  
  A list of 6 most recent webhook events:
  Each row: Time | Household | Worker | Amount | Webhook Status
  
  DEMO ROWS:
    14:01 | Sharma HH | PD-0203 | ₹3,500 | Processed ✓
    13:45 | Gupta HH  | RS-0156 | ₹8,000 | Processed ✓
    12:30 | Verma HH  | AM-0089 | ₹4,000 | Processed ✓
    11:15 | Sharma HH | PD-0203 | ₹500   | Processed ✓
    10:00 | Mehta HH  | SK-0201 | ₹3,000 | Processed ✓
    09:30 | Singh HH  | RK-0178 | ₹6,500 | Failed ✗

  "Processed ✓": #06B6D4 text · "Failed ✗": #EF4444 text

---

WHAT THIS SCREEN MUST NOT CONTAIN:
- No worker personal data (names, phone numbers) — Worker IDs only
- No ability to edit or delete any records from this panel
- No financial analytics or revenue dashboard
- No user management (password resets, etc.)

BACKGROUND: #F4F6FA for main content. #111827 for sidebar.
This screen is information-dense by design — tables and data dominate. 
This is acceptable for an admin tool.
```

---

---

## TROUBLESHOOTING — If Antigravity Drifts

Paste this correction block to realign:

```
CORRECTION: Please realign to the Credwork design system.

Colour check — only these four are permitted on user-facing screens:
  #111827  Charcoal Black   → text, headings, borders at rest
  #2563EB  Electric Blue    → buttons, CTAs, active borders, links
  #06B6D4  Cyan             → GigScore ring, accent indicators, verified badges
  #F4F6FA  Off-White        → all backgrounds, all card fills

Permitted exceptions:
  #E5E7EB  → disabled state backgrounds only
  #F59E0B  → Advance payment badges and warning states only
  #EF4444  → Delete account action only (X-03) and admin error states only

No white (#FFFFFF). No black (#000000).

Language check: English only. No Hindi unless explicitly instructed.

GigScore check: Always ring + number + label together. Never just a number.

Logo check: Use assets from /logo folder. Never recreate or redraw.

Navigation check:
  Gig Worker + Domestic Worker: Home · Certificate · Settings (3 items)
  Household: Home · Workers · Settings (3 items)
  Admin: left sidebar, web only, no bottom nav
```

---

*This file covers all remaining Credwork screens. Generate in order:*
*H-01 → H-02 → H-03 → H-04 → D-01 → D-02 → D-03 → D-04 → X-01 → X-02 → X-03 → X-04 → A-01*
*Keep this file open throughout the session. Paste the Master Context Block at the start of every new Antigravity session.*