"use client"

import { useState } from "react"
import {
  Cpu,
  Crown,
  Settings,
  Database,
  MessageSquare,
  ClipboardList,
  ChevronDown,
} from "lucide-react"
import { cn } from "@/lib/utils"

const products = [
  {
    id: "genque",
    name: "GENQUE",
    description: "Automatic Item Generator",
    icon: Cpu,
    color: "bg-blue-100 text-blue-600 border-blue-200",
    details:
      "Automate the creation of assessment items with our AI-powered generation engine. Save time and ensure consistency across your question bank.",
  },
  {
    id: "crown",
    name: "CROWN",
    description: "Credential Management System",
    icon: Crown,
    color: "bg-yellow-100 text-yellow-600 border-yellow-200",
    details:
      "Manage certifications, credentials, and professional licenses with a comprehensive tracking and verification system.",
  },
  {
    id: "merit",
    name: "MERIT",
    description: "Competency Model",
    icon: Settings,
    color: "bg-red-100 text-red-600 border-red-200",
    details:
      "Build and manage competency frameworks to align skills with organizational goals and track employee development.",
  },
  {
    id: "vault",
    name: "VAULT",
    description: "Item Bank",
    icon: Database,
    color: "bg-emerald-100 text-emerald-600 border-emerald-200",
    details:
      "Securely store and manage your assessment items with advanced search, tagging, and version control capabilities.",
  },
  {
    id: "wespeak",
    name: "WESPEAK",
    description: "Discussion Board",
    icon: MessageSquare,
    color: "bg-orange-100 text-orange-600 border-orange-200",
    details:
      "Foster collaboration and knowledge sharing with our intuitive discussion platform designed for teams.",
  },
  {
    id: "census",
    name: "CENSUS",
    description: "Survey Platform",
    icon: ClipboardList,
    color: "bg-purple-100 text-purple-600 border-purple-200",
    details:
      "Create, distribute, and analyze surveys with powerful reporting tools and real-time insights.",
  },
]

export function ProductsSection() {
  const [expandedId, setExpandedId] = useState<string | null>(null)

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id)
  }

  return (
    <section className="bg-white px-4 py-20">
      <div className="mx-auto max-w-6xl">
        {/* Section Header */}
        <div className="mb-12 text-center">
          <div className="mb-2 flex items-center justify-center gap-1">
            <span className="h-3 w-1 rounded-full bg-slate-800" />
            <span className="h-5 w-1 rounded-full bg-emerald-500" />
            <span className="h-3 w-1 rounded-full bg-slate-800" />
          </div>
          <span className="mb-2 inline-block text-sm font-semibold uppercase tracking-wider text-blue-600">
            Our Products
          </span>
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Empowering Innovation Through
            <span className="block">Software Excellence</span>
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-slate-600">
            We leverage the industry&apos;s best practices to deliver robust and
            scalable software products. Our turnkey solutions help minimize
            operational costs, reduce risk, &amp; increase business efficiency.
          </p>
        </div>

        {/* Products Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {products.map((product) => (
            <div
              key={product.id}
              className="group cursor-pointer overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-all duration-300 hover:shadow-md"
              onClick={() => toggleExpand(product.id)}
            >
              <div className="flex items-center gap-4 p-4">
                <div
                  className={cn(
                    "flex h-14 w-14 shrink-0 items-center justify-center rounded-full border-2",
                    product.color
                  )}
                >
                  <product.icon className="h-7 w-7" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-slate-900">{product.name}</h3>
                  <p className="text-sm text-slate-600">{product.description}</p>
                </div>
                <ChevronDown
                  className={cn(
                    "h-5 w-5 shrink-0 text-slate-400 transition-transform duration-200",
                    expandedId === product.id && "rotate-180"
                  )}
                />
              </div>
              <div
                className={cn(
                  "overflow-hidden border-t border-slate-100 bg-slate-50 transition-all duration-300",
                  expandedId === product.id
                    ? "max-h-40 opacity-100"
                    : "max-h-0 opacity-0"
                )}
              >
                <p className="p-4 text-sm text-slate-600">{product.details}</p>
              </div>
              {/* Left accent border */}
              <div
                className={cn(
                  "absolute left-0 top-0 h-full w-1 transition-all duration-300",
                  expandedId === product.id ? "bg-emerald-500" : "bg-transparent"
                )}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
