"use client"

import { motion } from "framer-motion"
import { FileCheck2 } from "lucide-react"

interface FloatingCardProps {
  variant: "gigscore" | "certificate" | "income" | "platform"
  platform?: "swiggy" | "zomato" | "rapido"
  className?: string
  delay?: number
}

export function FloatingCard({ variant, platform, className = "", delay = 0 }: FloatingCardProps) {
  // Platform badge
  if (variant === "platform" && platform) {
    const platformColors = {
      swiggy: "#FF5722",
      zomato: "#E23744", 
      rapido: "#FFD200"
    }
    const platformNames = {
      swiggy: "Swiggy",
      zomato: "Zomato",
      rapido: "Rapido"
    }
    
    return (
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay, type: "spring", stiffness: 400, damping: 15 }}
        className={`inline-flex items-center gap-2 rounded-full bg-white px-3 py-1.5 shadow-md border border-[#E2E8F0] ${className}`}
      >
        <span 
          className="h-2.5 w-2.5 rounded-full"
          style={{ backgroundColor: platformColors[platform] }}
        />
        <span className="text-xs font-medium text-[var(--cw-text-primary)]">
          {platformNames[platform]}
        </span>
      </motion.div>
    )
  }

  // GigScore Card
  if (variant === "gigscore") {
    return (
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className={`rounded-2xl bg-white p-4 shadow-lg border border-[#E2E8F0] ${className}`}
      >
        <div className="flex items-center gap-3">
          {/* Score circle */}
          <div className="relative w-12 h-12">
            <svg width="48" height="48" viewBox="0 0 48 48">
              <circle cx="24" cy="24" r="18" fill="none" stroke="#E2E8F0" strokeWidth="5"/>
              <circle 
                cx="24" cy="24" r="18" 
                fill="none" 
                stroke="#2563EB" 
                strokeWidth="5"
                strokeLinecap="round"
                strokeDasharray="113"
                strokeDashoffset="25"
                transform="rotate(-90 24 24)"
              />
              <text x="24" y="26" textAnchor="middle" fill="#111827" fontSize="12" fontWeight="bold">78</text>
            </svg>
          </div>
          <div>
            <p className="font-display text-sm font-bold text-[var(--cw-primary)]">GigScore™</p>
            <span className="inline-block mt-1 rounded-full bg-[#10B981]/15 px-2 py-0.5 text-[10px] font-semibold text-[#10B981]">
              Good
            </span>
          </div>
        </div>
      </motion.div>
    )
  }

  // Certificate Card
  if (variant === "certificate") {
    return (
      <motion.div
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className={`relative rounded-2xl bg-white p-4 shadow-lg border border-[#E2E8F0] ${className}`}
      >
        {/* UPI Badge */}
        <div className="absolute -top-2.5 left-4 rounded-md bg-[var(--cw-secondary)] px-2.5 py-0.5 text-[10px] font-bold text-white">
          UPI
        </div>
        
        <div className="flex items-center gap-2 mb-2 mt-1">
          <div className="w-7 h-7 rounded-lg bg-[var(--cw-secondary)]/10 flex items-center justify-center">
            <FileCheck2 className="h-4 w-4 text-[var(--cw-secondary)]" />
          </div>
          <span className="font-display text-sm font-bold text-[var(--cw-primary)]">
            Certificate Ready
          </span>
        </div>
        
        <p className="font-mono text-[10px] text-[var(--cw-text-muted)] mb-2">
          CW-2025-00847
        </p>
        
        <div className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-[var(--cw-accent)]" />
          <span className="text-[10px] text-[var(--cw-text-muted)]">
            Verified · Tamper-proof
          </span>
        </div>

        {/* Mini GigScore badge */}
        <div className="absolute -bottom-2 -right-2 flex items-center gap-1 rounded-full bg-white px-2 py-0.5 shadow-md border border-[#E2E8F0]">
          <span className="text-[9px] text-[var(--cw-text-muted)]">GigScore:</span>
          <span className="text-[10px] font-bold text-[var(--cw-secondary)]">78</span>
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="6" stroke="#06B6D4" strokeWidth="1.5" strokeDasharray="2 1.5"/>
            <path d="M6 8L7.5 9.5L10 6.5" stroke="#06B6D4" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
      </motion.div>
    )
  }

  // Income Card
  if (variant === "income") {
    return (
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className={`rounded-2xl bg-white p-4 shadow-lg border border-[#E2E8F0] ${className}`}
      >
        <p className="text-[9px] uppercase tracking-wider font-semibold text-[var(--cw-text-muted)] mb-1">
          Monthly Avg. Income
        </p>
        
        <p className="font-display text-2xl font-extrabold text-[var(--cw-primary)] mb-3">
          ₹18,900
        </p>
        
        {/* Bar chart */}
        <div className="flex items-end gap-1 h-7 mb-3">
          {[0.5, 0.7, 0.55, 0.8, 0.65, 0.9].map((h, i) => (
            <div
              key={i}
              className="w-3 rounded-sm"
              style={{ 
                height: `${h * 100}%`,
                backgroundColor: i === 5 ? "#06B6D4" : "#2563EB",
                opacity: i === 5 ? 1 : 0.4 + i * 0.1
              }}
            />
          ))}
        </div>
        
        {/* Platform pills */}
        <div className="flex flex-wrap gap-1">
          {[
            { name: "Swiggy", color: "#FF5722" },
            { name: "Zomato", color: "#E23744" },
            { name: "Rapido", color: "#FFD200" }
          ].map((p) => (
            <span
              key={p.name}
              className="inline-flex items-center gap-1 rounded-full bg-[#F1F5F9] px-2 py-0.5 text-[9px] font-medium text-[var(--cw-text-muted)]"
            >
              <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: p.color }} />
              {p.name}
            </span>
          ))}
        </div>
      </motion.div>
    )
  }

  return null
}
