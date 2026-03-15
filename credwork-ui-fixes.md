# Credwork — UI Fix Prompts for Antigravity
### Phased correction plan | Paste one phase at a time | Wait for completion before next phase

---

## HOW TO USE THIS FILE

1. Start a new Antigravity session
2. Paste the MASTER CONTEXT BLOCK first (from credwork-antigravity-rn-context.md)
3. Then paste Phase 1 prompt below
4. Wait for Phase 1 to complete fully and verify the fixes
5. Then paste Phase 2, and so on
6. Do NOT paste multiple phases at once — fixes build on each other

---

---

# PHASE 1 — Foundation Fixes
### Fix the global issues that affect every screen before touching individual screens.
### These are blocking bugs — nothing else can be properly evaluated until these are resolved.

---

```
PHASE 1 — FOUNDATION FIXES

These are system-wide issues affecting every screen. Fix all of them before 
touching any individual screen. Do not move to any other fixes until all 
items in this phase are confirmed working.

---

FIX 1 — SAFEAREAVIEW ON ALL SCREENS

Every single screen in the app must be wrapped in SafeAreaView from 
react-native-safe-area-context. No exceptions.

The correct import and usage:
  import { SafeAreaView } from 'react-native-safe-area-context';
  
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#F4F6FA' }}>
      {/* screen content */}
    </SafeAreaView>
  );

Go through every screen file in the project and confirm SafeAreaView 
is the outermost wrapper. The background colour of SafeAreaView must 
always be #F4F6FA so the status bar area matches the screen.

---

FIX 2 — COLOUR TOKEN VIOLATIONS (GLOBAL)

Audit every screen and every component in the project for colour violations.
The only permitted colours are:
  #111827  Charcoal Black   → text, headings, borders at rest
  #2563EB  Electric Blue    → ALL primary buttons, CTAs, active states, links
  #06B6D4  Cyan             → GigScore ring, verified badges, accent indicators
  #F4F6FA  Off-White        → ALL backgrounds, ALL card fills
  #E5E7EB  Light grey       → disabled backgrounds, dividers ONLY
  #F59E0B  Amber            → Advance payment badges and warning states ONLY
  #EF4444  Red              → Delete account action ONLY

SPECIFIC VIOLATIONS TO FIX:
- Any green colour anywhere in the app → replace with the correct token
- Dashed borders using green → replace border colour with #2563EB
- Checkmarks using green → replace with #06B6D4
- WhatsApp icon background using green → the WhatsApp icon uses its own 
  brand green ONLY for the icon itself — the row background must be #F4F6FA

---

FIX 3 — PRIMARY BUTTON COLOUR (GLOBAL)

Every primary action button in the app is rendering in Charcoal Black (#111827).
This is wrong. Every primary action button must use:
  backgroundColor: '#2563EB'
  color/Text: white (#FFFFFF is permitted for text ON a #2563EB button only)

Screens with broken primary buttons that must be fixed:
- S-04: "Send OTP" button
- S-04: "Verify" button  
- S-05: "Continue" button
- G-02: "Start Scan" button (active state only — disabled state stays grey)
- G-05: "View Full Certificate" button and "Share Certificate" button
- H-01: "Pay Now" button on every worker card
- H-02: "Find Worker" button and "Confirm and Add Worker" button
- H-03: "Pay ₹3,500" button
- X-02: Language card active state

Fix ALL of these in one pass. Search the entire codebase for 
backgroundColor: '#111827' on any TouchableOpacity or Button component
and evaluate whether it should be #2563EB instead.

---

FIX 4 — BOTTOM NAVIGATION BAR ICONS

The bottom tab bar icons are rendering as crossed-out placeholder boxes.
This means the icon library is either not installed or not imported correctly.

Fix:
1. Install @expo/vector-icons if not already installed:
   npx expo install @expo/vector-icons

2. Use Ionicons from @expo/vector-icons for all tab bar icons:
   import { Ionicons } from '@expo/vector-icons';

3. The three tab bar items and their icons:
   
   For Gig Worker and Domestic Worker tabs:
   - Home tab:        icon name "home" (inactive) / "home" (active, filled)
   - Certificate tab: icon name "document-text-outline" / "document-text"
   - Settings tab:    icon name "settings-outline" / "settings"
   
   For Household tabs:
   - Home tab:        icon name "home-outline" / "home"
   - Workers tab:     icon name "people-outline" / "people"
   - Settings tab:    icon name "settings-outline" / "settings"

4. Tab bar styling:
   tabBarActiveTintColor: '#2563EB'
   tabBarInactiveTintColor: 'rgba(17, 24, 39, 0.5)'
   tabBarStyle: { backgroundColor: '#F4F6FA', borderTopColor: '#E5E7EB', borderTopWidth: 1 }
   tabBarLabelStyle: { fontSize: 11, fontWeight: '500' }

---

FIX 5 — THE BLACK HEADER BOX (LOGO PLACEHOLDER)

A black rectangular block is rendering at the top of multiple screens 
(Gig Worker Dashboard, Domestic Worker Dashboard, Certificate screens).
This is a broken image reference.

Fix:
Replace every instance of this broken image block with the actual 
Credwork wordmark rendered as styled Text — since the PNG asset may 
not be loading correctly, use this reliable text-based wordmark as 
a temporary fix:

  <View style={{ flexDirection: 'row' }}>
    <Text style={{ fontSize: 20, fontWeight: 'bold', color: '#111827' }}>Cred</Text>
    <Text style={{ fontSize: 20, fontWeight: 'bold', color: '#2563EB' }}>work</Text>
  </View>

Apply this fix to every screen that shows the broken black box.
Once the PNG asset path is confirmed working, the Image component 
can be restored — but the styled Text fallback must work for now.

---

FIX 6 — CYAN LEFT BORDER ACCENT ON CARDS

The cyan left border accent on cards (Latest Certificate card, Current 
Household card) is rendering as a thick, clunky light-blue bar that 
looks broken.

The correct implementation:
  borderLeftWidth: 3,
  borderLeftColor: '#06B6D4',
  borderTopWidth: 0,
  borderRightWidth: 0,
  borderBottomWidth: 0,

Do NOT use a separate View as the accent bar. Apply the borderLeft 
directly to the card's container style. The accent should be a slim, 
elegant 3px line — not a thick block.

---

After completing all 6 fixes in Phase 1, confirm:
- No screen has content bleeding into the status bar
- All primary buttons are Electric Blue (#2563EB)
- No green colour exists anywhere in the app except the WhatsApp icon itself
- Bottom tab icons are visible and correct
- No black box appears on any screen
- All cyan left accents are slim 3px lines
```

