"use client"

import { motion, AnimatePresence } from "framer-motion"
import { phoneScreenTransition } from "@/lib/animations"
import { 
  OTPScreen, 
  UploadScreen, 
  IncomeScreen, 
  GigScoreScreen, 
  CertificateScreen 
} from "./PhoneScreens"

interface PhoneMockupProps {
  activeStep: number
}

const screens = [
  OTPScreen,
  UploadScreen,
  IncomeScreen,
  GigScoreScreen,
  CertificateScreen,
]

export function PhoneMockup({ activeStep }: PhoneMockupProps) {
  const ActiveScreen = screens[activeStep] || OTPScreen

  return (
    <div className="relative">
      {/* Glow effects */}
      <div 
        className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[200px] h-[200px] rounded-full -z-10"
        style={{
          background: "rgba(37,99,235,0.25)",
          filter: "blur(60px)",
        }}
      />
      <div 
        className="absolute left-[60%] top-[60%] -translate-x-1/2 -translate-y-1/2 w-[150px] h-[150px] rounded-full -z-10"
        style={{
          background: "rgba(6,182,212,0.20)",
          filter: "blur(50px)",
        }}
      />

      {/* Phone shell */}
      <div 
        className="relative"
        style={{
          width: 280,
          height: 580,
        }}
      >
        {/* Outer frame */}
        <svg 
          width="280" 
          height="580" 
          viewBox="0 0 280 580" 
          fill="none" 
          className="absolute inset-0"
          style={{
            filter: "drop-shadow(0 30px 80px rgba(17,24,39,0.35)) drop-shadow(0 0 60px rgba(37,99,235,0.15))"
          }}
        >
          {/* Phone body */}
          <rect 
            x="1" 
            y="1" 
            width="278" 
            height="578" 
            rx="44" 
            fill="#111827"
            stroke="rgba(255,255,255,0.15)"
            strokeWidth="2"
          />
          
          {/* Side buttons - left */}
          <rect x="-2" y="100" width="4" height="25" rx="2" fill="#1F2937" />
          <rect x="-2" y="135" width="4" height="50" rx="2" fill="#1F2937" />
          <rect x="-2" y="195" width="4" height="50" rx="2" fill="#1F2937" />
          
          {/* Side button - right */}
          <rect x="278" y="160" width="4" height="70" rx="2" fill="#1F2937" />
        </svg>

        {/* Dynamic Island / Notch */}
        <div 
          className="absolute top-4 left-1/2 -translate-x-1/2 w-20 h-6 rounded-full bg-[#111827] z-20"
        />

        {/* Screen area */}
        <div 
          className="absolute overflow-hidden bg-[var(--cw-bg)]"
          style={{
            top: 12,
            left: 12,
            right: 12,
            bottom: 12,
            borderRadius: 36,
          }}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={activeStep}
              initial={phoneScreenTransition.initial}
              animate={phoneScreenTransition.animate}
              exit={phoneScreenTransition.exit}
              className="w-full h-full"
            >
              <ActiveScreen />
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Home indicator */}
        <div 
          className="absolute bottom-3 left-1/2 -translate-x-1/2 w-24 h-1 rounded-full bg-white/30 z-20"
        />
      </div>
    </div>
  )
}
