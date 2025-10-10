"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts"

const data = [
  { name: "Bosque", value: 48.2, color: "#2E7D32" },
  { name: "Palma Aceitera", value: 13.3, color: "#C62828" },
  { name: "Urbano", value: 9.5, color: "#546E7A" },
  { name: "Vegetación", value: 19.6, color: "#A5D6A7" },
  { name: "Otros", value: 9.4, color: "#8D6E63" },
]

export function ChangeChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Proporción de Cobertura Terrestre</CardTitle>
        <CardDescription>Distribución porcentual del área analizada</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