---

---

# PHASE 2 — Auth Flow Fixes
### Fix all universal/auth screens. These are seen by every user type.

---

```
PHASE 2 — AUTH FLOW FIXES

Fix the following screens in order: S-02, S-03, S-04 (both states), S-05.

---

FIX 1 — S-02 LANGUAGE SELECT: Remove pagination dots + increase logo size

Two changes on this screen:
1. Remove the three pagination dots at the bottom of the screen entirely.
   There is only one screen here — dots imply a swipeable carousel which 
   does not exist. Delete any pagination/indicator component.

2. The Credwork logo/wordmark at the top is too small.
   Increase it so the wordmark is clearly readable — approximately 
   40% of screen width. Give it more vertical breathing room above 
   and below it.

---

FIX 2 — S-03 ROLE SELECT: Increase sub-label text size

The grey descriptive text under each role card label is too small.
These sub-labels exist specifically so low-literacy users recognise 
which role applies to them by reading familiar words.

Current issue: text is too small and light to read comfortably.
Fix: increase sub-label fontSize to at least 13, and set colour to 
'rgba(17, 24, 39, 0.7)' — dark enough to read, lighter than the 
primary label.

Sub-label text content (keep exactly as-is, just fix the size):
- Gig Worker: "Swiggy · Zomato · Rapido · Blinkit · Urban Company"
- Domestic Worker: "Cook · Cleaner · Driver · Caretaker"
- Household: "Pay your worker and help them build their credit history"

---

FIX 3 — S-04 PHONE ENTRY: Move "Send OTP" button below the input field

Current issue: "Send OTP" button is pinned to the bottom of the screen.
On Android, when the keyboard opens, the button is hidden behind it.
The user must dismiss the keyboard to find and tap the button.

Fix: Remove the button from the bottom fixed position.
Place it directly below the phone number input field and the reassurance 
text line. The button should be inline in the scroll flow, not fixed.

The screen layout from top to bottom should be:
  1. Credwork wordmark (top)
  2. Heading: "Enter your mobile number"
  3. Sub-heading in Hindi
  4. "MOBILE NUMBER" label
  5. Phone input field with +91 prefix
  6. Reassurance text: "We'll send a 6-digit code to this number"
  7. "Send OTP" button ← directly here, not at the bottom
  
Wrap the entire screen in KeyboardAvoidingView:
  import { KeyboardAvoidingView, Platform } from 'react-native';
  
  <KeyboardAvoidingView 
    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    style={{ flex: 1 }}
  >
    <ScrollView contentContainerStyle={{ flexGrow: 1, padding: 24 }}>
      {/* all content here */}
    </ScrollView>
  </KeyboardAvoidingView>

---

FIX 4 — S-04 OTP ENTRY: Fix digit visibility + move Verify button up

Two issues:
1. The typed digits inside the OTP boxes are not visible.
   Fix the TextInput styling for each OTP box:
     color: '#111827'          ← text colour (was probably white or transparent)
     fontSize: 24
     fontWeight: 'bold'
     textAlign: 'center'
     backgroundColor: '#F4F6FA'
     borderWidth: 1.5
     borderColor: '#111827'    ← rest state
     borderRadius: 8
     width: 44
     height: 52
   
   When a box is focused/active, border changes to:
     borderColor: '#2563EB'

2. Move the "Verify" button to directly below the OTP boxes and 
   the countdown timer. Same fix as the phone screen — button should 
   not be at the bottom behind the keyboard. Apply the same 
   KeyboardAvoidingView + ScrollView pattern.

---

FIX 5 — S-05 PROFILE SETUP: Add KeyboardAvoidingView + ScrollView

When a user taps the name or city input field, the keyboard appears 
and blocks what they are typing.

Fix: Wrap the entire screen in the same pattern as S-04:
  <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
    <ScrollView contentContainerStyle={{ flexGrow: 1, padding: 24 }}>
      {/* all fields */}
    </ScrollView>
  </KeyboardAvoidingView>

The "Continue" button should be inside the ScrollView at the bottom 
of the content — NOT fixed at the bottom of the screen. This way 
when the keyboard opens, the user can scroll to find the button.
```

