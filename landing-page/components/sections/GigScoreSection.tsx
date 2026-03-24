"use client"

import { motion, useInView } from "framer-motion"
import { useRef, useEffect, useState } from "react"
import { fadeLeft, fadeRight } from "@/lib/animations"

const scoreRanges = [
  { label: "Insufficient", range: "0–20", color: "#EF4444" },
  { label: "Low", range: "21–40", color: "#F59E0B" },
  { label: "Moderate", range: "41–60", color: "#F59E0B" },
  { label: "Good", range: "61–80", color: "#10B981", active: true },
  { label: "Excellent", range: "81–100", color: "#10B981" },
]

const metrics = [
  { label: "Income Consistency", value: 82 },
  { label: "Platform Diversity", value: 85 },
  { label: "Growth Trend", value: 74 },
  { label: "Verification Quality", value: 71 },
]

export function GigScoreSection() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })
  const [animatedScore, setAnimatedScore] = useState(0)

  useEffect(() => {
    if (isInView) {
      const duration = 1800
      const start = Date.now()
      const targetScore = 78

      const animate = () => {
        const elapsed = Date.now() - start
        const progress = Math.min(elapsed / duration, 1)
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3)
        setAnimatedScore(Math.round(targetScore * eased))

        if (progress < 1) {
          requestAnimationFrame(animate)
        }
      }
      requestAnimationFrame(animate)
    }
  }, [isInView])

  // Calculate arc length for score
  const arcLength = 235.6 // Circumference for 270 degree arc
  const scoreOffset = arcLength - (animatedScore / 100 * 176.7)

  return (
    <section 
      id="gigscore"
      ref={ref}
      className="bg-[var(--cw-bg)] py-24 lg:py-32 overflow-hidden"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left - Text content */}
          <motion.div
            variants={fadeLeft}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
          >
            <span className="inline-block font-body text-[13px] font-medium uppercase tracking-wider text-[var(--cw-accent)] mb-4">
              GigScore™
            </span>
            <h2 className="font-display text-[clamp(32px,4vw,48px)] font-extrabold tracking-[-0.03em] text-[var(--cw-primary)] mb-6 leading-tight">
              The score that banks finally understand
            </h2>
            <p className="font-body text-base lg:text-lg text-[var(--cw-text-muted)] mb-8 leading-relaxed max-w-lg">
              GigScore is Credwork's proprietary income credibility score. It analyzes 6 months of gig income across platforms, weighs consistency, growth, and platform diversity — and outputs a single number from 0 to 100.
            </p>

            {/* Score range labels */}
            <div className="flex flex-wrap gap-2 mb-8">
              {scoreRanges.map((range, i) => (
                <div
                  key={i}
                  className={`rounded-lg px-3 py-2 transition-all ${
                    range.active
                      ? "bg-[var(--cw-secondary)] text-white scale-105"
                      : "bg-[var(--cw-border)] text-[var(--cw-text-muted)]"
                  }`}
                >
                  <p className="text-xs font-semibold">{range.label}</p>
                  <p className="text-[10px] opacity-70">{range.range}</p>
                </div>
              ))}
            </div>

            <p className="font-body text-sm text-[var(--cw-text-light)] italic">
              Used by NBFCs, microfinance institutions, and property managers as a credit-equivalent score for unbanked gig workers.
            </p>
          </motion.div>

          {/* Right - Animated GigScore meter */}
          <motion.div
            variants={fadeRight}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
            className="flex flex-col items-center"
          >
            {/* Main arc */}
            <div className="relative w-[280px] h-[280px] mb-8">
              <svg viewBox="0 0 120 120" className="w-full h-full">
                {/* Background arc */}
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke="#E2E8F0"
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={arcLength}
                  strokeDashoffset="59"
                  transform="rotate(135 60 60)"
                />
                {/* Gradient arc */}
                <defs>
                  <linearGradient id="arcGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#2563EB" />
                    <stop offset="100%" stopColor="#06B6D4" />
                  </linearGradient>
                </defs>
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke="url(#arcGradient)"
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={arcLength}
                  strokeDashoffset={scoreOffset}
                  transform="rotate(135 60 60)"
                  className="transition-all duration-100"
                />
              </svg>
              
              {/* Center content */}
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-display text-[56px] font-extrabold text-[var(--cw-primary)] leading-none">
                  {animatedScore}
                </span>
                <span className="font-body text-sm text-[var(--cw-text-muted)] mt-1">
                  GigScore
                </span>
                <span className="mt-3 rounded-full bg-[var(--cw-success)] px-4 py-1 text-xs font-semibold text-white">
                  Good
                </span>
              </div>
            </div>

            {/* Sub-metrics */}
            <div className="w-full max-w-[320px] grid grid-cols-2 gap-4">
              {metrics.map((metric, i) => (
                <div key={i} className="bg-white rounded-xl border border-[var(--cw-border)] p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-body text-xs text-[var(--cw-text-muted)]">
                      {metric.label}
                    </span>
                    <span className="font-display text-sm font-bold text-[var(--cw-secondary)]">
                      {isInView ? metric.value : 0}
                    </span>
                  </div>
                  <div className="h-2 rounded-full bg-[var(--cw-border)] overflow-hidden">
                    <motion.div
                      className="h-full rounded-full bg-[var(--cw-secondary)]"
                      initial={{ width: 0 }}
                      animate={isInView ? { width: `${metric.value}%` } : {}}
                      transition={{ duration: 1.2, delay: 0.3 + i * 0.15, ease: [0.16, 1, 0.3, 1] }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
