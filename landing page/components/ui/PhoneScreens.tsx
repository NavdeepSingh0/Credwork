"use client"

// Phone screen components for each step of the app flow

export function OTPScreen() {
  return (
    <div className="flex flex-col h-full bg-[var(--cw-bg)] p-4">
      {/* Logo */}
      <div className="flex justify-center pt-8 pb-6">
        <div className="flex items-center gap-2">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#2563EB"/>
            <path d="M12 16L15 19L21 13" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className="font-display text-lg font-bold text-[var(--cw-primary)]">Credwork</span>
        </div>
      </div>
      
      <div className="flex-1 flex flex-col items-center justify-center px-4">
        <h2 className="font-display text-xl font-bold text-[var(--cw-primary)] mb-2 text-center">
          Enter your mobile number
        </h2>
        <p className="text-sm text-[var(--cw-text-muted)] mb-6 text-center">
          {"We'll send you a 6-digit OTP"}
        </p>
        
        {/* Phone input */}
        <div className="w-full max-w-[200px] mb-4">
          <div className="flex items-center gap-2 rounded-xl bg-white border border-[var(--cw-border)] p-3">
            <span className="text-sm font-medium text-[var(--cw-text-muted)]">+91</span>
            <div className="h-5 w-px bg-[var(--cw-border)]" />
            <span className="text-sm text-[var(--cw-text-light)]">98765 43210</span>
          </div>
        </div>
        
        {/* Send OTP button */}
        <button className="w-full max-w-[200px] rounded-xl bg-[var(--cw-secondary)] py-3 font-display text-sm font-semibold text-white">
          Send OTP
        </button>
        
        <p className="mt-4 text-xs text-[var(--cw-text-light)] text-center">
          By continuing, you agree to our Terms & Privacy Policy
        </p>
      </div>
      
      {/* Language selector */}
      <div className="flex justify-center gap-3 pb-4">
        <span className="text-xs font-medium text-[var(--cw-secondary)]">English</span>
        <span className="text-xs text-[var(--cw-text-light)]">हिंदी</span>
      </div>
    </div>
  )
}

export function UploadScreen() {
  return (
    <div className="flex flex-col h-full bg-[var(--cw-bg)] p-4">
      <div className="pt-4 pb-3">
        <h2 className="font-display text-lg font-bold text-[var(--cw-primary)] text-center">
          Upload Bank Statement
        </h2>
      </div>
      
      <div className="flex-1 flex flex-col items-center justify-center px-2">
        {/* Upload zone */}
        <div className="w-full rounded-2xl border-2 border-dashed border-[var(--cw-secondary)]/40 bg-[var(--cw-secondary)]/5 p-6 flex flex-col items-center">
          <div className="w-12 h-12 rounded-xl bg-[var(--cw-secondary)]/10 flex items-center justify-center mb-3">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="2">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
            </svg>
          </div>
          <p className="text-sm font-medium text-[var(--cw-primary)] mb-1">
            Upload PDF
          </p>
          <p className="text-xs text-[var(--cw-text-muted)] text-center">
            UPI bank statement
          </p>
        </div>
        
        {/* Progress bar */}
        <div className="w-full mt-4">
          <div className="flex justify-between text-xs mb-1">
            <span className="text-[var(--cw-text-muted)]">Processing...</span>
            <span className="text-[var(--cw-secondary)]">35%</span>
          </div>
          <div className="h-2 rounded-full bg-[var(--cw-border)]">
            <div className="h-full w-[35%] rounded-full bg-[var(--cw-secondary)]" />
          </div>
        </div>
        
        {/* Platform logos */}
        <div className="flex flex-wrap justify-center gap-2 mt-6">
          {["Swiggy", "Zomato", "Rapido", "Blinkit"].map((platform) => (
            <span 
              key={platform}
              className="rounded-full bg-white border border-[var(--cw-border)] px-2.5 py-1 text-[10px] font-medium text-[var(--cw-text-muted)]"
            >
              {platform}
            </span>
          ))}
        </div>
      </div>
      
      <p className="text-[10px] text-[var(--cw-text-light)] text-center pb-2">
        Your file is never stored on our servers
      </p>
    </div>
  )
}

