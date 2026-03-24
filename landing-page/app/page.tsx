import { Navbar } from "@/components/sections/Navbar"
import { HeroSection } from "@/components/sections/HeroSection"
import { PhoneShowcaseSection } from "@/components/sections/PhoneShowcaseSection"
import { HowItWorksSection } from "@/components/sections/HowItWorksSection"
import { GigScoreSection } from "@/components/sections/GigScoreSection"
import { TestimonialsSection } from "@/components/sections/TestimonialsSection"
import { CtaSection } from "@/components/sections/CtaSection"
import { Footer } from "@/components/sections/Footer"

export default function Home() {
  return (
    <main>
      <Navbar />
      <HeroSection />
      <PhoneShowcaseSection />
      <HowItWorksSection />
      <GigScoreSection />
      <TestimonialsSection />
      <CtaSection />
      <Footer />
    </main>
  )
}
