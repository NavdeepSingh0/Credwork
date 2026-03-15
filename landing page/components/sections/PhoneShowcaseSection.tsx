"use client"

import { useRef, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { phoneScreenTransition, stepContentTransition } from '@/lib/animations';
import { Shield, Zap, Clock, Globe, Check, Upload, BarChart3, Award, Share2 } from 'lucide-react';

const steps = [
  {
    badge: 'Step 01',
    heading: 'Sign in with your mobile number',
    body: 'No passwords, no forms. Just your phone number and a quick OTP. We verify your identity in seconds — completely secure.',
    chips: [{ icon: Clock, text: 'OTP in 30 seconds' }, { icon: Shield, text: 'No password needed' }, { icon: Globe, text: 'Hindi & English' }],
  },
  {
    badge: 'Step 02',
    heading: 'Upload your UPI bank statement',
    body: 'Download your bank statement PDF from your banking app. Upload it here — we automatically detect income from Swiggy, Zomato, Rapido, Blinkit, Urban Company, and 10+ other platforms.',
    chips: [{ icon: Upload, text: 'PDF auto-parsing' }, { icon: Shield, text: 'Fraud detection' }, { icon: Zap, text: 'File never stored' }],
  },
  {
    badge: 'Step 03',
    heading: 'Your income, automatically organized',
    body: 'Credwork reads every UPI transaction, identifies your platform earnings, and organizes them month by month. You can review each entry before your certificate is generated.',
    chips: [{ icon: BarChart3, text: '6-month history' }, { icon: BarChart3, text: 'Per-platform breakdown' }, { icon: Check, text: 'Editable entries' }],
  },
  {
    badge: 'Step 04',
    heading: 'Your GigScore: the number that speaks for you',
    body: 'The GigScore (0–100) measures your income consistency, platform diversity, growth trend, and verification quality. Banks, landlords, and lenders understand it instantly.',
    chips: [{ icon: Award, text: 'Consistency score' }, { icon: BarChart3, text: 'Income trend' }, { icon: Globe, text: 'Platform diversity' }],
  },
  {
    badge: 'Step 05',
    heading: 'Your official income certificate, in 2 minutes',
    body: 'A tamper-proof, digitally-signed income certificate with a unique ID. Share via WhatsApp, email, or a public verification link.',
    chips: [{ icon: Share2, text: 'Shareable link' }, { icon: Zap, text: 'WhatsApp share' }, { icon: Shield, text: 'QR verification' }],
  },
];

const PhoneScreen = ({ step }: { step: number }) => {
  const screens = [
    // Step 1 - OTP
    <div key={0} className="flex h-full flex-col items-center bg-white px-4 pt-8">
      <div className="mb-6 flex items-center gap-1.5">
        <div className="flex h-5 w-5 items-center justify-center rounded bg-[var(--cw-secondary)]"><Zap className="h-3 w-3 text-white" /></div>
        <span className="font-display text-sm font-bold text-[var(--cw-primary)]">Credwork</span>
      </div>
      <p className="mb-6 text-center font-body text-xs text-[var(--cw-text-muted)]">Enter your mobile number</p>
      <div className="mb-4 w-full rounded-xl border border-[var(--cw-border)] bg-white px-4 py-3">
        <span className="font-body text-sm text-[var(--cw-text-muted)]">+91 ___________</span>
      </div>
      <div className="w-full rounded-xl bg-[var(--cw-secondary)] py-3 text-center font-display text-sm font-semibold text-white">
        Send OTP
      </div>
      <p className="mt-3 font-body text-[10px] text-[var(--cw-text-muted)]">{"We'll send a 6-digit code"}</p>
    </div>,
    // Step 2 - Upload
    <div key={1} className="flex h-full flex-col items-center bg-white px-4 pt-6">
      <p className="mb-4 font-display text-sm font-bold text-[var(--cw-primary)]">Upload Bank Statement</p>
      <div className="mb-4 flex w-full flex-col items-center rounded-2xl border-2 border-dashed border-[var(--cw-secondary)]/30 bg-[var(--cw-surface-alt)] py-8">
        <Upload className="mb-2 h-8 w-8 text-[var(--cw-secondary)]/60" />
        <p className="font-body text-xs font-medium text-[var(--cw-primary)]">Upload PDF</p>
        <p className="font-body text-[10px] text-[var(--cw-text-muted)]">UPI bank statement</p>
      </div>
      <div className="mb-2 flex w-full items-center justify-between">
        <span className="font-body text-[10px] text-[var(--cw-text-muted)]">Processing...</span>
        <span className="font-body text-[10px] font-medium text-[var(--cw-secondary)]">35%</span>
      </div>
      <div className="w-full overflow-hidden rounded-full bg-[var(--cw-border)]">
        <div className="h-1.5 w-[35%] rounded-full bg-[var(--cw-secondary)]" />
      </div>
      <div className="mt-4 flex flex-wrap justify-center gap-1.5">
        {['Swiggy', 'Zomato', 'Rapido', 'Blinkit'].map(p => (
          <span key={p} className="rounded-full border border-[var(--cw-border)] bg-white px-2.5 py-1 font-body text-[9px] text-[var(--cw-text-muted)]">{p}</span>
        ))}
      </div>
      <p className="mt-4 font-body text-[9px] text-[var(--cw-text-light)]">Your file is never stored on our servers</p>
    </div>,
    // Step 3 - Income
    <div key={2} className="flex h-full flex-col bg-white px-4 pt-6">
      <div className="mb-3 flex items-center gap-2">
        <Check className="h-4 w-4 text-[var(--cw-success)]" />
        <p className="font-display text-sm font-bold text-[var(--cw-primary)]">Income Detected</p>
      </div>
      {[{ m: 'Oct 2024', a: '₹17,200', p: 'Swiggy + Zomato' }, { m: 'Nov 2024', a: '₹19,800', p: 'Swiggy + Zomato + Rapido' }, { m: 'Dec 2024', a: '₹15,500', p: 'Rapido + Blinkit' }].map((item, i) => (
        <div key={i} className="mb-2 rounded-xl border border-[var(--cw-border)] bg-white p-3">
          <div className="flex items-center justify-between">
            <span className="font-body text-[11px] font-medium text-[var(--cw-primary)]">{item.m}</span>
            <span className="font-display text-sm font-bold text-[var(--cw-primary)]">{item.a}</span>
          </div>
          <p className="mt-0.5 font-body text-[9px] text-[var(--cw-text-muted)]">{item.p}</p>
        </div>
      ))}
      <span className="mt-1 self-start rounded-full bg-[var(--cw-secondary)]/10 px-2 py-0.5 font-body text-[10px] font-medium text-[var(--cw-secondary)]">Avg ₹18,900/month</span>
      <div className="mt-auto mb-4 w-full rounded-xl bg-[var(--cw-secondary)] py-2.5 text-center font-display text-xs font-semibold text-white">Generate Certificate</div>
    </div>,
    // Step 4 - GigScore
    <div key={3} className="flex h-full flex-col items-center bg-white px-4 pt-6">
      <p className="mb-2 font-display text-sm font-bold text-[var(--cw-primary)]">Your GigScore</p>
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="50" fill="none" stroke="var(--cw-border)" strokeWidth="8" />
        <circle cx="60" cy="60" r="50" fill="none" stroke="var(--cw-secondary)" strokeWidth="8" strokeDasharray={`${78 * Math.PI * 100 / 100} ${Math.PI * 100}`} strokeLinecap="round" transform="rotate(-90 60 60)" />
        <text x="60" y="66" textAnchor="middle" fill="var(--cw-primary)" fontSize="28" fontWeight="800" fontFamily="var(--font-display)">78</text>
      </svg>
      <span className="mt-1 rounded-full bg-[var(--cw-success)]/10 px-3 py-0.5 font-body text-xs font-medium text-[var(--cw-success)]">Good</span>
      <div className="mt-4 grid w-full grid-cols-2 gap-2">
        {[{ l: 'Consistency', v: 82 }, { l: 'Growth', v: 74 }, { l: 'Diversity', v: 85 }, { l: 'Verification', v: 71 }].map(m => (
          <div key={m.l} className="rounded-lg border border-[var(--cw-border)] bg-white p-2 text-center">
            <p className="font-body text-[9px] text-[var(--cw-text-muted)]">{m.l}</p>
            <p className="font-display text-sm font-bold text-[var(--cw-secondary)]">{m.v}</p>
          </div>
        ))}
      </div>
    </div>,
    // Step 5 - Certificate
    <div key={4} className="flex h-full flex-col bg-white px-3 pt-5">
      <div className="rounded-xl border border-[var(--cw-border)] bg-white p-3 shadow-sm">
        <div className="mb-2 rounded-lg bg-[var(--cw-secondary)] px-3 py-1.5">
          <p className="font-display text-[10px] font-bold text-white">CREDWORK INCOME CERTIFICATE</p>
        </div>
        <div className="space-y-1.5">
          {[['Name', 'Raju Kumar'], ['Period', 'Oct 2024 – Mar 2025'], ['Monthly Avg', '₹18,900'], ['GigScore', '78 / Good'], ['ID', 'CW-2025-00847']].map(([k, v]) => (
            <div key={k} className="flex justify-between">
              <span className="font-body text-[9px] text-[var(--cw-text-muted)]">{k}</span>
              <span className="font-body text-[9px] font-medium text-[var(--cw-primary)]">{v}</span>
            </div>
          ))}
        </div>
        <div className="mt-2 flex items-center justify-between">
          <div className="flex h-8 w-8 items-center justify-center rounded-full border border-[var(--cw-accent)]/30 bg-[var(--cw-accent)]/10">
            <Award className="h-4 w-4 text-[var(--cw-accent)]" />
          </div>
          <svg width="32" height="32" viewBox="0 0 32 32">
            {[0,4,8,12,16,20,24,28].map(x => [0,4,8,12,16,20,24,28].map(y => (
              <rect key={`${x}-${y}`} x={x} y={y} width="3" height="3" rx="0.5" fill={(x + y) % 8 === 0 ? 'var(--cw-primary)' : 'var(--cw-border)'} />
            )))}
          </svg>
        </div>
      </div>
      <div className="mt-3 flex gap-2">
        <div className="flex-1 rounded-lg bg-[#25D366] py-2 text-center font-body text-[10px] font-medium text-white">WhatsApp</div>
        <div className="flex-1 rounded-lg bg-[var(--cw-secondary)] py-2 text-center font-body text-[10px] font-medium text-white">Copy Link</div>
        <div className="flex-1 rounded-lg bg-[var(--cw-primary)] py-2 text-center font-body text-[10px] font-medium text-white">PDF</div>
      </div>
      <div className="mt-2 flex items-center justify-center gap-1">
        <Check className="h-3 w-3 text-[var(--cw-success)]" />
        <span className="font-body text-[10px] font-medium text-[var(--cw-success)]">Certificate verified</span>
      </div>
    </div>,
  ];
  return screens[step] || screens[0];
};

export function PhoneShowcaseSection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [progress, setProgress] = useState(0);

  // Manual scroll tracking to avoid Framer Motion useScroll container warnings
  useEffect(() => {
    const handleScroll = () => {
      if (!sectionRef.current) return;
      const rect = sectionRef.current.getBoundingClientRect();
      const sectionHeight = sectionRef.current.offsetHeight;
      const viewportHeight = window.innerHeight;
      
      // Calculate progress (0 to 1) through the section
      const scrolled = -rect.top;
      const scrollableDistance = sectionHeight - viewportHeight;
      const rawProgress = Math.max(0, Math.min(1, scrolled / scrollableDistance));
      
      setProgress(rawProgress);
      const step = Math.min(Math.floor(rawProgress * steps.length), steps.length - 1);
      setActiveStep(step);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // Initial check
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <section id="how-it-works" ref={sectionRef} className="relative bg-[var(--cw-bg)]" style={{ height: `${(steps.length + 1) * 100}vh` }}>
      {/* Section header */}
      <div className="pb-16 pt-28 text-center">
        <p className="mb-3 font-body text-[13px] font-medium uppercase tracking-widest text-[var(--cw-accent)]">HOW IT WORKS</p>
        <h2 className="mx-auto max-w-3xl px-4 font-display text-[clamp(32px,4vw,56px)] font-extrabold leading-[1.1] tracking-[-0.03em] text-[var(--cw-primary)]">
          From bank statement <span className="gradient-text">to income certificate</span> in <span className="gradient-text">5 steps.</span>
        </h2>
        <p className="mx-auto mt-4 max-w-[520px] px-4 font-body text-[17px] text-[var(--cw-text-muted)]">
          {"No manual data entry. No waiting. No middlemen. Just upload your PDF and Credwork's fraud-proof engine does the rest."}
        </p>
      </div>

      <div className="sticky top-0 flex h-screen items-center">
        <div className="mx-auto grid w-full max-w-7xl grid-cols-1 items-center gap-12 px-6 lg:grid-cols-2 lg:gap-16">
          {/* Left - Step content */}
          <div className="relative pl-10 order-2 lg:order-1">
            {/* Progress line */}
            <div className="absolute bottom-0 left-0 top-0 w-[3px] rounded-full bg-[var(--cw-border)]">
              <div
                className="absolute left-0 top-0 w-[3px] rounded-full bg-gradient-to-b from-[var(--cw-secondary)] to-[var(--cw-accent)] transition-all duration-150"
                style={{ height: `${progress * 100}%` }}
              />
              {steps.map((_, i) => (
                <div
                  key={i}
                  className={`absolute left-1/2 h-4 w-4 -translate-x-1/2 rounded-full border-[3px] transition-all duration-300 ${
                    i <= activeStep ? 'scale-100 border-[var(--cw-secondary)] bg-[var(--cw-secondary)]' : 'scale-75 border-[var(--cw-border)] bg-[var(--cw-bg)]'
                  }`}
                  style={{ top: `${(i / (steps.length - 1)) * 100}%`, transform: 'translate(-50%, -50%)' }}
                />
              ))}
            </div>

            <AnimatePresence mode="wait">
              <motion.div
                key={activeStep}
                {...stepContentTransition}
                className="relative"
              >
                <span className="absolute -left-2 -top-8 select-none font-display text-[clamp(80px,10vw,120px)] font-extrabold text-[var(--cw-secondary)]/[0.06]">
                  0{activeStep + 1}
                </span>
                <span className="mb-3 inline-block rounded-full bg-[var(--cw-secondary)] px-3 py-1 font-display text-xs font-semibold text-white">
                  {steps[activeStep].badge}
                </span>
                <h3 className="mb-3 font-display text-[clamp(28px,3.5vw,42px)] font-bold leading-[1.1] tracking-[-0.03em] text-[var(--cw-primary)]">
                  {steps[activeStep].heading}
                </h3>
                <p className="mb-4 max-w-[400px] font-body text-[17px] leading-[1.7] text-[var(--cw-text-muted)]">
                  {steps[activeStep].body}
                </p>
                <div className="flex flex-wrap gap-2">
                  {steps[activeStep].chips.map((chip, i) => (
                    <span key={i} className="flex items-center gap-1.5 rounded-full border border-[var(--cw-border)] bg-white px-3 py-1.5 font-body text-[13px] font-medium text-[var(--cw-primary)]">
                      <chip.icon className="h-3.5 w-3.5 text-[var(--cw-secondary)]" />
                      {chip.text}
                    </span>
                  ))}
                </div>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Right - Phone */}
          <div className="flex flex-col items-center justify-center order-1 lg:order-2">
            {/* Phone glow */}
            <div className="relative">
              <div className="absolute left-1/2 top-1/2 -z-10 h-[200px] w-[200px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-60" style={{ background: 'radial-gradient(circle, var(--glow-blue), transparent 70%)', filter: 'blur(60px)' }} />
              <div className="absolute bottom-0 right-0 -z-10 h-[150px] w-[150px] rounded-full opacity-60" style={{ background: 'radial-gradient(circle, var(--glow-cyan), transparent 70%)', filter: 'blur(50px)' }} />

              {/* Phone frame */}
              <div className="relative h-[520px] w-[260px] overflow-hidden rounded-[44px] border-2 border-[var(--cw-primary)]/10 bg-[var(--cw-primary)] shadow-[0_30px_80px_rgba(17,24,39,0.35),0_0_60px_rgba(37,99,235,0.15)]">
                {/* Notch */}
                <div className="absolute left-1/2 top-3 z-20 h-[24px] w-[70px] -translate-x-1/2 rounded-full bg-[var(--cw-primary)]" />
                {/* Screen */}
                <div className="absolute inset-2.5 overflow-hidden rounded-[36px] bg-white">
                  <AnimatePresence mode="wait">
                    <motion.div
                      key={activeStep}
                      {...phoneScreenTransition}
                      className="h-full w-full pt-6"
                    >
                      <PhoneScreen step={activeStep} />
                    </motion.div>
                  </AnimatePresence>
                </div>
                {/* Home indicator */}
                <div className="absolute bottom-2.5 left-1/2 h-1 w-[90px] -translate-x-1/2 rounded-full bg-white/30" />
              </div>

              {/* Side buttons */}
              <div className="absolute -left-[3px] top-[100px] h-7 w-1 rounded-l bg-[var(--cw-primary)]/80" />
              <div className="absolute -left-[3px] top-[140px] h-10 w-1 rounded-l bg-[var(--cw-primary)]/80" />
              <div className="absolute -left-[3px] top-[175px] h-10 w-1 rounded-l bg-[var(--cw-primary)]/80" />
              <div className="absolute -right-[3px] top-[150px] h-14 w-1 rounded-r bg-[var(--cw-primary)]/80" />
            </div>

            {/* Step dots */}
            <div className="mt-6 flex items-center gap-2">
              {steps.map((_, i) => (
                <motion.div
                  key={i}
                  className="h-2 rounded-full"
                  animate={{
                    width: i === activeStep ? 24 : 8,
                    backgroundColor: i === activeStep ? 'var(--cw-secondary)' : 'var(--cw-border)',
                  }}
                  transition={{ type: 'spring', stiffness: 300, damping: 25 }}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default PhoneShowcaseSection;