---

---

# PHASE 3 — Gig Worker Flow Fixes
### Fix all gig worker screens. This is Demo Flow 1 — must be perfect.

---

```
PHASE 3 — GIG WORKER FLOW FIXES

Fix the following screens: G-01, G-02, G-03, G-05, G-07, G-08.

---

FIX 1 — G-01 DASHBOARD: Fix layout order + GigScore typography + logo

Three issues on the Gig Worker Dashboard:

ISSUE A — Layout reorder:
The current layout order is wrong. Reorder the sections to:
  1. Header bar (wordmark + avatar)
  2. Identity row (name + city + Verified badge)
  3. GigScore card (PRIMARY — largest element)
  4. Three quick action buttons row ← MOVE UP from bottom
  5. Latest Certificate card
  6. Income Snapshot (6-month bars)
  7. Bottom navigation bar

The quick action buttons must come IMMEDIATELY after the GigScore card,
not at the bottom of the screen. This is the user's most likely next 
action after seeing their score.

ISSUE B — GigScore typography too small:
The score number (e.g. "78") and the label (e.g. "Good") are too small.
Fix the GigScoreRing component:
  - Score number: fontSize: 40, fontWeight: 'bold', color: '#111827'
  - Label: fontSize: 16, fontWeight: '600', color: '#2563EB'
  - Ring outer diameter: 160px minimum
  - Ring stroke width: 16px

ISSUE C — Black box at top:
Already fixed in Phase 1 (the text-based wordmark fallback).
Confirm the fix is applied here.

---

FIX 2 — G-02 UPLOAD STATEMENT: Fix colour violations

The upload zone and related elements are using unapproved green colours.
Fix:
- Upload zone dashed border: change to #2563EB (Electric Blue)
- Upload zone background tint: #2563EB at 5% opacity
- Cloud upload icon inside the zone: #2563EB
- "Start Scan" button active state: #2563EB background, white text
- Any green checkmark when file is selected: change to #06B6D4

No green should exist anywhere on this screen.

---

FIX 3 — G-03 PROCESSING/SCANNING: Animate the loading indicator

The circular spinner on the current processing step is static and 
does not animate.

Fix using React Native's Animated API:
  import { Animated, Easing } from 'react-native';
  
  // In the component:
  const spinValue = useRef(new Animated.Value(0)).current;
  
  useEffect(() => {
    Animated.loop(
      Animated.timing(spinValue, {
        toValue: 1,
        duration: 1000,
        easing: Easing.linear,
        useNativeDriver: true,
      })
    ).start();
  }, []);
  
  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });
  
  // Apply to the spinner:
  <Animated.View style={{ transform: [{ rotate: spin }] }}>
    {/* spinner circle SVG or icon */}
  </Animated.View>

The spinner should only appear on the CURRENT step (step 3 — 
"Finding your gig payments" in the demo state). Completed steps 
show a filled cyan checkmark. Pending steps show an empty grey circle.

---

FIX 4 — G-05 SUCCESS SCREEN: Fix overlapping text layout

The "Average monthly income" text and the "78 Good" GigScore are 
overlapping or wrapping badly.

Fix the income summary card layout:
- The card uses a vertical stack (flexDirection: 'column') — not a row
- Each section inside the card is separated by a 1px #E5E7EB divider
- The GigScore row uses flexDirection: 'row' with the ring on the LEFT 
  and the label/sublabel stacked on the RIGHT — they should NEVER overlap

Correct structure inside the summary card:
  <View> ← card container, flexDirection: 'column'
    
    <View> ← ROW 1: average income (centred)
      <Text>Average monthly income</Text>  ← small label
      <Text>₹18,500 / month</Text>         ← large bold hero number
    </View>
    
    <View style={divider} />
    
    <View style={{ flexDirection: 'row', alignItems: 'center' }}> ← ROW 2: GigScore
      <GigScoreRing score={78} size={64} strokeWidth={8} />  ← small ring, left side
      <View style={{ marginLeft: 16 }}>                       ← text, right side
        <Text>GigScore</Text>
        <Text style={{ color: '#2563EB', fontWeight: 'bold' }}>Good</Text>
        <Text>Income consistency score</Text>
      </View>
    </View>
    
    <View style={divider} />
    
    <View style={{ flexDirection: 'row' }}> ← ROW 3: period + version side by side
      <View style={{ flex: 1 }}>
        <Text>Period</Text>
        <Text>Oct 2024 – Mar 2025</Text>
      </View>
      <View style={{ flex: 1 }}>
        <Text>Version</Text>
        <Text>v2</Text>
      </View>
    </View>
    
  </View>

---

FIX 5 — G-07 CERTIFICATE PREVIEW: Fix broken logo image

A dark-grey rectangle appears in the top-left of the certificate 
where the logo should be. This is a broken Image source.

Fix: Apply the same text-based wordmark fallback from Phase 1 Fix 5.
Inside the certificate card header:
  <View style={{ flexDirection: 'row' }}>
    <Text style={{ fontSize: 16, fontWeight: 'bold', color: '#111827' }}>Cred</Text>
    <Text style={{ fontSize: 16, fontWeight: 'bold', color: '#2563EB' }}>work</Text>
  </View>

---

FIX 6 — G-08 SHARE SHEET: Fix the context-breaking navigation bug

Current bug: Tapping "Share Profile" from the Home Dashboard navigates 
the user away from the dashboard to the Income Certificate screen, 
then opens the share sheet. The user's location changes unexpectedly.

This is a routing architecture fix:

The Share sheet (G-08) must be implemented as a Bottom Sheet Modal 
that renders ON TOP of whatever screen the user is currently on.
It must NOT be a separate screen that you navigate to.

Implementation using @gorhom/bottom-sheet:

  // In the component that has the Share button (Dashboard, Certificate):
  import BottomSheet, { BottomSheetView } from '@gorhom/bottom-sheet';
  const bottomSheetRef = useRef<BottomSheet>(null);
  
  // When Share is tapped:
  const handleShare = () => {
    bottomSheetRef.current?.expand();
  };
  
  // In the JSX — placed at the root level of the screen, after all content:
  <BottomSheet
    ref={bottomSheetRef}
    index={-1}          ← starts closed
    snapPoints={['65%']}
    enablePanDownToClose={true}
    backgroundStyle={{ backgroundColor: '#F4F6FA' }}
  >
    <BottomSheetView>
      {/* share options content here */}
    </BottomSheetView>
  </BottomSheet>

The user's screen underneath should remain visible (dimmed) when 
the sheet is open. The header should still show "Home" or whichever 
screen they were on — it must never change to "Income Certificate" 
unless the user explicitly navigated there.

Apply this same fix to D-04 as well (same bug in domestic worker flow).
```

