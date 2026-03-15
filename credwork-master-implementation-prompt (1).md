# Credwork — Master Implementation Prompt
### Complete phased build instructions for Antigravity | One phase at a time
### Current state: Frontend UI built, Backend built, Integration pending
### ML layer: IsolationForest anomaly detection (Phase 7B)

---

## HOW TO USE THIS FILE

1. Start every Antigravity session by pasting the SESSION CONTEXT BLOCK below
2. Then paste ONE phase prompt at a time
3. Wait for full completion and verify before pasting the next phase
4. Do NOT combine phases — each phase builds on the previous one
5. If Antigravity loses context mid-session, re-paste the SESSION CONTEXT BLOCK

---

---

# SESSION CONTEXT BLOCK
### Paste this at the start of every Antigravity session

---

```
You are working on Credwork — a React Native (Expo) mobile application and a 
FastAPI Python backend. Both are already partially built. Your job is to complete, 
fix, and integrate them.

PROJECT STRUCTURE:
- Frontend: React Native with Expo, located in /credwork folder
  - Language: TypeScript
  - Navigation: React Navigation v6
  - State: React Context (AuthContext)
  - HTTP: Axios with interceptors
  - Storage: expo-secure-store for JWT tokens
  
- Backend: FastAPI (Python), located in /Credwork Backend folder
  - Database: Supabase (PostgreSQL)
  - PDF parsing: pdfplumber + pikepdf
  - Certificate generation: ReportLab
  - ML layer: scikit-learn (IsolationForest for income anomaly detection)
  - Deployment target: Vercel (serverless)

ML CONTEXT — THIS IS IMPORTANT:
Credwork uses ML for income anomaly detection. The IsolationForest model
from scikit-learn is used to detect statistically anomalous income patterns
in a worker's monthly data. This replaces the hardcoded 15% divergence 
threshold in conflict_resolver.py with a real trained model.
This is the primary ML component of the project and must be preserved and
referenced correctly across all backend changes. Never remove or bypass
the anomaly detection step in the upload pipeline.

COLOUR SYSTEM (never deviate from these):
  #111827  Charcoal Black   → text, headings, borders
  #2563EB  Electric Blue    → all primary buttons, CTAs, active states
  #06B6D4  Cyan             → GigScore ring, verified badges, accents
  #F4F6FA  Off-White        → all backgrounds, card fills
  #E5E7EB                  → disabled states, dividers only
  #F59E0B  Amber            → advance payment badges only
  #EF4444  Red              → delete account + fraud/error states only

CORE RULE: Do not modify any file unless the phase explicitly instructs it.
Do not refactor working code. Only add or fix what the phase specifies.
Always show the complete modified file content, not just the diff.
```

---

---

# PHASE 1 — Environment & API Foundation
### Goal: Connect frontend to backend. Nothing works end-to-end until this is done.
### Files touched: src/api/config.ts, src/api/client.ts (new), src/store/AuthContext.tsx (new)

---

```
PHASE 1 — ENVIRONMENT & API FOUNDATION

We are establishing the foundational API layer that all subsequent phases depend on.
Complete every task in this phase before anything else.

---

TASK 1.1 — UPDATE API CONFIG (src/api/config.ts)

Replace the current hardcoded IP with a dynamic environment-aware URL:

  export const API_BASE_URL = __DEV__
    ? 'http://YOUR_LOCAL_IP:8000'
    : 'https://credwork-backend.vercel.app';

  // Instructions for the developer:
  // Replace YOUR_LOCAL_IP with your machine's actual local network IP
  // Find it by running: ipconfig (Windows) or ifconfig (Mac/Linux)
  // Example: http://192.168.1.105:8000
  // The backend runs on port 8000 (FastAPI default)
  // IMPORTANT: Use your machine's LAN IP, never 'localhost' — 
  // localhost on a phone means the phone itself, not your computer

---

TASK 1.2 — CREATE AXIOS CLIENT (src/api/client.ts) — NEW FILE

Create this file from scratch. It is the single HTTP client for the entire app.

  import axios from 'axios';
  import * as SecureStore from 'expo-secure-store';
  import { API_BASE_URL } from './config';

  export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 15000,
    headers: { 'Content-Type': 'application/json' },
  });

  // REQUEST INTERCEPTOR
  // Automatically attaches the JWT token to every outgoing request
  apiClient.interceptors.request.use(
    async (config) => {
      const token = await SecureStore.getItemAsync('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // RESPONSE INTERCEPTOR
  // Handles 401 Unauthorized globally — logs user out silently
  // The navigationRef allows navigation from outside React components
  import { navigationRef } from '../navigation/RootNavigator';

  apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status === 401) {
        // Clear all stored credentials
        await SecureStore.deleteItemAsync('access_token');
        await SecureStore.deleteItemAsync('user_role');
        await SecureStore.deleteItemAsync('has_completed_onboarding');
        // Navigate to login screen
        if (navigationRef.isReady()) {
          navigationRef.reset({
            index: 0,
            routes: [{ name: 'OTPLogin' }],
          });
        }
      }
      return Promise.reject(error);
    }
  );

---

TASK 1.3 — CREATE AUTH CONTEXT (src/store/AuthContext.tsx) — NEW FILE

This provides the user object globally to all screens without prop drilling.

  import React, { createContext, useContext, useState, useEffect } from 'react';
  import * as SecureStore from 'expo-secure-store';

  interface User {
    id: string;
    phone: string;
    role: 'gig_worker' | 'domestic_worker' | 'household';
    full_name: string | null;
    city: string | null;
    photo_url: string | null;
    is_verified: boolean;
  }

  interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (token: string, user: User) => Promise<void>;
    logout: () => Promise<void>;
    updateProfile: (data: Partial<User>) => void;
  }

  const AuthContext = createContext<AuthContextType | null>(null);

  export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // On app start, check if a valid token exists
    useEffect(() => {
      const bootstrapAuth = async () => {
        try {
          const token = await SecureStore.getItemAsync('access_token');
          const storedUser = await SecureStore.getItemAsync('user_data');
          if (token && storedUser) {
            setUser(JSON.parse(storedUser));
          }
        } catch (e) {
          console.error('Auth bootstrap failed:', e);
        } finally {
          setIsLoading(false);
        }
      };
      bootstrapAuth();
    }, []);

    const login = async (token: string, userData: User) => {
      await SecureStore.setItemAsync('access_token', token);
      await SecureStore.setItemAsync('user_role', userData.role);
      await SecureStore.setItemAsync('has_completed_onboarding', 'true');
      await SecureStore.setItemAsync('user_data', JSON.stringify(userData));
      setUser(userData);
    };

    const logout = async () => {
      await SecureStore.deleteItemAsync('access_token');
      await SecureStore.deleteItemAsync('user_role');
      await SecureStore.deleteItemAsync('has_completed_onboarding');
      await SecureStore.deleteItemAsync('user_data');
      setUser(null);
    };

    const updateProfile = (data: Partial<User>) => {
      if (user) {
        const updated = { ...user, ...data };
        setUser(updated);
        SecureStore.setItemAsync('user_data', JSON.stringify(updated));
      }
    };

    return (
      <AuthContext.Provider value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        updateProfile,
      }}>
        {children}
      </AuthContext.Provider>
    );
  };

  export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within AuthProvider');
    return context;
  };

---

TASK 1.4 — ADD NAVIGATION REF (src/navigation/RootNavigator.tsx)

The axios response interceptor needs to navigate from outside React.
Add a navigationRef export to the root navigator:

  import { createNavigationContainerRef } from '@react-navigation/native';
  export const navigationRef = createNavigationContainerRef();

  // Then in the NavigationContainer:
  <NavigationContainer ref={navigationRef}>

---

TASK 1.5 — WRAP APP IN AUTH PROVIDER (App.tsx)

Wrap the entire app in AuthProvider so every screen can access auth state:

  import { AuthProvider } from './src/store/AuthContext';

  export default function App() {
    return (
      <AuthProvider>
        <NavigationContainer ref={navigationRef}>
          {/* existing navigation */}
        </NavigationContainer>
      </AuthProvider>
    );
  }

---

TASK 1.6 — UPDATE SPLASH SCREEN ROUTING (src/screens/auth/SplashScreen.tsx)

The splash screen must check auth state to decide where to navigate.
Replace the current hardcoded navigation with this logic:

  import { useAuth } from '../../store/AuthContext';

  const { isAuthenticated, user, isLoading } = useAuth();

  useEffect(() => {
    if (isLoading) return; // Wait for auth bootstrap to complete
    
    const timer = setTimeout(() => {
      if (isAuthenticated && user) {
        // User is logged in — go directly to their dashboard
        // Use navigation.reset so they cannot back-swipe to splash
        navigation.reset({
          index: 0,
          routes: [{ name: getRoleNavigator(user.role) }],
        });
      } else {
        // New user — start onboarding
        navigation.replace('LanguageSelect');
      }
    }, 2000);
    
    return () => clearTimeout(timer);
  }, [isLoading, isAuthenticated]);

  const getRoleNavigator = (role: string) => {
    switch (role) {
      case 'gig_worker': return 'GigWorkerTabs';
      case 'domestic_worker': return 'DomesticWorkerTabs';
      case 'household': return 'HouseholdTabs';
      default: return 'LanguageSelect';
    }
  };

---

VERIFICATION FOR PHASE 1:
After completing all tasks, confirm:
- The app builds without TypeScript errors
- AuthContext is accessible in any screen via useAuth()
- The Splash screen correctly routes to LanguageSelect for new users
- The axios client file exists and exports apiClient
- navigationRef is attached to NavigationContainer
```

