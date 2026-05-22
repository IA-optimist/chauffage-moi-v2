export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        marine: {
          DEFAULT: '#0F2A44',
          soft: '#1B3A5C',
          deep: '#081928',
        },
        cuivre: {
          DEFAULT: '#C2632A',
          hover: '#A8521F',
          soft: '#FFF1E6',
        },
        whatsapp: {
          DEFAULT: '#25D366',
          hover: '#1DA851',
        },
      },
      fontFamily: {
        sans: ["'Inter'", 'system-ui', 'sans-serif'],
        body: ["'Inter'", 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        tightish: '-0.02em',
      },
    },
  },
  plugins: [],
};
