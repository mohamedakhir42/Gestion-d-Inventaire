import { cn } from "@/lib/utils"

interface LoaderProps {
  size?: "sm" | "md" | "lg"
  variant?: "default" | "primary" | "secondary"
  fullScreen?: boolean
}

export function Loader({ size = "md", variant = "default", fullScreen = false }: LoaderProps) {
  const sizeClass = {
    sm: "h-6 w-6",
    md: "h-10 w-10",
    lg: "h-16 w-16",
  }[size]

  const variantClass = {
    default: "border-gray-300 border-t-foreground",
    primary: "border-primary/20 border-t-primary",
    secondary: "border-secondary/20 border-t-secondary",
  }[variant]

  const spinnerContent = (
    <div className={cn("animate-spin rounded-full border-4 border-solid", sizeClass, variantClass)} />
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white/50 backdrop-blur-sm">
        {spinnerContent}
      </div>
    )
  }

  return <div className="flex justify-center">{spinnerContent}</div>
}

export function SkeletonLoader() {
  return (
    <div className="space-y-4">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="animate-pulse rounded-lg bg-gray-200 h-12" />
      ))}
    </div>
  )
}

export function PageLoader() {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-white z-50">
      <div className="text-center">
        <Loader size="lg" variant="primary" />
        <p className="mt-4 text-foreground font-medium">Loading...</p>
      </div>
    </div>
  )
}