---

---

# PHASE 2 — Authentication Flow Integration
### Goal: Wire OTP login screens to the real backend /auth endpoints
### Files touched: OTPLoginScreen.tsx, ProfileSetupScreen.tsx, RoleSelectScreen.tsx

---

```
PHASE 2 — AUTHENTICATION FLOW INTEGRATION

Connect the auth screens to the FastAPI backend. Use the apiClient from Phase 1.
The backend auth endpoints are:
  POST /auth/send-otp    → body: { phone: "9876543210" }
  POST /auth/verify-otp  → body: { phone: "9876543210", otp: "123456" }
  POST /auth/setup-profile → body: { full_name, city, role, photo_url }
  GET  /auth/me          → returns current user (requires Bearer token)

---

TASK 2.1 — PHONE ENTRY: Wire "Send OTP" to backend (OTPLoginScreen.tsx)

Replace the current simulation with a real API call.
The phone entry state handles:

  const [phone, setPhone] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSendOTP = async () => {
    if (phone.length !== 10) return;
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post('/auth/send-otp', { phone });
      // On success, switch to OTP entry state
      setCurrentState('otp_entry');
      startResendTimer(); // Start the 30-second countdown
    } catch (err: any) {
      if (err.response?.status === 429) {
        setError('Too many attempts. Please wait before requesting another code.');
      } else {
        setError('Could not send OTP. Check your network and try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // While loading, show a spinner inside the "Send OTP" button
  // Replace button text with <ActivityIndicator color="white" size="small" />
  // Disable the button while isLoading is true

  // Show error below the phone input field:
  // {error && <Text style={{ color: '#EF4444', fontSize: 12, marginTop: 4 }}>{error}</Text>}

---

TASK 2.2 — RESEND TIMER (OTPLoginScreen.tsx)

Implement the 30-second countdown before "Resend OTP" becomes available:

  const [resendTimer, setResendTimer] = useState(30);
  const [canResend, setCanResend] = useState(false);

  const startResendTimer = () => {
    setResendTimer(30);
    setCanResend(false);
    const interval = setInterval(() => {
      setResendTimer(prev => {
        if (prev <= 1) {
          clearInterval(interval);
          setCanResend(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  // Display below OTP boxes:
  // If canResend is false: <Text>Resend in 00:{resendTimer.toString().padStart(2,'0')}</Text>
  // If canResend is true: <TouchableOpacity onPress={handleResend}><Text style={{color:'#2563EB'}}>Resend OTP</Text></TouchableOpacity>

---

TASK 2.3 — OTP VERIFICATION: Wire "Verify" to backend (OTPLoginScreen.tsx)

  const handleVerifyOTP = async () => {
    const otpString = otpValues.join(''); // Join the 6 individual box values
    if (otpString.length !== 6) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.post('/auth/verify-otp', {
        phone,
        otp: otpString,
      });
      
      const { status, access_token, temp_token, user } = response.data;
      
      if (status === 'existing_user') {
        // User already has a profile — log them in and go to dashboard
        await auth.login(access_token, user);
        navigation.reset({
          index: 0,
          routes: [{ name: getRoleNavigator(user.role) }],
        });
      } else if (status === 'new_user') {
        // New user — save temp token and go to role selection
        await SecureStore.setItemAsync('temp_token', temp_token);
        navigation.navigate('RoleSelect');
      }
    } catch (err: any) {
      if (err.response?.status === 400) {
        const detail = err.response.data?.detail || '';
        if (detail.includes('expired')) {
          setError('Code expired. Request a new one.');
          setCanResend(true); // Immediately allow resend
        } else {
          setError('Incorrect code. Please try again.');
          // Clear all OTP boxes on wrong code
          setOtpValues(['', '', '', '', '', '']);
          otpRefs[0].current?.focus();
        }
      } else {
        setError('Verification failed. Check your network and try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

---

TASK 2.4 — ROLE SELECT: Pass role to profile setup (RoleSelectScreen.tsx)

When a user taps a role card, store the selection and navigate to Profile Setup:

  const handleRoleSelect = (role: 'gig_worker' | 'domestic_worker' | 'household') => {
    // Navigate to profile setup, passing the selected role
    navigation.navigate('ProfileSetup', { selectedRole: role });
  };

---

TASK 2.5 — PROFILE SETUP: Wire "Continue" to backend (ProfileSetupScreen.tsx)

  const { selectedRole } = route.params; // Received from RoleSelectScreen

  const handleContinue = async () => {
    if (!fullName.trim() || !city.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Use temp_token for this request (not the full access_token yet)
      const tempToken = await SecureStore.getItemAsync('temp_token');
      
      const response = await apiClient.post(
        '/auth/setup-profile',
        {
          full_name: fullName.trim(),
          city: city.trim(),
          role: selectedRole,
          photo_url: photoUrl || null,
        },
        {
          headers: { Authorization: `Bearer ${tempToken}` }
        }
      );
      
      const { access_token, user } = response.data;
      
      // Clean up temp token
      await SecureStore.deleteItemAsync('temp_token');
      
      // Log in with the full access token
      await auth.login(access_token, user);
      
      // Navigate to role-appropriate dashboard
      navigation.reset({
        index: 0,
        routes: [{ name: getRoleNavigator(selectedRole) }],
      });
    } catch (err: any) {
      setError('Could not save your profile. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

---

VERIFICATION FOR PHASE 2:
- Send OTP button calls real backend and shows loading spinner
- Wrong OTP shows red inline error message, clears boxes
- Expired OTP shows specific "Code expired" message
- Existing user goes directly to their dashboard
- New user completes role select → profile setup → dashboard
- No user can navigate back to the splash or onboarding after login
```

---

---

# PHASE 3 — Gig Worker Dashboard & Upload Integration
### Goal: Replace demo data with real API data on G-01 and wire the upload pipeline
### Files touched: DashboardScreen.tsx (gig), UploadScreen.tsx, ProcessingScreen.tsx

---

