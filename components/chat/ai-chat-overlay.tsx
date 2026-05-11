"use client"

import { useState, useRef, useEffect } from "react"
import { X, Send, Bot, Sparkles, Database, Truck, HelpCircle, ClipboardList, MessageSquare, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
}

interface AiChatOverlayProps {
  isOpen: boolean
  onClose: () => void
}

// API Configuration - Change this to your backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8003"

export function AiChatOverlay({ isOpen, onClose }: AiChatOverlayProps) {
  const [activeAgent, setActiveAgent] = useState<"rag" | "tool">("rag")
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: "Hello! I'm your AI assistant. How can I help you today?",
      role: "assistant",
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [showToolFeatures, setShowToolFeatures] = useState(true)
  const [apiError, setApiError] = useState<string | null>(null)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const toolFeatures = [
    { id: "feedback", label: "Feedback", icon: MessageSquare },
    { id: "query", label: "Query", icon: HelpCircle },
    { id: "career", label: "Career", icon: Truck },
    { id: "assign-task", label: "Assign Task", icon: ClipboardList },
  ]

  const isDarkMode = activeAgent === "tool"

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [messages])

  // Fetch response from backend API
  const fetchAgentResponse = async (query: string): Promise<string> => {
    try {
      setApiError(null)
      const endpoint = activeAgent === "rag" ? "/api/rag-agent" : "/api/tool-agent"
      const fullUrl = `${API_BASE_URL}${endpoint}`
      
      console.log('Making API call to:', fullUrl)
      console.log('Active agent:', activeAgent)
      console.log('Query:', query)
      
      const response = await fetch(fullUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          session_id: "default",
          context: undefined,
        }),
      })

      if (!response.ok) {
        console.error('API response not ok:', response.status, response.statusText)
        throw new Error(`API error: ${response.status}`)
      }

      const data = await response.json()
      console.log('API response data:', data)
      
      if (data.success) {
        return data.result
      } else {
        console.error('API returned error:', data.error)
        throw new Error(data.error || "Agent error")
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to connect to backend"
      console.error('API call failed:', error)
      setApiError(errorMessage)
      return `Error: ${errorMessage}. Please ensure the backend server is running at ${API_BASE_URL}`
    }
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsTyping(true)
    setShowToolFeatures(false)

    try {
      const aiResponse = await fetchAgentResponse(inputValue)
      
      console.log('AI Response received:', aiResponse)
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        role: "assistant",
        timestamp: new Date(),
      }
      console.log('AI Message created:', aiMessage)
      setMessages((prev) => {
        console.log('Messages updated:', [...prev, aiMessage])
        return [...prev, aiMessage]
      })
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error"
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Error: ${errorMessage}`,
        role: "assistant",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  if (!isOpen) return null

  return (
    <div
      className={cn(
        "fixed inset-0 z-50 flex items-center justify-center transition-all duration-300",
        isDarkMode ? "bg-slate-950" : "bg-white"
      )}
    >
      {/* Close Button */}
      <Button
        variant="ghost"
        size="icon"
        onClick={onClose}
        className={cn(
          "absolute right-4 top-4 rounded-full transition-colors",
          isDarkMode
            ? "text-slate-400 hover:bg-slate-800 hover:text-white"
            : "text-slate-500 hover:bg-slate-100 hover:text-slate-900"
        )}
      >
        <X className="h-6 w-6" />
      </Button>

      {/* Chat Container */}
      <div className="flex h-full w-full max-w-4xl flex-col px-4 py-16">
        {/* Header */}
        <div className="mb-6 text-center">
          <div className="mb-4 flex items-center justify-center gap-2">
            <Bot
              className={cn(
                "h-8 w-8",
                isDarkMode ? "text-emerald-400" : "text-blue-600"
              )}
            />
            <h1
              className={cn(
                "text-2xl font-bold tracking-tight",
                isDarkMode ? "text-white" : "text-slate-900"
              )}
            >
              OpenEyes
            </h1>
          </div>

          {/* Agent Toggle Buttons */}
          <div className="flex items-center justify-center gap-3">
            <Button
              onClick={() => {
                setActiveAgent("rag")
                setShowToolFeatures(true)
              }}
              variant={activeAgent === "rag" ? "default" : "outline"}
              className={cn(
                "gap-2 rounded-full px-6 transition-all duration-300",
                activeAgent === "rag"
                  ? "bg-blue-600 text-white hover:bg-blue-700"
                  : isDarkMode
                    ? "border-slate-700 bg-transparent text-slate-400 hover:bg-slate-800 hover:text-white"
                    : "border-slate-300 bg-transparent text-slate-600 hover:bg-slate-100"
              )}
            >
              <Database className="h-4 w-4" />
              RAG Agent
            </Button>
            <Button
              onClick={() => {
                setActiveAgent("tool")
                setShowToolFeatures(true)
              }}
              variant={activeAgent === "tool" ? "default" : "outline"}
              className={cn(
                "gap-2 rounded-full px-6 transition-all duration-300",
                activeAgent === "tool"
                  ? "bg-emerald-500 text-white hover:bg-emerald-600"
                  : isDarkMode
                    ? "border-slate-700 bg-transparent text-slate-400 hover:bg-slate-800 hover:text-white"
                    : "border-slate-300 bg-transparent text-slate-600 hover:bg-slate-100"
              )}
            >
              <Sparkles className="h-4 w-4" />
              Tool Agent
            </Button>
          </div>
        </div>

        {/* API Error Banner */}
        {apiError && (
          <div className={cn(
            "mb-4 flex items-center gap-2 rounded-lg p-3",
            isDarkMode ? "bg-red-900/30 text-red-200" : "bg-red-50 text-red-700"
          )}>
            <AlertCircle className="h-4 w-4 flex-shrink-0" />
            <span className="text-sm">{apiError}</span>
          </div>
        )}

        {/* Messages Area */}
        <ScrollArea
          className={cn(
            "flex-1 rounded-2xl border p-4 transition-colors duration-300 overflow-hidden",
            isDarkMode
              ? "border-slate-800 bg-slate-900/50"
              : "border-slate-200 bg-slate-50/50"
          )}
          style={{ height: 'calc(100vh - 200px)' }}
        >
          <div ref={scrollAreaRef} className="space-y-4 overflow-y-auto max-h-full">
            {messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  "flex",
                  message.role === "user" ? "justify-end" : "justify-start"
                )}
              >
                <div
                  className={cn(
                    "max-w-[80%] rounded-2xl px-4 py-3 transition-colors duration-300",
                    message.role === "user"
                      ? isDarkMode
                        ? "bg-emerald-600 text-white"
                        : "bg-blue-600 text-white"
                      : isDarkMode
                        ? "bg-slate-800 text-slate-100"
                        : "bg-white text-slate-800 shadow-sm"
                  )}
                >
                  <p className="text-sm leading-relaxed">{message.content}</p>
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <div
                  className={cn(
                    "rounded-2xl px-4 py-3",
                    isDarkMode ? "bg-slate-800" : "bg-white shadow-sm"
                  )}
                >
                  <div className="flex items-center gap-1">
                    <span
                      className={cn(
                        "h-2 w-2 animate-bounce rounded-full",
                        isDarkMode ? "bg-emerald-400" : "bg-blue-600"
                      )}
                      style={{ animationDelay: "0ms" }}
                    />
                    <span
                      className={cn(
                        "h-2 w-2 animate-bounce rounded-full",
                        isDarkMode ? "bg-emerald-400" : "bg-blue-600"
                      )}
                      style={{ animationDelay: "150ms" }}
                    />
                    <span
                      className={cn(
                        "h-2 w-2 animate-bounce rounded-full",
                        isDarkMode ? "bg-emerald-400" : "bg-blue-600"
                      )}
                      style={{ animationDelay: "300ms" }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Tool Agent Feature Labels */}
            {activeAgent === "tool" && showToolFeatures && (
              <div className="mt-8 flex flex-col items-center justify-center gap-6">
                <p className={cn("text-base", isDarkMode ? "text-slate-300" : "text-slate-600")}>
                  Ask me anything, the agent will help you with:
                </p>
                <div className="flex flex-wrap items-center justify-center gap-3">
                  {toolFeatures.map((feature) => {
                    const IconComponent = feature.icon
                    return (
                      <div
                        key={feature.id}
                        className={cn(
                          "flex items-center gap-2 rounded-full border px-4 py-2",
                          isDarkMode
                            ? "border-slate-700 bg-slate-800/50"
                            : "border-slate-300 bg-slate-100/50"
                        )}
                      >
                        <IconComponent className={cn(
                          "h-4 w-4",
                          isDarkMode ? "text-emerald-400" : "text-blue-600"
                        )} />
                        <span className={cn(
                          "text-sm font-medium",
                          isDarkMode ? "text-slate-300" : "text-slate-700"
                        )}>
                          {feature.label}
                        </span>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="mt-4">
          <div
            className={cn(
              "flex items-center gap-2 rounded-2xl border p-2 transition-colors duration-300",
              isDarkMode
                ? "border-slate-700 bg-slate-900"
                : "border-slate-200 bg-white shadow-sm"
            )}
          >
            <Input
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message..."
              disabled={isTyping}
              className={cn(
                "flex-1 border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0",
                isDarkMode
                  ? "text-white placeholder:text-slate-500"
                  : "text-slate-900 placeholder:text-slate-400"
              )}
            />
            <Button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping}
              size="icon"
              className={cn(
                "rounded-xl transition-colors",
                isDarkMode
                  ? "bg-emerald-500 text-white hover:bg-emerald-600 disabled:bg-slate-700"
                  : "bg-blue-600 text-white hover:bg-blue-700 disabled:bg-slate-200"
              )}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <p
            className={cn(
              "mt-2 text-center text-xs",
              isDarkMode ? "text-slate-500" : "text-slate-400"
            )}
          >
            {activeAgent === "rag"
              ? "RAG Agent: Retrieval-Augmented Generation for knowledge-based responses"
              : "Tool Agent: Execute tools and actions for complex tasks"}
          </p>
        </div>
      </div>
    </div>
  )
}
