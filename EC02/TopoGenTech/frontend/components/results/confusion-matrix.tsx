"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const matrixData = [
  { actual: "Bosque", bosque: 892, palma: 12, urbano: 8, otros: 15 },
  { actual: "Palma", bosque: 18, palma: 856, urbano: 5, otros: 21 },
  { actual: "Urbano", bosque: 6, palma: 9, urbano: 912, otros: 13 },
  { actual: "Otros", bosque: 24, palma: 16, urbano: 11, otros: 849 },
]

export function ConfusionMatrix() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Matriz de Confusión</CardTitle>
        <CardDescription>Precisión del modelo de clasificación</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-24">Real / Pred</TableHead>
                <TableHead className="text-center">Bosque</TableHead>
                <TableHead className="text-center">Palma</TableHead>
                <TableHead className="text-center">Urbano</TableHead>
                <TableHead className="text-center">Otros</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {matrixData.map((row, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{row.actual}</TableCell>
                  <TableCell className="text-center bg-primary/10 font-semibold">{row.bosque}</TableCell>
                  <TableCell className="text-center">{row.palma}</TableCell>
                  <TableCell className="text-center">{row.urbano}</TableCell>
                  <TableCell className="text-center">{row.otros}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <div className="mt-4 space-y-1 text-xs text-muted-foreground">
          <p>
            <strong>Precisión Global:</strong> 94.2%
          </p>
          <p>
            <strong>Kappa:</strong> 0.89
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
