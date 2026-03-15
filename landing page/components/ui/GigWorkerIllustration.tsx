"use client"

import { motion } from "framer-motion"

export function GigWorkerIllustration() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
      className="relative w-full max-w-[480px] mx-auto"
    >
      {/* Background rings */}
      <svg 
        className="absolute inset-0 w-full h-full" 
        viewBox="0 0 480 480"
        style={{ transform: 'translate(-10%, -5%)' }}
      >
        <circle 
          cx="280" cy="240" r="180" 
          fill="none" 
          stroke="#E2E8F0" 
          strokeWidth="1" 
          strokeDasharray="8 8"
          className="animate-slow-spin"
          style={{ transformOrigin: '280px 240px' }}
        />
        <circle 
          cx="280" cy="240" r="140" 
          fill="none" 
          stroke="#E2E8F0" 
          strokeWidth="1" 
          strokeDasharray="4 6"
          className="animate-slow-spin-reverse"
          style={{ transformOrigin: '280px 240px' }}
        />
      </svg>

      {/* Main SVG */}
      <svg
        viewBox="0 0 480 520"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="relative z-10 w-full h-auto"
      >
        <defs>
          <filter id="softShadow">
            <feDropShadow dx="0" dy="4" stdDeviation="8" floodOpacity="0.12"/>
          </filter>
          <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#2563EB"/>
            <stop offset="100%" stopColor="#06B6D4"/>
          </linearGradient>
        </defs>

        {/* Ground shadow */}
        <ellipse cx="260" cy="420" rx="120" ry="20" fill="rgba(17,24,39,0.06)"/>

        {/* Scooter */}
        <g filter="url(#softShadow)">
          {/* Wheels */}
          <circle cx="180" cy="400" r="35" fill="none" stroke="#111827" strokeWidth="8"/>
          <circle cx="180" cy="400" r="12" fill="#111827"/>
          <circle cx="340" cy="400" r="35" fill="none" stroke="#111827" strokeWidth="8"/>
          <circle cx="340" cy="400" r="12" fill="#111827"/>
          
          {/* Wheel spokes */}
          <g stroke="#64748B" strokeWidth="2">
            <line x1="180" y1="370" x2="180" y2="430"/>
            <line x1="150" y1="400" x2="210" y2="400"/>
            <line x1="340" y1="370" x2="340" y2="430"/>
            <line x1="310" y1="400" x2="370" y2="400"/>
          </g>
          
          {/* Scooter body */}
          <rect x="160" y="350" width="200" height="40" rx="10" fill="#111827"/>
          <rect x="300" y="300" width="60" height="55" rx="8" fill="#111827"/>
          
          {/* Handlebar */}
          <rect x="155" y="280" width="12" height="80" rx="4" fill="#111827"/>
          <rect x="140" y="270" width="42" height="14" rx="7" fill="#111827"/>
        </g>

        {/* Rider body */}
        <g filter="url(#softShadow)">
          {/* Legs */}
          <rect x="210" y="340" width="25" height="50" rx="8" fill="#64748B"/>
          <rect x="245" y="340" width="25" height="50" rx="8" fill="#64748B"/>
          
          {/* Torso */}
          <rect x="200" y="240" width="80" height="110" rx="12" fill="#111827"/>
          
          {/* Blue stripe on jacket */}
          <rect x="200" y="290" width="80" height="8" fill="#2563EB"/>
          
          {/* Arms */}
          <rect x="175" y="260" width="25" height="60" rx="8" fill="#111827" transform="rotate(-20 187 290)"/>
          <rect x="280" y="260" width="25" height="60" rx="8" fill="#111827" transform="rotate(15 292 290)"/>
          
          {/* Hands */}
          <circle cx="165" cy="295" r="12" fill="#FBBF7A"/>
          <circle cx="310" cy="300" r="12" fill="#FBBF7A"/>
          
          {/* Head */}
          <circle cx="240" cy="200" r="45" fill="#FBBF7A"/>
          
          {/* Helmet */}
          <path d="M195 195 Q195 150 240 150 Q285 150 285 195 L285 200 L195 200 Z" fill="#2563EB"/>
          <rect x="195" y="195" width="90" height="10" fill="#111827"/>
          
          {/* Face */}
          <circle cx="225" cy="210" r="5" fill="#111827"/>
          <circle cx="255" cy="210" r="5" fill="#111827"/>
          <path d="M230 230 Q240 240 250 230" stroke="#111827" strokeWidth="3" fill="none" strokeLinecap="round"/>
        </g>

        {/* Phone on handlebar */}
        <rect x="148" y="250" width="24" height="40" rx="4" fill="#2563EB" stroke="#111827" strokeWidth="2"/>
        <rect x="152" y="256" width="16" height="28" rx="2" fill="white"/>
      </svg>

      {/* Floating rupee symbol */}
      <motion.div
        animate={{ 
          y: [0, -10, 0],
          rotate: [0, 5, 0]
        }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-[20%] left-[25%]"
      >
        <div className="w-10 h-10 rounded-full bg-[#F59E0B] flex items-center justify-center text-white font-bold text-lg shadow-lg">
          ₹
        </div>
      </motion.div>

      {/* Platform badges */}
      <motion.div
        animate={{ y: [0, -6, 0] }}
        transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-[15%] right-[5%]"
      >
        <div className="flex items-center gap-1.5 bg-white rounded-full px-3 py-1.5 shadow-md border border-[var(--cw-border)]">
          <div className="w-2 h-2 rounded-full bg-[#FC8019]"/>
          <span className="text-xs font-medium text-[var(--cw-text-primary)]">Swiggy</span>
        </div>
      </motion.div>

      <motion.div
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 4.2, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
        className="absolute bottom-[35%] right-[0%]"
      >
        <div className="flex items-center gap-1.5 bg-white rounded-full px-3 py-1.5 shadow-md border border-[var(--cw-border)]">
          <div className="w-2 h-2 rounded-full bg-[#FFD700]"/>
          <span className="text-xs font-medium text-[var(--cw-text-primary)]">Rapido</span>
        </div>
      </motion.div>

      {/* UPI Badge */}
      <motion.div
        animate={{ y: [-4, 4, -4] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-[40%] right-[8%]"
      >
        <div className="bg-[#2563EB] text-white text-xs font-bold px-3 py-1 rounded-md shadow-lg">
          UPI
        </div>
      </motion.div>
    </motion.div>
  )
}
