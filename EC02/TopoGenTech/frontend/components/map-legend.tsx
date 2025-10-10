"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface MapLegendProps {
  selectedLayer: "rgb" | "classification" | "change"
}

export function MapLegend({ selectedLayer }: MapLegendProps) {
  if (selectedLayer === "rgb") return null

  const legendItems =
    selectedLayer === "classification"
      ? [
          { color: "bg-[#2E7D32]", label: "Bosque" },
          { color: "bg-[#C62828]", label: "Palma Aceitera" },
          { color: "bg-[#546E7A]", label: "Urbano" },
          { color: "bg-[#A5D6A7]", label: "Vegetación" },
          { color: "bg-[#8D6E63]", label: "Suelo Desnudo" },
          { color: "bg-[#0277BD]", label: "Agua" },
        ]
      : [
          { color: "bg-[#2E7D32]", label: "Sin cambio" },
          { color: "bg-[#FDD835]", label: "Cambio menor" },
          { color: "bg-[#FF6F00]", label: "Cambio moderado" },
          { color: "bg-[#C62828]", label: "Cambio severo" },
        ]

  return (
    <div className="absolute bottom-4 right-4 w-64">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm font-semibold">Leyenda</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {legendItems.map((item, index) => (
            <div key={index} className="flex items-center gap-2">
              <div className={`w-4 h-4 rounded ${item.color} shrink-0`} />
              <span className="text-xs text-muted-foreground">{item.label}</span>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
