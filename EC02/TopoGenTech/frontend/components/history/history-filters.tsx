"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, X } from "lucide-react"

interface HistoryFiltersProps {
  filters: {
    region: string
    dateRange: string
    analysisType: string
  }
  setFilters: (filters: any) => void
}

export function HistoryFilters({ filters, setFilters }: HistoryFiltersProps) {
  const handleReset = () => {
    setFilters({
      region: "all",
      dateRange: "all",
      analysisType: "all",
    })
  }

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="grid gap-4 md:grid-cols-4">
          <div className="space-y-2">
            <Label htmlFor="region-filter">Región</Label>
            <Select value={filters.region} onValueChange={(value) => setFilters({ ...filters, region: value })}>
              <SelectTrigger id="region-filter">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todas las regiones</SelectItem>
                <SelectItem value="norte">Ecuador Norte</SelectItem>
                <SelectItem value="centro">Ecuador Central</SelectItem>
                <SelectItem value="sur">Ecuador Sur</SelectItem>
                <SelectItem value="amazonia">Amazonía</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="date-filter">Período</Label>
            <Select value={filters.dateRange} onValueChange={(value) => setFilters({ ...filters, dateRange: value })}>
              <SelectTrigger id="date-filter">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todo el tiempo</SelectItem>
                <SelectItem value="week">Última semana</SelectItem>
                <SelectItem value="month">Último mes</SelectItem>
                <SelectItem value="quarter">Último trimestre</SelectItem>
                <SelectItem value="year">Último año</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="type-filter">Tipo de Análisis</Label>
            <Select
              value={filters.analysisType}
              onValueChange={(value) => setFilters({ ...filters, analysisType: value })}
            >
              <SelectTrigger id="type-filter">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos los tipos</SelectItem>
                <SelectItem value="classification">Clasificación</SelectItem>
                <SelectItem value="change">Detección de Cambios</SelectItem>
                <SelectItem value="metrics">Métricas</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="search">Buscar</Label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input id="search" placeholder="Buscar..." className="pl-8" />
              </div>
              <Button variant="outline" size="icon" onClick={handleReset} title="Limpiar filtros">
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
