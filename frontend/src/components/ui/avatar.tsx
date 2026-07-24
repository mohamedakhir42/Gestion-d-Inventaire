import * as React from "react"
import * as AvatarPrimitive from "@radix-ui/react-avatar"
import { cn } from "@/lib/utils"
import { getInitials } from "@/lib/utils"

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root> & {
    name?: string
    size?: "sm" | "md" | "lg"
  }
>(({ className, name, size = "md", ...props }, ref) => {
  const sizeClass = {
    sm: "h-8 w-8 text-xs",
    md: "h-10 w-10 text-sm",
    lg: "h-12 w-12 text-base",
  }[size]

  return (
    <AvatarPrimitive.Root
      ref={ref}
      className={cn("relative inline-flex items-center justify-center overflow-hidden rounded-full bg-primary/10", sizeClass, className)}
      {...props}
    />
  )
})
Avatar.displayName = AvatarPrimitive.Root.displayName

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ ...props }, ref) => <AvatarPrimitive.Image ref={ref} className="h-full w-full object-cover" {...props} />)
AvatarImage.displayName = AvatarPrimitive.Image.displayName

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback> & {
    name?: string
  }
>(({ className, name, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn("flex items-center justify-center bg-primary/10 text-foreground font-semibold", className)}
    {...props}
  >
    {name ? getInitials(name) : "?"}
  </AvatarPrimitive.Fallback>
))
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName

export { Avatar, AvatarImage, AvatarFallback }
