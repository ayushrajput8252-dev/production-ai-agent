"use client"

import { MessageCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface FloatingAssistantButtonProps {
  onClick: () => void
  isOpen: boolean
}

export function FloatingAssistantButton({
  onClick,
  isOpen,
}: FloatingAssistantButtonProps) {
  if (isOpen) return null

  return (
    <Button
      onClick={onClick}
      size="icon"
      className={cn(
        "fixed bottom-6 right-6 z-40 h-14 w-14 rounded-full shadow-lg transition-all duration-300 hover:scale-110",
        "bg-gradient-to-br from-blue-600 to-blue-700 text-white hover:from-blue-500 hover:to-blue-600"
      )}
    >
      <MessageCircle className="h-6 w-6" />
      <span className="sr-only">Open AI Assistant</span>
      
      {/* Pulse animation ring */}
      <span className="absolute inset-0 -z-10 animate-ping rounded-full bg-blue-400 opacity-30" />
    </Button>
  )
}
