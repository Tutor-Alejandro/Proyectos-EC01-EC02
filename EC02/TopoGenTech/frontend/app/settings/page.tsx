"use client"

import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { AppHeader } from "@/components/app-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function SettingsPage() {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <div className="flex flex-1 flex-col">
          <AppHeader />
          <main className="flex-1 overflow-auto">
            <div className="container mx-auto px-4 py-6 space-y-6 max-w-4xl">
              <div>
                <h1 className="text-3xl font-bold font-[family-name:var(--font-poppins)]">Configuración</h1>
                <p className="text-muted-foreground mt-1">Administra las preferencias del sistema</p>
              </div>

              {/* User Settings */}
              <Card>
                <CardHeader>
                  <CardTitle>Perfil de Usuario</CardTitle>
                  <CardDescription>Información personal y credenciales</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="name">Nombre</Label>
                      <Input id="name" placeholder="Juan Pérez" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <Input id="email" type="email" placeholder="juan@ejemplo.com" />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="organization">Organización</Label>
                    <Input id="organization" placeholder="Universidad / Institución" />
                  </div>
                  <Button>Guardar Cambios</Button>
                </CardContent>
              </Card>

              {/* Analysis Settings */}
              <Card>
                <CardHeader>
                  <CardTitle>Configuración de Análisis</CardTitle>
                  <CardDescription>Parámetros predeterminados para nuevos análisis</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="default-region">Región Predeterminada</Label>
                    <Select defaultValue="centro">
                      <SelectTrigger id="default-region">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="norte">Ecuador Norte</SelectItem>
                        <SelectItem value="centro">Ecuador Central</SelectItem>
                        <SelectItem value="sur">Ecuador Sur</SelectItem>
                        <SelectItem value="amazonia">Amazonía</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="cloud-threshold">Umbral de Nubosidad (%)</Label>
                    <Input id="cloud-threshold" type="number" defaultValue="20" min="0" max="100" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Notificaciones de Análisis</Label>
                      <p className="text-sm text-muted-foreground">Recibir alertas cuando un análisis finalice</p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  <Button>Guardar Configuración</Button>
                </CardContent>
              </Card>

              {/* API Settings */}
              <Card>
                <CardHeader>
                  <CardTitle>Integración API</CardTitle>
                  <CardDescription>Configuración de Google Earth Engine y servicios externos</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="gee-project">Proyecto GEE</Label>
                    <Input id="gee-project" placeholder="mi-proyecto-gee" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Caché de Imágenes</Label>
                      <p className="text-sm text-muted-foreground">Almacenar imágenes localmente para acceso rápido</p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  <Separator />
                  <div className="space-y-2">
                    <Label>Estado de Conexión</Label>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-primary" />
                      <span className="text-sm text-muted-foreground">Conectado a Google Earth Engine</span>
                    </div>
                  </div>
                  <Button variant="outline">Reconectar</Button>
                </CardContent>
              </Card>

              {/* Export Settings */}
              <Card>
                <CardHeader>
                  <CardTitle>Exportación de Datos</CardTitle>
                  <CardDescription>Formato y opciones de descarga de reportes</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="export-format">Formato Predeterminado</Label>
                    <Select defaultValue="pdf">
                      <SelectTrigger id="export-format">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pdf">PDF</SelectItem>
                        <SelectItem value="csv">CSV</SelectItem>
                        <SelectItem value="geojson">GeoJSON</SelectItem>
                        <SelectItem value="shp">Shapefile</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Incluir Metadatos</Label>
                      <p className="text-sm text-muted-foreground">Agregar información técnica en exportaciones</p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  <Button>Guardar Preferencias</Button>
                </CardContent>
              </Card>
            </div>
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}
