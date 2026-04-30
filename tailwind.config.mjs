export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'brand-orange': '#E8521A',
        'brand-orange-hover': '#d4461a',
        'brand-blue': '#1B3A5C',
        'brand-darkblue': '#0D1F33',
        'brand-light': '#F8FAFC',
        'brand-green': '#25D366',
        'brand-green-hover': '#1da851',
      },
      fontFamily: {
        display: ["'Playfair Display'", 'serif'],
        body: ["'Inter'", 'sans-serif'],
      },
    },
  },
  plugins: [],
};
