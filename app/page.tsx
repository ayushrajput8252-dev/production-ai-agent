"use client"

import { useState } from "react"
import { HeroSection } from "@/components/landing/hero-section"
import { IndustryCards } from "@/components/landing/industry-cards"
import { ProductsSection } from "@/components/landing/products-section"
import { Footer } from "@/components/landing/footer"
import { FloatingAssistantButton } from "@/components/chat/floating-assistant-button"
import { AiChatOverlay } from "@/components/chat/ai-chat-overlay"

export default function Home() {
  const [isChatOpen, setIsChatOpen] = useState(false)

  return (
    <main className="min-h-screen bg-white">
      {/* Landing Page Sections */}
      <HeroSection />
      <IndustryCards />
      <ProductsSection />
      <Footer />

      {/* AI Chat Assistant */}
      <FloatingAssistantButton
        onClick={() => setIsChatOpen(true)}
        isOpen={isChatOpen}
      />
      <AiChatOverlay isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </main>
  )
}
