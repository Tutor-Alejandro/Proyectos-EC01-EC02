"use client"

import * as React from "react"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { AppHeader } from "@/components/app-header"
import { AnalysisTable } from "@/components/history/analysis-table"
import { HistoryFilters } from "@/components/history/history-filters"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, TrendingUp, Clock } from "lucide-react"

export default function HistoryPage() {
  const [filters, setFilters] = React.useState({
    region: "all",
    dateRange: "all",
    analysisType: "all",
  })

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <div className="flex flex-1 flex-col">
          <AppHeader />
          <main className="flex-1 overflow-auto">
            <div className="container mx-auto px-4 py-6 space-y-6">
              {/* Header */}
              <div>
                <h1 className="text-3xl font-bold font-[family-name:var(--font-poppins)]">Historial de Análisis</h1>
                <p className="text-muted-foreground mt-1">Consulta y descarga reportes de análisis anteriores</p>
              </div>

              {/* Stats Cards */}
              <div className="grid gap-4 md:grid-cols-3">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Análisis</CardTitle>
                    <FileText className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold font-[family-name:var(--font-poppins)]">127</div>
                    <p className="text-xs text-muted-foreground">+12 este mes</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Área Total Analizada</CardTitle>
                    <TrendingUp className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold font-[family-name:var(--font-poppins)]">
                      94,608<span className="text-base font-normal text-muted-foreground ml-1">ha</span>
                    </div>
                    <p className="text-xs text-muted-foreground">Acumulado</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Último Análisis</CardTitle>
                    <Clock className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold font-[family-name:var(--font-poppins)]">Hoy</div>
                    <p className="text-xs text-muted-foreground">Hace 2 horas</p>
                  </CardContent>
                </Card>
              </div>

              {/* Filters */}
              <HistoryFilters filters={filters} setFilters={setFilters} />

              {/* Analysis Table */}
              <AnalysisTable filters={filters} />
            </div>
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}
