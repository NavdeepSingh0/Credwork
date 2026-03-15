"use client"

import { motion } from "framer-motion"
import { useInView } from "framer-motion"
import { useRef } from "react"
import { Shield, TrendingUp, FileCheck2 } from "lucide-react"
import { fadeUp, stagger } from "@/lib/animations"

const pillars = [
  {
    icon: Shield,
    iconColor: "#06B6D4",
    title: "Upload Bank PDF",
    description: "Your file is never stored. Ever. We process it in real-time, extract the income data, and delete it immediately.",
  },
  {
    icon: TrendingUp,
    iconColor: "#2563EB",
    title: "GigScore Calculated",
    description: "A score built for gig economy reality. Measures consistency, growth, and platform diversity across your earnings.",
  },
  {
    icon: FileCheck2,
    iconColor: "#10B981",
    title: "Certificate Generated",
    description: "Verifiable by any institution, anywhere. A tamper-proof document with a unique ID and QR code verification.",
  },
]

export function HowItWorksSection() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section 
      id="features"
      className="relative bg-[var(--cw-primary)] py-16 lg:py-20 overflow-hidden"
    >
      {/* Background decorations */}
      <div className="absolute inset-0 opacity-[0.03]">
        <svg className="w-full h-full">
          <defs>
            <pattern id="dotGridDark" width="32" height="32" patternUnits="userSpaceOnUse">
              <circle cx="16" cy="16" r="1" fill="white" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#dotGridDark)" />
        </svg>
      </div>

      <div ref={ref} className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="text-center mb-10"
        >
          <h2 className="font-display text-[clamp(28px,3.5vw,40px)] font-extrabold tracking-[-0.03em] text-white mb-3">
            Built for the way you work
          </h2>
          <p className="font-body text-sm text-white/60 max-w-lg mx-auto">
            Traditional income proof was never designed for gig workers. Credwork changes that.
          </p>
        </motion.div>

        {/* 3 pillars */}
        <motion.div
          variants={stagger(0.2, 0.1)}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
          className="grid md:grid-cols-3 gap-6 lg:gap-8"
        >
          {pillars.map((pillar, i) => (
            <motion.div
              key={i}
              variants={fadeUp}
              className="group relative rounded-2xl bg-white/[0.04] border border-white/[0.08] p-6 lg:p-8 transition-all duration-300 hover:bg-[var(--cw-secondary)]/[0.06] hover:border-[var(--cw-secondary)]/40 hover:-translate-y-1"
            >
              {/* Icon */}
              <div 
                className="w-12 h-12 rounded-xl flex items-center justify-center mb-5 transition-transform duration-300 group-hover:scale-110"
                style={{ background: `${pillar.iconColor}15` }}
              >
                <pillar.icon 
                  className="w-6 h-6" 
                  style={{ color: pillar.iconColor }}
                />
              </div>

              {/* Content */}
              <h3 className="font-display text-lg lg:text-xl font-bold text-white mb-2">
                {pillar.title}
              </h3>
              <p className="font-body text-sm text-white/60 leading-relaxed">
                {pillar.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
