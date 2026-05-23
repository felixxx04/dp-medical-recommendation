import * as React from 'react'
import { cn } from '@/lib/utils'

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  icon?: React.ReactNode
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, icon, ...props }, ref) => {
    const classes = cn(
      'flex h-10 w-full rounded-md border-0 bg-surface-inset px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/60 focus-visible:outline-none focus-visible:shadow-[inset_2px_2px_5px_var(--sh-d),inset_-1.5px_-1.5px_4px_var(--sh-l),0_0_0_2px_rgba(8,145,178,0.12)] shadow-neu-inset disabled:cursor-not-allowed disabled:opacity-40 transition-all duration-150',
      className
    )

    if (icon) {
      return (
        <div className="relative">
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">{icon}</div>
          <input type={type} className={cn(classes, 'pl-10')} ref={ref} {...props} />
        </div>
      )
    }

    return <input type={type} className={classes} ref={ref} {...props} />
  }
)
Input.displayName = 'Input'

export { Input }
