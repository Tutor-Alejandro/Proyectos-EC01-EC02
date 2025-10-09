"use client"

import * as React from "react"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { AppHeader } from "@/components/app-header"
import { MapView } from "@/components/map-view"
import { MapControls } from "@/components/map-controls"
import { MapLegend } from "@/components/map-legend"

export default function MapPage() {
  const [selectedLayer, setSelectedLayer] = React.useState<"rgb" | "classification" | "change">("rgb")
  const [dateRange, setDateRange] = React.useState({ start: "2020-01-01", end: "2024-12-31" })
  const [isDrawing, setIsDrawing] = React.useState(false)

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <div className="flex flex-1 flex-col">
          <AppHeader />
          <main className="flex-1 overflow-hidden relative">
            <div className="absolute inset-0 flex">
              {/* Map View */}
              <div className="flex-1 relative">
                <MapView selectedLayer={selectedLayer} dateRange={dateRange} isDrawing={isDrawing} />
                <MapLegend selectedLayer={selectedLayer} />
              </div>

              {/* Side Panel */}
              <MapControls
                selectedLayer={selectedLayer}
                setSelectedLayer={setSelectedLayer}
                dateRange={dateRange}
                setDateRange={setDateRange}
                isDrawing={isDrawing}
                setIsDrawing={setIsDrawing}
              />
            </div>
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}
