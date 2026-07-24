import { Bell, Search, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { useAuth } from "@/contexts/auth-context"

export function TopBar() {
  const { user } = useAuth()

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-white px-4 py-3 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between gap-4">
        {/* Search */}
        <div className="flex-1 max-w-md hidden sm:flex">
          <Input
            placeholder="Search products, SKU, warehouses..."
            icon={<Search className="h-4 w-4" />}
          />
        </div>

        {/* Right side */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <Button variant="ghost" size="md" className="relative">
            <Bell className="h-5 w-5" />
            <span className="absolute top-0 right-0 h-2 w-2 bg-error rounded-full" />
          </Button>

          {/* User menu */}
          <div className="flex items-center gap-3 border-l border-border pl-4">
            <div className="hidden sm:flex flex-col text-right">
              <p className="text-sm font-medium text-foreground">
                {user?.firstName} {user?.lastName}
              </p>
              <p className="text-xs text-muted capitalize">{user?.role}</p>
            </div>
            <button className="flex items-center gap-2 hover:bg-gray-100 rounded-lg p-1 transition-smooth">
              <Avatar size="sm" name={`${user?.firstName} ${user?.lastName}`}>
                <AvatarImage src={user?.avatar} />
                <AvatarFallback name={`${user?.firstName} ${user?.lastName}`} />
              </Avatar>
              <ChevronDown className="h-4 w-4 text-muted hidden sm:block" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
