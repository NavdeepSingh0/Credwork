"use client"

import { motion, AnimatePresence } from "framer-motion"
import { useEffect, useState } from "react"

// Bar data
const bars = [
  { month: "Oct", x: 38, height: 90, income: "₹17.2k", color: "#2563EB" },
  { month: "Nov", x: 116, height: 122, income: "₹19.8k", color: "#2563EB" },
  { month: "Dec", x: 194, height: 86, income: "₹15.5k", color: "#818CF8" },
  { month: "Jan", x: 272, height: 152, income: "₹21k", color: "#10B981" },
  { month: "Feb", x: 350, height: 165, income: "₹18.9k", color: "#2563EB" },
  { month: "Mar", x: 428, height: 190, income: "₹19.1k", color: "#06B6D4" },
]

// Character positions (percentage based for responsiveness)
const charPositions = [
  { left: "2%", bottom: "32%" },
  { left: "12%", bottom: "38%" },
  { left: "24%", bottom: "31%" },
  { left: "35%", bottom: "43%" },
  { left: "47%", bottom: "46%" },
  { left: "56%", bottom: "50%" },
]

const barWidth = 64
const baseline = 458
const depth3D = 10
const depthY = 6

export function StaircaseIllustration() {
  const [mounted, setMounted] = useState(false)
  const [currentBar, setCurrentBar] = useState(0)
  const [showChar, setShowChar] = useState(false)
  const [showCert, setShowCert] = useState(false)
  const [showChips, setShowChips] = useState(false)

  useEffect(() => {
    setMounted(true)
    
    let animationFrame: number
    let isRunning = true
    
    const runSequence = () => {
      if (!isRunning) return
      
      // Reset state
      setCurrentBar(0)
      setShowChar(false)
      setShowCert(false)
      setShowChips(false)
      
      const timers: NodeJS.Timeout[] = []
      
      // Show character after bars animate in
      timers.push(setTimeout(() => setShowChar(true), 1000))
      
      // Walk through bars (slower - 700ms between steps)
      timers.push(setTimeout(() => setCurrentBar(1), 1800))
      timers.push(setTimeout(() => setCurrentBar(2), 2600))
      timers.push(setTimeout(() => setCurrentBar(3), 3400))
      timers.push(setTimeout(() => setCurrentBar(4), 4200))
      timers.push(setTimeout(() => setCurrentBar(5), 5000))
      
      // Show certificate and chips
      timers.push(setTimeout(() => setShowCert(true), 5800))
      timers.push(setTimeout(() => setShowChips(true), 6400))
      
      // Loop after 5 second delay (total cycle ~12s)
      timers.push(setTimeout(() => {
        if (isRunning) runSequence()
      }, 12000))
      
      return timers
    }
    
    const timers = runSequence()
    
    return () => {
      isRunning = false
      timers?.forEach(clearTimeout)
    }
  }, [])

  if (!mounted) return null

  return (
    <div className="relative w-full" style={{ aspectRatio: "740/560" }}>
      {/* SVG Layer */}
      <svg
        viewBox="0 0 740 560"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="absolute inset-0 w-full h-full"
        style={{ zIndex: 1 }}
      >
        <defs>
          {/* Gradients */}
          <linearGradient id="barGradBlue" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#3B82F6" />
            <stop offset="100%" stopColor="#2563EB" />
          </linearGradient>
          <linearGradient id="barGradCyan" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#22D3EE" />
            <stop offset="100%" stopColor="#06B6D4" />
          </linearGradient>
          <linearGradient id="barGradGreen" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#34D399" />
            <stop offset="100%" stopColor="#10B981" />
          </linearGradient>
          <radialGradient id="bgGlow" cx="90%" cy="10%" r="60%">
            <stop offset="0%" stopColor="#2563EB" stopOpacity="0.08" />
            <stop offset="100%" stopColor="#2563EB" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* Background glow */}
        <ellipse cx="640" cy="50" rx="300" ry="250" fill="url(#bgGlow)" />

        {/* Dot grid */}
        <g opacity="0.25">
          {Array.from({ length: 18 }).map((_, i) =>
            Array.from({ length: 12 }).map((_, j) => (
              <circle
                key={`${i}-${j}`}
                cx={40 + i * 40}
                cy={30 + j * 45}
                r="1.5"
                fill="#CBD5E1"
              />
            ))
          )}
        </g>

        {/* Bars with 3D effect */}
        {bars.map((bar, i) => {
          const topY = baseline - bar.height
          const isFinal = i === 5
          const gradient = isFinal ? "url(#barGradCyan)" : i === 3 ? "url(#barGradGreen)" : "url(#barGradBlue)"

          return (
            <motion.g
              key={bar.month}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1, duration: 0.5, ease: "easeOut" }}
            >
              {/* Front face */}
              <rect
                x={bar.x}
                y={topY}
                width={barWidth}
                height={bar.height}
                rx={6}
                fill={gradient}
              />
              {/* Top face (3D) */}
              <path
                d={`M${bar.x},${topY} L${bar.x + depth3D},${topY - depthY} L${bar.x + barWidth + depth3D},${topY - depthY} L${bar.x + barWidth},${topY} Z`}
                fill={isFinal ? "#67E8F9" : i === 3 ? "#6EE7B7" : "#60A5FA"}
                opacity={0.7}
              />
              {/* Right face (3D) */}
              <path
                d={`M${bar.x + barWidth},${topY} L${bar.x + barWidth + depth3D},${topY - depthY} L${bar.x + barWidth + depth3D},${baseline - depthY} L${bar.x + barWidth},${baseline} Z`}
                fill={isFinal ? "#0891B2" : i === 3 ? "#059669" : "#1D4ED8"}
                opacity={0.5}
              />
              {/* Month label */}
              <text
                x={bar.x + barWidth / 2}
                y={baseline + 24}
                textAnchor="middle"
                fill="#64748B"
                fontSize="13"
                fontWeight="500"
              >
                {bar.month}
              </text>
              
              {/* Final bar glow */}
              {isFinal && (
                <rect
                  x={bar.x - 4}
                  y={topY - 4}
                  width={barWidth + 8}
                  height={bar.height + 8}
                  rx={10}
                  fill="none"
                  stroke="#06B6D4"
                  strokeWidth={2}
                  strokeOpacity={0.3}
                />
              )}
            </motion.g>
          )
        })}

        {/* Connector line from bar 6 to certificate area */}
        <motion.path
          d="M 510 280 Q 560 250 590 180"
          stroke="#06B6D4"
          strokeWidth="2"
          strokeDasharray="6 4"
          fill="none"
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 0.5 }}
          transition={{ delay: 3.2, duration: 0.8 }}
        />
      </svg>

      {/* Character */}
      <AnimatePresence>
        {showChar && (
          <motion.div
            className="absolute"
            style={{
              width: "22%",
              left: charPositions[currentBar].left,
              bottom: charPositions[currentBar].bottom,
              zIndex: 20,
              transition: "left 0.6s cubic-bezier(0.34, 1.2, 0.64, 1), bottom 0.5s cubic-bezier(0.34, 1.2, 0.64, 1)",
            }}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
          >
            <motion.img
              src="/images/delivery-character.png"
              alt="Delivery worker"
              className="w-full h-auto"
              style={{ mixBlendMode: "multiply" }}
              animate={{ y: [0, -6, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 3 }}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Income label floating above current bar */}
      <AnimatePresence mode="wait">
        {showChar && (
          <motion.div
            key={currentBar}
            className="absolute bg-white rounded-lg px-3 py-1.5 shadow-lg border border-gray-100"
            style={{
              left: `${5 + currentBar * 11}%`,
              bottom: `${38 + (bars[currentBar].height / 190) * 18}%`,
              zIndex: 22,
            }}
            initial={{ opacity: 0, y: 10, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.9 }}
            transition={{ duration: 0.25 }}
          >
            <p className="text-xs text-gray-500 font-medium">{bars[currentBar].month}</p>
            <p className="text-sm font-bold text-gray-900">{bars[currentBar].income}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Certificate Card */}
      <AnimatePresence>
        {showCert && (
          <motion.div
            className="absolute bg-white rounded-xl border border-gray-200 overflow-hidden shadow-xl"
            style={{
              right: "2%",
              top: "12%",
              width: "28%",
              minWidth: 180,
              zIndex: 15,
              transform: "rotate(4deg)",
            }}
            initial={{ opacity: 0, scale: 0.7, y: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.34, 1.4, 0.64, 1] }}
          >
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-2">
              <p className="text-white text-[11px] font-bold tracking-wide">INCOME CERTIFICATE</p>
            </div>
            <div className="p-4">
              <p className="text-gray-500 text-[10px] mb-0.5">Certified to</p>
              <p className="text-gray-900 text-sm font-bold mb-3">Rajesh Kumar</p>
              <div className="flex items-center justify-between mb-3">
                <div>
                  <p className="text-gray-500 text-[9px]">GigScore</p>
                  <p className="text-blue-600 text-lg font-bold">78</p>
                </div>
                <div className="w-8 h-8 rounded-full bg-cyan-50 border-2 border-cyan-400 flex items-center justify-center">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#06B6D4" strokeWidth="3">
                    <path d="M20 6L9 17l-5-5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-green-500"/>
                <p className="text-green-600 text-[10px] font-medium">Verified</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Stat Chips */}
      <AnimatePresence>
        {showChips && (
          <>
            {/* Chip 1: Platforms */}
            <motion.div
              className="absolute bg-white rounded-2xl border border-gray-100 px-4 py-2.5 shadow-md flex items-center gap-3"
              style={{ left: "2%", top: "35%", zIndex: 10 }}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1, duration: 0.4 }}
            >
              <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="2">
                  <rect x="3" y="3" width="7" height="7" rx="1"/>
                  <rect x="14" y="3" width="7" height="7" rx="1"/>
                  <rect x="3" y="14" width="7" height="7" rx="1"/>
                  <rect x="14" y="14" width="7" height="7" rx="1"/>
                </svg>
              </div>
              <div>
                <p className="text-gray-500 text-[10px]">Platforms</p>
                <p className="text-gray-900 text-sm font-bold">4 Active</p>
              </div>
            </motion.div>

            {/* Chip 2: Consistency */}
            <motion.div
              className="absolute bg-white rounded-2xl border border-gray-100 px-4 py-2.5 shadow-md flex items-center gap-3"
              style={{ left: "32%", top: "15%", zIndex: 10 }}
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.4 }}
            >
              <div className="w-8 h-8 rounded-lg bg-green-50 flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                  <path d="M22 4L12 14.01l-3-3"/>
                </svg>
              </div>
              <div>
                <p className="text-gray-500 text-[10px]">Consistency</p>
                <p className="text-gray-900 text-sm font-bold">92%</p>
              </div>
            </motion.div>

            {/* Chip 3: Approved */}
            <motion.div
              className="absolute bg-white rounded-2xl border border-gray-100 px-4 py-2.5 shadow-md flex items-center gap-3"
              style={{ right: "5%", bottom: "18%", zIndex: 10 }}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3, duration: 0.4 }}
            >
              <div className="w-8 h-8 rounded-lg bg-cyan-50 flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#06B6D4" strokeWidth="2">
                  <path d="M9 12l2 2 4-4"/>
                  <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <p className="text-gray-500 text-[10px]">Status</p>
                <p className="text-green-600 text-sm font-bold">Approved</p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}
