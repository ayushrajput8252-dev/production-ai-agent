import { Handshake, Landmark, Box } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

const industries = [
  {
    title: "Nonprofit",
    icon: Handshake,
    description: "Empowering nonprofits with intelligent tools for greater impact",
  },
  {
    title: "Government",
    icon: Landmark,
    description: "Modernizing government services with secure AI solutions",
  },
  {
    title: "Commercial",
    icon: Box,
    description: "Driving business growth with cutting-edge AI technology",
  },
]

export function IndustryCards() {
  return (
    <section className="bg-slate-50 px-4 py-20">
      <div className="mx-auto max-w-6xl">
        <div className="mb-12 text-center">
          <span className="mb-2 inline-block text-sm font-semibold uppercase tracking-wider text-blue-600">
            Industries We Serve
          </span>
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Solutions for Every Sector
          </h2>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {industries.map((industry) => (
            <Card
              key={industry.title}
              className="group cursor-pointer border-0 bg-white shadow-md transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
            >
              <CardContent className="flex flex-col items-center p-8 text-center">
                <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-slate-800 to-slate-900 transition-transform duration-300 group-hover:scale-110">
                  <industry.icon className="h-10 w-10 text-white" />
                </div>
                <h3 className="mb-2 text-xl font-bold text-slate-900">
                  {industry.title}
                </h3>
                <p className="text-sm text-slate-600">{industry.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