```
PHASE 3 — GIG WORKER DASHBOARD & UPLOAD INTEGRATION

Create the API service files and wire the gig worker dashboard and upload flow
to real backend data.

---

TASK 3.1 — CREATE WORKER API SERVICE (src/api/worker.ts) — NEW FILE

  import { apiClient } from './client';

  // Get dashboard data — GigScore, certificate status, income bars
  export const getWorkerDashboard = async () => {
    const response = await apiClient.get('/worker/dashboard');
    return response.data;
  };

  // Get all income entries
  export const getIncomeHistory = async () => {
    const response = await apiClient.get('/worker/income');
    return response.data;
  };

  // Get all certificates (versioned list)
  export const getCertificates = async () => {
    const response = await apiClient.get('/certificates');
    return response.data;
  };

  // Get specific certificate
  export const getCertificateById = async (certId: string) => {
    const response = await apiClient.get(`/certificates/${certId}`);
    return response.data;
  };

---

TASK 3.2 — CREATE UPLOAD API SERVICE (src/api/upload.ts) — NEW FILE

  import { apiClient } from './client';

  // Upload a bank statement PDF
  // Uses FormData for multipart file upload
  export const uploadStatement = async (fileUri: string, fileName: string) => {
    const formData = new FormData();
    formData.append('file', {
      uri: fileUri,
      name: fileName,
      type: 'application/pdf',
    } as any);

    const response = await apiClient.post('/upload/statement', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 30000, // 30 second timeout for file uploads
    });
    return response.data; // Returns { upload_id, status: 'processing' }
  };

  // Poll upload processing status
  export const getUploadStatus = async (uploadId: string) => {
    const response = await apiClient.get(`/upload/status/${uploadId}`);
    return response.data;
    // Returns { upload_id, status, fraud_check, months_found, platforms_found, gigscore, certificate_id }
  };

---

TASK 3.3 — WIRE DASHBOARD TO REAL DATA (src/screens/gig/DashboardScreen.tsx)

Replace the hardcoded DEMO_GIG_WORKER data with a real API call.
Keep the demo data as a fallback if the API fails.

  import { getWorkerDashboard } from '../../api/worker';
  import { DEMO_GIG_WORKER } from '../../utils/demoData';

  const [dashboardData, setDashboardData] = useState(DEMO_GIG_WORKER); // fallback
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const data = await getWorkerDashboard();
        setDashboardData(data);
      } catch (err) {
        console.warn('Dashboard API failed, using demo data:', err);
        setError(true);
        // Keep demo data as fallback — screen still shows
      } finally {
        setIsLoading(false);
      }
    };
    loadDashboard();
  }, []);

  // Show skeleton/loading state while fetching:
  if (isLoading) {
    return (
      <SafeAreaView style={{ flex: 1, backgroundColor: '#F4F6FA', 
                             justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#2563EB" />
      </SafeAreaView>
    );
  }

  // EMPTY STATE — no data yet (new user, no uploads):
  // If dashboardData.gigscore === 0 AND dashboardData.certificateStatus === 'none':
  // Show a greyed-out GigScore ring with "Upload a statement to get started"
  // and a large "Upload Statement" primary button
  // Do NOT show the number 0 in the ring — show an icon instead

---

TASK 3.4 — WIRE UPLOAD SCREEN TO BACKEND (src/screens/gig/UploadScreen.tsx)

Replace the current placeholder with real document picker + upload flow.

  import * as DocumentPicker from 'expo-document-picker';
  import { uploadStatement } from '../../api/upload';

  const handleSelectFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'application/pdf',
        copyToCacheDirectory: true,
      });
      
      if (!result.canceled && result.assets[0]) {
        const file = result.assets[0];
        // Check file size (max 10MB = 10 * 1024 * 1024 bytes)
        if (file.size && file.size > 10 * 1024 * 1024) {
          setError('File too large. Maximum size is 10MB.');
          return;
        }
        setSelectedFile(file);
        setError(null);
      }
    } catch (err) {
      setError('Could not open file picker. Please try again.');
    }
  };

  const handleStartScan = async () => {
    if (!selectedFile) return;
    setIsUploading(true);
    
    try {
      const result = await uploadStatement(selectedFile.uri, selectedFile.name);
      // result.upload_id is used to poll status on the next screen
      navigation.navigate('Processing', { uploadId: result.upload_id });
    } catch (err: any) {
      if (err.response?.status === 422) {
        setError('This file could not be processed. Ensure it is a valid bank statement PDF.');
      } else {
        setError('Upload failed. Check your connection and try again.');
      }
    } finally {
      setIsUploading(false);
    }
  };

---

TASK 3.5 — WIRE PROCESSING SCREEN TO POLLING (src/screens/gig/ProcessingScreen.tsx)

The processing screen receives the upload_id and polls until complete.

  import { getUploadStatus } from '../../api/upload';

  const { uploadId } = route.params;
  const [currentStep, setCurrentStep] = useState(0);
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Map backend status to checklist step index
  const getStepFromStatus = (status: string, fraudCheck: string | null) => {
    if (fraudCheck === 'failed') return -1; // fraud failure
    if (status === 'processing') return 2;  // still running
    if (status === 'passed') return 6;      // all done
    if (status === 'failed') return -1;     // error
    return 1;
  };

  useEffect(() => {
    // Start polling every 2 seconds
    pollingRef.current = setInterval(async () => {
      try {
        const result = await getUploadStatus(uploadId);
        const step = getStepFromStatus(result.status, result.fraud_check);
        
        if (step === -1) {
          // Failed — navigate to error screen
          clearInterval(pollingRef.current!);
          navigation.replace('UploadFailed', {
            reason: result.fraud_reason || 'Could not process this document.',
          });
          return;
        }
        
        setCurrentStep(step);
        
        // Animate through steps as they complete
        // Each step lights up progressively every 1.5 seconds
        
        if (result.status === 'passed') {
          clearInterval(pollingRef.current!);
          // Wait for the last step animation to finish (800ms)
          setTimeout(() => {
            navigation.replace('Success', {
              gigscore: result.gigscore,
              certificateId: result.certificate_id,
              monthsFound: result.months_found,
              platformsFound: result.platforms_found,
            });
          }, 800);
        }
      } catch (err) {
        console.warn('Polling error:', err);
        // Keep polling on network errors — don't stop for transient failures
      }
    }, 2000);

    // Max timeout of 90 seconds before showing a "taking too long" message
    const timeout = setTimeout(() => {
      clearInterval(pollingRef.current!);
      navigation.replace('UploadFailed', {
        reason: 'Processing is taking longer than expected. Please try again.',
      });
    }, 90000);

    return () => {
      clearInterval(pollingRef.current!);
      clearTimeout(timeout);
    };
  }, [uploadId]);

  // Prevent Android back button during processing
  useEffect(() => {
    const backHandler = BackHandler.addEventListener('hardwareBackPress', () => true);
    return () => backHandler.remove();
  }, []);

---

VERIFICATION FOR PHASE 3:
- Dashboard loads real data from backend (falls back to demo data gracefully)
- Empty state shows correctly for new users with no uploads
- Document picker opens and selects PDF files correctly
- File size validation rejects files > 10MB
- Processing screen polls every 2 seconds and animates through steps
- Successful processing navigates to Success screen with real data
- Failed processing navigates to UploadFailed screen with plain-language reason
- Back button is disabled during processing
```

---

---

# PHASE 4 — Certificate Flow Integration
### Goal: Wire certificate preview and share to real backend data
### Files touched: SuccessScreen.tsx, CertificateScreen.tsx, ShareScreen.tsx (gig)

---

