"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

const data = [
  { name: "Bosque", area: 45230, color: "#2E7D32" },
  { name: "Palma", area: 12458, color: "#C62828" },
  { name: "Urbano", area: 8920, color: "#546E7A" },
  { name: "Vegetación", area: 18450, color: "#A5D6A7" },
  { name: "Suelo", area: 6340, color: "#8D6E63" },
  { name: "Agua", area: 3210, color: "#0277BD" },
]

export function CoverageChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Cobertura por Tipo de Uso de Suelo</CardTitle>
        <CardDescription>Área detectada en hectáreas (2024)</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="name" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
            <Bar dataKey="area" fill="#2E7D32" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