---

---

# PHASE 4 — Domestic Worker Flow Fixes
### Fix all domestic worker screens.

---

```
PHASE 4 — DOMESTIC WORKER FLOW FIXES

Fix the following screens: D-01, D-02, D-03, D-04.

---

FIX 1 — D-01 DASHBOARD: Fix GigScore dullness + Current Household card

Two issues:

ISSUE A — "Your GigScore" heading is dull:
The GigScore section on the domestic worker dashboard looks flat and 
lacks visual impact compared to the gig worker version.
Fix: Apply the exact same GigScore card treatment as G-01 —
same card border (1.5px #111827), same ring size (160px), 
same typography fix from Phase 3 Fix 1 Issue B.
The ring and numbers should look identical on both dashboards.

ISSUE B — Current Household card: fix cyan bar + fix "March paid ✓" alignment:
The cyan left border is rendering as a thick clunky bar (fixed in Phase 1 Fix 6).
Confirm that fix is applied here.

The "March paid ✓" pill is misaligned — it's floating to the top-right 
of the card instead of being vertically centred on the right side.
Fix the card layout:
  <View style={{ flexDirection: 'row', alignItems: 'center' }}> ← card container
    <View style={{ flex: 1 }}> ← left side
      <Text>CURRENT EMPLOYER</Text>
      <Text>Sharma Household</Text>
      <Text>New Delhi · Since Oct 2024</Text>
    </View>
    <View> ← right side — the pill sits here, vertically centred by alignItems: 'center' on parent
      <View style={paidPillStyle}>
        <Text>March paid ✓</Text>
      </View>
    </View>
  </View>

Pill style for "March paid ✓":
  backgroundColor: 'rgba(6, 182, 212, 0.15)'
  paddingHorizontal: 10
  paddingVertical: 5
  borderRadius: 999
  Text color: '#06B6D4'
  fontSize: 12
  fontWeight: '600'

---

FIX 2 — D-02 PAYMENT HISTORY: Rewrite layout to match Household version

The current D-02 layout is poor. The Household Payment History (H-04) 
layout is clean and well-structured. Rewrite D-02 to use the same 
layout pattern as H-04.

The target layout (matching H-04 structure):
  - Total earnings summary card at the top (with cyan top border accent)
  - Filter chips row below (All · Salary · Bonus · Advance)
  - Payment list grouped by month
  - Each month has a bold header with month name + total on the right
  - Each payment row: icon (left) + name + type + date (centre) + amount + Verified (right)
  - Month groups separated by subtle dividers

The content is different (D-02 shows payments RECEIVED, H-04 shows 
payments MADE) but the visual structure must be identical.

Key difference in D-02 rows vs H-04 rows:
  H-04 shows: Worker name + payment type
  D-02 shows: Household name ("Sharma Household") + payment type

---

FIX 3 — D-03 CERTIFICATE PREVIEW: Add Certificate History section

The Gig Worker certificate (G-07) has a "Certificate History" section 
at the bottom showing version history. D-03 is missing this entirely.

Add the Certificate History section to D-03, below the certificate card:

  <View style={{ marginTop: 24 }}>
    <Text style={{ fontSize: 14, fontWeight: 'bold', color: '#111827', marginBottom: 12 }}>
      Certificate History
    </Text>
    
    {/* Version row */}
    <View style={{ flexDirection: 'row', alignItems: 'center', 
                   paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: '#E5E7EB' }}>
      <Ionicons name="document-text-outline" size={18} color="#06B6D4" />
      <View style={{ flex: 1, marginLeft: 12 }}>
        <Text style={{ fontSize: 13, fontWeight: '600', color: '#111827' }}>Version 1.0</Text>
        <Text style={{ fontSize: 11, color: 'rgba(17,24,39,0.6)' }}>Generated on 15 Feb 2025</Text>
      </View>
      <View style={{ backgroundColor: 'rgba(6,182,212,0.15)', paddingHorizontal: 8, 
                     paddingVertical: 4, borderRadius: 999 }}>
        <Text style={{ fontSize: 11, color: '#06B6D4', fontWeight: '600' }}>ACTIVE</Text>
      </View>
    </View>
  </View>

---

FIX 4 — D-04 SHARE SHEET: Fix context-breaking navigation bug

Same bug as G-08. Apply the identical bottom sheet fix from Phase 3 Fix 6.
The share sheet must open ON TOP of D-01 or D-03 without navigating away.
The user's current screen context must never change when the share sheet opens.
```