```
PHASE 4 — CERTIFICATE FLOW INTEGRATION

---

TASK 4.1 — SUCCESS SCREEN: Use real data from navigation params (SuccessScreen.tsx)

The processing screen already passes real data via route.params.
Replace the hardcoded demo values with the params:

  const { gigscore, certificateId, monthsFound, platformsFound } = route.params;

  // If any param is missing, fall back to demo data
  const displayScore = gigscore ?? DEMO_GIG_WORKER.gigscore;
  const displayCertId = certificateId ?? DEMO_GIG_WORKER.certificateId;

  // NAVIGATION FIX — Flush the stack so user cannot swipe back to Processing
  // The "View Full Certificate" and "Back to Home" buttons must use:
  navigation.reset({
    index: 0,
    routes: [{ name: 'GigWorkerTabs' }],
  });
  // NOT navigation.goBack() or navigation.navigate()
  // The processing screens must be gone from the stack after success

  // "View Full Certificate" button:
  const handleViewCertificate = () => {
    navigation.navigate('Certificate', { certId: displayCertId });
  };

---

TASK 4.2 — CERTIFICATE SCREEN: Load real certificate data (CertificateScreen.tsx)

  import { getCertificateById } from '../../api/worker';

  const { certId } = route.params;
  const [certificate, setCertificate] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadCertificate = async () => {
      try {
        const data = await getCertificateById(certId);
        setCertificate(data);
      } catch (err) {
        // Fall back to demo data if API fails
        setCertificate(buildDemoCertificate());
      } finally {
        setIsLoading(false);
      }
    };
    loadCertificate();
  }, [certId]);

  // The certificate renders the following fields from API response:
  // cert_id, worker_name, worker_city, period_start, period_end,
  // monthly_avg_inr, gigscore, gigscore_label, monthly_breakdown[],
  // platforms_verified[], issued_at, version, verification_url

---

TASK 4.3 — SHARE SHEET: Implement real sharing (ShareScreen.tsx / bottom sheet)

The share sheet must be a bottom sheet that overlays the current screen.
It must NOT navigate to a separate screen. (Architecture fix from UI audit.)

For the share options, implement real device sharing:

  import * as Sharing from 'expo-sharing';
  import * as FileSystem from 'expo-file-system';
  import Clipboard from '@react-native-clipboard/clipboard';

  // OPTION 1 — WhatsApp share (certificate PDF)
  const handleWhatsAppShare = async () => {
    try {
      // Download the certificate PDF to local cache
      const pdfUrl = `${API_BASE_URL}/certificates/${certId}/pdf`;
      const localUri = `${FileSystem.cacheDirectory}certificate_${certId}.pdf`;
      
      await FileSystem.downloadAsync(pdfUrl, localUri, {
        headers: { Authorization: `Bearer ${await SecureStore.getItemAsync('access_token')}` }
      });
      
      // Share via system share sheet (user can choose WhatsApp from it)
      await Sharing.shareAsync(localUri, {
        mimeType: 'application/pdf',
        dialogTitle: 'Share your income certificate',
      });
    } catch (err) {
      Alert.alert('Could not prepare the certificate for sharing.');
    }
  };

  // OPTION 2 — Save to phone
  const handleSaveToPhone = async () => {
    // Same download logic as above but save to document directory
    const pdfUrl = `${API_BASE_URL}/certificates/${certId}/pdf`;
    const localUri = `${FileSystem.documentDirectory}credwork_certificate_${certId}.pdf`;
    await FileSystem.downloadAsync(pdfUrl, localUri);
    Alert.alert('Saved', 'Certificate saved to your device.');
  };

  // OPTION 3 — Email
  const handleEmail = async () => {
    // Same as WhatsApp — use expo-sharing, user selects email app
    await handleWhatsAppShare(); // Reuse the same share sheet logic
  };

  // OPTION 4 — Copy verification link
  const handleCopyLink = async () => {
    const verifyUrl = `https://credwork.in/verify/${certId}`;
    Clipboard.setString(verifyUrl);
    // Show toast: "Link copied!"
    setShowCopiedToast(true);
    setTimeout(() => setShowCopiedToast(false), 2000);
  };

---

VERIFICATION FOR PHASE 4:
- Success screen shows real GigScore and certificate ID from the upload result
- Back button from Success correctly resets to dashboard (no way back to Processing)
- Certificate screen loads real monthly breakdown from backend
- Certificate PDF downloads and shares correctly
- Share sheet opens as bottom sheet overlay — does not navigate away
- Verification link copies to clipboard with toast confirmation
```

---

---

# PHASE 5 — Household & Domestic Worker Integration
### Goal: Wire ServiConnect payment flow and domestic worker dashboard to backend
### Files touched: household/DashboardScreen.tsx, PaymentScreen.tsx, domestic/DashboardScreen.tsx

---

```
PHASE 5 — HOUSEHOLD & DOMESTIC WORKER INTEGRATION

---

TASK 5.1 — CREATE HOUSEHOLD API SERVICE (src/api/household.ts) — NEW FILE

  import { apiClient } from './client';

  export const getHouseholdDashboard = async () => {
    const response = await apiClient.get('/household/dashboard');
    return response.data;
  };

  export const addWorker = async (data: {
    worker_phone: string;
    worker_role: string;
    monthly_salary: number;
    payment_day: number;
  }) => {
    const response = await apiClient.post('/household/add-worker', data);
    return response.data;
    // Returns { status: 'linked' | 'invited', worker, household_worker_id }
  };

  export const makePayment = async (data: {
    worker_id: string;
    amount_inr: number;
    payment_type: 'salary' | 'bonus' | 'advance';
    payment_month: string; // YYYY-MM format
  }) => {
    const response = await apiClient.post('/household/payment', data);
    return response.data; // Returns { payment_id, status: 'pending' }
  };

  export const pollPaymentStatus = async (paymentId: string) => {
    const response = await apiClient.get(`/household/payment-status/${paymentId}`);
    return response.data;
  };

  export const getPaymentHistory = async (workerId?: string) => {
    const url = workerId
      ? `/household/payments/${workerId}`
      : '/household/payments';
    const response = await apiClient.get(url);
    return response.data;
  };

---

TASK 5.2 — WIRE HOUSEHOLD DASHBOARD (src/screens/household/DashboardScreen.tsx)

  import { getHouseholdDashboard } from '../../api/household';

  const [dashboardData, setDashboardData] = useState(DEMO_HOUSEHOLD);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getHouseholdDashboard();
        setDashboardData(data);
      } catch (err) {
        console.warn('Household dashboard failed, using demo data');
      } finally {
        setIsLoading(false);
      }
    };
    load();
  }, []);

  // When "Pay Now" is tapped, navigate to payment screen with worker data:
  const handlePayNow = (worker: Worker) => {
    navigation.navigate('MakePayment', {
      workerId: worker.id,
      workerName: worker.name,
      workerRole: worker.role,
      monthlySalary: worker.salary,
    });
  };

---

TASK 5.3 — WIRE PAYMENT SCREEN WITH POLLING (src/screens/household/PaymentScreen.tsx)

  import { makePayment, pollPaymentStatus } from '../../api/household';

  const { workerId, workerName, workerRole, monthlySalary } = route.params;
  const [paymentType, setPaymentType] = useState<'salary'|'bonus'|'advance'>('salary');
  const [amount, setAmount] = useState(monthlySalary.toString());
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentSuccess, setPaymentSuccess] = useState(false);

  const handlePay = async () => {
    setIsProcessing(true);
    try {
      // Step 1: Create the payment
      const { payment_id } = await makePayment({
        worker_id: workerId,
        amount_inr: parseInt(amount),
        payment_type: paymentType,
        payment_month: getCurrentMonth(), // Returns current YYYY-MM
      });

      // Step 2: Poll for Razorpay confirmation (simulated 3-second delay)
      const pollInterval = setInterval(async () => {
        const status = await pollPaymentStatus(payment_id);
        if (status.status === 'processed') {
          clearInterval(pollInterval);
          setPaymentSuccess(true);
          setIsProcessing(false);
          // Auto-navigate back to household dashboard after 2 seconds
          setTimeout(() => {
            navigation.reset({
              index: 0,
              routes: [{ name: 'HouseholdTabs' }],
            });
          }, 2000);
        } else if (status.status === 'failed') {
          clearInterval(pollInterval);
          setIsProcessing(false);
          Alert.alert('Payment Failed', 'The payment could not be processed. Please try again.');
        }
      }, 1000); // Poll every second

      // Max 10-second timeout
      setTimeout(() => {
        clearInterval(pollInterval);
        if (!paymentSuccess) {
          setIsProcessing(false);
          Alert.alert('Timeout', 'Payment is taking too long. Check your payment history.');
        }
      }, 10000);

    } catch (err) {
      setIsProcessing(false);
      Alert.alert('Error', 'Could not initiate payment. Try again.');
    }
  };

  const getCurrentMonth = () => {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  };

  // SUCCESS MICRO-STATE — shown when paymentSuccess is true:
  // A cyan checkmark animation, "Payment sent!", worker name, amount, month chips
  // Then auto-navigates back after 2 seconds

---

