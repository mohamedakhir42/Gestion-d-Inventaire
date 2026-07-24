import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
import { AlertCircle, Info, CheckCircle, AlertTriangle } from "lucide-react"

const alertVariants = cva(
  "relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-current",
  {
    variants: {
      variant: {
        default: "bg-blue-50 text-blue-900 border-blue-200 [&>svg]:text-blue-600",
        destructive: "bg-red-50 text-red-900 border-red-200 [&>svg]:text-red-600",
        warning: "bg-yellow-50 text-yellow-900 border-yellow-200 [&>svg]:text-yellow-600",
        success: "bg-green-50 text-green-900 border-green-200 [&>svg]:text-green-600",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof alertVariants> {}

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(({ className, variant, ...props }, ref) => (
  <div ref={ref} role="alert" className={cn(alertVariants({ variant }), className)} {...props} />
))
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h5 ref={ref} className={cn("mb-1 font-medium leading-tight", className)} {...props} />
  )
)
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("text-sm [&_p]:leading-relaxed", className)} {...props} />
  )
)
AlertDescription.displayName = "AlertDescription"

interface AlertMessageProps {
  variant?: "default" | "destructive" | "warning" | "success"
  title?: string
  message: string
  icon?: React.ReactNode
}

const AlertMessage: React.FC<AlertMessageProps> = ({ variant = "default", title, message, icon }) => {
  const getIcon = () => {
    if (icon) return icon
    switch (variant) {
      case "destructive":
        return <AlertCircle className="h-4 w-4" />
      case "warning":
        return <AlertTriangle className="h-4 w-4" />
      case "success":
        return <CheckCircle className="h-4 w-4" />
      default:
        return <Info className="h-4 w-4" />
    }
  }

  return (
    <Alert variant={variant}>
      {getIcon()}
      {title && <AlertTitle>{title}</AlertTitle>}
      <AlertDescription>{message}</AlertDescription>
    </Alert>
  )
}

export { Alert, AlertTitle, AlertDescription, AlertMessage }