---

---

# PHASE 5 — Household Flow Fixes
### Fix all household screens.

---

```
PHASE 5 — HOUSEHOLD FLOW FIXES

Fix the following screens: H-01, H-02, H-03.
H-04 Payment History is the reference layout — do not change it.

---

FIX 1 — H-01 DASHBOARD: Fix "Pay Now" button styling

The "Pay Now" buttons on the worker cards look dark, disabled, 
and unclickable. They must use primary button styling.

Fix every "Pay Now" button on the worker cards:
  backgroundColor: '#2563EB'
  color: white (for the Text inside)
  paddingHorizontal: 16
  paddingVertical: 8
  borderRadius: 999  ← pill shape
  fontWeight: 'bold'
  fontSize: 13

For Ramesh Singh's card (already paid this month), the "Pay Now" 
button should be in the DISABLED state:
  backgroundColor: '#E5E7EB'
  Text color: 'rgba(17, 24, 39, 0.3)'
  Not tappable (disabled={true} on TouchableOpacity)

The visual distinction between "Pay Now" (active, blue) and 
"Paid ✓" (disabled, grey) must be immediately obvious at a glance.

---

FIX 2 — H-02 ADD WORKER: Fix button colour

The "Find Worker" and "Confirm and Add Worker" buttons are rendering 
in Charcoal Black. Apply primary button styling:
  backgroundColor: '#2563EB'
  Text: white
  
Same fix as Phase 1 Fix 3 — confirm it was applied here specifically.

---

FIX 3 — H-03 MAKE PAYMENT: Fix segmented control active state

The Salary/Bonus/Advance segmented control uses Charcoal Black 
for its active/selected segment instead of Electric Blue.

Fix the selected segment style:
  Selected:   backgroundColor: '#2563EB', Text color: white
  Unselected: backgroundColor: '#F4F6FA', Text color: '#111827', 
              border: 1px solid '#E5E7EB'

The segmented control container:
  borderWidth: 1.5
  borderColor: '#111827'
  borderRadius: 8
  flexDirection: 'row'
  overflow: 'hidden'   ← so selected segment fills cleanly to the border
```

