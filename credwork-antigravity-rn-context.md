# Credwork — Antigravity React Native Build Context
### Master briefing document | Paste this before starting the React Native build

---

## WHAT YOU ARE BUILDING

You are converting all designed screens from Stitch into a complete, working 
React Native mobile application called **Credwork**.

Credwork gives India's informal workforce — gig workers and domestic workers — 
a verified income certificate they can take to any bank or lender, exactly like 
a salaried employee would. Households who employ domestic workers can also make 
recorded salary payments that build the worker's income history.

This is a real product being built for a hackathon (deadline: 16 March 2025).
It must be fully functional, not a prototype. Both demo flows must work end to end.

---

## STITCH PROJECTS → REACT Native SCREENS

There are 5 Stitch projects. Here is exactly what each contains and what it maps to:

### Project 1: "Credwork S-04 Screen"
Contains all universal screens — shown to every user before role is determined:
- Splash Screen (S-01)
- Language Select (S-02)
- Role Select (S-03)
- Phone + OTP Login (S-04) — two states: phone entry and OTP entry
- Profile Setup (S-05)

### Project 2: "Credwork Gig Worker Screens"
Contains all gig worker screens — shown after login if role = gig_worker:
- Home Dashboard (G-01) — GigScore ring, certificate status, income bars, quick actions
- Upload Bank Statement (G-02) — two states: empty and file selected
- Processing / Scanning (G-03) — live checklist animation
- Income Summary / Success (G-05) — verified screen with GigScore and income
- Certificate Preview (G-07) — full certificate document view
- Share / Export (G-08) — bottom sheet with WhatsApp, download, email, copy link

### Project 3: "Credwork Household Screens"
Contains all household employer screens — shown after login if role = household:
- Home Dashboard (H-01) — worker cards with Pay Now buttons
- Add Worker (H-02) — two states: search and confirmation
- Make Payment (H-03) — payment form with success micro-state
- Payment History (H-04) — grouped by month, filterable

### Project 4: "Credwork Domestic Worker Screens"
Contains all domestic worker screens — shown after login if role = domestic_worker:
- Home Dashboard (D-01) — GigScore, household card, certificate status
- Payment History (D-02) — all payments received, grouped by month
- Certificate Preview (D-03) — same structure as G-07 but ServiConnect data
- Share / Export (D-04) — identical to G-08

### Project 5: "Credwork Global & Admin Screens"
Contains settings screens (all roles) and the admin panel (web only):
- Notification Preferences (X-01)
- Language Toggle (X-02)
- Privacy + Data (X-03)
- Help / FAQ (X-04)
- Admin Dashboard (A-01) — web only, skip for React Native build

---

## TECH STACK

```
Framework:        React Native with Expo (managed workflow)
Navigation:       React Navigation v6
  - Native Stack Navigator for screen-to-screen navigation
  - Bottom Tab Navigator for the main app tabs
PDF parsing:      expo-document-picker (for selecting the PDF)
SVG:              react-native-svg (for the GigScore ring)
Storage:          expo-secure-store (for auth token)
HTTP:             axios or fetch (for backend API calls)
```

Setup commands:
```bash
npx create-expo-app credwork --template blank-typescript
npx expo install @react-navigation/native @react-navigation/native-stack @react-navigation/bottom-tabs
npx expo install react-native-screens react-native-safe-area-context
npx expo install react-native-svg
npx expo install expo-document-picker
npx expo install expo-secure-store
npx expo install expo-sharing expo-file-system
```

---

## DESIGN TOKENS

These are the only colours used in the entire app.
Define these as constants and reference them everywhere — never hardcode hex values.

```javascript
// theme.js
export const colors = {
  primary:     '#111827',   // Charcoal Black — all text, headings, borders
  secondary:   '#2563EB',   // Electric Blue — buttons, CTAs, active states, links
  accent:      '#06B6D4',   // Cyan — GigScore ring, verified badges, data indicators
  background:  '#F4F6FA',   // Off-White — all screen backgrounds, card fills
  disabled:    '#E5E7EB',   // Disabled state backgrounds
  disabledText:'rgba(17, 24, 39, 0.3)',  // Disabled text
  amber:       '#F59E0B',   // Advance payment badges and warnings ONLY
  danger:      '#EF4444',   // Delete account action ONLY
  border:      '#111827',   // Default border colour
  borderLight: '#E5E7EB',   // Subtle dividers and light borders
  textMuted:   'rgba(17, 24, 39, 0.6)',  // Secondary text
  textFaint:   'rgba(17, 24, 39, 0.4)',  // Tertiary text
};

export const spacing = {
  xs: 4, sm: 8, md: 16, lg: 24, xl: 32, xxl: 48,
};

export const radius = {
  sm: 8, md: 12, lg: 16, xl: 24, full: 9999,
};

export const fontSize = {
  xs: 11, sm: 13, base: 15, md: 17, lg: 20, xl: 24, xxl: 32, hero: 40,
};
```