export function IncomeScreen() {
  const incomeData = [
    { month: "Oct 2024", amount: "₹17,200", platforms: "Swiggy + Zomato" },
    { month: "Nov 2024", amount: "₹19,800", platforms: "Swiggy + Zomato + Rapido" },
    { month: "Dec 2024", amount: "₹15,500", platforms: "Rapido + Blinkit" },
  ]
  
  return (
    <div className="flex flex-col h-full bg-[var(--cw-bg)] p-4">
      <div className="flex items-center gap-2 pt-2 pb-4">
        <div className="w-6 h-6 rounded-full bg-[var(--cw-success)]/10 flex items-center justify-center">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M2 6L5 9L10 3" stroke="#10B981" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </div>
        <h2 className="font-display text-base font-bold text-[var(--cw-primary)]">
          Income Detected
        </h2>
      </div>
      
      <div className="flex-1 overflow-hidden">
        {/* Income cards */}
        <div className="space-y-2">
          {incomeData.map((item, i) => (
            <div key={i} className="rounded-xl bg-white border border-[var(--cw-border)] p-3">
              <div className="flex justify-between items-start mb-1">
                <span className="text-xs text-[var(--cw-text-muted)]">{item.month}</span>
                <span className="font-display text-base font-bold text-[var(--cw-primary)]">{item.amount}</span>
              </div>
              <p className="text-[10px] text-[var(--cw-text-light)]">{item.platforms}</p>
            </div>
          ))}
        </div>
        
        {/* Average chip */}
        <div className="flex justify-center mt-4">
          <span className="rounded-full bg-[var(--cw-secondary)]/10 px-3 py-1.5 text-xs font-medium text-[var(--cw-secondary)]">
            Avg ₹18,900/month
          </span>
        </div>
        
        {/* Mini bar chart */}
        <div className="mt-4 px-2">
          <div className="flex items-end justify-between h-10 gap-1">
            {[60, 80, 50, 90, 70, 100].map((h, i) => (
              <div key={i} className="flex-1 rounded-t bg-[var(--cw-secondary)]" style={{ height: `${h}%`, opacity: 0.3 + i * 0.1 }} />
            ))}
          </div>
        </div>
      </div>
      
      <button className="w-full rounded-xl bg-[var(--cw-secondary)] py-3 font-display text-sm font-semibold text-white mt-4">
        Generate Certificate
      </button>
    </div>
  )
}

