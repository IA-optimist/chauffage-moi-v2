# Redesign Chauffage & Moi Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refondre le design des 4 pages du site Astro `chauffageetmoi-v2` (palette marine/cuivre, typo 100% Inter, hero split, mobile-first 320px+) et déployer sur le projet Vercel `chauffage-mirror` — contenu inchangé sauf email lowercase.

**Architecture :** Tokens centralisés dans `tailwind.config.mjs` + utilitaires dans `global.css`. Composants partagés (Header/Footer/Layout) refondus une fois. Pages refondues section par section en réutilisant les utilitaires. Aucun changement de logique JS (ChatBot, Lightbox, mobile menu).

**Tech Stack :** Astro 5, Tailwind 3, TypeScript, Node 22, Vercel CLI pour déploiement.

**Spec source :** `docs/superpowers/specs/2026-05-22-redesign-pro-epure-design.md`

**Working dir :** `C:\Users\maxen\chauffageetmoi-v2`

**Photos disponibles** (`public/photos/`) : baignoire-ilot, douche-italienne, equipe-travail, plancher-chauffant2, remplacement-avant-apres, sdb-renovation, technicien-bruleur, technicien, tuyauterie-per, vaillant-avant-apres.

**Note testing :** Pas de framework de test JS dans le projet. La vérification de chaque tâche = `npm run build` sans erreur + (sur quelques tâches clés) `npm run dev` + inspection visuelle dans devtools mobile/desktop. Lighthouse final avant déploiement.

---

## Task 0 : Sauvegarder le WIP existant

**Files:**
- Modify (commit) : 9 fichiers déjà modifiés + 1 nouveau dans le working tree

État avant : 10 fichiers en WIP (`.gitignore`, `ChatBot.astro`, `Footer.astro`, `Header.astro`, `Layout.astro`, `contact.astro`, `index.astro`, `services.astro`, `global.css` modifiés, `Lightbox.astro` untracked).

- [ ] **Step 1 : Commiter le WIP en l'état sur main**

```bash
cd /c/Users/maxen/chauffageetmoi-v2
git add -A
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "wip: pre-redesign snapshot"
```

Attendu : 1 commit créé sur `main`.

- [ ] **Step 2 : Vérifier l'état propre**

```bash
git status --short
```

Attendu : aucune sortie.

---

## Task 1 : Créer la branche de refonte

**Files:**
- Aucun fichier modifié, juste un changement de HEAD git.

- [ ] **Step 1 : Créer et basculer sur la branche `redesign-2026-05`**

```bash
cd /c/Users/maxen/chauffageetmoi-v2
git checkout -b redesign-2026-05
```

Attendu : `Switched to a new branch 'redesign-2026-05'`.

- [ ] **Step 2 : Vérifier**

```bash
git branch --show-current
```

Attendu : `redesign-2026-05`.

---

## Task 2 : Tokens Tailwind (palette + typo)

**Files:**
- Modify : `tailwind.config.mjs` (réécriture complète du bloc `extend`)

- [ ] **Step 1 : Remplacer le contenu du fichier**

Contenu cible complet :

```js
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
```

- [ ] **Step 2 : Vérifier le build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : `Complete!` ou équivalent succès, pas d'erreur de classes Tailwind cassées. (Des warnings sur des classes legacy comme `bg-[#E8521A]` sont normaux à ce stade — elles sont des hex inline, pas des tokens, donc elles continuent de fonctionner.)

- [ ] **Step 3 : Commit**

```bash
git add tailwind.config.mjs
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): nouveaux tokens marine/cuivre/whatsapp dans Tailwind"
```

---

## Task 3 : Refonte `global.css`

**Files:**
- Modify : `src/styles/global.css` (réécriture complète)

- [ ] **Step 1 : Remplacer le contenu intégral**

Contenu cible :

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    scroll-behavior: smooth;
    overflow-x: hidden;
  }
  body {
    font-family: 'Inter', system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
  }
  img, video {
    max-width: 100%;
    height: auto;
  }
  /* Targets tactiles WCAG */
  @media (max-width: 640px) {
    a, button {
      min-height: 44px;
    }
    .min-h-touch-exempt {
      min-height: 0;
    }
  }
}