TASK 5.4 — WIRE DOMESTIC WORKER DASHBOARD (src/screens/domestic/DashboardScreen.tsx)

  import { getWorkerDashboard } from '../../api/worker';

  // Same pattern as gig worker dashboard — real data with demo fallback
  // The API response shape is the same but:
  // - gigscore is based on household payments, not PDF uploads
  // - certificateStatus reflects ServiConnect-sourced certificate
  // - currentHousehold shows the linked household name and city
  // - marchPaid boolean controls the "March paid ✓" vs "March pending" pill

  // The pill styling:
  // marchPaid === true:
  //   backgroundColor: 'rgba(6, 182, 212, 0.15)', color: '#06B6D4', text: 'March paid ✓'
  // marchPaid === false:
  //   backgroundColor: 'rgba(245, 158, 11, 0.15)', color: '#F59E0B', text: 'March pending'

---

VERIFICATION FOR PHASE 5:
- Household dashboard loads real worker cards from backend
- Pay Now navigates to payment screen with correct worker data
- Payment screen shows Salary pre-filled with monthly salary amount
- Payment processing shows loading state during the simulated 3-second webhook delay
- Payment success micro-state shows correctly then auto-navigates to dashboard
- Domestic worker dashboard shows payment-sourced GigScore
- March paid/pending pill shows correct state and colour
```

---

---

# PHASE 6 — Error States & Edge Cases
### Goal: Build the missing error screens and handle all API error responses
### Files touched: New UploadFailedScreen.tsx, all screens with error handling

---

```
PHASE 6 — ERROR STATES & EDGE CASES

---

TASK 6.1 — CREATE UPLOAD FAILED SCREEN (src/screens/gig/UploadFailedScreen.tsx) — NEW FILE

This screen is shown when fraud is detected or processing fails.
It receives a plain-language reason from the backend.

  import { SafeAreaView, View, Text, TouchableOpacity, StyleSheet } from 'react-native';
  import { Ionicons } from '@expo/vector-icons';

  const UploadFailedScreen = ({ route, navigation }) => {
    const { reason } = route.params;
    
    // Determine if this is a fraud failure or a system error
    // based on keywords in the reason string
    const isFraudFailure = reason.toLowerCase().includes('edited') ||
                           reason.toLowerCase().includes('modified') ||
                           reason.toLowerCase().includes('tamper');
    
    return (
      <SafeAreaView style={{ flex: 1, backgroundColor: '#F4F6FA' }}>
        <View style={{ flex: 1, padding: 24, alignItems: 'center', justifyContent: 'center' }}>
          
          {/* Icon — amber warning for system errors, red for fraud */}
          <View style={{
            width: 72, height: 72, borderRadius: 36,
            backgroundColor: isFraudFailure ? 'rgba(239,68,68,0.1)' : 'rgba(245,158,11,0.1)',
            alignItems: 'center', justifyContent: 'center', marginBottom: 24
          }}>
            <Ionicons
              name={isFraudFailure ? 'shield-checkmark-outline' : 'warning-outline'}
              size={36}
              color={isFraudFailure ? '#EF4444' : '#F59E0B'}
            />
          </View>
          
          {/* Heading — non-accusatory language */}
          <Text style={{ fontSize: 22, fontWeight: 'bold', color: '#111827', 
                         textAlign: 'center', marginBottom: 12 }}>
            {isFraudFailure ? "We couldn't verify this statement" : "Something went wrong"}
          </Text>
          
          {/* Plain-language reason from backend */}
          <Text style={{ fontSize: 15, color: 'rgba(17,24,39,0.7)', 
                         textAlign: 'center', lineHeight: 22, marginBottom: 32 }}>
            {reason}
          </Text>
          
          {/* What to do next section */}
          <View style={{ width: '100%', backgroundColor: '#F4F6FA', 
                         borderWidth: 1.5, borderColor: '#E5E7EB',
                         borderRadius: 12, padding: 16, marginBottom: 32 }}>
            <Text style={{ fontSize: 13, fontWeight: 'bold', color: '#111827', marginBottom: 8 }}>
              What to do next
            </Text>
            {isFraudFailure ? (
              <>
                <Text style={{ fontSize: 13, color: 'rgba(17,24,39,0.7)', marginBottom: 4 }}>1. Open your bank's official mobile app</Text>
                <Text style={{ fontSize: 13, color: 'rgba(17,24,39,0.7)', marginBottom: 4 }}>2. Download a fresh statement as PDF</Text>
                <Text style={{ fontSize: 13, color: 'rgba(17,24,39,0.7)' }}>3. Upload the new statement to Credwork</Text>
              </>
            ) : (
              <>
                <Text style={{ fontSize: 13, color: 'rgba(17,24,39,0.7)', marginBottom: 4 }}>1. Check your internet connection</Text>
                <Text style={{ fontSize: 13, color: 'rgba(17,24,39,0.7)' }}>2. Try uploading again in a few minutes</Text>
              </>
            )}
          </View>
          
          {/* Try Again button */}
          <TouchableOpacity
            style={{ width: '100%', backgroundColor: '#2563EB', 
                     borderRadius: 12, padding: 16, alignItems: 'center' }}
            onPress={() => navigation.replace('Upload')}
          >
            <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 16 }}>Try Again</Text>
          </TouchableOpacity>
          
        </View>
      </SafeAreaView>
    );
  };

  export default UploadFailedScreen;

  // Add this screen to the navigation stack in GigWorkerStack

---

TASK 6.2 — EMPTY STATE FOR DASHBOARD (src/screens/gig/DashboardScreen.tsx)

When gigscore is 0 AND no certificate exists (new user), show this instead of 
the normal GigScore card:

  // Inside the GigScore card, conditional render:
  {hasNoData ? (
    <View style={{ alignItems: 'center', padding: 24 }}>
      {/* Greyed-out ring outline */}
      <View style={{ width: 120, height: 120, borderRadius: 60,
                     borderWidth: 8, borderColor: '#E5E7EB',
                     alignItems: 'center', justifyContent: 'center' }}>
        <Ionicons name="bar-chart-outline" size={40} color="#E5E7EB" />
      </View>
      <Text style={{ fontSize: 16, fontWeight: 'bold', color: '#111827', marginTop: 16 }}>
        No data yet
      </Text>
      <Text style={{ fontSize: 13, color: 'rgba(17,24,39,0.6)', textAlign: 'center', marginTop: 4 }}>
        Upload your bank statement to generate your GigScore
      </Text>
      <TouchableOpacity
        style={{ backgroundColor: '#2563EB', borderRadius: 12, 
                 paddingVertical: 12, paddingHorizontal: 24, marginTop: 16 }}
        onPress={() => navigation.navigate('Upload')}
      >
        <Text style={{ color: 'white', fontWeight: 'bold' }}>Upload Statement</Text>
      </TouchableOpacity>
    </View>
  ) : (
    <GigScoreRing score={dashboardData.gigscore} />
    // ... rest of normal dashboard
  )}

  // hasNoData condition:
  const hasNoData = !dashboardData.gigscore || dashboardData.gigscore === 0;

---

TASK 6.3 — HANDLE ALL HTTP ERROR CODES GLOBALLY

Add these error handling patterns to every screen that makes API calls.
These complement the global 401 interceptor in client.ts:

  // HTTP 429 — Rate limited (too many OTP requests)
  // Show: "Too many attempts. Please wait before requesting a new code."

  // HTTP 422 — Fraud detected / no income found
  // Navigate to UploadFailedScreen with err.response.data.detail as reason

  // HTTP 500 — Server error during PDF processing
  // Show toast: "We had a technical issue. Your file was not stored. Please try again."

  // Network error (no response) — Axios throws without err.response
  // Show: "No internet connection. Check your network and try again."

  // Example error handler utility (src/utils/errorHandler.ts):
  export const getErrorMessage = (err: any): string => {
    if (!err.response) return 'No internet connection. Check your network and try again.';
    switch (err.response.status) {
      case 400: return err.response.data?.detail || 'Invalid request.';
      case 401: return 'Session expired. Please log in again.';
      case 422: return err.response.data?.detail || 'Could not process this request.';
      case 429: return 'Too many attempts. Please wait a moment.';
      case 500: return 'Server error. Please try again in a few minutes.';
      default: return 'Something went wrong. Please try again.';
    }
  };

---

