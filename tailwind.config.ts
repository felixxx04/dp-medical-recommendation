import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  prefix: '',
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'rgba(140,160,180,0.22)',
        input: 'rgba(155,175,200,0.22)',
        ring: 'rgba(8,145,178,0.25)',
        background: '#dde6f0',
        foreground: '#0a2f2f',
        primary: {
          DEFAULT: '#0891b2',
          foreground: '#ffffff',
          hover: '#0e7490',
          light: '#22d3ee',
        },
        secondary: {
          DEFAULT: '#3d5f73',
          foreground: '#0a2f2f',
        },
        destructive: {
          DEFAULT: '#b91c1c',
          foreground: '#ffffff',
        },
        warning: {
          DEFAULT: '#b45309',
          foreground: '#ffffff',
        },
        success: {
          DEFAULT: '#059669',
          foreground: '#ffffff',
        },
        info: {
          DEFAULT: '#0369a1',
          foreground: '#ffffff',
        },
        muted: {
          DEFAULT: '#d2deea',
          foreground: '#5e7f92',
        },
        accent: {
          DEFAULT: '#14b8a6',
          foreground: '#ffffff',
        },
        popover: {
          DEFAULT: '#edf3fa',
          foreground: '#0a2f2f',
        },
        card: {
          DEFAULT: '#e8eff7',
          foreground: '#0a2f2f',
        },
        surface: {
          base: '#dde6f0',
          DEFAULT: '#dde6f0',
          elevated: '#edf3fa',
          inset: '#d2deea',
        },
        brand: {
          sky: '#0891b2',
          teal: '#14b8a6',
          mint: '#5eead4',
          navy: '#0a2f2f',
        },
        neu: {
          light: 'rgba(255,255,255,0.72)',
          dark: 'rgba(135,155,178,0.48)',
          'dark-hover': 'rgba(130,148,170,0.38)',
          'dark-subtle': 'rgba(125,142,165,0.28)',
        },
      },
      borderRadius: {
        none: '0px',
        xs: '4px',
        sm: '8px',
        DEFAULT: '10px',
        md: '10px',
        lg: '12px',
        xl: '16px',
        '2xl': '24px',
        full: '9999px',
      },
      fontSize: {
        'ia-hero': ['clamp(2.5rem, 5vw, 3.25rem)', { lineHeight: '1.15', letterSpacing: '-0.03em' }],
        'ia-section': ['1.5rem', { lineHeight: '1.3', letterSpacing: '-0.02em' }],
        'ia-tile': ['1.375rem', { lineHeight: '1.35', letterSpacing: '-0.02em' }],
        'ia-card-title': ['1.125rem', { lineHeight: '1.3', letterSpacing: '-0.01em' }],
        'ia-body': ['1rem', { lineHeight: '1.65' }],
        'ia-label': ['0.875rem', { lineHeight: '1.5' }],
        'ia-caption': ['0.875rem', { lineHeight: '1.5' }],
        'ia-micro': ['0.75rem', { lineHeight: '1.4' }],
      },
      fontFamily: {
        sans: ['Inter', 'SF Pro Display', '-apple-system', 'BlinkMacSystemFont', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Consolas', 'monospace'],
      },
      boxShadow: {
        xs: '0 1px 3px rgba(0,0,0,0.06)',
        sm: '0 4px 12px rgba(0,0,0,0.08)',
        md: '0 8px 24px rgba(0,0,0,0.10)',
        lg: '0 16px 40px rgba(0,0,0,0.12)',
        xl: '0 24px 56px rgba(0,0,0,0.14)',
        'neu-raised': '5px 5px 12px rgba(135,155,178,0.48), -5px -5px 12px rgba(255,255,255,0.72)',
        'neu-raised-hover': '7px 7px 16px rgba(130,148,170,0.38), -7px -7px 16px rgba(255,255,255,0.72)',
        'neu-inset': 'inset 1.5px 1.5px 4px rgba(135,155,178,0.48), inset -1px -1px 3px rgba(255,255,255,0.72)',
        'neu-inset-soft': 'inset 1px 1px 3px rgba(135,155,178,0.48), inset -0.5px -0.5px 2px rgba(255,255,255,0.72)',
        'neu-pressed': 'inset 2px 2px 4px rgba(0,0,0,0.15)',
        'btn-primary': '3px 3px 7px rgba(135,155,178,0.48), -2px -2px 5px rgba(255,255,255,0.72), 0 2px 6px rgba(8,145,178,0.2)',
        'btn-primary-hover': '5px 5px 10px rgba(130,148,170,0.38), -3px -3px 7px rgba(255,255,255,0.72), 0 4px 12px rgba(8,145,178,0.3)',
        'btn-glass': '3px 3px 7px rgba(135,155,178,0.48), -3px -3px 7px rgba(255,255,255,0.72)',
        'btn-glass-hover': '4px 4px 9px rgba(130,148,170,0.38), -4px -4px 9px rgba(255,255,255,0.72)',
        'glow-primary': '0 0 20px rgba(8,145,178,0.1)',
        'glow-sm': '0 0 0 2px rgba(8,145,178,0.12)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        'slide-up': {
          from: { transform: 'translateY(8px)', opacity: '0' },
          to: { transform: 'translateY(0)', opacity: '1' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.25s ease-out forwards',
        'slide-up': 'slide-up 0.3s ease-out forwards',
        shimmer: 'shimmer 1.5s infinite',
      },
      transitionDuration: {
        DEFAULT: '200ms',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}

export default config