---

---

# PHASE 6 — Settings Flow Fixes
### Fix settings screens. Lower priority — not in the demo flow but must look correct.

---

```
PHASE 6 — SETTINGS FLOW FIXES

Fix the following screens: X-01, X-02.
X-03 and X-04 are static content screens — only fix if colour violations exist.

---

FIX 1 — X-01 NOTIFICATIONS: Fix toggle switch colours

The toggle switches are rendering in default black and white.
The active "ON" state must be Electric Blue.

Fix using React Native's Switch component:
  <Switch
    value={isEnabled}
    onValueChange={setIsEnabled}
    trackColor={{ 
      false: '#E5E7EB',    ← OFF state track: light grey
      true: '#2563EB'      ← ON state track: Electric Blue
    }}
    thumbColor={'#FFFFFF'}  ← thumb always white
    ios_backgroundColor={'#E5E7EB'}
  />

Apply this to every toggle on the Notifications screen.
All toggles default to ON (true) as per the design spec.

---

FIX 2 — X-02 LANGUAGE TOGGLE: Fix active card state

The currently selected language card must show the active state:
  - Border: 1.5px solid #2563EB (instead of #111827)
  - Background: rgba(37, 99, 235, 0.05) — very subtle blue tint
  - A filled checkmark icon on the right: #2563EB colour
    Use: <Ionicons name="checkmark-circle" size={22} color="#2563EB" />

The inactive card:
  - Border: 1.5px solid #111827
  - Background: #F4F6FA
  - No checkmark icon

English is the active card by default in this build.
```