export function GigScoreScreen() {
  const metrics = [
    { label: "Consistency", value: 82 },
    { label: "Income Growth", value: 74 },
    { label: "Platform Diversity", value: 85 },
    { label: "Verification", value: 71 },
  ]
  
  return (
    <div className="flex flex-col h-full bg-[var(--cw-bg)] p-4">
      <h2 className="font-display text-base font-bold text-[var(--cw-primary)] text-center pt-2 pb-4">
        Your GigScore
      </h2>
      
      <div className="flex-1 flex flex-col items-center">
        {/* Score circle */}
        <div className="relative w-36 h-36 mb-4">
          <svg viewBox="0 0 120 120" className="w-full h-full">
            {/* Background arc */}
            <circle
              cx="60"
              cy="60"
              r="50"
              fill="none"
              stroke="#E2E8F0"
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray="235.6"
              strokeDashoffset="59"
              transform="rotate(135 60 60)"
            />
            {/* Filled arc */}
            <circle
              cx="60"
              cy="60"
              r="50"
              fill="none"
              stroke="url(#scoreGradient)"
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray="235.6"
              strokeDashoffset={235.6 - (0.78 * 176.7)}
              transform="rotate(135 60 60)"
            />
            <defs>
              <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#2563EB" />
                <stop offset="100%" stopColor="#06B6D4" />
              </linearGradient>
            </defs>
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="font-display text-3xl font-extrabold text-[var(--cw-primary)]">78</span>
            <span className="text-xs text-[var(--cw-text-muted)]">GigScore</span>
          </div>
        </div>
        
        {/* Good badge */}
        <span className="rounded-full bg-[var(--cw-success)] px-4 py-1 text-xs font-semibold text-white mb-6">
          Good
        </span>
        
        {/* Sub-metrics */}
        <div className="w-full grid grid-cols-2 gap-3">
          {metrics.map((metric) => (
            <div key={metric.label} className="rounded-xl bg-white border border-[var(--cw-border)] p-2.5">
              <div className="flex items-center gap-2 mb-1.5">
                <div className="relative w-6 h-6">
                  <svg viewBox="0 0 24 24" className="w-full h-full">
                    <circle cx="12" cy="12" r="10" fill="none" stroke="#E2E8F0" strokeWidth="3" />
                    <circle
                      cx="12"
                      cy="12"
                      r="10"
                      fill="none"
                      stroke="#2563EB"
                      strokeWidth="3"
                      strokeDasharray={62.8}
                      strokeDashoffset={62.8 - (metric.value / 100 * 62.8)}
                      strokeLinecap="round"
                      transform="rotate(-90 12 12)"
                    />
                  </svg>
                </div>
                <span className="font-display text-sm font-bold text-[var(--cw-secondary)]">{metric.value}</span>
              </div>
              <p className="text-[10px] text-[var(--cw-text-muted)]">{metric.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export function CertificateScreen() {
  return (
    <div className="flex flex-col h-full bg-[var(--cw-bg)] p-4">
      <h2 className="font-display text-base font-bold text-[var(--cw-primary)] text-center pt-2 pb-3">
        Certificate Ready
      </h2>
      
      <div className="flex-1 flex flex-col">
        {/* Mini certificate preview */}
        <div className="rounded-xl bg-white border border-[var(--cw-border)] overflow-hidden shadow-sm">
          {/* Header */}
          <div className="bg-[var(--cw-secondary)] px-3 py-2">
            <span className="text-[10px] font-bold text-white tracking-wide">CREDWORK</span>
          </div>
          
          <div className="p-3 relative">
            <p className="text-xs font-semibold text-[var(--cw-primary)] mb-2">Income Certificate</p>
            
            <div className="space-y-1.5 text-[10px]">
              <div className="flex justify-between">
                <span className="text-[var(--cw-text-muted)]">Name</span>
                <span className="font-medium text-[var(--cw-primary)]">Raju Kumar</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[var(--cw-text-muted)]">Period</span>
                <span className="font-medium text-[var(--cw-primary)]">Oct 2024 – Mar 2025</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[var(--cw-text-muted)]">Monthly Avg</span>
                <span className="font-bold text-[var(--cw-primary)]">₹18,900</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[var(--cw-text-muted)]">GigScore</span>
                <span className="font-bold text-[var(--cw-success)]">78 / Good</span>
              </div>
            </div>
            
            <div className="mt-2 pt-2 border-t border-[var(--cw-border)]">
              <p className="text-[9px] font-mono text-[var(--cw-text-light)]">ID: CW-2025-00847</p>
            </div>
            
            {/* Seal */}
            <div className="absolute right-2 bottom-2">
              <svg width="28" height="28" viewBox="0 0 28 28">
                <circle cx="14" cy="14" r="12" fill="none" stroke="#06B6D4" strokeWidth="1.5" strokeDasharray="3 2"/>
                <circle cx="14" cy="14" r="8" fill="#06B6D4" opacity="0.2"/>
                <path d="M10 14L13 17L19 11" stroke="#06B6D4" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </div>
          </div>
        </div>
        
        {/* Verified chip */}
        <div className="flex justify-center mt-3">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-[var(--cw-success)]/10 px-3 py-1 text-[10px] font-medium text-[var(--cw-success)]">
            <span className="h-1.5 w-1.5 rounded-full bg-[var(--cw-success)]" />
            Certificate verified
          </span>
        </div>
        
        {/* Share buttons */}
        <div className="flex gap-2 mt-4">
          <button className="flex-1 flex items-center justify-center gap-1.5 rounded-xl bg-[#25D366] py-2.5 text-[11px] font-semibold text-white">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
            </svg>
            WhatsApp
          </button>
          <button className="flex-1 flex items-center justify-center gap-1.5 rounded-xl bg-[var(--cw-secondary)] py-2.5 text-[11px] font-semibold text-white">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/>
              <path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/>
            </svg>
            Copy Link
          </button>
        </div>
        
        <button className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-[var(--cw-primary)] py-2.5 text-[11px] font-semibold text-white mt-2">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
          </svg>
          Download PDF
        </button>
      </div>
    </div>
  )
}
