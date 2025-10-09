"use client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Download, Eye, MoreHorizontal } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import Link from "next/link"

interface AnalysisTableProps {
  filters: {
    region: string
    dateRange: string
    analysisType: string
  }
}

const analysisData = [
  {
    id: "AN-2024-127",
    date: "2024-10-09",
    region: "Ecuador Central",
    type: "Clasificación",
    area: "12,458 ha",
    palmArea: "2,341 ha",
    accuracy: "94.2%",
    status: "Completado",
  },
  {
    id: "AN-2024-126",
    date: "2024-10-08",
    region: "Ecuador Norte",
    type: "Detección de Cambios",
    area: "8,920 ha",
    palmArea: "1,856 ha",
    accuracy: "92.8%",
    status: "Completado",
  },
  {
    id: "AN-2024-125",
    date: "2024-10-07",
    region: "Amazonía",
    type: "Clasificación",
    area: "18,450 ha",
    palmArea: "3,124 ha",
    accuracy: "93.5%",
    status: "Completado",
  },
  {
    id: "AN-2024-124",
    date: "2024-10-06",
    region: "Ecuador Sur",
    type: "Métricas",
    area: "6,340 ha",
    palmArea: "892 ha",
    accuracy: "95.1%",
    status: "Completado",
  },
  {
    id: "AN-2024-123",
    date: "2024-10-05",
    region: "Ecuador Central",
    type: "Detección de Cambios",
    area: "15,230 ha",
    palmArea: "2,678 ha",
    accuracy: "91.9%",
    status: "Completado",
  },
  {
    id: "AN-2024-122",
    date: "2024-10-04",
    region: "Ecuador Norte",
    type: "Clasificación",
    area: "9,840 ha",
    palmArea: "1,456 ha",
    accuracy: "93.8%",
    status: "Completado",
  },
]

export function AnalysisTable({ filters }: AnalysisTableProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Análisis Realizados</CardTitle>
        <CardDescription>Lista completa de análisis con opciones de descarga</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Fecha</TableHead>
                <TableHead>Región</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead>Área Total</TableHead>
                <TableHead>Área Palma</TableHead>
                <TableHead>Precisión</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead className="text-right">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {analysisData.map((analysis) => (
                <TableRow key={analysis.id}>
                  <TableCell className="font-mono text-sm">{analysis.id}</TableCell>
                  <TableCell>{new Date(analysis.date).toLocaleDateString("es-ES")}</TableCell>
                  <TableCell>{analysis.region}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{analysis.type}</Badge>
                  </TableCell>
                  <TableCell>{analysis.area}</TableCell>
                  <TableCell className="font-semibold text-destructive">{analysis.palmArea}</TableCell>
                  <TableCell>
                    <span className="text-primary font-semibold">{analysis.accuracy}</span>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className="bg-primary/10 text-primary">
                      {analysis.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="ghost" size="icon" asChild>
                        <Link href="/results">
                          <Eye className="h-4 w-4" />
                          <span className="sr-only">Ver resultados</span>
                        </Link>
                      </Button>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon">
                            <MoreHorizontal className="h-4 w-4" />
                            <span className="sr-only">Más opciones</span>
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuLabel>Acciones</DropdownMenuLabel>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem>
                            <Download className="mr-2 h-4 w-4" />
                            Descargar PDF
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Download className="mr-2 h-4 w-4" />
                            Descargar CSV
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Download className="mr-2 h-4 w-4" />
                            Descargar GeoJSON
                          </DropdownMenuItem>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem>Duplicar análisis</DropdownMenuItem>
                          <DropdownMenuItem className="text-destructive">Eliminar</DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between mt-4">
          <p className="text-sm text-muted-foreground">Mostrando 6 de 127 análisis</p>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" disabled>
              Anterior
            </Button>
            <Button variant="outline" size="sm">
              Siguiente
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
