/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./templates/**/*.html', './website/forms.py'],
  theme: {
    extend: {
      colors: {
        night: {
          DEFAULT: '#0b0b10',
          950: '#06060a',
          900: '#0f0f16',
          850: '#12121a',
          800: '#181822',
        },
        opal: {
          violet: '#4b98ff',
          violetdeep: '#1d7dfc',
          cyan: '#64adff',
          mint: '#82beff',
          rose: '#3a90ff',
          amber: '#a5d0ff',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'Segoe UI', 'sans-serif'],
      },
      letterSpacing: {
        hero: '-0.03em',
        widecap: '0.08em',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      boxShadow: {
        glow: '0 0 60px -12px rgba(29, 125, 252, 0.45)',
        'glow-cyan': '0 0 70px -15px rgba(29, 125, 252, 0.4)',
        'glow-rose': '0 0 50px -10px rgba(29, 125, 252, 0.35)',
        glass: '0 8px 40px rgba(0, 0, 0, 0.45)',
        'inner-soft': 'inset 0 1px 0 rgba(255, 255, 255, 0.06)',
      },
      backgroundImage: {
        'mesh-opal':
          'radial-gradient(ellipse 80% 60% at 20% 10%, rgba(29, 125, 252, 0.28) 0%, transparent 55%), radial-gradient(ellipse 70% 50% at 85% 15%, rgba(29, 125, 252, 0.18) 0%, transparent 50%), radial-gradient(ellipse 60% 45% at 10% 80%, rgba(29, 125, 252, 0.12) 0%, transparent 50%), radial-gradient(ellipse 50% 40% at 70% 90%, rgba(29, 125, 252, 0.1) 0%, transparent 45%)',
        'hero-fade': 'linear-gradient(180deg, rgba(6, 6, 10, 0) 0%, #06060a 100%)',
      },
      animation: {
        float: 'float 11s ease-in-out infinite',
        'float-delayed': 'float 13s ease-in-out infinite 1.2s',
        'stat-card-3d': 'statCard3d 7s ease-in-out infinite',
        'pulse-soft': 'pulseSoft 6s ease-in-out infinite',
        'success-pop': 'successPop 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) both',
        'success-shimmer': 'successShimmer 2.2s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        statCard3d: {
          '0%, 100%': {
            transform:
              'translate3d(0, 0, 0) rotateX(2deg) rotateY(-4deg) translateZ(0)',
          },
          '33%': {
            transform:
              'translate3d(0, -8px, 0) rotateX(-3deg) rotateY(5deg) translateZ(6px)',
          },
          '66%': {
            transform:
              'translate3d(0, -4px, 0) rotateX(4deg) rotateY(-3deg) translateZ(10px)',
          },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '0.55' },
          '50%': { opacity: '0.95' },
        },
        successPop: {
          '0%': { opacity: '0', transform: 'scale(0.94) translateY(-12px)' },
          '100%': { opacity: '1', transform: 'scale(1) translateY(0)' },
        },
        successShimmer: {
          '0%, 100%': { opacity: '0.45' },
          '50%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};
