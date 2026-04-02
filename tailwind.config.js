/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
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
          violet: '#a78bfa',
          violetdeep: '#7c3aed',
          cyan: '#22d3ee',
          mint: '#34d399',
          rose: '#fb7185',
          amber: '#fbbf24',
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
        glow: '0 0 60px -12px rgba(167, 139, 250, 0.45)',
        'glow-cyan': '0 0 70px -15px rgba(34, 211, 238, 0.4)',
        'glow-rose': '0 0 50px -10px rgba(251, 113, 133, 0.35)',
        glass: '0 8px 40px rgba(0, 0, 0, 0.45)',
        'inner-soft': 'inset 0 1px 0 rgba(255, 255, 255, 0.06)',
      },
      backgroundImage: {
        'mesh-opal':
          'radial-gradient(ellipse 80% 60% at 20% 10%, rgba(124, 58, 237, 0.22) 0%, transparent 55%), radial-gradient(ellipse 70% 50% at 85% 15%, rgba(34, 211, 238, 0.14) 0%, transparent 50%), radial-gradient(ellipse 60% 45% at 10% 80%, rgba(251, 113, 133, 0.1) 0%, transparent 50%), radial-gradient(ellipse 50% 40% at 70% 90%, rgba(52, 211, 153, 0.08) 0%, transparent 45%)',
        'hero-fade': 'linear-gradient(180deg, rgba(6, 6, 10, 0) 0%, #06060a 100%)',
      },
      animation: {
        float: 'float 7s ease-in-out infinite',
        'float-delayed': 'float 9s ease-in-out infinite 1s',
        'pulse-soft': 'pulseSoft 5s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '0.55' },
          '50%': { opacity: '0.95' },
        },
      },
    },
  },
  plugins: [],
};
