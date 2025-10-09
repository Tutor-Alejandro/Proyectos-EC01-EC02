"use client"

import * as React from "react"
import { Calendar, Layers, Play, Square, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"

interface MapControlsProps {
  selectedLayer: "rgb" | "classification" | "change"
  setSelectedLayer: (layer: "rgb" | "classification" | "change") => void
  dateRange: { start: string; end: string }
  setDateRange: (range: { start: string; end: string }) => void
  isDrawing: boolean
  setIsDrawing: (drawing: boolean) => void
}

export function MapControls({
  selectedLayer,
  setSelectedLayer,
  dateRange,
  setDateRange,
  isDrawing,
  setIsDrawing,
}: MapControlsProps) {
  const [analysisType, setAnalysisType] = React.useState<"classification" | "change" | "metrics">("classification")
  const [isAnalyzing, setIsAnalyzing] = React.useState(false)
  const [progress, setProgress] = React.useState(0)
  const [statusMessage, setStatusMessage] = React.useState("")

  const handleExecuteAnalysis = () => {
    setIsAnalyzing(true)
    setProgress(0)
    setStatusMessage("Iniciando análisis...")

    // Simulate analysis progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsAnalyzing(false)
          setStatusMessage("Análisis completado exitosamente")
          return 100
        }
        return prev + 10
      })
    }, 500)
  }

  return (
    <div className="w-96 border-l bg-card overflow-y-auto">
      <div className="p-6 space-y-6">
        {/* Drawing Tools */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Herramientas de Dibujo</CardTitle>
            <CardDescription>Dibuja un polígono o bounding box en el mapa</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex gap-2">
              <Button
                variant={isDrawing ? "default" : "outline"}
                className="flex-1"
                onClick={() => setIsDrawing(!isDrawing)}
              >
                {isDrawing ? (
                  <>
                    <Square className="mr-2 h-4 w-4" />
                    Detener
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Dibujar Área
                  </>
                )}
              </Button>
              <Button variant="outline" disabled={!isDrawing}>
                Limpiar
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Layer Selection */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Layers className="h-4 w-4" />
              Capas del Mapa
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <Label htmlFor="layer-select">Capa Activa</Label>
              <Select value={selectedLayer} onValueChange={(value: any) => setSelectedLayer(value)}>
                <SelectTrigger id="layer-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="rgb">RGB Sentinel-2</SelectItem>
                  <SelectItem value="classification">Clasificación de Cobertura</SelectItem>
                  <SelectItem value="change">Detección de Cambios</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Date Range */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Rango de Fechas
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <Label htmlFor="start-date">Fecha Inicio</Label>
              <Input
                id="start-date"
                type="date"
                value={dateRange.start}
                onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="end-date">Fecha Fin</Label>
              <Input
                id="end-date"
                type="date"
                value={dateRange.end}
                onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
              />
            </div>
          </CardContent>
        </Card>

        <Separator />

        {/* Analysis Configuration */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Configuración de Análisis</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <Label htmlFor="analysis-type">Tipo de Análisis</Label>
              <Select value={analysisType} onValueChange={(value: any) => setAnalysisType(value)}>
                <SelectTrigger id="analysis-type">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="classification">Clasificación de Uso de Suelo</SelectItem>
                  <SelectItem value="change">Detección de Cambios</SelectItem>
                  <SelectItem value="metrics">Métricas y Estadísticas</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Button className="w-full" size="lg" onClick={handleExecuteAnalysis} disabled={isAnalyzing}>
              {isAnalyzing ? "Analizando..." : "Ejecutar Análisis"}
            </Button>

            {isAnalyzing && (
              <div className="space-y-2">
                <Progress value={progress} className="w-full" />
                <p className="text-xs text-muted-foreground text-center">{progress}% completado</p>
              </div>
            )}

            {statusMessage && (
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription className="text-xs">{statusMessage}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card className="bg-muted/50">
          <CardContent className="pt-6">
            <div className="space-y-2 text-xs text-muted-foreground">
              <p>
                <strong>Instrucciones:</strong>
              </p>
              <ol className="list-decimal list-inside space-y-1 ml-2">
                <li>Dibuja un área de interés en el mapa</li>
                <li>Selecciona el rango de fechas</li>
                <li>Elige el tipo de análisis</li>
                <li>Ejecuta el análisis</li>
              </ol>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
