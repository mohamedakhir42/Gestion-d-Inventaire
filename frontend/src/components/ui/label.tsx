import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const labelVariants = cva("text-sm font-medium text-foreground", {
  variants: {
    required: {
      true: "after:content-['*'] after:ml-1 after:text-error",
    },
  },
})

export interface LabelProps extends React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>, VariantProps<typeof labelVariants> {}

const Label = React.forwardRef<React.ElementRef<typeof LabelPrimitive.Root>, LabelProps>(
  ({ className, required, ...props }, ref) => (
    <LabelPrimitive.Root
      ref={ref}
      className={cn(labelVariants({ required, className }))}
      {...props}
    />
  )
)
Label.displayName = LabelPrimitive.Root.displayName

export { Label }
