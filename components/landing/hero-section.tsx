import { Sparkles, Shield, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 px-4 py-20 sm:py-32">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -right-20 -top-20 h-96 w-96 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="absolute -bottom-20 -left-20 h-96 w-96 rounded-full bg-emerald-500/10 blur-3xl" />
        {/* Tech lines decoration */}
        <svg
          className="absolute inset-0 h-full w-full opacity-20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <pattern
              id="grid"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="currentColor"
                strokeWidth="0.5"
                className="text-blue-400"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="relative mx-auto max-w-6xl text-center">
        {/* Logo/Brand */}
        <div className="mb-8 flex items-center justify-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-emerald-500">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <span className="text-2xl font-bold text-white">OpenEyes</span>
        </div>

        <h1 className="mb-6 text-balance text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl">
          Custom AI Solutions
          <span className="mt-2 block bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            For Your Business
          </span>
        </h1>

        <p className="mx-auto mb-10 max-w-2xl text-balance text-lg text-slate-300">
          We deliver enterprise and technology modernization solutions to organizations.
          Our AI-powered tools help you design the best solutions using trusted content
          and intelligent technologies.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button
            size="lg"
            className="rounded-full bg-blue-600 px-8 text-white hover:bg-blue-500"
          >
            Get Started
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="rounded-full border-slate-600 bg-transparent px-8 text-white hover:bg-slate-800"
          >
            Learn More
          </Button>
        </div>

        {/* Feature Pills */}
        <div className="mt-16 flex flex-wrap items-center justify-center gap-4">
          <div className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800/50 px-4 py-2 text-sm text-slate-300">
            <Shield className="h-4 w-4 text-emerald-400" />
            Enterprise Security
          </div>
          <div className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800/50 px-4 py-2 text-sm text-slate-300">
            <Zap className="h-4 w-4 text-yellow-400" />
            Lightning Fast
          </div>
          <div className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800/50 px-4 py-2 text-sm text-slate-300">
            <Sparkles className="h-4 w-4 text-blue-400" />
            AI Powered
          </div>
        </div>
      </div>
    </section>
  )
}