---

---

# PHASE 7 — Final Polish & Demo Preparation
### Run through both demo flows completely. Fix anything that breaks the flow.

---

```
PHASE 7 — FINAL POLISH & DEMO PREP

Run both demo flows from start to finish and fix any remaining issues.

---

DEMO FLOW 1 — GIG WORKER (run through this completely):
  Login → G-01 Dashboard → Upload Statement → G-02 → G-03 Processing → 
  G-05 Success → G-07 Certificate → G-08 Share Sheet

Check each transition:
- Does navigation.replace work correctly from Splash (no back to splash)?
- Does the role-based navigation correctly show GigWorkerTabs after login?
- Does the Share sheet open as a bottom sheet WITHOUT navigating away?
- Does the processing animation actually animate (spinner rotating)?
- Do all buttons show Electric Blue?
- Is the GigScore ring visible with correct size and colour?

---

DEMO FLOW 2 — HOUSEHOLD + DOMESTIC WORKER (run through this completely):
  Household login → H-01 Dashboard → H-03 Make Payment → Success state → 
  Switch to domestic worker → D-01 Dashboard → D-03 Certificate

Check each transition:
- Does the household role correctly show HouseholdTabs after login?
- Are the Pay Now buttons Electric Blue and tappable?
- Does the payment success micro-state show and then navigate back to H-01?
- Does the domestic worker dashboard show GigScore ring correctly?
- Does D-03 have the Certificate History section?

---

FINAL CHECKS (apply fixes for anything found):

1. Run on a physical Android device via Expo Go — not just simulator
2. Check that no content bleeds into the status bar on any screen
3. Check that keyboard does not block buttons on S-04, S-05
4. Check that all card left-border accents are slim 3px lines
5. Check that payment type badges use correct colours:
   Salary: cyan (#06B6D4)
   Bonus: blue (#2563EB)  
   Advance: amber (#F59E0B)
6. Check that the GigScore ring correctly shows percentage fill 
   (78% filled = 78 score, not 78% of the visual)
7. Check that demo data is showing correctly on all screens 
   (Raju Kumar, ₹18,500/month, GigScore 78 on gig worker side)
   (Priya Devi, ₹3,500/month, GigScore 71 on domestic worker side)
```

---

---

## QUICK REFERENCE — Fix Priority Order

```
Phase 1 — Foundation (do first, blocks everything else)
  ✓ SafeAreaView on all screens
  ✓ Colour token violations (remove all green)
  ✓ Primary buttons = Electric Blue everywhere
  ✓ Bottom nav icons fixed
  ✓ Black header box replaced with text wordmark
  ✓ Cyan left border = slim 3px line

Phase 2 — Auth Flow
  ✓ Language screen: remove dots, bigger logo
  ✓ Role screen: bigger sub-label text
  ✓ Phone screen: Send OTP button below input
  ✓ OTP screen: visible digits + Verify button up
  ✓ Profile screen: KeyboardAvoidingView + ScrollView

Phase 3 — Gig Worker (Demo Flow 1 — critical)
  ✓ Dashboard: reorder layout + bigger GigScore text
  ✓ Upload: remove green, use Electric Blue
  ✓ Processing: animate the spinner
  ✓ Success: fix overlapping GigScore + income layout
  ✓ Certificate: fix broken logo
  ✓ Share: fix context-breaking navigation bug

Phase 4 — Domestic Worker
  ✓ Dashboard: GigScore impact + fix "March paid" alignment
  ✓ Payment History: rewrite to match Household layout
  ✓ Certificate: add Certificate History section
  ✓ Share: fix same context-breaking bug as gig worker

Phase 5 — Household
  ✓ Dashboard: Pay Now buttons = Electric Blue
  ✓ Add Worker: button colour fix
  ✓ Make Payment: segmented control active = Electric Blue

Phase 6 — Settings
  ✓ Notifications: toggle switches = Electric Blue when ON
  ✓ Language: active card gets blue border + checkmark

Phase 7 — Demo Prep
  ✓ Run both demo flows end to end
  ✓ Fix anything that breaks
  ✓ Test on physical Android device
```

---

*Paste one phase at a time. Verify fixes before moving to the next phase.*
*Phase 1 and Phase 3 are the most critical — they directly affect the demo.*
