"use client"

import { motion, AnimatePresence } from "framer-motion"
import { Smartphone } from "lucide-react"
import { useState, useEffect } from "react"
import Image from "next/image"

const navLinks = [
  { label: "Features", href: "#features" },
  { label: "How it works", href: "#how-it-works" },
  { label: "GigScore", href: "#gigscore" },
  { label: "Download", href: "/credwork.apk", download: "credwork.apk" },
]

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [activeSection, setActiveSection] = useState<string>("")
  const [isScrolled, setIsScrolled] = useState(false)
  const [navHeight, setNavHeight] = useState(72)
  
  // Track scroll state for background and height
  useEffect(() => {
    const handleScroll = () => {
      const scrolled = window.scrollY > 20
      setIsScrolled(scrolled)
      // Smoothly interpolate height from 72 to 64 based on scroll
      const newHeight = Math.max(64, 72 - (window.scrollY / 80) * 8)
      setNavHeight(newHeight)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // IntersectionObserver for active section detection
  useEffect(() => {
    const sections = navLinks.map(link => link.href.replace('#', ''))
    
    const observers = sections.map(sectionId => {
      const element = document.getElementById(sectionId)
      if (!element) return null

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              setActiveSection(`#${sectionId}`)
            }
          })
        },
        { threshold: 0.3, rootMargin: "-20% 0px -60% 0px" }
      )
      
      observer.observe(element)
      return { observer, element }
    })

    return () => {
      observers.forEach(obs => {
        if (obs) obs.observer.disconnect()
      })
    }
  }, [])

  // Staggered entrance animation
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.07,
        delayChildren: 0.1,
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: -10, filter: "blur(4px)" },
    visible: { 
      opacity: 1, 
      y: 0, 
      filter: "blur(0px)",
      transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] }
    }
  }

  const ctaVariants = {
    hidden: { opacity: 0, scale: 0.9, y: -10 },
    visible: { 
      opacity: 1, 
      scale: 1, 
      y: 0,
      transition: { 
        type: "spring", 
        stiffness: 400, 
        damping: 15,
        delay: 0.5 
      }
    }
  }

  return (
    <motion.header
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="fixed top-0 left-0 right-0 z-50"
    >
      {/* Background layer with smooth scroll transitions */}
      <motion.div 
        className={`absolute inset-0 border-b transition-all duration-300 ease-out ${
          isScrolled 
            ? 'bg-[rgba(244,246,250,0.95)] backdrop-blur-md border-[rgba(226,232,240,0.8)] shadow-[0_4px_20px_rgba(17,24,39,0.08)]' 
            : 'bg-transparent border-transparent'
        }`}
      />
      
      <motion.nav 
        className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"
        style={{ height: navHeight, transition: "height 0.15s ease-out" }}
      >
        <div className="flex h-full items-center justify-between">
          {/* Logo with spring animation */}
          <motion.a 
            href="#"
            className="flex items-center"
            variants={itemVariants}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: "spring", stiffness: 500, damping: 15, delay: 0.2 }}
              className="relative h-12"
            >
              <Image
                src="/images/credwork-logo.png"
                alt="Credwork"
                width={210}
                height={48}
                className="h-12 object-contain"
                style={{ width: 'auto' }}
                priority
              />
            </motion.div>
          </motion.a>

          {/* Desktop Navigation with sliding pill */}
          <div className="hidden md:flex items-center gap-1 relative">
            {navLinks.map((link) => (
              <motion.a
                key={link.href}
                href={link.href}
                className="relative px-4 py-2 font-body text-[15px] font-medium text-[var(--cw-text-muted)] transition-colors hover:text-[var(--cw-primary)]"
                variants={itemVariants}
              >
                {/* Sliding pill background */}
                {activeSection === link.href && (
                  <motion.div
                    layoutId="navPill"
                    className="absolute inset-0 rounded-full bg-[var(--cw-secondary)]/10"
                    transition={{ type: "spring", stiffness: 400, damping: 30 }}
                  />
                )}
                <span className={`relative z-10 ${activeSection === link.href ? 'text-[var(--cw-secondary)]' : ''}`}>
                  {link.label}
                </span>
              </motion.a>
            ))}
          </div>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-4">
            <motion.a
              href="#employers"
              className="font-body text-[15px] font-medium text-[var(--cw-text-muted)] hover:text-[var(--cw-primary)] transition-colors"
              variants={itemVariants}
            >
              For Employers
            </motion.a>
            <motion.a
              href="/credwork.apk"
              download="credwork.apk"
              className="group relative flex items-center gap-2 rounded-full bg-[var(--cw-secondary)] px-5 py-2.5 font-display text-sm font-semibold text-white overflow-hidden shadow-[0_2px_8px_rgba(37,99,235,0.3)] hover:shadow-[0_4px_16px_rgba(37,99,235,0.4)] hover:bg-[#1d4ed8] transition-all duration-200"
              variants={ctaVariants}
              whileHover={{ y: -2, scale: 1.02 }}
              whileTap={{ scale: 0.96 }}
              transition={{ type: "spring", stiffness: 400, damping: 20 }}
            >
              <Smartphone className="h-4 w-4 relative z-10" />
              <span className="relative z-10">Download App</span>
            </motion.a>
          </div>

          {/* Mobile Menu Button - Morphing hamburger */}
          <motion.button
            className="md:hidden p-2 text-[var(--cw-primary)] relative w-10 h-10 flex items-center justify-center"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            whileTap={{ scale: 0.95 }}
            variants={itemVariants}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <motion.line
                x1="4" y1="6" x2="20" y2="6"
                animate={mobileMenuOpen ? { rotate: 45, y: 6, x1: 4, y1: 12, x2: 20, y2: 12 } : { rotate: 0, y: 0 }}
                transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
              />
              <motion.line
                x1="4" y1="12" x2="20" y2="12"
                animate={mobileMenuOpen ? { opacity: 0, x: 10 } : { opacity: 1, x: 0 }}
                transition={{ duration: 0.2 }}
              />
              <motion.line
                x1="4" y1="18" x2="20" y2="18"
                animate={mobileMenuOpen ? { rotate: -45, y: -6, x1: 4, y1: 12, x2: 20, y2: 12 } : { rotate: 0, y: 0 }}
                transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
              />
            </svg>
          </motion.button>
        </div>

        {/* Mobile Menu with clipPath wipe animation */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ clipPath: "circle(0% at calc(100% - 40px) 32px)" }}
              animate={{ clipPath: "circle(150% at calc(100% - 40px) 32px)" }}
              exit={{ clipPath: "circle(0% at calc(100% - 40px) 32px)" }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="md:hidden absolute top-full left-0 right-0 bg-[var(--cw-surface)] border-b border-[var(--cw-border)] shadow-lg"
            >
              <motion.div 
                className="flex flex-col p-4 gap-2"
                initial="hidden"
                animate="visible"
                variants={{
                  hidden: { opacity: 0 },
                  visible: { 
                    opacity: 1,
                    transition: { staggerChildren: 0.05, delayChildren: 0.1 }
                  }
                }}
              >
                {navLinks.map((link) => (
                  <motion.a
                    key={link.href}
                    href={link.href}
                    className={`font-body text-base font-medium py-3 px-4 rounded-xl transition-colors ${
                      activeSection === link.href 
                        ? 'bg-[var(--cw-secondary)]/10 text-[var(--cw-secondary)]' 
                        : 'text-[var(--cw-text-muted)] hover:text-[var(--cw-primary)] hover:bg-[var(--cw-surface-alt)]'
                    }`}
                    onClick={() => setMobileMenuOpen(false)}
                    variants={{
                      hidden: { opacity: 0, x: -20 },
                      visible: { opacity: 1, x: 0 }
                    }}
                  >
                    {link.label}
                  </motion.a>
                ))}
                <motion.a
                  href="#employers"
                  className="font-body text-base font-medium text-[var(--cw-text-muted)] hover:text-[var(--cw-primary)] hover:bg-[var(--cw-surface-alt)] py-3 px-4 rounded-xl transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                  variants={{
                    hidden: { opacity: 0, x: -20 },
                    visible: { opacity: 1, x: 0 }
                  }}
                >
                  For Employers
                </motion.a>
                <motion.a
                  href="/credwork.apk"
                  download="credwork.apk"
                  className="flex items-center justify-center gap-2 rounded-full bg-[var(--cw-secondary)] px-5 py-3 font-display text-sm font-semibold text-white mt-2"
                  onClick={() => setMobileMenuOpen(false)}
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >
                  <Smartphone className="h-4 w-4" />
                  Download App
                </motion.a>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.nav>
    </motion.header>
  )
}
