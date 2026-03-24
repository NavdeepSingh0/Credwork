// Framer Motion animation variants for Credwork landing page
import type { Variants, Transition, TargetAndTransition } from 'framer-motion'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

export const fadeUp: Variants = {
  hidden: { opacity: 0, y: 48, filter: 'blur(8px)' },
  visible: { 
    opacity: 1, 
    y: 0, 
    filter: 'blur(0px)',
    transition: { duration: 0.65, ease } as Transition
  }
}

export const fadeLeft: Variants = {
  hidden: { opacity: 0, x: -60 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.7, ease } as Transition
  }
}

export const fadeRight: Variants = {
  hidden: { opacity: 0, x: 60 },
  visible: { 
    opacity: 1, 
    x: 0,
    transition: { duration: 0.7, ease } as Transition
  }
}

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.86 },
  visible: { 
    opacity: 1, 
    scale: 1.0,
    transition: { duration: 0.6, ease } as Transition
  }
}

export const stagger = (delay = 0, staggerChildren = 0.09): Variants => ({
  hidden: {},
  visible: { 
    transition: { staggerChildren, delayChildren: delay } as Transition
  }
})

export const phoneScreenTransition = {
  initial: { opacity: 0, x: 30, scale: 0.96 } as TargetAndTransition,
  animate: { 
    opacity: 1, 
    x: 0, 
    scale: 1.0,
    transition: { duration: 0.45, ease } as Transition
  } as TargetAndTransition,
  exit: { 
    opacity: 0, 
    x: -30, 
    scale: 0.96,
    transition: { duration: 0.3, ease: 'easeIn' } as Transition
  } as TargetAndTransition
}

export const stepContentTransition = {
  initial: { opacity: 0, y: 48, filter: 'blur(6px)' } as TargetAndTransition,
  animate: { 
    opacity: 1, 
    y: 0, 
    filter: 'blur(0px)',
    transition: { duration: 0.55, ease } as Transition
  } as TargetAndTransition,
  exit: { 
    opacity: 0, 
    y: -32, 
    filter: 'blur(6px)',
    transition: { duration: 0.3, ease: 'easeIn' } as Transition
  } as TargetAndTransition
}

export const navbarVariants: Variants = {
  hidden: { opacity: 0, y: -16 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.5, ease } as Transition
  }
}

export const wordAnimation: Variants = {
  hidden: { opacity: 0, y: 20, filter: 'blur(4px)' },
  visible: { 
    opacity: 1, 
    y: 0, 
    filter: 'blur(0px)',
    transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] } as Transition
  }
}

export const cardFloat: Variants = {
  hidden: { opacity: 0, x: 40 },
  visible: (delay: number) => ({
    opacity: 1,
    x: 0,
    transition: { duration: 0.6, delay, ease } as Transition
  })
}
