"use client"

import { motion, useInView } from "framer-motion"
import { useRef, useState } from "react"
import { fadeUp, stagger } from "@/lib/animations"

const testimonials = [
  {
    quote: "Applied for a personal loan and the bank asked for income proof. Uploaded my statement and got my certificate in 90 seconds. Loan approved the same day.",
    name: "Raju Kumar",
    role: "Delivery Partner",
    location: "Mumbai",
    initials: "RK",
    rotation: -2,
    yOffset: 8,
  },
  {
    quote: "My employer uses ServiConnect. My salary is tracked automatically now. I finally have official proof of income for my daughter's school admission.",
    name: "Priya Devi",
    role: "Domestic Worker",
    location: "New Delhi",
    initials: "PD",
    rotation: 0,
    yOffset: 0,
    featured: true,
  },
  {
    quote: "GigScore 82 — Excellent. Showed it to the landlord and got the apartment without any guarantor. This is life-changing for us gig workers.",
    name: "Arjun Singh",
    role: "Rapido Rider",
    location: "Bangalore",
    initials: "AS",
    rotation: 2,
    yOffset: 8,
  },
]

function StarRating() {
  return (
    <div className="flex gap-1 mb-4">
      {[...Array(5)].map((_, i) => (
        <svg key={i} width="18" height="18" viewBox="0 0 18 18" fill="#2563EB">
          <path d="M9 0l2.47 5.01L17 5.82l-4 3.9.94 5.49L9 12.69l-4.94 2.52.94-5.49-4-3.9 5.53-.81L9 0z" />
        </svg>
      ))}
    </div>
  )
}

export function TestimonialsSection() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)

  return (
    <section className="bg-[var(--cw-surface)] py-24 lg:py-32 overflow-hidden">
      <div ref={ref} className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="text-center mb-16"
        >
          <span className="inline-block font-body text-[13px] font-medium uppercase tracking-wider text-[var(--cw-accent)] mb-4">
            Real Workers, Real Results
          </span>
          <h2 className="font-display text-[clamp(32px,4vw,48px)] font-extrabold tracking-[-0.03em] text-[var(--cw-primary)] mb-4">
            Lakhs of gig workers trust Credwork
          </h2>
          <p className="font-body text-base text-[var(--cw-text-muted)] max-w-lg mx-auto">
            From delivery riders to domestic helpers — income credibility for everyone.
          </p>
        </motion.div>

        {/* Testimonial cards */}
        <motion.div
          variants={stagger(0.2, 0.1)}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
          className="grid md:grid-cols-3 gap-6 lg:gap-8"
        >
          {testimonials.map((testimonial, i) => (
            <motion.div
              key={i}
              variants={fadeUp}
              className={`relative rounded-[20px] bg-white border p-8 transition-all duration-300 cursor-default ${
                testimonial.featured
                  ? "border-[var(--cw-secondary)] shadow-lg"
                  : "border-[var(--cw-border)]"
              }`}
              style={{
                transform: hoveredIndex === i 
                  ? "rotate(0deg) translateY(-10px)" 
                  : `rotate(${testimonial.rotation}deg) translateY(${testimonial.yOffset}px)`,
                boxShadow: hoveredIndex === i ? "var(--shadow-lg)" : undefined,
              }}
              onMouseEnter={() => setHoveredIndex(i)}
              onMouseLeave={() => setHoveredIndex(null)}
            >
              <StarRating />
              
              <p className="font-body text-base text-[var(--cw-text-primary)] leading-relaxed mb-6">
                "{testimonial.quote}"
              </p>

              <div className="flex items-center gap-3">
                {/* Avatar */}
                <div 
                  className="w-11 h-11 rounded-full flex items-center justify-center text-sm font-semibold text-white"
                  style={{
                    background: `linear-gradient(135deg, #2563EB 0%, #06B6D4 100%)`,
                  }}
                >
                  {testimonial.initials}
                </div>
                <div>
                  <p className="font-body text-[15px] font-semibold text-[var(--cw-primary)]">
                    {testimonial.name}
                  </p>
                  <p className="font-body text-[13px] text-[var(--cw-text-muted)]">
                    {testimonial.role}, {testimonial.location}
                  </p>
                </div>
              </div>

              {/* Verified badge */}
              <div className="absolute bottom-4 right-4 flex items-center gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-[var(--cw-accent)]" />
                <span className="text-[10px] font-medium text-[var(--cw-text-light)]">
                  Verified via Credwork
                </span>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
