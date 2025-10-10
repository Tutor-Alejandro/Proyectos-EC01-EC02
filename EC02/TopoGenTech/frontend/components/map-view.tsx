"use client"

import * as React from "react"
import { ZoomIn, ZoomOut, Maximize2, Pencil } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

interface MapViewProps {
  selectedLayer: "rgb" | "classification" | "change"
  dateRange: { start: string; end: string }
  isDrawing: boolean
}

export function MapView({ selectedLayer, dateRange, isDrawing }: MapViewProps) {
  const [zoom, setZoom] = React.useState(8)
  const [center, setCenter] = React.useState({ lat: -1.8312, lng: -78.1834 }) // Ecuador center

  const handleZoomIn = () => setZoom((prev) => Math.min(prev + 1, 18))
  const handleZoomOut = () => setZoom((prev) => Math.max(prev - 1, 3))
  const handleReset = () => {
    setZoom(8)
    setCenter({ lat: -1.8312, lng: -78.1834 })
  }

  return (
    <div className="relative w-full h-full bg-muted">
      {/* Map Container - Placeholder for actual map implementation */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center space-y-4 p-8">
          <div className="w-full h-[600px] rounded-lg border-2 border-dashed border-border bg-card/50 flex items-center justify-center">
            <div className="space-y-2 text-muted-foreground">
              <Pencil className="w-12 h-12 mx-auto" />
              <p className="text-sm">Mapa Interactivo</p>
              <p className="text-xs">
                Capa:{" "}
                {selectedLayer === "rgb"
                  ? "RGB Sentinel-2"
                  : selectedLayer === "classification"
                    ? "Clasificación"
                    : "Detección de Cambios"}
              </p>
              <p className="text-xs">
                Período: {dateRange.start} - {dateRange.end}
              </p>
              <p className="text-xs">Zoom: {zoom}</p>
              {isDrawing && <p className="text-xs text-primary font-semibold">Modo dibujo activo</p>}
            </div>
          </div>
        </div>
      </div>

      {/* Map Controls */}
      <div className="absolute top-4 right-4 flex flex-col gap-2">
        <Card className="p-1">
          <div className="flex flex-col gap-1">
            <Button variant="ghost" size="icon" onClick={handleZoomIn} title="Acercar">
              <ZoomIn className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={handleZoomOut} title="Alejar">
              <ZoomOut className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={handleReset} title="Restablecer vista">
              <Maximize2 className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      </div>

      {/* Coordinates Display */}
      <div className="absolute bottom-4 left-4">
        <Card className="px-3 py-2">
          <p className="text-xs text-muted-foreground">
            Lat: {center.lat.toFixed(4)}, Lng: {center.lng.toFixed(4)}
          </p>
        </Card>
      </div>
    </div>
  )
}
