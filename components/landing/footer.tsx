import { Sparkles } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-slate-900 px-4 py-12 text-slate-400">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-emerald-500">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            <span className="font-bold text-white">OpenAI Agent</span>
          </div>

          {/* Links */}
          <nav className="flex flex-wrap items-center justify-center gap-6 text-sm">
            <a href="#" className="transition-colors hover:text-white">
              Home
            </a>
            <a href="#" className="transition-colors hover:text-white">
              About Us
            </a>
            <a href="#" className="transition-colors hover:text-white">
              Products
            </a>
            <a href="#" className="transition-colors hover:text-white">
              Services
            </a>
            <a href="#" className="transition-colors hover:text-white">
              Careers
            </a>
            <a href="#" className="transition-colors hover:text-white">
              Contact
            </a>
          </nav>

          {/* Copyright */}
          <p className="text-sm">
            © {new Date().getFullYear()} OpenAI Agent. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
