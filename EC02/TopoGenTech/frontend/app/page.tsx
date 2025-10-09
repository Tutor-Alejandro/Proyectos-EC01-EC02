import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Satellite, TrendingUp, MapPin, Database, Sparkles, Shield } from "lucide-react"
import Link from "next/link"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { AppHeader } from "@/components/app-header"

export default function HomePage() {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-gradient-to-br from-background via-background to-muted/30">
        <AppSidebar />
        <div className="flex flex-1 flex-col">
          <AppHeader />
          <main className="flex-1 overflow-auto">
            <div className="container mx-auto px-4 py-12 md:py-16">
              <div className="mx-auto max-w-6xl space-y-12">
                <div className="text-center space-y-6">
                  <div className="inline-flex items-center justify-center w-24 h-24 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 mb-6 shadow-lg shadow-primary/10">
                    <Satellite className="w-12 h-12 text-primary" />
                  </div>
                  <div className="space-y-4">
                    <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold font-[family-name:var(--font-poppins)] text-balance bg-gradient-to-br from-foreground to-foreground/70 bg-clip-text text-transparent leading-tight">
                      Detección de Palma Aceitera
                    </h1>
                    <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto text-pretty leading-relaxed">
                      Sistema avanzado de análisis geoespacial para monitorear cambios en el uso de suelo utilizando
                      datos de <span className="font-semibold text-primary">Alpha Earth</span>
                    </p>
                  </div>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
                    <Button asChild size="lg" className="text-base h-12 px-8 shadow-lg shadow-primary/20">
                      <Link href="/map">
                        <Sparkles className="w-4 h-4 mr-2" />
                        Iniciar Análisis
                      </Link>
                    </Button>
                    <Button
                      asChild
                      variant="outline"
                      size="lg"
                      className="text-base h-12 px-8 bg-card hover:bg-accent/50 border-2"
                    >
                      <Link href="/history">Ver Historial</Link>
                    </Button>
                  </div>
                </div>

                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 pt-8">
                  <Card className="border-2 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 group bg-card/50 backdrop-blur">
                    <CardContent className="pt-6 pb-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 group-hover:scale-110 transition-transform duration-300">
                          <MapPin className="w-7 h-7 text-primary" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="font-semibold text-xl font-[family-name:var(--font-poppins)]">
                            Mapas Interactivos
                          </h3>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            Visualiza imágenes Sentinel-2, dibuja áreas de interés y explora clasificaciones con
                            herramientas intuitivas
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-2 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 group bg-card/50 backdrop-blur">
                    <CardContent className="pt-6 pb-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 group-hover:scale-110 transition-transform duration-300">
                          <TrendingUp className="w-7 h-7 text-primary" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="font-semibold text-xl font-[family-name:var(--font-poppins)]">
                            Detección de Cambios
                          </h3>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            Analiza la evolución del uso de suelo entre 2020-2024 y detecta expansión de cultivos con
                            alta precisión
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-2 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 group bg-card/50 backdrop-blur">
                    <CardContent className="pt-6 pb-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 group-hover:scale-110 transition-transform duration-300">
                          <Database className="w-7 h-7 text-primary" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="font-semibold text-xl font-[family-name:var(--font-poppins)]">
                            Clasificación ML
                          </h3>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            Modelos de machine learning con embeddings para clasificar bosques, palma y otros usos de
                            suelo
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-2 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 group bg-card/50 backdrop-blur">
                    <CardContent className="pt-6 pb-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 group-hover:scale-110 transition-transform duration-300">
                          <Satellite className="w-7 h-7 text-primary" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="font-semibold text-xl font-[family-name:var(--font-poppins)]">
                            Datos Satelitales
                          </h3>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            Imágenes multiespectrales de Sentinel-2 procesadas con Alpha Earth para análisis de alta
                            calidad
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-2 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 group bg-card/50 backdrop-blur">
                    <CardContent className="pt-6 pb-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 group-hover:scale-110 transition-transform duration-300">
                          <Shield className="w-7 h-7 text-primary" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="font-semibold text-xl font-[family-name:var(--font-poppins)]">
                            Alta Precisión
                          </h3>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            Métricas de rendimiento detalladas con matrices de confusión y validación de resultados
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-2 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 group bg-card/50 backdrop-blur">
                    <CardContent className="pt-6 pb-6">
                      <div className="space-y-4">
                        <div className="flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 group-hover:scale-110 transition-transform duration-300">
                          <Sparkles className="w-7 h-7 text-primary" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="font-semibold text-xl font-[family-name:var(--font-poppins)]">
                            Reportes Exportables
                          </h3>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            Descarga resultados en múltiples formatos: PDF, CSV, GeoJSON para análisis posteriores
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                <Card className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent border-2 border-primary/20 shadow-xl shadow-primary/10">
                  <CardContent className="pt-8 pb-8">
                    <div className="grid gap-8 md:grid-cols-3 text-center">
                      <div className="space-y-2">
                        <div className="text-4xl md:text-5xl font-bold text-primary font-[family-name:var(--font-poppins)]">
                          2020-2024
                        </div>
                        <div className="text-sm font-medium text-muted-foreground">Período de Análisis</div>
                      </div>
                      <div className="space-y-2">
                        <div className="text-4xl md:text-5xl font-bold text-primary font-[family-name:var(--font-poppins)]">
                          Alpha Earth
                        </div>
                        <div className="text-sm font-medium text-muted-foreground">Fuente de Datos</div>
                      </div>
                      <div className="space-y-2">
                        <div className="text-4xl md:text-5xl font-bold text-primary font-[family-name:var(--font-poppins)]">
                          Ecuador
                        </div>
                        <div className="text-sm font-medium text-muted-foreground">Área de Estudio</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}
