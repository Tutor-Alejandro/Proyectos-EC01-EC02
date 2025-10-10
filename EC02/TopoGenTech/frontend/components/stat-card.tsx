interface StatCardProps {
  value: string
  label: string
}

export function StatCard({ value, label }: StatCardProps) {
  return (
    <div className="space-y-2">
      <div className="text-4xl md:text-5xl font-bold text-primary font-[family-name:var(--font-poppins)]">{value}</div>
      <div className="text-sm font-medium text-muted-foreground">{label}</div>
    </div>
  )
}