VERIFICATION FOR PHASE 6:
- UploadFailedScreen shows with fraud-appropriate language for tampered PDFs
- UploadFailedScreen shows with system-error language for processing failures
- Empty state shows for new users with no uploads (no "0" in the ring)
- All API calls have error handling that shows meaningful user-facing messages
- No API call can crash the app silently
```

---

---

# PHASE 7 — Backend: Supabase Storage & Production Readiness
### Goal: Fix the certificate storage bug + make backend deployable
### Files touched: Backend — cert_generator.py, main.py, settings.py

---

```
PHASE 7 — BACKEND: SUPABASE STORAGE & PRODUCTION READINESS

The backend currently saves certificates to a local directory. This breaks on 
Vercel because Vercel is serverless — local files disappear between requests.
Fix this by uploading to Supabase Storage.

---

TASK 7.1 — UPDATE CERT GENERATOR (app/utils/cert_generator.py)

Replace the local file save with Supabase Storage upload:

  from supabase import create_client
  import os
  import io

  supabase = create_client(
      os.environ['SUPABASE_URL'],
      os.environ['SUPABASE_SERVICE_KEY']
  )

  def save_certificate_to_storage(pdf_bytes: bytes, cert_id: str) -> str:
    """
    Uploads certificate PDF to Supabase Storage.
    Returns the public URL.
    """
    file_path = f"certificates/{cert_id}.pdf"
    
    # Upload to 'certificates' bucket
    response = supabase.storage.from_('certificates').upload(
        path=file_path,
        file=pdf_bytes,
        file_options={"content-type": "application/pdf", "upsert": True}
    )
    
    # Get the public URL
    public_url = supabase.storage.from_('certificates').get_public_url(file_path)
    return public_url

  # Replace all local os.makedirs and open() calls with:
  # pdf_bytes = generate_certificate_pdf(certificate_data)  # returns bytes
  # public_url = save_certificate_to_storage(pdf_bytes, cert_id)
  # Store public_url in the certificates table instead of a local path

---

TASK 7.2 — FIX SETTINGS VALIDATION (app/config/settings.py)

Add env_file and extra="ignore" to prevent crashes on missing variables:

  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      supabase_url: str
      supabase_service_key: str
      jwt_secret: str
      jwt_algorithm: str = "HS256"
      jwt_expiry_days: int = 30
      
      model_config = {
          "env_file": ".env",
          "extra": "ignore"  # Don't crash on unknown env vars
      }

---

TASK 7.3 — TIGHTEN CORS (main.py)

Replace the wildcard CORS with specific allowed origins:

  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=[
          "http://localhost:8081",           # Expo development
          "http://localhost:3000",           # Local web
          "https://credwork-dashboard.vercel.app",  # V0 dashboard
      ],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

---

TASK 7.4 — EXPAND VPA CONFIG (vpa_config.json)

Add these additional VPAs that were missing:

  Add to Swiggy: "swiggypay@hdfcbank", "swiggy.instamart@upi", "swiggyit@upi"
  Add to Zomato: "zomato@paytm", "zomatofood@icici", "zomato@hdfcbank"
  Add to new entry Uber: 
    { "name": "Uber", "vpas": ["uber.india@sbi", "uberpayments@axis", "uber@icici"] }
  Add to Zepto: "zepto@yesbank", "zepto@paytm"

---

VERIFICATION FOR PHASE 7:
- Certificates upload to Supabase Storage and return a public HTTPS URL
- The /certificates/:cert_id/pdf endpoint redirects to the Supabase URL
- Settings load correctly without crashing even if extra env vars exist
- CORS only allows known origins
- VPA config has expanded platform coverage
```

---

---

# PHASE 7B — ML: Income Anomaly Detection
### Goal: Add the IsolationForest ML model to the upload pipeline
### This is the core ML component of Credwork — it must exist before the demo
### Files touched: Backend — new file app/ml/anomaly_detector.py, upload pipeline

---

```
PHASE 7B — ML: INCOME ANOMALY DETECTION

Credwork's ML layer uses scikit-learn's IsolationForest algorithm to detect
statistically anomalous income patterns in a worker's monthly data.

This replaces the hardcoded 15% threshold in conflict_resolver.py with a 
real trained ML model. The model is trained on the worker's own income history
(unsupervised learning — no labelled dataset required) and flags months whose
income values are statistical outliers relative to the worker's pattern.

This is what makes Credwork an AI/ML project. Every upload runs through this
model. The output feeds into both the fraud_flags table and the GigScore 
calculation. Never skip or bypass this step.

---

TASK 7B.1 — INSTALL SCIKIT-LEARN

Add to requirements.txt:
  scikit-learn==1.4.0
  numpy==1.26.4

---

TASK 7B.2 — CREATE ANOMALY DETECTOR MODULE
(app/ml/anomaly_detector.py) — NEW FILE

Create the directory app/ml/ and add an __init__.py file to make it a package.
Then create anomaly_detector.py with the following complete implementation:

  import numpy as np
  from sklearn.ensemble import IsolationForest
  from typing import List, Dict, Any

  def detect_income_anomalies(monthly_amounts: List[float]) -> Dict[str, Any]:
    """
    Uses IsolationForest (unsupervised ML) to detect anomalous months
    in a worker's income history.
    
    IsolationForest works by building random decision trees and measuring
    how quickly each data point can be "isolated". Points that are isolated
    quickly (few splits needed) are anomalies — they are far from the cluster.
    
    Args:
        monthly_amounts: List of monthly income totals in INR.
                         Must be in chronological order.
                         Zero-income months must be included (not excluded).
    
    Returns:
        Dict containing:
          - anomaly_detected: bool — True if any month is anomalous
          - anomalous_indices: List[int] — indices of anomalous months
          - anomaly_scores: List[float] — anomaly score per month (-1 to 0, 
                            lower = more anomalous)
          - model_confidence: float — how reliable this detection is 
                              (based on sample size, 0 to 1)
          - reason: str | None — plain language explanation if anomaly found
    """
    
    # Minimum 3 data points required for meaningful anomaly detection
    if len(monthly_amounts) < 3:
      return {
        "anomaly_detected": False,
        "anomalous_indices": [],
        "anomaly_scores": [],
        "model_confidence": 0.0,
        "reason": None,
        "skipped": True,
        "skip_reason": "Insufficient data — need at least 3 months"
      }
    
    # Reshape for scikit-learn: needs 2D array (n_samples, n_features)
    X = np.array(monthly_amounts).reshape(-1, 1)
    
    # contamination: expected proportion of outliers in the data
    # For income data, we assume at most 20% of months are genuinely anomalous
    # This is a conservative estimate — gig income is inherently variable
    contamination = min(0.2, 1.0 / len(monthly_amounts))
    
    # n_estimators: number of isolation trees — 100 is standard
    # random_state: fixed for reproducibility across identical inputs
    model = IsolationForest(
      n_estimators=100,
      contamination=contamination,
      random_state=42,
      n_jobs=-1  # Use all available CPU cores
    )
    
    # fit_predict returns: 1 for normal, -1 for anomaly
    predictions = model.fit_predict(X)
    
    # score_samples returns anomaly scores: more negative = more anomalous
    # Scores range roughly from -0.5 (very anomalous) to 0 (very normal)
    scores = model.score_samples(X)
    
    anomalous_indices = [i for i, pred in enumerate(predictions) if pred == -1]
    
    # Model confidence scales with sample size
    # 3 months = low confidence, 6 months = full confidence
    model_confidence = min(1.0, len(monthly_amounts) / 6.0)
    
    # Build a human-readable reason if anomalies found
    reason = None
    if anomalous_indices:
      mean_income = np.mean([monthly_amounts[i] for i in range(len(monthly_amounts)) 
                             if i not in anomalous_indices]) if len(anomalous_indices) < len(monthly_amounts) else np.mean(monthly_amounts)
      
      anomalous_values = [monthly_amounts[i] for i in anomalous_indices]
      
      if any(v > mean_income * 2 for v in anomalous_values):
        reason = f"Income spike detected — one or more months show unusually high earnings compared to the worker's typical pattern."
      elif any(v == 0 for v in anomalous_values):
        reason = f"Zero-income months detected — the worker had no recorded gig income in {len(anomalous_indices)} month(s)."
      else:
        reason = f"Unusual income pattern detected in {len(anomalous_indices)} month(s). Manual review recommended."
    
    return {
      "anomaly_detected": len(anomalous_indices) > 0,
      "anomalous_indices": anomalous_indices,
      "anomaly_scores": scores.tolist(),
      "model_confidence": round(model_confidence, 2),
      "reason": reason,
      "skipped": False,
      "skip_reason": None
    }


  def get_anomaly_severity(anomaly_result: Dict[str, Any]) -> str:
    """
    Classifies the severity of detected anomalies.
    Returns: 'none' | 'low' | 'medium' | 'high'
    
    Used to decide whether to hard-block the upload, flag for review,
    or just log silently.
    """
    if not anomaly_result["anomaly_detected"]:
      return "none"
    
    # Low confidence model (< 3 months of data) = low severity regardless
    if anomaly_result["model_confidence"] < 0.5:
      return "low"
    
    # Count how many months are anomalous relative to total
    num_anomalous = len(anomaly_result["anomalous_indices"])
    total_months = len(anomaly_result["anomaly_scores"])
    anomaly_ratio = num_anomalous / total_months
    
    # More than 33% of months are anomalous — high severity
    if anomaly_ratio > 0.33:
      return "high"
    
    # 1-2 anomalous months — medium severity
    if num_anomalous <= 2:
      return "medium"
    
    return "high"

