// Framer Motion animation variants for Credwork landing page

export const fadeUp = {
  hidden: { opacity: 0, y: 48, filter: 'blur(8px)' },
  visible: { 
    opacity: 1, 
    y: 0, 
    filter: 'blur(0px)',
    transition: { duration: 0.65, ease: [0.16, 1, 0.3, 1] } 
  }
}

export const fadeLeft = {
  hidden: { opacity: 0, x: -60 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] } 
  }
}

export const fadeRight = {
  hidden: { opacity: 0, x: 60 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] } 
  }
}

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.86 },
  visible: { 
    opacity: 1, 
    scale: 1.0,
    transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] } 
  }
}

export const stagger = (delay = 0, staggerChildren = 0.09) => ({
  hidden: {},
  visible: { 
    transition: { staggerChildren, delayChildren: delay } 
  }
})

export const phoneScreenTransition = {
  initial: { opacity: 0, x: 30, scale: 0.96 },
  animate: { 
    opacity: 1, 
    x: 0, 
    scale: 1.0,
    transition: { duration: 0.45, ease: [0.16, 1, 0.3, 1] } 
  },
  exit: { 
    opacity: 0, 
    x: -30, 
    scale: 0.96,
    transition: { duration: 0.3, ease: 'easeIn' } 
  }
}

export const stepContentTransition = {
  initial: { opacity: 0, y: 48, filter: 'blur(6px)' },
  animate: { 
    opacity: 1, 
    y: 0, 
    filter: 'blur(0px)',
    transition: { duration: 0.55, ease: [0.16, 1, 0.3, 1] } 
  },
  exit: { 
    opacity: 0, 
    y: -32, 
    filter: 'blur(6px)',
    transition: { duration: 0.3, ease: 'easeIn' } 
  }
}

export const navbarVariants = {
  hidden: { opacity: 0, y: -16 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] }
  }
}

export const wordAnimation = {
  hidden: { opacity: 0, y: 20, filter: 'blur(4px)' },
  visible: { 
    opacity: 1, 
    y: 0, 
    filter: 'blur(0px)',
    transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }
  }
}

export const cardFloat = {
  hidden: { opacity: 0, x: 40 },
  visible: (delay: number) => ({
    opacity: 1,
    x: 0,
    transition: { duration: 0.6, delay, ease: [0.16, 1, 0.3, 1] }
  })
}