@layer components {
  .btn-primary {
    @apply inline-flex items-center justify-center gap-2 bg-cuivre hover:bg-cuivre-hover text-white px-7 py-3.5 rounded-full font-semibold text-base transition-colors min-h-[44px];
  }
  .btn-whatsapp {
    @apply inline-flex items-center justify-center gap-2 bg-whatsapp hover:bg-whatsapp-hover text-white px-7 py-3.5 rounded-full font-semibold text-base transition-colors min-h-[44px];
  }
  .btn-secondary {
    @apply inline-flex items-center justify-center gap-2 bg-white hover:bg-stone-50 text-marine border border-stone-200 px-7 py-3.5 rounded-full font-semibold text-base transition-colors min-h-[44px];
  }
  .section-title {
    @apply text-3xl md:text-4xl lg:text-5xl font-bold tracking-tightish text-marine text-center;
  }
  .section-eyebrow {
    @apply text-cuivre font-semibold text-xs uppercase tracking-[0.18em] text-center block mb-3;
  }
  .section-lead {
    @apply text-lg text-stone-600 max-w-2xl mx-auto text-center mt-3 mb-12;
  }
  .reveal {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .reveal.revealed {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile menu */
.mobile-menu-closed { max-height: 0; opacity: 0; }
.mobile-menu-open { max-height: 500px; opacity: 1; }

/* Scrollbar hide */
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

/* Chatbot animations (conservées) */
@keyframes proactiveFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes chatbotEntrance {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes chatWindowOpen {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* Suggestion buttons ChatBot */
.suggestion-btn {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  color: #475569;
  transition: all 0.2s;
  font-family: inherit;
}
.suggestion-btn:hover {
  border-color: #C2632A;
  color: #C2632A;
  background: #FFF1E6;
}

/* Form card */
.type-card { background: white; }
.type-card.selected {
  border-color: #C2632A !important;
  background: #FFF1E6 !important;
}
```

Changements : suppression `.btn-orange`, `.btn-green`, `.btn-outline`, suppression `.nav-link-active`, suppression `font-display`, suppression du sélecteur `#site-header` (logique JS du header va changer), modification des couleurs suggestion-btn/type-card pour le nouveau cuivre.

- [ ] **Step 2 : Build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : succès. Note : les pages utilisant encore `.btn-orange` etc. casseront visuellement mais ne devraient pas casser le build (les utilitaires n'existent juste plus). On les remplacera dans les tâches suivantes.

- [ ] **Step 3 : Commit**

```bash
git add src/styles/global.css
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte global.css (utilitaires Inter + marine/cuivre)"
```

---

## Task 4 : Layout.astro (fonts + email Schema.org)

**Files:**
- Modify : `src/layouts/Layout.astro:37` (email Schema.org), `src/layouts/Layout.astro:117` (lien Google Fonts)

- [ ] **Step 1 : Corriger l'email Schema.org**

Remplacer ligne 37 :

```
"email": "Chauffagesanitaire@outlook.com",
```

par :

```
"email": "chauffagesanitaire@outlook.com",
```

- [ ] **Step 2 : Supprimer Playfair Display du lien Google Fonts**

Remplacer ligne 117 :

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700;800;900&display=swap" rel="stylesheet" />
```

par :

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
```

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : succès.

- [ ] **Step 4 : Commit**

```bash
git add src/layouts/Layout.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): retire Playfair Display, fix email lowercase Schema.org"
```

---

## Task 5 : Header.astro — refonte complète

**Files:**
- Modify : `src/components/Header.astro` (réécriture)

L'objectif : header **toujours opaque** (`bg-white/90 backdrop-blur-md`), texte stone-700 / marine, soulignement cuivre fin sur actif, CTA cuivre rond.

- [ ] **Step 1 : Lire le fichier existant pour vérifier la structure**

```bash
wc -l src/components/Header.astro
```

Attendu : ~164 lignes.

- [ ] **Step 2 : Remplacer le contenu intégral**

Contenu cible :

```astro
---
const currentPath = Astro.url.pathname;
const isHome = currentPath === '/';
const isServices = currentPath.startsWith('/services');
const isApropos = currentPath.startsWith('/apropos');
const isContact = currentPath.startsWith('/contact');
const linkClass = (active: boolean) => `relative px-4 py-2.5 text-sm font-medium transition-colors duration-200 nav-link group ${active ? 'text-marine' : 'text-stone-700 hover:text-marine'}`;
const underlineClass = (active: boolean) => `absolute -bottom-0.5 left-1/2 -translate-x-1/2 h-0.5 bg-cuivre rounded-full transition-all duration-300 ${active ? 'w-3/4' : 'w-0 group-hover:w-3/4'}`;
const mobileLinkClass = (active: boolean) => `px-4 py-3.5 rounded-lg text-sm font-medium transition-colors duration-200 flex items-center justify-between ${active ? 'bg-cuivre-soft text-marine border border-cuivre/30' : 'text-stone-700 hover:bg-stone-50 hover:text-marine'}`;
---

<header id="site-header" class="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md transition-shadow duration-300">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16 lg:h-20">
      <!-- Logo -->
      <a href="/" class="flex items-center gap-2 sm:gap-3 group z-10 min-h-touch-exempt">
        <img src="/logo.png" alt="Chauffage & Moi" class="h-10 sm:h-12 w-10 sm:w-12 object-contain group-hover:scale-105 transition-transform duration-300" />
        <div>
          <span class="text-marine font-bold text-base sm:text-lg leading-tight block tracking-tightish">Chauffage &amp; Moi</span>
          <span class="text-stone-500 text-[10px] sm:text-xs leading-tight block">Coquis-Meunier</span>
        </div>
      </a>

      <!-- Desktop Navigation -->
      <nav class="hidden md:flex items-center gap-1 absolute left-1/2 -translate-x-1/2" aria-label="Navigation principale">
        <a href="/" class={linkClass(isHome)} aria-current={isHome ? 'page' : undefined}>
          Accueil<span class={underlineClass(isHome)}></span>
        </a>
        <a href="/services" class={linkClass(isServices)} aria-current={isServices ? 'page' : undefined}>
          Services<span class={underlineClass(isServices)}></span>
        </a>
        <a href="/apropos" class={linkClass(isApropos)} aria-current={isApropos ? 'page' : undefined}>
          À propos<span class={underlineClass(isApropos)}></span>
        </a>
        <a href="/contact" class={linkClass(isContact)} aria-current={isContact ? 'page' : undefined}>
          Contact<span class={underlineClass(isContact)}></span>
        </a>
      </nav>

      <!-- Desktop CTA -->
      <div class="hidden md:flex items-center gap-4">
        <a href="tel:+32491873419" class="text-stone-600 hover:text-marine text-sm font-medium transition-colors flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
          0491/87.34.19
        </a>
        <a href="/contact" class="inline-flex items-center gap-1.5 bg-cuivre hover:bg-cuivre-hover text-white px-5 py-2.5 rounded-full font-semibold text-sm transition-colors">
          Devis gratuit
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" /></svg>
        </a>
      </div>

      <!-- Mobile: tel + burger -->
      <div class="flex items-center gap-2 md:hidden">
        <a href="tel:+32491873419" class="inline-flex items-center justify-center w-10 h-10 bg-cuivre text-white rounded-full transition-transform hover:scale-105" aria-label="Appeler">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
        </a>
        <button id="menu-btn" type="button" class="inline-flex items-center justify-center w-10 h-10 text-marine hover:bg-stone-100 rounded-full transition-colors" aria-expanded="false" aria-controls="mobile-menu" aria-label="Ouvrir le menu">
          <svg id="icon-open" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
          <svg id="icon-close" class="w-6 h-6 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Mobile Menu -->
  <div id="mobile-menu" class="mobile-menu-closed md:hidden overflow-hidden transition-all duration-400 ease-in-out" role="navigation" aria-label="Menu mobile">
    <div class="bg-white/95 backdrop-blur-xl border-t border-stone-200 px-4 pb-6 pt-4">
      <nav class="flex flex-col gap-1 mb-4">
        <a href="/" class={mobileLinkClass(isHome)} aria-current={isHome ? 'page' : undefined}>
          Accueil
          <svg class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </a>
        <a href="/services" class={mobileLinkClass(isServices)} aria-current={isServices ? 'page' : undefined}>
          Services
          <svg class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </a>
        <a href="/apropos" class={mobileLinkClass(isApropos)} aria-current={isApropos ? 'page' : undefined}>
          À propos
          <svg class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </a>
        <a href="/contact" class={mobileLinkClass(isContact)} aria-current={isContact ? 'page' : undefined}>
          Contact
          <svg class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </a>
      </nav>
      <a href="/contact" class="btn-primary w-full">
        Devis gratuit
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
      </a>
    </div>
  </div>
</header>

<!-- Spacer pour clear le header fixe -->
<div class="h-16 lg:h-20"></div>

<script is:inline>
  const menuBtn = document.getElementById('menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const iconOpen = document.getElementById('icon-open');
  const iconClose = document.getElementById('icon-close');
  let menuOpen = false;
  menuBtn?.addEventListener('click', () => {
    menuOpen = !menuOpen;
    menuBtn.setAttribute('aria-expanded', String(menuOpen));
    mobileMenu?.classList.toggle('mobile-menu-closed', !menuOpen);
    mobileMenu?.classList.toggle('mobile-menu-open', menuOpen);
    iconOpen?.classList.toggle('hidden', menuOpen);
    iconClose?.classList.toggle('hidden', !menuOpen);
  });

  // Shadow au scroll
  const header = document.getElementById('site-header');
  const onScroll = () => {
    if (window.pageYOffset > 12) {
      header?.classList.add('shadow-sm');
    } else {
      header?.classList.remove('shadow-sm');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
</script>
```

**Changements clés** :
- Hauteur header réduite : `h-16 lg:h-20` (vs `h-20 lg:h-24`).
- Spacer après header : nouveau, exposé en flux (vs caché précédent) — pour pousser le hero sous le header.
- Container : `max-w-6xl` (vs 7xl).
- Couleurs : marine/stone/cuivre (plus aucune référence à `#1B3A5C`, `#E8521A`, `blue-100`, `blue-200`).
- JS scroll : ne fait QUE basculer `shadow-sm` (plus de bascule de fond).

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : succès.

- [ ] **Step 4 : Commit**

```bash
git add src/components/Header.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte Header (fond blanc opaque, marine/cuivre, max-w-6xl)"
```

---

## Task 6 : Footer.astro — refonte + email

**Files:**
- Modify : `src/components/Footer.astro` (réécriture)

- [ ] **Step 1 : Vérifier la structure existante**

```bash
wc -l src/components/Footer.astro
```

Attendu : ~178 lignes.

- [ ] **Step 2 : Remplacer le contenu**

Contenu cible :

```astro
<footer class="bg-marine text-stone-300">
  <div class="border-t border-cuivre/20"></div>

  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-20">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 lg:gap-16">
      <!-- Col 1 — Brand -->
      <div>
        <a href="/" class="flex items-center gap-3 mb-6 group">
          <img src="/logo.png" alt="Chauffage &amp; Moi" class="h-12 w-12 object-contain group-hover:scale-105 transition-transform" />
          <div>
            <span class="text-white font-bold text-lg leading-tight block tracking-tightish">Chauffage &amp; Moi</span>
            <span class="text-stone-400 text-xs">Coquis-Meunier</span>
          </div>
        </a>
        <p class="text-stone-400 text-sm leading-relaxed mb-6 max-w-xs">
          Votre spécialiste en chauffage, sanitaire et pompes à chaleur dans le Hainaut depuis plus de 15 ans. Installation, entretien, dépannage.
        </p>
        <div class="inline-flex items-center gap-2 bg-cuivre/15 border border-cuivre/30 text-cuivre rounded-full px-4 py-1.5 text-xs font-semibold mb-6">
          <span class="w-1.5 h-1.5 bg-cuivre rounded-full animate-pulse"></span>
          Urgences 7j/7
        </div>
        <div>
          <p class="text-stone-500 text-xs uppercase tracking-wider font-semibold mb-3">Suivez-nous</p>
          <a href="https://www.facebook.com/ChauffageSanitaire1" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-stone-300 hover:text-white px-4 py-2 rounded-full text-sm font-medium transition-colors">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" /></svg>
            Facebook
          </a>
        </div>
      </div>

      <!-- Col 2 — Links -->
      <div>
        <div class="grid grid-cols-2 gap-8">
          <div>
            <h3 class="text-white font-bold text-xs uppercase tracking-widest mb-5 flex items-center gap-2">
              <span class="w-4 h-0.5 bg-cuivre rounded-full"></span>Navigation
            </h3>
            <ul class="space-y-3 text-sm">
              <li><a href="/" class="text-stone-400 hover:text-white transition-colors">Accueil</a></li>
              <li><a href="/services" class="text-stone-400 hover:text-white transition-colors">Services</a></li>
              <li><a href="/apropos" class="text-stone-400 hover:text-white transition-colors">À propos</a></li>
              <li><a href="/contact" class="text-stone-400 hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-white font-bold text-xs uppercase tracking-widest mb-5 flex items-center gap-2">
              <span class="w-4 h-0.5 bg-cuivre rounded-full"></span>Services
            </h3>
            <ul class="space-y-3 text-sm">
              <li><a href="/services#chauffage" class="text-stone-400 hover:text-white transition-colors">Installation chaudières</a></li>
              <li><a href="/services#pompes" class="text-stone-400 hover:text-white transition-colors">Pompes à chaleur</a></li>
              <li><a href="/services#sanitaire" class="text-stone-400 hover:text-white transition-colors">Sanitaire &amp; plomberie</a></li>
              <li><a href="/services#ventilation" class="text-stone-400 hover:text-white transition-colors">Ventilation VMC</a></li>
              <li><a href="/services#depannage" class="text-stone-400 hover:text-white transition-colors">Dépannage urgent</a></li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Col 3 — Contact -->
      <div>
        <h3 class="text-white font-bold text-xs uppercase tracking-widest mb-5 flex items-center gap-2">
          <span class="w-4 h-0.5 bg-cuivre rounded-full"></span>Contact
        </h3>
        <ul class="space-y-4 mb-6">
          <li>
            <a href="tel:+32491873419" class="group flex items-center gap-3 transition-colors">
              <div class="w-9 h-9 bg-cuivre/15 group-hover:bg-cuivre/25 rounded-lg flex items-center justify-center flex-shrink-0 transition-colors">
                <svg class="w-4 h-4 text-cuivre" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
              </div>
              <div>
                <p class="text-xs text-stone-500 mb-0.5">Téléphones</p>
                <p class="text-white font-semibold text-sm">0491 87 34 19</p>
                <p class="text-stone-400 text-xs mt-0.5">0472 80 58 71 &middot; 0470 32 81 47</p>
              </div>
            </a>
          </li>
          <li>
            <a href="mailto:chauffagesanitaire@outlook.com" class="group flex items-center gap-3 transition-colors">
              <div class="w-9 h-9 bg-cuivre/15 group-hover:bg-cuivre/25 rounded-lg flex items-center justify-center flex-shrink-0 transition-colors">
                <svg class="w-4 h-4 text-cuivre" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
              </div>
              <div class="min-w-0">
                <p class="text-xs text-stone-500 mb-0.5">Email</p>
                <p class="text-white font-semibold text-sm break-all">chauffagesanitaire@outlook.com</p>
              </div>
            </a>
          </li>
          <li class="flex items-start gap-3">
            <div class="w-9 h-9 bg-cuivre/15 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg class="w-4 h-4 text-cuivre" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            </div>
            <div>
              <p class="text-xs text-stone-500 mb-0.5">Adresse</p>
              <p class="text-stone-300 text-sm leading-relaxed">Ghlin (Mons)<br />Province du Hainaut, Belgique</p>
            </div>
          </li>
          <li class="flex items-start gap-3">
            <div class="w-9 h-9 bg-cuivre/15 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg class="w-4 h-4 text-cuivre" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <div>
              <p class="text-xs text-stone-500 mb-0.5">Horaires</p>
              <p class="text-stone-300 text-sm leading-relaxed">Lun–Ven : 7h – 18h<br />Sam : 8h – 12h</p>
            </div>
          </li>
        </ul>
        <a href="/contact" class="btn-primary w-full">
          Demander un devis gratuit
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </a>
      </div>
    </div>
  </div>

  <div class="border-t border-white/5">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
        <p class="text-stone-500 text-xs">&copy; 2026 Chauffage &amp; Moi (Coquis-Meunier) &mdash; Tous droits réservés</p>
        <p class="text-stone-500 text-xs">TVA BE 1023.953.081 &middot; Ghlin, Hainaut, Belgique</p>
      </div>
    </div>
  </div>
</footer>
```

**Changements clés :**
- Email lowercase dans mailto + display.
- Suppression de la barre dégradée orange en haut.
- Container `max-w-6xl`.
- Couleurs : `bg-marine` au lieu de `bg-[#0D1F33]`, `text-stone-*` au lieu de `text-blue-*`.
- Bouton final : `.btn-primary` (cuivre).

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : succès.

- [ ] **Step 4 : Commit**

```bash
git add src/components/Footer.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte Footer (marine/cuivre, email lowercase, max-w-6xl)"
```

---

## Task 7 : index.astro — Hero split

**Files:**
- Modify : `src/pages/index.astro:53-81` (section hero)

L'objectif : remplacer le hero text-only (avec fond marine + motif radial) par un split 2 colonnes, fond `bg-stone-50`, photo `/photos/equipe-travail.jpg` à droite.

- [ ] **Step 1 : Remplacer la section hero**

Remplacer le bloc `<!-- Hero Section - SANS PHOTO -->` ... `</section>` (lignes 53-81 actuelles) par :

```astro
  <!-- Hero Section - Split -->
  <section class="bg-stone-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
      <div class="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
        <!-- Texte -->
        <div class="order-2 lg:order-1">
          <div class="inline-flex items-center gap-2 bg-white border border-stone-200 rounded-full px-4 py-1.5 mb-6 shadow-sm">
            <span class="w-2 h-2 bg-whatsapp rounded-full animate-pulse"></span>
            <span class="text-stone-700 text-xs font-medium">Agréés G1 · G2 · L1 — Urgences 7j/7</span>
          </div>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tightish text-marine leading-[1.05] mb-6">
            Votre confort,<br/>notre expertise.
          </h1>
          <p class="text-lg text-stone-600 mb-8 max-w-lg leading-relaxed">
            Chauffage · Sanitaire · Pompes à chaleur.<br class="hidden sm:block" />
            Mons &amp; Hainaut — Devis gratuit sous 24h.
          </p>
          <div class="flex flex-col sm:flex-row gap-3 mb-6">
            <a href="/contact" class="btn-primary">
              Demander un devis gratuit
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
            </a>
            <a href="https://wa.me/32491873419" target="_blank" rel="noopener" class="btn-whatsapp">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
              WhatsApp
            </a>
          </div>
          <a href="#avis-google" class="inline-flex items-center gap-2 text-stone-600 hover:text-marine text-sm transition-colors">
            <span class="text-yellow-400">★★★★★</span>
            <span><strong class="text-marine">4,9/5</strong> sur 20 avis Google</span>
          </a>
        </div>
        <!-- Photo -->
        <div class="order-1 lg:order-2">
          <div class="relative aspect-[4/5] rounded-2xl overflow-hidden shadow-xl">
            <img src="/photos/equipe-travail.jpg" alt="Équipe Chauffage &amp; Moi sur chantier" class="w-full h-full object-cover" loading="eager" />
          </div>
        </div>
      </div>
    </div>
  </section>
```

- [ ] **Step 2 : Build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : succès.

- [ ] **Step 3 : Commit**

```bash
git add src/pages/index.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): hero split (texte + photo équipe), fond stone-50"
```

---

## Task 8 : index.astro — Stats + Services (SVG icons)

**Files:**
- Modify : `src/pages/index.astro` (sections Stats et Services)

- [ ] **Step 1 : Refondre la stat card**

Remplacer le bloc `<!-- Stats -->` ... `</section>` par :

```astro
  <!-- Stats -->
  <section class="relative -mt-10 z-20">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="bg-white rounded-2xl shadow-xl border border-stone-200 p-6 md:p-8 grid grid-cols-2 md:grid-cols-4 gap-6 md:divide-x md:divide-stone-200">
        {stats.map(s => (
          <div class="text-center md:px-4">
            <div class="text-3xl md:text-4xl font-extrabold tracking-tightish text-marine">{s.value}</div>
            <div class="text-stone-500 text-xs sm:text-sm mt-1">{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  </section>
```

- [ ] **Step 2 : Refondre la section Services (cards + SVG icons)**

Remplacer le bloc `<!-- Services -->` ... `</section>` par :

```astro
  <!-- Services -->
  <section id="services" class="py-20 lg:py-28 bg-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <span class="section-eyebrow">Notre savoir-faire</span>
      <h2 class="section-title">Tout pour votre confort</h2>
      <p class="section-lead">Une seule entreprise, tous les savoir-faire.</p>
      <div class="grid md:grid-cols-3 gap-6">
        <a href="/services#chauffage" class="group bg-white rounded-lg border border-stone-200 hover:border-cuivre p-8 transition-colors hover:shadow-md">
          <div class="w-11 h-11 rounded-lg bg-cuivre-soft text-cuivre flex items-center justify-center mb-5">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003.001 2.48z"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z"/></svg>
          </div>
          <h3 class="text-lg font-semibold text-marine mb-2 tracking-tightish">Chaudières</h3>
          <p class="text-stone-600 text-sm leading-relaxed">Installation, remplacement et entretien annuel. Gaz, mazout, condensation. Agréés G1 · G2.</p>
        </a>
        <a href="/services#energies" class="group bg-white rounded-lg border border-stone-200 hover:border-cuivre p-8 transition-colors hover:shadow-md">
          <div class="w-11 h-11 rounded-lg bg-cuivre-soft text-cuivre flex items-center justify-center mb-5">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"/></svg>
          </div>
          <h3 class="text-lg font-semibold text-marine mb-2 tracking-tightish">Pompes à chaleur</h3>
          <p class="text-stone-600 text-sm leading-relaxed">Air/eau, géothermie, systèmes hybrides. Audit énergétique et accompagnement aux primes.</p>
        </a>
        <a href="/services#sanitaire" class="group bg-white rounded-lg border border-stone-200 hover:border-cuivre p-8 transition-colors hover:shadow-md">
          <div class="w-11 h-11 rounded-lg bg-cuivre-soft text-cuivre flex items-center justify-center mb-5">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 2.25c-2.429 5.778-5.25 7.875-5.25 12a5.25 5.25 0 0010.5 0c0-4.125-2.821-6.222-5.25-12z"/></svg>
          </div>
          <h3 class="text-lg font-semibold text-marine mb-2 tracking-tightish">Sanitaire</h3>
          <p class="text-stone-600 text-sm leading-relaxed">Salles de bain complètes, douches, baignoires, chauffe-eaux, adoucisseurs, détection fuites.</p>
        </a>
      </div>
    </div>
  </section>
```

**Changements clés** : SVG (flamme, sun, droplet) au lieu d'emojis, fond stone-soft cuivre, hover sur bord seulement (pas de translate), tailles typo réduites (lg vs xl).

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : succès.

- [ ] **Step 4 : Commit**

```bash
git add src/pages/index.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte stat card et services (SVG icons)"
```

---

## Task 9 : index.astro — Gamme Adoucisseurs + Comparatif

**Files:**
- Modify : `src/pages/index.astro` (section Gamme Adoucisseurs et tableau comparatif)

- [ ] **Step 1 : Remplacer la section Gamme Adoucisseurs**

Remplacer le bloc `<!-- Gamme Adoucisseurs -->` ... `</section>` par :

```astro
  <!-- Gamme Adoucisseurs -->
  <section id="gamme" class="py-20 lg:py-28 bg-stone-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <span class="section-eyebrow">Notre gamme</span>
      <h2 class="section-title">Adoucisseurs d'eau</h2>
      <p class="section-lead">Deux technologies complémentaires. Choisissez la solution adaptée à votre maison.</p>

      <div class="grid md:grid-cols-2 gap-6 lg:gap-8 max-w-5xl mx-auto">
        <!-- Solucalc -->
        <div class="bg-white rounded-2xl p-8 border border-stone-200 hover:border-cuivre transition-colors relative">
          <span class="absolute top-6 right-6 inline-flex items-center gap-1 bg-whatsapp/10 text-whatsapp text-[10px] font-semibold uppercase tracking-wider px-2.5 py-1 rounded-full">Écologique</span>
          <div class="flex items-center gap-4 mb-5">
            <div class="w-12 h-12 rounded-lg bg-cuivre-soft text-cuivre flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 2.25c-2.429 5.778-5.25 7.875-5.25 12a5.25 5.25 0 0010.5 0c0-4.125-2.821-6.222-5.25-12z"/></svg>
            </div>
            <div>
              <h3 class="text-xl font-bold text-marine tracking-tightish">Solucalc</h3>
              <p class="text-stone-500 text-xs">Technologie au CO₂</p>
            </div>
          </div>
          <p class="text-stone-600 text-sm mb-6 leading-relaxed">
            L'adoucisseur écologique qui utilise le dioxyde de carbone pour neutraliser le calcaire sans sel, sans électricité et sans rejet. Respectueux de l'environnement, il préserve les minéraux essentiels de l'eau.
          </p>
          <ul class="space-y-2.5 mb-6 text-sm">
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Zéro sel</strong> — aucun sac à transporter</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Zéro électricité</strong> — fonctionnement 100% mécanique</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Zéro rejet</strong> — pas d'eau gaspillée</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Minéraux préservés</strong> — calcium et magnésium conservés</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Entretien minimal</strong> — cartouche tous les 2-3 ans</span></li>
          </ul>
          <div class="border-t border-stone-200 pt-5">
            <div class="flex items-baseline justify-between mb-4">
              <div>
                <span class="text-2xl font-extrabold text-marine tracking-tightish">À partir de 1.490€</span>
                <p class="text-stone-500 text-xs mt-0.5">HTVA, pose comprise</p>
              </div>
            </div>
            <a href="https://wa.me/32491873419?text=Bonjour%2C%20je%20souhaite%20un%20devis%20pour%20l%27adoucisseur%20Solucalc" target="_blank" rel="noopener" class="btn-whatsapp w-full text-sm">
              Devis Solucalc WhatsApp
            </a>
          </div>
        </div>

        <!-- Durlem -->
        <div class="bg-white rounded-2xl p-8 border border-stone-200 hover:border-cuivre transition-colors relative">
          <span class="absolute top-6 right-6 inline-flex items-center gap-1 bg-marine/10 text-marine text-[10px] font-semibold uppercase tracking-wider px-2.5 py-1 rounded-full">Best-seller</span>
          <div class="flex items-center gap-4 mb-5">
            <div class="w-12 h-12 rounded-lg bg-cuivre-soft text-cuivre flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9" cy="10" r="1" fill="currentColor"/><circle cx="14" cy="9" r="1" fill="currentColor"/><circle cx="13" cy="14" r="1" fill="currentColor"/><circle cx="10" cy="15" r="1" fill="currentColor"/></svg>
            </div>
            <div>
              <h3 class="text-xl font-bold text-marine tracking-tightish">Durlem</h3>
              <p class="text-stone-500 text-xs">Technologie au sel</p>
            </div>
          </div>
          <p class="text-stone-600 text-sm mb-6 leading-relaxed">
            L'adoucisseur à résine échangeuse d'ions, la solution traditionnelle éprouvée pour une eau parfaitement douce. Régénération automatique au sel, idéal pour les grandes familles et les eaux très dures du Hainaut.
          </p>
          <ul class="space-y-2.5 mb-6 text-sm">
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Eau ultra-douce</strong> — 0°TH, fini les traces de calcaire</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Grande capacité</strong> — jusqu'à 6 personnes</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Régénération intelligente</strong> — s'adapte à votre consommation</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Protection électroménager</strong> — prolonge la durée de vie</span></li>
            <li class="flex items-start gap-2.5 text-stone-700"><span class="text-cuivre mt-0.5">✓</span> <span><strong class="text-marine">Garantie 5 ans</strong> — pièces et main d'œuvre</span></li>
          </ul>
          <div class="border-t border-stone-200 pt-5">
            <div class="flex items-baseline justify-between mb-4">
              <div>
                <span class="text-2xl font-extrabold text-marine tracking-tightish">À partir de 1.190€</span>
                <p class="text-stone-500 text-xs mt-0.5">HTVA, pose comprise</p>
              </div>
            </div>
            <a href="https://wa.me/32491873419?text=Bonjour%2C%20je%20souhaite%20un%20devis%20pour%20l%27adoucisseur%20Durlem" target="_blank" rel="noopener" class="btn-whatsapp w-full text-sm">
              Devis Durlem WhatsApp
            </a>
          </div>
        </div>
      </div>

      <!-- Comparatif -->
      <div class="mt-16 max-w-3xl mx-auto bg-white rounded-2xl border border-stone-200 p-6 lg:p-8">
        <h3 class="text-lg font-semibold text-center text-marine mb-6 tracking-tightish">Comparatif Solucalc vs Durlem</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead>
              <tr class="border-b border-stone-200">
                <th class="py-3 pr-4 text-stone-500 text-xs uppercase tracking-wider font-medium">Critère</th>
                <th class="py-3 px-4 text-center text-marine text-xs uppercase tracking-wider font-semibold">Solucalc CO₂</th>
                <th class="py-3 pl-4 text-center text-marine text-xs uppercase tracking-wider font-semibold">Durlem Sel</th>
              </tr>
            </thead>
            <tbody class="text-stone-700">
              <tr class="border-b border-stone-100"><td class="py-3 pr-4">Technologie</td><td class="py-3 px-4 text-center">CO₂ sous pression</td><td class="py-3 pl-4 text-center">Résine échangeuse d'ions</td></tr>
              <tr class="border-b border-stone-100"><td class="py-3 pr-4">Consommation sel</td><td class="py-3 px-4 text-center font-semibold text-marine">Aucune</td><td class="py-3 pl-4 text-center">~2 sacs/mois</td></tr>
              <tr class="border-b border-stone-100"><td class="py-3 pr-4">Électricité</td><td class="py-3 px-4 text-center font-semibold text-marine">Aucune</td><td class="py-3 pl-4 text-center">Faible (transfo)</td></tr>
              <tr class="border-b border-stone-100"><td class="py-3 pr-4">Rejet eau</td><td class="py-3 px-4 text-center font-semibold text-marine">Aucun</td><td class="py-3 pl-4 text-center">~30L/régénération</td></tr>
              <tr class="border-b border-stone-100"><td class="py-3 pr-4">Entretien</td><td class="py-3 px-4 text-center">Cartouche / 2-3 ans</td><td class="py-3 pl-4 text-center">Sel + contrôle annuel</td></tr>
              <tr class="border-b border-stone-100"><td class="py-3 pr-4">Dureté obtenue</td><td class="py-3 px-4 text-center">~8-12°TH</td><td class="py-3 pl-4 text-center font-semibold text-marine">0°TH</td></tr>
              <tr><td class="py-3 pr-4">Idéal pour</td><td class="py-3 px-4 text-center">Écologie, santé</td><td class="py-3 pl-4 text-center">Confort maximal</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
```

- [ ] **Step 2 : Build**

```bash
npm run build 2>&1 | tail -10
```

- [ ] **Step 3 : Commit**

```bash
git add src/pages/index.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte gamme adoucisseurs et comparatif"
```

---

## Task 10 : index.astro — Réalisations (galerie)

**Files:**
- Modify : `src/pages/index.astro` (section Réalisations)

- [ ] **Step 1 : Remplacer la section Réalisations**

Remplacer le bloc `<!-- Réalisations -->` ... `</section>` par :

```astro
  <!-- Réalisations -->
  <section class="py-20 lg:py-28 bg-stone-100">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <span class="section-eyebrow">Nos chantiers finis</span>
      <h2 class="section-title">Travail propre, finitions soignées</h2>
      <p class="section-lead">Des réalisations livrées à des clients heureux dans tout le Hainaut.</p>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
        {[
          { src: '/photos/sdb-renovation.jpg', label: 'Salle de bain rénovée' },
          { src: '/photos/baignoire-ilot.jpg', label: 'Baignoire îlot' },
          { src: '/photos/douche-italienne.jpg', label: 'Douche italienne' },
          { src: '/photos/plancher-chauffant2.jpg', label: 'Plancher chauffant' },
          { src: '/photos/vaillant-avant-apres.jpg', label: 'Chaudière condensation · avant/après' },
          { src: '/photos/remplacement-avant-apres.jpg', label: 'Remplacement installation · avant/après' },
          { src: '/photos/tuyauterie-per.jpg', label: 'Tuyauterie multi-couche' },
          { src: '/photos/equipe-travail.jpg', label: 'Notre équipe sur chantier' },
        ].map(item => (
          <button type="button" data-lightbox="realisations" data-lightbox-src={item.src} data-lightbox-caption={item.label} class="relative group overflow-hidden rounded-2xl aspect-[4/3] shadow-md cursor-zoom-in text-left bg-stone-200">
            <img src={item.src} alt={item.label} class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
            <div class="absolute inset-0 bg-gradient-to-t from-marine/80 via-marine/20 to-transparent opacity-90 group-hover:opacity-100 transition-opacity"></div>
            <div class="absolute bottom-0 left-0 right-0 p-3 sm:p-4 text-white">
              <p class="font-semibold text-xs sm:text-sm leading-tight">{item.label}</p>
            </div>
          </button>
        ))}
      </div>
      <p class="text-center text-stone-500 text-xs mt-8">Cliquez sur une photo pour ouvrir la galerie complète</p>
    </div>
  </section>
```

- [ ] **Step 2 : Build**

```bash
npm run build 2>&1 | tail -10
```

- [ ] **Step 3 : Commit**

```bash
git add src/pages/index.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte galerie réalisations (stone-100, overlay marine)"
```

---

## Task 11 : index.astro — Avis Google (+ scroll snap mobile)

**Files:**
- Modify : `src/pages/index.astro` (section Avis Google)

- [ ] **Step 1 : Remplacer la section**

Remplacer le bloc `<!-- Témoignages Google avis -->` ... `</section>` par :

```astro
  <!-- Témoignages Google avis -->
  <section id="avis-google" class="py-20 lg:py-28 bg-stone-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <span class="section-eyebrow">Avis Google vérifiés</span>
      <h2 class="section-title">Ce que disent nos clients</h2>
      <p class="section-lead">{totalReviews} avis Google de clients satisfaits dans tout le Hainaut.</p>

      <!-- Score card -->
      <div class="max-w-2xl mx-auto bg-white border border-stone-200 rounded-2xl shadow-sm p-6 mb-12 flex flex-wrap items-center justify-center gap-x-6 gap-y-3">
        <svg class="w-8 h-8" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
          <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C12.955 4 4 12.955 4 24s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>
          <path fill="#FF3D00" d="m6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C16.318 4 9.656 8.337 6.306 14.691z"/>
          <path fill="#4CAF50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.91 11.91 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>
          <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002l6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z"/>
        </svg>
        <div class="flex items-baseline gap-1">
          <span class="text-4xl font-extrabold text-marine tracking-tightish">{avgRating}</span>
          <span class="text-stone-400 text-lg">/ 5</span>
        </div>
        <div class="flex gap-0.5 text-yellow-400 text-xl">★★★★★</div>
        <span class="text-stone-500 text-sm">Basé sur {totalReviews} avis</span>
        <a href={googleReviewsUrl} target="_blank" rel="noopener" class="text-cuivre hover:text-cuivre-hover text-sm font-semibold inline-flex items-center gap-1">
          Voir sur Google
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </a>
      </div>

      <!-- Reviews : mobile scroll horizontal, desktop grid -->
      <div class="md:hidden -mx-4 px-4 overflow-x-auto snap-x snap-mandatory flex gap-4 pb-4 scrollbar-hide">
        {googleReviews.map(review => (
          <article class="snap-center shrink-0 w-[85vw] max-w-sm bg-white rounded-lg border border-stone-200 p-5">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 bg-gradient-to-br from-marine to-marine-soft rounded-full flex items-center justify-center text-white font-bold shrink-0 text-sm">{review.name.charAt(0)}</div>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-marine truncate text-sm">{review.name}</p>
                <p class="text-xs text-stone-400">{new Date(review.date).toLocaleDateString('fr-BE', { year: 'numeric', month: 'long' })}</p>
              </div>
              <div class="text-yellow-400 text-xs tracking-tight">{'★'.repeat(review.rating)}<span class="text-stone-200">{'★'.repeat(5 - review.rating)}</span></div>
            </div>
            <p class="text-stone-600 text-sm leading-relaxed">&ldquo;{review.text}&rdquo;</p>
          </article>
        ))}
      </div>

      <div class="hidden md:grid md:grid-cols-2 lg:grid-cols-3 gap-5">
        {googleReviews.map(review => (
          <article class="bg-white rounded-lg border border-stone-200 p-6 hover:shadow-md transition-shadow">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 bg-gradient-to-br from-marine to-marine-soft rounded-full flex items-center justify-center text-white font-bold shrink-0 text-sm">{review.name.charAt(0)}</div>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-marine truncate text-sm">{review.name}</p>
                <p class="text-xs text-stone-400">{new Date(review.date).toLocaleDateString('fr-BE', { year: 'numeric', month: 'long' })}</p>
              </div>
              <div class="text-yellow-400 text-xs tracking-tight">{'★'.repeat(review.rating)}<span class="text-stone-200">{'★'.repeat(5 - review.rating)}</span></div>
            </div>
            <p class="text-stone-600 text-sm leading-relaxed">&ldquo;{review.text}&rdquo;</p>
          </article>
        ))}
      </div>

      <div class="text-center mt-12">
        <a href={googleReviewsUrl} target="_blank" rel="noopener" class="btn-secondary">
          Lire tous les avis sur Google
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </a>
      </div>
    </div>
  </section>
```

- [ ] **Step 2 : Build**

```bash
npm run build 2>&1 | tail -10
```

- [ ] **Step 3 : Commit**

```bash
git add src/pages/index.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte avis Google (score bandeau + scroll snap mobile)"
```

---

## Task 12 : index.astro — Zone intervention + CTA final

**Files:**
- Modify : `src/pages/index.astro` (sections Zone d'intervention et CTA final)

- [ ] **Step 1 : Remplacer la section Zone d'intervention**

Remplacer le bloc `<!-- Zone d'intervention SEO -->` ... `</section>` par :

```astro
  <!-- Zone d'intervention SEO -->
  <section class="py-20 lg:py-28 bg-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <span class="section-eyebrow">Zone d'intervention</span>
      <h2 class="section-title">Tout le Hainaut</h2>
      <p class="section-lead">Basés à Ghlin, au cœur de la région de Mons. Devis gratuit dans toute la province.</p>

      <div class="bg-stone-50 rounded-2xl border border-stone-200 p-6 lg:p-8 max-w-5xl mx-auto">
        <p class="text-marine font-semibold text-sm text-center mb-6">Nous intervenons dans toutes les communes du Hainaut</p>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-1.5">
          {communesHainaut.map(commune => (
            <span class="text-sm text-stone-600 hover:text-cuivre hover:bg-cuivre-soft transition-colors py-2 px-3 rounded-md text-center">
              {commune}
            </span>
          ))}
        </div>
        <p class="text-center text-stone-500 text-xs mt-6">
          Vous ne trouvez pas votre commune ? Contactez-nous — nous couvrons l'ensemble du Hainaut et ses environs.
        </p>
      </div>
    </div>
  </section>
```

- [ ] **Step 2 : Remplacer le CTA final**

Remplacer le bloc `<!-- CTA -->` ... `</section>` (juste avant `</Layout>`) par :

```astro
  <!-- CTA final -->
  <section class="py-16 lg:py-24 bg-marine">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 class="text-3xl md:text-4xl lg:text-5xl font-extrabold text-white tracking-tightish mb-5">
        Prêt à améliorer votre confort ?
      </h2>
      <p class="text-lg text-stone-300 mb-10 max-w-2xl mx-auto">
        Devis gratuit sous 24h — Intervention rapide dans tout le Hainaut
      </p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <a href="/contact" class="btn-primary">
          Demander un devis
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
        </a>
        <a href="https://wa.me/32491873419" target="_blank" rel="noopener" class="btn-whatsapp">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          WhatsApp
        </a>
      </div>
    </div>
  </section>
```

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

- [ ] **Step 4 : Commit**

```bash
git add src/pages/index.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): zone intervention + CTA final marine (au lieu d'orange)"
```

---

## Task 13 : services.astro — application des tokens

**Files:**
- Modify : `src/pages/services.astro`

- [ ] **Step 1 : Lire le fichier entier**

```bash
cat src/pages/services.astro | head -80
```

- [ ] **Step 2 : Appliquer le pattern uniforme**

Règles de transformation (à appliquer à TOUT le fichier, du début à la fin) :

1. **Hero (haut de page)** : si le hero existant a un fond marine/dégradé/motif, le remplacer par un bloc identique à la structure suivante (en gardant le contenu textuel exact) :

```astro
  <section class="bg-stone-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
      <div class="max-w-3xl">
        <span class="section-eyebrow text-left">[Eyebrow existant ou "Services"]</span>
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tightish text-marine leading-[1.1] mb-5">[Titre H1 existant exact]</h1>
        <p class="text-lg text-stone-600 leading-relaxed">[Sous-titre/lead existant exact]</p>
      </div>
    </div>
  </section>
```

(Note : `text-left` à ajouter à `section-eyebrow` dans ce contexte car il est `block mb-3` par défaut.)

2. **Remplacements globaux dans le fichier** (chaque chaîne à remplacer toutes ses occurrences) :
   - `font-[family-name:Playfair_Display,serif]` → (vide, supprimer la classe)
   - `bg-[#1B3A5C]` → `bg-marine`
   - `bg-[#0D1F33]` → `bg-marine` (même apparence visuelle)
   - `text-[#1B3A5C]` → `text-marine`
   - `bg-[#E8521A]` → `bg-cuivre`
   - `bg-[#d4461a]` → `bg-cuivre-hover`
   - `text-[#E8521A]` → `text-cuivre`
   - `hover:bg-[#d4461a]` → `hover:bg-cuivre-hover`
   - `from-[#1B3A5C]` → `from-marine`
   - `to-[#0D1F33]` → `to-marine-deep`
   - `bg-[#F8FAFC]` → `bg-stone-50`
   - `btn-orange` → `btn-primary`
   - `btn-green` → `btn-whatsapp`
   - `font-display` → (vide)
   - `text-blue-100`, `text-blue-200`, `text-blue-300` → `text-stone-300`
   - `text-blue-400`, `text-blue-500` → `text-stone-400`
   - `border-blue-200` → `border-stone-200`
   - `hover:bg-orange-50` → `hover:bg-cuivre-soft`
   - `bg-orange-100` → `bg-cuivre-soft`
   - `bg-orange-50` → `bg-cuivre-soft`
   - `text-orange-100`, `text-orange-200`, `text-orange-300` → `text-stone-300`
   - `shadow-2xl` → `shadow-xl`
   - `hover:-translate-y-1` → (vide)
   - `hover:-translate-y-2` → (vide)
   - `rounded-3xl` → `rounded-2xl`
   - `max-w-7xl` → `max-w-6xl`
   - `py-24` → `py-20 lg:py-28`
   - `Chauffagesanitaire@outlook.com` → `chauffagesanitaire@outlook.com`

3. **Cards/sections de service** : si le fichier a des grilles de services avec emojis (🔥, 🌿, 🚿, 🛁, 💧, ❄️, 🛠, etc.) dans des conteneurs colorés, conserver la structure mais :
   - Conteneur icône : `w-11 h-11 rounded-lg bg-cuivre-soft text-cuivre flex items-center justify-center`
   - Remplacer l'emoji par un SVG outline 24px adapté (utiliser ces SVG selon le contexte) :
     - **Chaudière/feu** : `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003.001 2.48z"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z"/></svg>`
     - **Pompe à chaleur/soleil** : `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"/></svg>`
     - **Eau/goutte/sanitaire** : `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 2.25c-2.429 5.778-5.25 7.875-5.25 12a5.25 5.25 0 0010.5 0c0-4.125-2.821-6.222-5.25-12z"/></svg>`
     - **VMC/vent** : `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 7.5h11.25a3 3 0 110 6H3.75M3.75 12h13.5a3 3 0 110 6H3.75"/></svg>`
     - **Dépannage/outil** : `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z"/></svg>`

4. **Cards** : `rounded-2xl` → `rounded-lg`, `shadow-lg`/`shadow-xl` → `border border-stone-200`, `hover:shadow-2xl hover:-translate-y-2` → `hover:border-cuivre hover:shadow-md`.

Implémentation : **lire le fichier complet, identifier chaque section, appliquer les transformations**. Quand un bloc HTML est trop complexe à transformer in-situ, le réécrire entièrement en suivant la structure de référence des sections de `index.astro`.

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

Attendu : succès. Si erreur sur une classe Tailwind, vérifier qu'on n'a pas oublié un hex inline.

- [ ] **Step 4 : Commit**

```bash
git add src/pages/services.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte services.astro (tokens marine/cuivre, SVG icons, max-w-6xl)"
```

---

## Task 14 : apropos.astro — application des tokens

**Files:**
- Modify : `src/pages/apropos.astro`

Procéder **exactement** comme Task 13 (mêmes règles, mêmes substitutions, même pattern hero), adapté au contenu de cette page.

- [ ] **Step 1 : Lire le fichier**

```bash
cat src/pages/apropos.astro | head -80
```

- [ ] **Step 2 : Appliquer toutes les substitutions et patterns** de Task 13 step 2 (règles 1, 2, 3, 4) à `apropos.astro`.

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

- [ ] **Step 4 : Commit**

```bash
git add src/pages/apropos.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte apropos.astro (tokens marine/cuivre, SVG icons)"
```

---

## Task 15 : contact.astro — application des tokens

**Files:**
- Modify : `src/pages/contact.astro`

Procéder **exactement** comme Task 13. Attention particulière sur les liens email `mailto:` et tout affichage d'email — assurer `chauffagesanitaire@outlook.com` lowercase partout.

- [ ] **Step 1 : Lire le fichier**

```bash
cat src/pages/contact.astro | head -120
```

- [ ] **Step 2 : Appliquer toutes les substitutions et patterns** de Task 13 step 2 (règles 1, 2, 3, 4) à `contact.astro`. **Vérifier explicitement** que :
   - Toutes les occurrences de `Chauffagesanitaire@outlook.com` deviennent `chauffagesanitaire@outlook.com`
   - Le formulaire de contact (s'il existe) conserve sa logique JS et son endpoint, on ne modifie QUE le style

- [ ] **Step 3 : Build**

```bash
npm run build 2>&1 | tail -10
```

- [ ] **Step 4 : Commit**

```bash
git add src/pages/contact.astro
git -c commit.gpgsign=false -c user.name="0xUniTy" -c user.email="maxence.londot11@gmail.com" \
  commit -m "feat(design): refonte contact.astro (tokens marine/cuivre, email lowercase)"
```

---

## Task 16 : Audit final & vérification responsive

**Files:** Aucun (vérification seulement).

- [ ] **Step 1 : Recherche d'éventuels résidus**

```bash
cd /c/Users/maxen/chauffageetmoi-v2
grep -r "Playfair" src/ 2>&1
grep -r "Chauffagesanitaire" src/ 2>&1
grep -r "btn-orange\|btn-green\|btn-outline" src/ 2>&1
grep -r "bg-\[#1B3A5C\]\|bg-\[#E8521A\]\|bg-\[#0D1F33\]" src/ 2>&1
grep -r "shadow-2xl" src/ 2>&1
grep -r "max-w-7xl" src/ 2>&1
grep -r "font-\[family-name:Playfair" src/ 2>&1
```

Attendu : **aucune sortie** sur tous ces greps. Si un résidu apparaît, le corriger et recommiter.

- [ ] **Step 2 : Build complet**

```bash
npm run build 2>&1 | tail -20
```

Attendu : tout vert. Vérifier qu'il y a bien 4 pages générées dans `dist/`.

- [ ] **Step 3 : Démarrer dev server pour inspection**

```bash
npm run dev 2>&1 &
```

(Démarrer en arrière-plan, port 4321 par défaut.)

- [ ] **Step 4 : Capture rapide responsive**

Ouvrir manuellement (ou via Playwright/Puppeteer si dispo) http://localhost:4321 dans devtools :
- 320px wide (iPhone SE 1ère gén)
- 375px (iPhone moderne)
- 768px (tablette portrait)
- 1280px (desktop standard)

Vérifier que **aucun élément ne déborde horizontalement**, **tous les boutons sont cliquables 44px**, **le hero photo passe au-dessus du texte sur mobile**, et **les avis défilent horizontalement avec snap sur mobile**.

- [ ] **Step 5 : Arrêter dev server**

```bash
# Tuer le process node port 4321
kill $(lsof -ti:4321 2>/dev/null) 2>/dev/null || true
```

- [ ] **Step 6 : Commit éventuels correctifs**

S'il y a eu des correctifs en Step 1, ils sont déjà commités. Sinon, rien à faire.

---

## Task 17 : Déploiement Vercel `chauffage-mirror`

**Files:**
- Possiblement créer/écraser : `.vercel/project.json`

- [ ] **Step 1 : Vérifier l'installation Vercel CLI**

```bash
vercel --version 2>&1
```

Attendu : version (ex. `Vercel CLI 39.x.x`). Si absente :

```bash
npm install -g vercel
```

- [ ] **Step 2 : Vérifier l'authentification**

```bash
vercel whoami 2>&1
```

Attendu : un username (probablement `unity01`). Sinon :

```bash
vercel login
```

(Login interactif. Si interactif impossible, mentionner au user.)

- [ ] **Step 3 : Lier le projet local au projet Vercel `chauffage-mirror`**

S'il existe déjà un `.vercel/project.json`, vérifier son `projectId` :

```bash
cat .vercel/project.json 2>&1
```

Si l'ID correspond à `prj_zWuD1eY4Y8nhc7AsCUMFrmqJM8f0` (chauffage-mirror), tout va bien. Sinon, le réécrire :

```bash
mkdir -p .vercel
cat > .vercel/project.json << 'EOF'
{
  "projectId": "prj_zWuD1eY4Y8nhc7AsCUMFrmqJM8f0",
  "orgId": "team_DOGcDOlXPgZzA5YKesanglgt"
}
EOF
```

- [ ] **Step 4 : Déployer en production**

```bash
vercel --prod --yes 2>&1 | tee /tmp/vercel-deploy.log | tail -30
```

Attendu : ligne finale contenant l'URL `https://chauffage-mirror-*.vercel.app` et `Production: https://chauffage-mirror.vercel.app`.

- [ ] **Step 5 : Extraire l'URL et la noter**

```bash
grep -oE 'https://chauffage-mirror[^ ]+\.vercel\.app' /tmp/vercel-deploy.log | tail -1
```

Attendu : 1 URL. À communiquer au user.

---

## Task 18 : Vérification post-déploiement

**Files:** Aucun.

- [ ] **Step 1 : Curl HEAD sur la prod**

```bash
curl -I https://chauffage-mirror.vercel.app/ 2>&1 | head -5
curl -I https://chauffage-mirror.vercel.app/services 2>&1 | head -5
curl -I https://chauffage-mirror.vercel.app/apropos 2>&1 | head -5
curl -I https://chauffage-mirror.vercel.app/contact 2>&1 | head -5
```

Attendu : chaque page renvoie `HTTP/2 200`.

- [ ] **Step 2 : Vérifier que l'email est bien lowercase dans le HTML produit**

```bash
curl -s https://chauffage-mirror.vercel.app/ | grep -o 'chauffagesanitaire@outlook\.com\|Chauffagesanitaire@outlook\.com' | sort -u
```

Attendu : `chauffagesanitaire@outlook.com` (et **rien d'autre**).

- [ ] **Step 3 : Vérifier que Playfair n'est plus chargé**

```bash
curl -s https://chauffage-mirror.vercel.app/ | grep -c 'Playfair'
```

Attendu : `0`.

- [ ] **Step 4 : Communiquer l'URL au user**

URL principale : `https://chauffage-mirror.vercel.app/`

---

## Self-Review (post-rédaction)

**Couverture spec :**
- Section 1 (Design system) → Tasks 2, 3 ✓
- Section 2 (Header) → Task 5 ✓
- Section 3 (Footer) → Task 6 ✓
- Section 4.1 → 4.8 (sections index) → Tasks 7-12 ✓
- Section 5 (services/apropos/contact) → Tasks 13-15 ✓
- Section 6 (Mobile) → Task 16 step 4 ✓
- Section 7 (fichiers à modifier) → Tasks 2-15 couvrent les 9 fichiers ✓
- Section 8 (stratégie de livraison) → Tasks 0-1 (WIP + branche), 17 (deploy), 18 (verif) ✓
- Section 9 (critères d'acceptation) → couvert par Tasks 16 (audit) et 18 (post-deploy)
- Section 10 (risques) → photo hero (`equipe-travail.jpg` choisie par défaut, ajustable Task 7 step 1), working tree dirty (Task 0), remote git mort (Task 17 contourne via Vercel CLI), pages secondaires (Tasks 13-15 ont des règles explicites)

**Placeholders :** aucun "TBD" ou "implement later". Les Tasks 13-15 ont des **règles de transformation explicites** (pas "appliquer les mêmes principes") mais demandent une lecture préalable du fichier — c'est nécessaire pour ces 3 pages dont le contenu exact n'a pas été inspecté.

**Cohérence types :** noms de tokens stables (`marine`, `cuivre`, `cuivre-soft`, `marine-soft`, `marine-deep`, `whatsapp`, `whatsapp-hover`). Classes utilitaires stables (`btn-primary`, `btn-whatsapp`, `btn-secondary`, `section-title`, `section-eyebrow`, `section-lead`).

**Risque résiduel identifié pendant la review :**
- Task 17 step 3 suppose que le link `.vercel/project.json` n'existe pas encore localement. Si l'utilisateur a déjà fait un `vercel link` avant, le projectId pourrait être celui de `chauffageetmoi-v2` (différent de `chauffage-mirror`). Le step 3 est explicite : vérifier puis écraser si nécessaire — donc OK.
- Task 16 step 4 dit "ouvrir manuellement". Sur Windows en PowerShell sans navigateur graphique disponible côté Claude, la vérification responsive sera limitée. Plan B accepté : se reposer sur `npm run build` (statique = pas de bug runtime) et la `curl` de Task 18.
