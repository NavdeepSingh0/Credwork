"use client"

import { motion } from "framer-motion"
import { Download, ChevronDown } from "lucide-react"
import { StaircaseIllustration } from "@/components/ui/StaircaseIllustration"

const headlineWords = [
  { text: "Your", gradient: false },
  { text: "gig", gradient: false },
  { text: "income,", gradient: false },
  { text: "finally", gradient: true },
  { text: "official.", gradient: true },
]

const avatarData = [
  { initials: "RK", gradient: "linear-gradient(135deg, #2563EB 0%, #06B6D4 100%)" },
  { initials: "PS", gradient: "linear-gradient(135deg, #10B981 0%, #06B6D4 100%)" },
  { initials: "AD", gradient: "linear-gradient(135deg, #F59E0B 0%, #EF4444 100%)" },
  { initials: "MG", gradient: "linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)" },
  { initials: "NK", gradient: "linear-gradient(135deg, #2563EB 0%, #8B5CF6 100%)" },
]

export function HeroSection() {
  return (
    <section className="relative min-h-svh overflow-hidden bg-[var(--cw-bg)]">
      {/* Background Elements */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Blue glow - top right */}
        <div 
          className="absolute -right-[150px] -top-[50px] h-[500px] w-[500px]"
          style={{
            background: "radial-gradient(circle, rgba(37,99,235,0.12) 0%, transparent 65%)",
            filter: "blur(60px)",
          }}
        />
        
        {/* Cyan glow - bottom left */}
        <div 
          className="absolute -left-[100px] bottom-[10%] h-[350px] w-[350px]"
          style={{
            background: "radial-gradient(circle, rgba(6,182,212,0.1) 0%, transparent 65%)",
            filter: "blur(80px)",
          }}
        />

        {/* Dot grid */}
        <svg className="absolute inset-0 w-full h-full opacity-[0.03]">
          <defs>
            <pattern id="heroGrid" width="32" height="32" patternUnits="userSpaceOnUse">
              <circle cx="16" cy="16" r="1" fill="#64748B" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#heroGrid)" />
        </svg>
      </div>

      {/* Main Content */}
      <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-28 lg:pt-36">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center min-h-[calc(100svh-8rem)]">
          
          {/* Left Column - Text */}
          <div className="flex flex-col justify-center lg:pr-8">
            {/* Eyebrow badge */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 self-start rounded-full border border-[var(--cw-accent)]/25 bg-[var(--cw-accent)]/10 px-4 py-1.5 mb-6"
            >
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[var(--cw-accent)] opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-[var(--cw-accent)]"></span>
              </span>
              <span className="font-body text-[13px] font-medium text-[var(--cw-accent)]">
                {"India's First Gig Income Certificate"}
              </span>
            </motion.div>

            {/* Headline */}
            <motion.h1
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="font-display text-[clamp(40px,6vw,72px)] font-extrabold leading-[1.05] tracking-[-0.035em] text-[var(--cw-primary)] mb-6"
            >
              {headlineWords.map((word, i) => (
                <motion.span
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.15 + i * 0.08, duration: 0.5 }}
                  className={`inline-block mr-[0.22em] ${word.gradient ? "gradient-text" : ""}`}
                >
                  {word.text}
                </motion.span>
              ))}
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.5 }}
              className="font-body text-lg text-[var(--cw-text-muted)] max-w-[500px] leading-relaxed mb-8"
            >
              Upload your UPI bank statement from Swiggy, Zomato, Rapido, or any gig platform — get a verifiable income certificate with your GigScore in under 2 minutes.
            </motion.p>

            {/* CTA Row */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.75, duration: 0.5 }}
              className="flex flex-wrap items-center gap-4 mb-10"
            >
              <motion.a
                href="/credwork.apk"
                download="credwork.apk"
                className="inline-flex items-center gap-2.5 rounded-full bg-[var(--cw-secondary)] px-7 py-3.5 font-display text-[15px] font-semibold text-white shadow-[0_4px_20px_rgba(37,99,235,0.25)] transition-all hover:shadow-[0_8px_30px_rgba(37,99,235,0.35)] hover:bg-[#1d4ed8]"
                whileHover={{ y: -2 }}
                whileTap={{ scale: 0.98 }}
              >
                <Download className="h-5 w-5" />
                Download Free App
              </motion.a>
              
              <a
                href="#how-it-works"
                className="group inline-flex items-center gap-1.5 font-body text-[15px] font-medium text-[var(--cw-text-muted)] transition-colors hover:text-[var(--cw-secondary)]"
              >
                <span className="relative">
                  See how it works
                  <span className="absolute -bottom-0.5 left-0 h-[2px] w-0 bg-[var(--cw-secondary)] transition-all duration-300 group-hover:w-full" />
                </span>
                <ChevronDown className="h-4 w-4" />
              </a>
            </motion.div>

            {/* Social proof */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9, duration: 0.5 }}
              className="flex items-center gap-4"
            >
              <div className="flex -space-x-2.5">
                {avatarData.map((avatar, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 1 + i * 0.08, type: "spring", stiffness: 400 }}
                    className="relative flex h-10 w-10 items-center justify-center rounded-full border-[2.5px] border-[var(--cw-bg)] text-xs font-bold text-white shadow-sm"
                    style={{ background: avatar.gradient, zIndex: 5 - i }}
                  >
                    {avatar.initials}
                  </motion.div>
                ))}
              </div>
              <div className="flex flex-col">
                <span className="font-body text-sm text-[var(--cw-text-muted)]">
                  Trusted by <span className="font-semibold text-[var(--cw-primary)]">10,000+</span> workers
                </span>
                <span className="font-body text-xs text-[var(--cw-text-light)]">
                  across India
                </span>
              </div>
            </motion.div>
          </div>

          {/* Right Column - Illustration */}
          <div className="relative flex items-center justify-center lg:justify-end">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              className="w-full max-w-[560px]"
            >
              <StaircaseIllustration />
            </motion.div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2 }}
        className="absolute bottom-6 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 6, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          className="flex flex-col items-center gap-1.5"
        >
          <span className="text-[11px] font-medium tracking-wide text-[var(--cw-text-light)] uppercase">Scroll</span>
          <ChevronDown className="h-4 w-4 text-[var(--cw-text-light)]" />
        </motion.div>
      </motion.div>
    </section>
  )
}
