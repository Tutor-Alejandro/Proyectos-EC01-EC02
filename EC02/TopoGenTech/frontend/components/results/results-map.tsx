"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { MapPin } from "lucide-react"

export function ResultsMap() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Mapa de Detección de Cambios</CardTitle>
        <CardDescription>Zonas con cambios significativos resaltadas en rojo</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="w-full h-[400px] rounded-lg border-2 border-dashed border-border bg-muted/50 flex items-center justify-center">
          <div className="text-center space-y-2 text-muted-foreground">
            <MapPin className="w-12 h-12 mx-auto" />
            <p className="text-sm">Mapa de Resultados</p>
            <p className="text-xs">Visualización de áreas con cambios detectados</p>
            <div className="flex gap-4 justify-center mt-4 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-[#2E7D32]" />
                <span>Sin cambio</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-[#FDD835]" />
                <span>Cambio menor</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-[#C62828]" />
                <span>Cambio severo</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
