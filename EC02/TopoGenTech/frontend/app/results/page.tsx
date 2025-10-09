"use client"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { AppHeader } from "@/components/app-header"
import { KPICards } from "@/components/results/kpi-cards"
import { CoverageChart } from "@/components/results/coverage-chart"
import { ChangeChart } from "@/components/results/change-chart"
import { ConfusionMatrix } from "@/components/results/confusion-matrix"
import { ResultsMap } from "@/components/results/results-map"
import { Button } from "@/components/ui/button"
import { Download, Share2 } from "lucide-react"

export default function ResultsPage() {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <div className="flex flex-1 flex-col">
          <AppHeader />
          <main className="flex-1 overflow-auto">
            <div className="container mx-auto px-4 py-6 space-y-6">
              {/* Header */}
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-3xl font-bold font-[family-name:var(--font-poppins)]">Resultados del Análisis</h1>
                  <p className="text-muted-foreground mt-1">Región: Ecuador Central | Período: 2020-2024</p>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline">
                    <Share2 className="mr-2 h-4 w-4" />
                    Compartir
                  </Button>
                  <Button>
                    <Download className="mr-2 h-4 w-4" />
                    Descargar PDF
                  </Button>
                </div>
              </div>

              {/* KPI Cards */}
              <KPICards />

              {/* Charts Grid */}
              <div className="grid gap-6 lg:grid-cols-2">
                <CoverageChart />
                <ChangeChart />
              </div>

              {/* Map and Matrix */}
              <div className="grid gap-6 lg:grid-cols-3">
                <div className="lg:col-span-2">
                  <ResultsMap />
                </div>
                <div>
                  <ConfusionMatrix />
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}