---

TASK 7B.3 — INTEGRATE INTO UPLOAD PIPELINE

The anomaly detector must be called AFTER monthly aggregation and BEFORE
GigScore calculation. Find the upload processing function in the backend
(likely in app/routers/upload.py or app/utils/vpa_parser.py) and add
this integration:

  from app.ml.anomaly_detector import detect_income_anomalies, get_anomaly_severity

  # After monthly_totals is computed from VPA extraction:
  # monthly_totals = { "2025-01": 21000, "2025-02": 18000, ... }

  # Step: Run ML anomaly detection
  monthly_amounts_list = [
    monthly_totals.get(month, 0)
    for month in sorted(monthly_totals.keys())
  ]
  
  anomaly_result = detect_income_anomalies(monthly_amounts_list)
  severity = get_anomaly_severity(anomaly_result)
  
  # Severity-based action:
  if severity == "high":
    # High severity = flag for manual review
    # Do NOT reject — still generate GigScore and certificate
    # But create a fraud_flag record for the admin queue
    await create_fraud_flag(
      worker_id=worker_id,
      upload_id=upload_id,
      flag_type="ml_anomaly_high",
      flag_reason=anomaly_result["reason"] or "ML model detected high-severity income anomaly.",
    )
  
  elif severity == "medium":
    # Medium severity = log silently, no admin action required
    # The anomaly note is stored in the upload record for audit purposes
    await update_upload_record(upload_id, {
      "ml_anomaly_note": anomaly_result["reason"]
    })
  
  # severity == "low" or "none" = no action, proceed normally
  
  # Store the anomaly result in pdf_uploads for the admin dashboard:
  await update_upload_record(upload_id, {
    "ml_anomaly_detected": anomaly_result["anomaly_detected"],
    "ml_anomaly_score": min(anomaly_result["anomaly_scores"]) if anomaly_result["anomaly_scores"] else None,
    "ml_model_confidence": anomaly_result["model_confidence"],
  })

---

TASK 7B.4 — ADD ML COLUMNS TO PDF_UPLOADS TABLE

Add these columns to the pdf_uploads table in Supabase:

  ALTER TABLE pdf_uploads ADD COLUMN ml_anomaly_detected BOOLEAN DEFAULT FALSE;
  ALTER TABLE pdf_uploads ADD COLUMN ml_anomaly_score FLOAT;
  ALTER TABLE pdf_uploads ADD COLUMN ml_model_confidence FLOAT;
  ALTER TABLE pdf_uploads ADD COLUMN ml_anomaly_note TEXT;

These columns allow the admin dashboard to show ML results per upload.

---

TASK 7B.5 — EXPOSE ML RESULT IN UPLOAD STATUS ENDPOINT

The GET /upload/status/:id endpoint must include ML results so the
frontend can surface them if needed:

  # Add to the upload status response:
  {
    "upload_id": "...",
    "status": "passed",
    "fraud_check": "passed",
    "months_found": 6,
    "platforms_found": ["Swiggy", "Zomato"],
    "gigscore": 78,
    "certificate_id": "CW-2025-00847",
    "ml_anomaly_detected": false,      ← NEW
    "ml_anomaly_note": null,           ← NEW
    "ml_model_confidence": 0.83        ← NEW
  }

---

TASK 7B.6 — ADD ML RESULTS TO ADMIN DASHBOARD

Update the GET /admin/uploads endpoint to include ML columns in the
recent uploads table response. The admin dashboard already shows
fraud_check status — add an "ML" column alongside it:

  # Each upload row in the admin response:
  {
    "timestamp": "14:32",
    "worker_id": "GW-0892",
    "status": "passed",
    "fraud_check": "passed",
    "ml_anomaly": "none",     ← NEW: "none" | "low" | "medium" | "high"
    "gigscore": 81
  }

---

TASK 7B.7 — DEMO TEST FOR ML MODEL

Before the hackathon demo, verify the ML model works by testing with
these synthetic income arrays directly in Python:

  from app.ml.anomaly_detector import detect_income_anomalies, get_anomaly_severity

  # Test 1: Consistent income — should return no anomaly
  consistent = [18000, 19500, 17800, 20000, 18500, 19100]
  result1 = detect_income_anomalies(consistent)
  assert result1["anomaly_detected"] == False, "Consistent income should not be flagged"

  # Test 2: One massive spike — should detect anomaly
  spike = [18000, 19000, 17500, 18800, 75000, 19200]  # Month 5 is a spike
  result2 = detect_income_anomalies(spike)
  assert result2["anomaly_detected"] == True, "Income spike should be flagged"
  assert 4 in result2["anomalous_indices"], "Month index 4 (the spike) should be anomalous"

  # Test 3: Zero-income months — should detect anomaly
  with_zeros = [18000, 0, 19000, 18500, 0, 17800]
  result3 = detect_income_anomalies(with_zeros)
  assert result3["anomaly_detected"] == True, "Zero-income months should be flagged"

  # Test 4: Insufficient data — should skip gracefully
  too_short = [18000, 19000]
  result4 = detect_income_anomalies(too_short)
  assert result4["skipped"] == True, "Less than 3 months should skip detection"

  print("All ML model tests passed.")

Run this test before the demo. If any assertion fails, debug the
anomaly_detector.py implementation before proceeding.

---

VERIFICATION FOR PHASE 7B:
- app/ml/__init__.py exists
- app/ml/anomaly_detector.py exists with both functions fully implemented
- scikit-learn and numpy are in requirements.txt
- detect_income_anomalies is called in the upload pipeline after aggregation
- High-severity anomalies create fraud_flag records
- Medium-severity anomalies are logged to the upload record silently
- ML columns exist in pdf_uploads table
- Upload status endpoint includes ml_anomaly_detected, ml_anomaly_note, ml_model_confidence
- Admin dashboard uploads table includes ml_anomaly column
- All 4 demo tests pass without assertion errors
```

---

---

# PHASE 8 — GigScore Ring Animation & UI Polish
### Goal: Make the GigScore ring animate on load + final UI polish pass
### Files touched: GigScoreRing.tsx, DashboardScreen.tsx (gig + domestic)

---

```
PHASE 8 — GIGSCORE RING ANIMATION & FINAL UI POLISH

---

TASK 8.1 — ANIMATE GIGSCORE RING ON LOAD (src/components/GigScoreRing.tsx)