---

## NAVIGATION ARCHITECTURE

The app has two top-level stacks: Auth and Main.
The user starts in Auth. After successful login + profile setup, they move to Main permanently.
Main is role-based — the tab structure depends on the user's role.

```
NavigationContainer
  ├── AuthStack (Stack.Navigator)
  │     ├── Splash          → /screens/auth/SplashScreen.tsx
  │     ├── LanguageSelect  → /screens/auth/LanguageSelectScreen.tsx
  │     ├── RoleSelect      → /screens/auth/RoleSelectScreen.tsx
  │     ├── OTPLogin        → /screens/auth/OTPLoginScreen.tsx
  │     └── ProfileSetup    → /screens/auth/ProfileSetupScreen.tsx
  │
  └── MainStack (role-determined on login)
        ├── GigWorkerTabs (Bottom Tab Navigator) — if role = gig_worker
        │     ├── Home tab
        │     │     ├── GigWorkerDashboard   → /screens/gig/DashboardScreen.tsx
        │     │     ├── UploadStatement      → /screens/gig/UploadScreen.tsx
        │     │     ├── Processing           → /screens/gig/ProcessingScreen.tsx
        │     │     ├── Success              → /screens/gig/SuccessScreen.tsx
        │     │     └── ShareExport          → /screens/gig/ShareScreen.tsx
        │     ├── Certificate tab
        │     │     └── CertificatePreview   → /screens/gig/CertificateScreen.tsx
        │     └── Settings tab
        │           ├── SettingsIndex        → /screens/settings/SettingsScreen.tsx
        │           ├── Notifications        → /screens/settings/NotificationsScreen.tsx
        │           ├── Language             → /screens/settings/LanguageScreen.tsx
        │           ├── Privacy              → /screens/settings/PrivacyScreen.tsx
        │           └── HelpFAQ              → /screens/settings/HelpScreen.tsx
        │
        ├── HouseholdTabs (Bottom Tab Navigator) — if role = household
        │     ├── Home tab
        │     │     ├── HouseholdDashboard   → /screens/household/DashboardScreen.tsx
        │     │     ├── AddWorker            → /screens/household/AddWorkerScreen.tsx
        │     │     ├── MakePayment          → /screens/household/PaymentScreen.tsx
        │     │     └── ShareExport          → /screens/household/ShareScreen.tsx
        │     ├── Workers tab
        │     │     └── PaymentHistory       → /screens/household/PaymentHistoryScreen.tsx
        │     └── Settings tab
        │           └── (same settings screens as above)
        │
        └── DomesticWorkerTabs (Bottom Tab Navigator) — if role = domestic_worker
              ├── Home tab
              │     └── DomesticDashboard    → /screens/domestic/DashboardScreen.tsx
              ├── Certificate tab
              │     ├── CertificatePreview   → /screens/domestic/CertificateScreen.tsx
              │     ├── PaymentHistory       → /screens/domestic/PaymentHistoryScreen.tsx
              │     └── ShareExport          → /screens/domestic/ShareScreen.tsx
              └── Settings tab
                    └── (same settings screens as above)
```

---

## FOLDER STRUCTURE

