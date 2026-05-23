import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-semibold tracking-tight transition-all duration-200 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/25 focus-visible:ring-offset-1 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50 relative overflow-hidden',
  {
    variants: {
      variant: {
        default:
          'bg-gradient-to-br from-[#0a9dc4] to-[#077f9f] text-white shadow-btn-primary hover:shadow-btn-primary-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0 after:absolute after:top-0 after:left-0 after:right-0 after:h-px after:bg-gradient-to-r after:from-transparent after:via-white/15 after:to-transparent',
        destructive:
          'bg-red-50/80 backdrop-blur-sm text-destructive border border-red-200/60 shadow-btn-glass hover:shadow-btn-glass-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0',
        outline:
          'bg-white/35 backdrop-blur-sm text-primary border border-white/50 shadow-btn-glass hover:bg-white/50 hover:shadow-btn-glass-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0 after:absolute after:top-0 after:left-0 after:right-0 after:h-px after:bg-gradient-to-r after:from-transparent after:via-white/15 after:to-transparent',
        secondary:
          'bg-background text-secondary-foreground shadow-btn-glass hover:text-primary hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0',
        ghost:
          'hover:bg-muted/50 hover:text-primary text-muted-foreground',
        success:
          'bg-gradient-to-br from-[#06a873] to-[#048a5e] text-white shadow-btn-primary hover:shadow-btn-primary-hover hover:-translate-y-0.5 active:shadow-neu-pressed active:translate-y-0 after:absolute after:top-0 after:left-0 after:right-0 after:h-px after:bg-gradient-to-r after:from-transparent after:via-white/15 after:to-transparent',
      },
      size: {
        default: 'h-10 px-5 py-2',
        sm: 'h-8 rounded-sm px-3 text-xs',
        lg: 'h-12 rounded-lg px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
  loading?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, loading, children, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={loading || props.disabled}
        {...props}
      >
        {loading ? (
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        ) : children}
      </button>
    )
  }
)
Button.displayName = 'Button'

export { Button, buttonVariants }
