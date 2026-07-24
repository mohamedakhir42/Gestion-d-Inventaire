import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: boolean
  icon?: React.ReactNode
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, icon, ...props }, ref) => (
    <div className="relative">
      {icon && <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted">{icon}</div>}
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-lg border border-border bg-white px-4 py-2 text-base placeholder:text-muted transition-smooth focus-ring",
          icon && "pl-10",
          error && "border-error focus:ring-error",
          className
        )}
        ref={ref}
        {...props}
      />
    </div>
  )
)
Input.displayName = "Input"

export { Input }
