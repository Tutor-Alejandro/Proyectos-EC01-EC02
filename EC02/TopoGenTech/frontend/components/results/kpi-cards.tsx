"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown, Target, Percent } from "lucide-react"

export function KPICards() {
  const kpis = [
    {
      title: "Área Total Palma",
      value: "12,458",
      unit: "ha",
      change: "+18.5%",
      trend: "up",
      icon: TrendingUp,
      color: "text-destructive",
    },
    {
      title: "Cambio en 4 Años",
      value: "2,341",
      unit: "ha",
      change: "+23.1%",
      trend: "up",
      icon: TrendingUp,
      color: "text-warning",
    },
    {
      title: "Precisión del Modelo",
      value: "94.2",
      unit: "%",
      change: "+2.1%",
      trend: "up",
      icon: Target,
      color: "text-primary",
    },
    {
      title: "F1-Score",
      value: "0.91",
      unit: "",
      change: "+0.05",
      trend: "up",
      icon: Percent,
      color: "text-primary",
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {kpis.map((kpi, index) => {
        const Icon = kpi.icon
        const TrendIcon = kpi.trend === "up" ? TrendingUp : TrendingDown
        return (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{kpi.title}</CardTitle>
              <Icon className={`h-4 w-4 ${kpi.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold font-[family-name:var(--font-poppins)]">
                {kpi.value}
                <span className="text-base font-normal text-muted-foreground ml-1">{kpi.unit}</span>
              </div>
              <p className="text-xs text-muted-foreground flex items-center mt-1">
                <TrendIcon className={`h-3 w-3 mr-1 ${kpi.trend === "up" ? "text-destructive" : "text-primary"}`} />
                {kpi.change} desde 2020
              </p>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