The ring should animate from 0 to the target score over 1500ms when it first renders.
This makes the data feel "premium" and earned.

  import { useEffect, useRef } from 'react';
  import Animated, {
    useSharedValue,
    useAnimatedProps,
    withTiming,
    Easing,
  } from 'react-native-reanimated';
  import Svg, { Circle } from 'react-native-svg';

  const AnimatedCircle = Animated.createAnimatedComponent(Circle);

  export const GigScoreRing: React.FC<GigScoreRingProps> = ({ score, size = 160, strokeWidth = 16 }) => {
    const radius = (size - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    
    // Animated value starts at 0, animates to the target fill
    const progress = useSharedValue(0);
    
    useEffect(() => {
      progress.value = withTiming(score / 100, {
        duration: 1500,
        easing: Easing.out(Easing.cubic), // Ease out — fast start, slow finish
      });
    }, [score]);
    
    const animatedProps = useAnimatedProps(() => ({
      strokeDasharray: [progress.value * circumference, circumference],
    }));
    
    return (
      <View style={{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }}>
        <Svg width={size} height={size} style={{ position: 'absolute' }}>
          {/* Background ring */}
          <Circle cx={size/2} cy={size/2} r={radius}
            stroke="#E5E7EB" strokeWidth={strokeWidth} fill="none" />
          {/* Animated filled ring */}
          <AnimatedCircle cx={size/2} cy={size/2} r={radius}
            stroke="#06B6D4" strokeWidth={strokeWidth} fill="none"
            animatedProps={animatedProps}
            strokeLinecap="round"
            rotation="-90"
            origin={`${size/2}, ${size/2}`}
          />
        </Svg>
        <Text style={{ fontSize: 40, fontWeight: 'bold', color: '#111827' }}>{score}</Text>
        <Text style={{ fontSize: 16, fontWeight: '600', color: '#2563EB' }}>{getLabel(score)}</Text>
      </View>
    );
  };

---

TASK 8.2 — INPUT FOCUS BORDER COLOUR

On every TextInput in the app, the border should change to #2563EB when focused.
Add this pattern to all TextInput components:

  const [isFocused, setIsFocused] = useState(false);
  
  <TextInput
    style={[
      styles.input,
      { borderColor: isFocused ? '#2563EB' : '#111827' }
    ]}
    onFocus={() => setIsFocused(true)}
    onBlur={() => setIsFocused(false)}
  />

---

TASK 8.3 — NAVIGATION STACK RESET ON SUCCESS

Confirm these navigation.reset() calls are in place:
- After successful OTP login (existing user) → reset to role dashboard
- After profile setup → reset to role dashboard  
- After upload success → reset to GigWorkerTabs (removes processing screens from stack)
- After payment success → reset to HouseholdTabs

Pattern:
  navigation.reset({ index: 0, routes: [{ name: 'TargetScreen' }] });

---

VERIFICATION FOR PHASE 8:
- GigScore ring animates smoothly from 0 to target score over 1.5 seconds
- Ring animation uses ease-out curve (fast start, slow finish)
- All TextInputs show blue border when focused, dark border when unfocused
- No screen allows the user to swipe back into a processing or transition state
```

---

---

# PHASE 9 — Final Demo Preparation
### Goal: Seed demo data, run both demo flows, fix any remaining issues

---

```
PHASE 9 — FINAL DEMO PREPARATION

This is the final phase before submission. The goal is to ensure both demo 
flows run perfectly on a physical Android device.

---

TASK 9.1 — SEED DEMO DATA IN BACKEND

Run these commands against the Supabase database to create demo accounts.
The backend team must run this SQL before the demo:

  -- DEMO GIG WORKER: Raju Kumar
  INSERT INTO users (id, phone, role, full_name, city, is_verified)
  VALUES ('demo-gig-001', '9000000001', 'gig_worker', 'Raju Kumar', 'Mumbai', true);

  -- DEMO DOMESTIC WORKER: Priya Devi  
  INSERT INTO users (id, phone, role, full_name, city, is_verified)
  VALUES ('demo-domestic-001', '9000000002', 'domestic_worker', 'Priya Devi', 'New Delhi', true);

  -- DEMO HOUSEHOLD: Sharma Household
  INSERT INTO users (id, phone, role, full_name, city, is_verified)
  VALUES ('demo-household-001', '9000000003', 'household', 'Sharma Household', 'New Delhi', true);

  -- Link Priya Devi to Sharma Household
  INSERT INTO household_workers (household_id, worker_id, worker_role, monthly_salary, payment_day)
  VALUES ('demo-household-001', 'demo-domestic-001', 'Cook', 3500, 1);

  -- For the hackathon OTP demo: the backend should accept '123456' as valid OTP
  -- for all demo phone numbers (9000000001, 9000000002, 9000000003)
  -- Add this check to the verify-otp endpoint for demo phones only

---

TASK 9.2 — DEMO FLOW 1 CHECKLIST (Gig Worker)

Walk through this flow on a physical Android device before the demo:

  □ Open app → Splash shows Credwork logo for 2 seconds
  □ Language Select → tap English
  □ Role Select → tap "I'm a gig worker"
  □ Phone Entry → enter 9000000001 → Send OTP
  □ OTP Entry → enter 123456 → Verify
  □ (If new profile) → enter name + city → Continue
  □ Dashboard loads with GigScore 78, certificate v2
  □ Tap Upload Statement → file picker opens
  □ Select demo PDF → Start Scan
  □ Processing screen → checklist animates through 6 steps
  □ Success screen → "Verified!" → ₹18,500/month → GigScore 78
  □ Tap View Full Certificate → certificate document renders
  □ Tap Share → bottom sheet slides up (NOT navigating away)
  □ Tap Send via WhatsApp → system share sheet opens

---

TASK 9.3 — DEMO FLOW 2 CHECKLIST (Household + Domestic Worker)

  □ Switch to household account (9000000003)
  □ Dashboard shows Priya Devi (due) + Ramesh Singh (paid)
  □ Priya's Pay Now button is Electric Blue
  □ Tap Pay Now on Priya's card
  □ Payment screen shows ₹3,500 pre-filled, Salary selected
  □ Tap "Pay ₹3,500"
  □ Processing indicator shows for ~3 seconds
  □ Success micro-state: "Payment sent! Priya Devi's record has been updated."
  □ Auto-navigates back to household dashboard
  □ Switch to domestic worker account (9000000002)
  □ Dashboard shows "March paid ✓" in cyan pill
  □ GigScore ring animates to 71
  □ Tap My Certificate → certificate document renders with March payment

---

TASK 9.4 — FINAL DEVICE CHECKS

Run on a physical Android device (not simulator) and verify:
  □ No content bleeds into status bar on any screen
  □ Keyboard does not block buttons on login/profile/payment screens
  □ Bottom tab icons are visible and correct
  □ All primary buttons are Electric Blue
  □ No green colour exists anywhere except the WhatsApp icon
  □ GigScore ring animates on both dashboards
  □ Share sheet opens as overlay, not navigation
  □ Back button is disabled during processing
  □ The UploadFailedScreen shows correctly for a rejected PDF
```

---

---

## QUICK REFERENCE — Phase Summary

```
Phase 1 — Environment & API Foundation
  API config, axios client with interceptors, AuthContext, navigation ref

Phase 2 — Auth Flow Integration  
  OTP send/verify wired to backend, routing by user status, error messages

Phase 3 — Gig Worker Dashboard & Upload
  Dashboard loads real data, upload wires to backend, processing polls status

Phase 4 — Certificate Flow
  Success screen uses real params, certificate loads from API, real PDF sharing

Phase 5 — Household & Domestic Worker
  Payment flow with Razorpay simulation, domestic worker dashboard live data

Phase 6 — Error States & Edge Cases
  UploadFailedScreen, empty state for new users, global error handling

Phase 7 — Backend: Storage & Production
  Supabase Storage for certificates, CORS fix, VPA expansion

Phase 7B — ML: Income Anomaly Detection ← NEW
  IsolationForest model, anomaly_detector.py, pipeline integration,
  admin dashboard ML column, demo test verification

Phase 8 — Animation & Polish
  GigScore ring animates, input focus borders, navigation stack resets

Phase 9 — Demo Preparation
  Seed data, walk both demo flows, physical device verification
```

---

*One phase at a time. Verify before proceeding. Phase 1 must be complete before any other phase.*
*Phase 7B (ML) must be complete before Phase 9 demo prep — judges will ask about the ML component.*
*The demo flows in Phase 9 are the acceptance criteria for the entire build.*