```
credwork/
  ├── app/                      # If using Expo Router (alternative)
  ├── src/
  │     ├── screens/
  │     │     ├── auth/         # S-01 to S-05
  │     │     ├── gig/          # G-01 to G-08
  │     │     ├── household/    # H-01 to H-04
  │     │     ├── domestic/     # D-01 to D-04
  │     │     └── settings/     # X-01 to X-04
  │     ├── components/         # Shared reusable components
  │     │     ├── GigScoreRing.tsx
  │     │     ├── CertificateCard.tsx
  │     │     ├── PaymentRow.tsx
  │     │     ├── WorkerCard.tsx
  │     │     ├── IncomeBar.tsx
  │     │     └── BottomSheet.tsx
  │     ├── navigation/
  │     │     ├── AuthStack.tsx
  │     │     ├── GigWorkerTabs.tsx
  │     │     ├── HouseholdTabs.tsx
  │     │     ├── DomesticWorkerTabs.tsx
  │     │     └── RootNavigator.tsx
  │     ├── api/                # All backend API calls
  │     │     ├── auth.ts
  │     │     ├── upload.ts
  │     │     ├── certificates.ts
  │     │     ├── household.ts
  │     │     └── worker.ts
  │     ├── store/              # App state (Context API or Zustand)
  │     │     ├── AuthContext.tsx
  │     │     └── UserContext.tsx
  │     ├── theme.ts            # Design tokens (colours, spacing, typography)
  │     └── utils/
  │           ├── gigscore.ts   # GigScore label logic
  │           └── format.ts     # Currency, date formatting
  ├── assets/
  │     └── logo/
  │           ├── credwork-logo-full.png
  │           ├── credwork-wordmark.png
  │           └── credwork-icon.png
  └── App.tsx                   # Root entry point
```

---

## THE GIGSCORE RING COMPONENT

This is the most important shared component. Build it once, use it everywhere.
It appears on: G-01, G-05, D-01, D-03, G-07, and the V0 dashboard.

```typescript
// src/components/GigScoreRing.tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Svg, { Circle } from 'react-native-svg';
import { colors, fontSize } from '../theme';

interface GigScoreRingProps {
  score: number;
  size?: number;        // default 160
  strokeWidth?: number; // default 16
}

const getLabel = (score: number): string => {
  if (score >= 85) return 'Excellent';
  if (score >= 70) return 'Good';
  if (score >= 55) return 'Moderate';
  if (score >= 40) return 'Low';
  return 'Insufficient';
};

export const GigScoreRing: React.FC<GigScoreRingProps> = ({
  score,
  size = 160,
  strokeWidth = 16,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const filled = (score / 100) * circumference;
  const label = getLabel(score);

  return (
    <View style={{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }}>
      <Svg width={size} height={size} style={{ position: 'absolute' }}>
        <Circle
          cx={size / 2} cy={size / 2} r={radius}
          stroke={colors.disabled}
          strokeWidth={strokeWidth}
          fill="none"
        />
        <Circle
          cx={size / 2} cy={size / 2} r={radius}
          stroke={colors.accent}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={`${filled} ${circumference}`}
          strokeLinecap="round"
          rotation="-90"
          origin={`${size / 2}, ${size / 2}`}
        />
      </Svg>
      <Text style={styles.scoreNumber}>{score}</Text>
      <Text style={styles.scoreLabel}>{label}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  scoreNumber: {
    fontSize: fontSize.xxl,
    fontWeight: 'bold',
    color: colors.primary,
    lineHeight: fontSize.xxl * 1.1,
  },
  scoreLabel: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.secondary,
    marginTop: 2,
  },
});
```

---

## WEB-TO-REACT-NATIVE CONVERSION RULES

When converting Stitch/Antigravity components to React Native:

```
HTML/CSS                    →    React Native
────────────────────────────────────────────────────────
<div>                       →    <View>
<p>, <span>, <h1>–<h6>     →    <Text>
<button>                    →    <TouchableOpacity><Text>
<input type="text">         →    <TextInput>
<img>                       →    <Image source={require(...)} />
<a>                         →    <TouchableOpacity onPress={navigate}>
<ul><li>                    →    <FlatList> or mapped <View>s
className="..."             →    style={styles.name}
onClick                     →    onPress
overflow-y: scroll          →    <ScrollView>
position: fixed (bottom)    →    position: 'absolute', bottom: 0
display: flex               →    default in RN (no need to declare)
border-radius: 12px         →    borderRadius: 12   (no 'px')
background-color: #F4F6FA   →    backgroundColor: '#F4F6FA'
font-weight: 600            →    fontWeight: '600'  (string not number)
box-shadow                  →    elevation: 4 (Android) / shadow* (iOS)
gap: 16px                   →    gap: 16  (supported in RN 0.71+)
padding: 16px 24px          →    paddingVertical: 16, paddingHorizontal: 24
```

---

## THE TWO DEMO FLOWS — MUST WORK END TO END

These are the only flows that absolutely must be functional for the demo.
Everything else can have placeholder data.

