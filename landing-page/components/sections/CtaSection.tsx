"use client"

import { motion, useInView } from "framer-motion"
import { useRef } from "react"
import { Download, Users, Shield, Zap } from "lucide-react"
import { fadeUp } from "@/lib/animations"

export function CtaSection() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section 
      id="download"
      className="relative py-24 lg:py-32 overflow-hidden bg-[#111827]"
    >
      {/* Subtle grid pattern */}
      <div className="absolute inset-0 opacity-[0.03]">
        <svg className="w-full h-full">
          <defs>
            <pattern id="ctaGrid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" strokeWidth="1" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#ctaGrid)" />
        </svg>
      </div>

      {/* Accent line at top */}
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[var(--cw-secondary)]/30 to-transparent" />

      <div ref={ref} className="relative mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Headline */}
          <motion.h2
            variants={fadeUp}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
            className="font-display text-[clamp(32px,4.5vw,56px)] font-extrabold tracking-[-0.03em] text-white mb-5 leading-[1.15]"
          >
            Every gig worker deserves{" "}
            <span className="text-[var(--cw-secondary)]">financial credibility.</span>
          </motion.h2>

          {/* Subtext */}
          <motion.p
            variants={fadeUp}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
            transition={{ delay: 0.1 }}
            className="font-body text-base lg:text-lg text-white/55 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Download Credwork. Upload your statement. Get your certificate. 
            {"It's"} free, instant, and finally gives your income the recognition it deserves.
          </motion.p>

          {/* Single CTA Button */}
          <motion.div
            variants={fadeUp}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
            transition={{ delay: 0.2 }}
            className="mb-12"
          >
            <motion.a
              href="/credwork.apk"
              download="credwork.apk"
              className="inline-flex items-center gap-3 rounded-full bg-[var(--cw-secondary)] px-8 py-4 font-body text-base font-semibold text-white transition-all hover:bg-[var(--cw-secondary)]/90"
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
            >
              <Download className="h-5 w-5" />
              Download App
            </motion.a>
          </motion.div>

          {/* Trust indicators */}
          <motion.div
            variants={fadeUp}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
            transition={{ delay: 0.3 }}
            className="flex flex-wrap items-center justify-center gap-6 lg:gap-10"
          >
            <div className="flex items-center gap-2 text-white/50">
              <Users className="h-4 w-4 text-[var(--cw-accent)]" />
              <span className="font-body text-sm">10,000+ Workers</span>
            </div>
            <div className="flex items-center gap-2 text-white/50">
              <Shield className="h-4 w-4 text-[var(--cw-accent)]" />
              <span className="font-body text-sm">Bank-grade Security</span>
            </div>
            <div className="flex items-center gap-2 text-white/50">
              <Zap className="h-4 w-4 text-[var(--cw-accent)]" />
              <span className="font-body text-sm">Free Forever</span>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