### Demo Flow 1 — Gig Worker (Raju Kumar)
```
Login with demo phone
        ↓
G-01 Home Dashboard
Shows: GigScore 78 "Good", certificate v2 active, income bars for 6 months
        ↓
Tap "Upload Statement" quick action
        ↓
G-02 Upload Bank Statement
Select a demo PDF file
        ↓
G-03 Processing / Scanning
Live checklist animates through 6 steps
        ↓
G-05 Success — Income Summary
Shows: ₹18,500/month verified, GigScore 78, platforms Swiggy/Zomato/Blinkit
        ↓
Tap "View Full Certificate"
        ↓
G-07 Certificate Preview
Full certificate document with monthly breakdown table
        ↓
Tap share icon → bottom sheet slides up
        ↓
G-08 Share / Export
WhatsApp option primary, 4 share options visible
```

### Demo Flow 2 — ServiConnect (Sharma Household + Priya Devi)
```
Login with household demo phone
        ↓
H-01 Household Dashboard
Shows: Priya Devi (due) + Ramesh Singh (paid)
        ↓
Tap "Pay Now" on Priya Devi's card
        ↓
H-03 Make Payment
Pre-filled: ₹3,500, March 2025, Salary
Tap "Pay ₹3,500"
        ↓
Success micro-state: "Payment sent! Priya Devi's record has been updated."
        ↓
Login with domestic worker demo phone (second device or switch accounts)
        ↓
D-01 Domestic Worker Dashboard
Shows: GigScore updated, March now shows as "Paid ✓"
        ↓
Tap "My Certificate" → D-03 Certificate Preview
Shows updated certificate with March payment included
```

---

## BACKEND API BASE URL

```javascript
// src/api/config.ts
export const API_BASE_URL = 'http://YOUR_BACKEND_IP:3000';
// Replace with actual backend URL when ready
// For local testing: use your machine's local IP (not localhost — 
// localhost on a phone means the phone itself, not your computer)
// Find your IP: run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
// Example: http://192.168.1.105:3000
```

---

## DEMO DATA (hardcode this as fallback if backend isn't ready)

If the backend isn't connected yet, screens should show this data.
This ensures the UI is always demonstrable even during development.

```javascript
// src/utils/demoData.ts

export const DEMO_GIG_WORKER = {
  id: 'demo-gig-001',
  name: 'Raju Kumar',
  city: 'Mumbai',
  role: 'gig_worker',
  gigscore: 78,
  gigscoreLabel: 'Good',
  monthlyAvgInr: 18500,
  certificateId: 'CW-2025-00847',
  certificateVersion: 2,
  certificateStatus: 'active',
  certificateIssued: '1 March 2025',
  incomeMonths: [
    { month: 'Oct', amount: 17200, pct: 70 },
    { month: 'Nov', amount: 19800, pct: 85 },
    { month: 'Dec', amount: 15500, pct: 60 },
    { month: 'Jan', amount: 21000, pct: 90 },
    { month: 'Feb', amount: 18900, pct: 80 },
    { month: 'Mar', amount: 19100, pct: 75 },
  ],
  platforms: ['Swiggy', 'Zomato', 'Blinkit', 'Rapido'],
};

export const DEMO_DOMESTIC_WORKER = {
  id: 'demo-domestic-001',
  name: 'Priya Devi',
  city: 'New Delhi',
  role: 'domestic_worker',
  gigscore: 71,
  gigscoreLabel: 'Good',
  monthlyAvgInr: 3500,
  certificateId: 'CW-2025-01203',
  certificateVersion: 1,
  certificateStatus: 'active',
  certificateIssued: '15 February 2025',
  currentHousehold: 'Sharma Household',
  householdCity: 'New Delhi',
  memberSince: 'October 2024',
  marchPaid: true,
  payments: [
    { month: 'Feb 2025', household: 'Sharma Household', type: 'Salary', date: '1 Feb 2025', amount: 3500 },
    { month: 'Jan 2025', household: 'Sharma Household', type: 'Salary', date: '1 Jan 2025', amount: 3500 },
    { month: 'Dec 2024', household: 'Sharma Household', type: 'Salary', date: '1 Dec 2024', amount: 3500 },
    { month: 'Dec 2024', household: 'Sharma Household', type: 'Bonus', date: '20 Dec 2024', amount: 500 },
    { month: 'Nov 2024', household: 'Sharma Household', type: 'Salary', date: '1 Nov 2024', amount: 3500 },
    { month: 'Oct 2024', household: 'Sharma Household', type: 'Salary', date: '1 Oct 2024', amount: 3000 },
  ],
};

export const DEMO_HOUSEHOLD = {
  id: 'demo-household-001',
  name: 'Sharma Household',
  city: 'New Delhi',
  role: 'household',
  workers: [
    {
      id: 'demo-domestic-001',
      name: 'Priya Devi',
      role: 'Cook · Full-time',
      salary: 3500,
      lastPayment: '1 Feb 2025',
      marchPaid: false,
    },
    {
      id: 'demo-domestic-002',
      name: 'Ramesh Singh',
      role: 'Driver',
      salary: 8000,
      lastPayment: '1 Mar 2025',
      marchPaid: true,
    },
  ],
};
```

---

## SCREENS THAT CAN HAVE PLACEHOLDER UI FOR DEMO

These screens will not be shown during the demo presentation.
Build them but they don't need to be connected to the backend.

- X-01 Notification Preferences — static toggles, no backend
- X-02 Language Toggle — just switches a state variable
- X-03 Privacy + Data — static content
- X-04 Help / FAQ — static accordions
- D-02 Payment History — can use DEMO_DOMESTIC_WORKER.payments
- H-04 Payment History — can use static demo data
- G-03 Processing screen — animation only, no backend polling needed for demo

---

## IMPORTANT REACT NATIVE BEHAVIOURS TO KNOW

**Safe area:** Always wrap screens in `<SafeAreaView>` from 
`react-native-safe-area-context`. Without this, content goes behind 
the phone's notch and status bar.

**Keyboard avoiding:** For screens with text inputs (OTP, Profile Setup, 
Add Worker, Make Payment), wrap in `<KeyboardAvoidingView>` so the keyboard 
doesn't cover the input fields.

**Bottom sheet (G-08, D-04):** Use `react-native-reanimated` + 
`@gorhom/bottom-sheet` for the share sheet. This is the cleanest 
bottom sheet library for Expo.
```bash
npx expo install react-native-reanimated @gorhom/bottom-sheet
```

**FlatList vs ScrollView:** Use `<FlatList>` for payment history lists 
(long, dynamic lists). Use `<ScrollView>` for screens with a fixed number 
of items (dashboards, forms).

**Image assets:** Logo files go in `/assets/logo/`. Reference them as:
```javascript
<Image source={require('../../assets/logo/credwork-wordmark.png')} />
```

**No CSS units:** All StyleSheet values are unitless numbers. 
`padding: 16` means 16 density-independent pixels. No 'px', 'rem', '%'.
Exception: `flex: 1` is the way to fill available space.

---

## WHAT TO TELL ANTIGRAVITY WHEN STARTING THE BUILD

Paste the entire contents of this file, then add:

```
I have 5 Stitch projects with all screens already designed.
I need you to:

1. Start with the navigation skeleton — App.tsx + all navigators + 
   empty screen files. Every screen should render a placeholder View 
   with the screen name as a Text label. The app must be runnable 
   immediately after this step.

2. Then convert each Stitch screen one by one into working React Native 
   components, starting with the auth flow (S-01 → S-02 → S-03 → S-04 → S-05).

3. Then the gig worker flow (G-01 → G-02 → G-03 → G-05 → G-07 → G-08).

4. Then the household flow (H-01 → H-02 → H-03 → H-04).

5. Then the domestic worker flow (D-01 → D-02 → D-03 → D-04).

6. Then the settings screens (X-01 → X-02 → X-03 → X-04).

For each screen: import from theme.ts for all colours and spacing.
Use the GigScoreRing component wherever a GigScore is displayed.
Use demo data from demoData.ts until the backend is connected.
Every screen must use SafeAreaView.
All screens with text inputs must use KeyboardAvoidingView.
```
```

---

## FUTURE USE (second hackathon or production)

This codebase is structured to extend cleanly. When building on this later:

- Backend URL lives in one place (`src/api/config.ts`) — one change connects to production
- Demo data is isolated in `src/utils/demoData.ts` — easy to rip out when real data flows
- GigScoreRing is a pure component — takes any score, renders correctly
- Navigation is role-based from the root — adding a new role means adding one new Tab Navigator
- All colours are tokens — rebranding means changing theme.ts only
- Certificate generation is backend-driven — the frontend just renders what the API returns

---

*This document is the complete context for building Credwork's React Native frontend.*
*Share with Antigravity at the start of every session.*
*Keep it open alongside the Stitch projects.*
