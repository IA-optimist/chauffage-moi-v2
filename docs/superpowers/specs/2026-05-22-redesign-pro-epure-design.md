# Redesign Chauffage & Moi — pro épuré + chaleureux

**Date :** 2026-05-22
**Cible déployée :** https://chauffage-mirror.vercel.app/ (projet Vercel `chauffage-mirror`, équipe `unity01s-projects`)
**Working dir source :** `C:\Users\maxen\chauffageetmoi-v2`
**Stack :** Astro 5 + Tailwind 3 + TypeScript, Node 22
**Hors scope :** contenu textuel, copywriting, logique ChatBot, logique Lightbox, schémas Schema.org, meta SEO, liste des 20 avis Google, liste des 69 communes du Hainaut.

## Objectif

Refonte purement design : passer d'un site visuellement chargé (mix shadows-2xl, radii incohérents, Playfair Display partout, emojis services, fond marine omniprésent) à un site **pro épuré avec touches chaleureuses** — direction « Stripe / Linear adapté au métier de chauffagiste ». Aucun contenu n'est modifié à l'exception d'une correction d'email (typo). Mobile-first non négociable.

## Décisions cadrées (brainstorming)

- Direction esthétique : **hybride tech épuré + chaleureux**
- Photos : pro disponibles dans `/public/photos/` (8 photos exploitables)
- Hero : **split** (texte gauche / photo droite, stack mobile photo dessus)
- Palette : marine `#0F2A44` + cuivre brûlé `#C2632A` + WhatsApp `#25D366` + neutres stone
- Typographie : **100% Inter** (Playfair Display supprimé)
- Responsive : 320px → 4K, exigence non négociable
- Correction email : `Chauffagesanitaire@outlook.com` → `chauffagesanitaire@outlook.com` (lowercase) dans `Layout.astro` Schema.org + `Footer.astro` (mailto + display)

## 1. Design system

### Tokens couleurs (`tailwind.config.mjs`)

```js
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
  // stone-50/100/200/700/900 utilisés directement depuis Tailwind
}
```

Les couleurs legacy `brand-orange`, `brand-blue`, `brand-darkblue` sont supprimées. Toutes les classes `bg-[#1B3A5C]`, `bg-[#E8521A]`, `text-[#E8521A]`, etc. inlinées dans le code sont remplacées par les nouveaux tokens.

### Typographie

- **Une seule famille : Inter** (300 → 800). Supprimer le link Google Fonts Playfair Display dans `Layout.astro` ; ne garder que `Inter:wght@300;400;500;600;700;800`.
- Échelle : `text-sm` 14, `text-base` 16, `text-lg` 18, `text-2xl` 24, `text-3xl` 30, `text-4xl` 40, `text-5xl` 56, `text-6xl` 72 max.
- Poids : H1 800, H2 700, H3 600, body 400/500.
- Letter-spacing : `tracking-tight` (-0.025em) sur tous les H1/H2, neutre sur le corps.
- Supprimer `font-family: 'Playfair Display'` de `global.css` et toutes les classes inline `font-[family-name:Playfair_Display,serif]` (présentes ~12 fois dans `index.astro` seul).

### Espacement, rayons, ombres

- Container principal : `max-w-6xl mx-auto px-4 sm:px-6 lg:px-8` (vs `max-w-7xl` actuel).
- Sections : `py-20 lg:py-28` uniforme partout (vs `py-24` + variations).
- Radii : `rounded-lg` (8px) pour cards, `rounded-full` pour boutons et chips, `rounded-2xl` réservé aux **visuels** (photos hero, gallery thumbnails). Suppression de tous les `rounded-3xl`.
- Ombres : 3 niveaux uniquement — `shadow-sm` (cards repos), `shadow-md` (cards hover), `shadow-xl` (stat card flottante + lightbox). Suppression intégrale de `shadow-2xl`.
- Animations : conservation du `.reveal` au scroll. Suppression de tous les `hover:-translate-y-1` et `hover:-translate-y-2`. Conserver les transitions `colors` et `shadow` (durée 200ms).

### Utilitaires `global.css` à réécrire

```css
.btn-primary  { @apply inline-flex items-center justify-center gap-2 bg-cuivre hover:bg-cuivre-hover text-white px-7 py-3.5 rounded-full font-semibold text-base transition-colors min-h-[44px]; }
.btn-whatsapp { @apply inline-flex items-center justify-center gap-2 bg-whatsapp hover:bg-whatsapp-hover text-white px-7 py-3.5 rounded-full font-semibold text-base transition-colors min-h-[44px]; }
.btn-secondary { @apply inline-flex items-center justify-center gap-2 bg-white hover:bg-stone-50 text-marine border border-stone-200 px-7 py-3.5 rounded-full font-semibold text-base transition-colors min-h-[44px]; }
.section-title    { @apply text-3xl md:text-4xl lg:text-5xl font-bold tracking-tight text-marine; }
.section-eyebrow  { @apply text-cuivre font-semibold text-xs uppercase tracking-[0.18em]; }
.section-lead     { @apply text-lg text-stone-600 max-w-2xl; }
```

Les anciennes classes `.btn-orange`, `.btn-green`, `.btn-outline` sont supprimées.

## 2. Header

- Position : `fixed top-0` (inchangé).
- **Toujours opaque** : `bg-white/90 backdrop-blur-md`, ombre `shadow-sm` ajoutée au scroll (`> 80px`). Suppression de l'état `bg-transparent` car le hero a un fond clair `bg-stone-50` (cf. 4.1) — un header transparent rendrait le texte blanc illisible.
- **Logique JS scroll à simplifier** : on garde le listener mais il n'ajoute/retire que `shadow-md` (pas de bascule de fond).
- Logo + sous-titre "Coquis-Meunier" : conservés.
- Nav desktop : liens `text-stone-700 hover:text-marine`, soulignement cuivre fin `h-0.5 w-4/5` sur actif et au hover. Lien actif `text-marine`.
- CTA droite : tel discret (`text-stone-600 hover:text-marine`) + bouton cuivre "Devis gratuit" (`.btn-primary` size sm).
- Mobile : bouton rond tel cuivre + burger (icônes `text-marine`). Menu mobile fond `bg-white/95 backdrop-blur-xl` avec liens marine.

## 3. Footer

- Fond marine `bg-marine` (`#0F2A44`).
- Suppression de la barre dégradée orange en haut → remplacée par `border-t border-cuivre/20`.
- 3 colonnes : Brand + social, Liens nav + services, Contact.
- Icônes contact : conteneur uniformisé `w-9 h-9 rounded-lg bg-cuivre/15 text-cuivre`.
- Email affiché et `mailto:` : `chauffagesanitaire@outlook.com` (lowercase).
- Bouton "Demander un devis gratuit" en bas col 3 : style `btn-primary` (cuivre, plus de marine).
- Bottom bar : `border-t border-white/5`, texte `text-stone-400 text-xs`.

## 4. Page d'accueil — section par section

### 4.1 Hero (refonte majeure : split)

- Container `max-w-6xl`, grid `lg:grid-cols-2 gap-12 items-center` (stack mobile).
- **Colonne gauche :**
  - Chip : `Agréés G1·G2·L1 — Urgences 7j/7` (fond blanc, bord stone-200, point vert pulsant)
  - H1 (Inter 800, `text-4xl sm:text-5xl lg:text-6xl tracking-tight`) : « Votre confort, notre expertise. »
  - Lead `text-lg text-stone-600` : « Chauffage · Sanitaire · Pompes à chaleur — Mons & Hainaut. Devis gratuit sous 24h. »
  - 2 CTA en ligne : `.btn-primary` "Demander un devis" + `.btn-whatsapp` avec icône
  - Sous les boutons : lien micro-trust « ★ 4,9/5 sur 20 avis Google » (cliquable → `#avis-google`)
- **Colonne droite :**
  - `<img src="/photos/equipe-travail.jpg">` ratio `aspect-[4/5]`, `rounded-2xl`, `shadow-xl`, `object-cover`. **Choix de photo final à confirmer pendant l'implémentation** parmi les 8 disponibles ; fallback `equipe-travail.jpg`.
- **Fond global section :** `bg-stone-50` (cassé, pas blanc pur), suppression du gradient marine + suppression du motif radial-gradient blanc.
- **Mobile :** photo passe au-dessus du texte, ratio `aspect-[3/2]` pour gagner en hauteur.
- **Header au top :** comme le fond hero est clair, le header transparent devient illisible — donc on inverse : header **toujours en `bg-white/90 backdrop-blur`** (on supprime l'état transparent).

### 4.2 Stat card flottante

- `-mt-12` chevauchement conservé.
- Fond blanc, `rounded-2xl`, `shadow-xl`, padding `p-6 md:p-8`.
- 4 stats en grille `grid-cols-2 md:grid-cols-4`, séparateurs verticaux fins stone-200 entre colonnes sur desktop.
- Chiffres : Inter 800, marine, `text-3xl md:text-4xl`. Label : `text-stone-500 text-sm`.

### 4.3 Services

- 3 cards `grid md:grid-cols-3 gap-6`.
- Card : fond blanc, `border border-stone-200 rounded-lg p-8`.
- Hover : `border-cuivre`, `shadow-md`. Pas de translate.
- **Icônes** : remplacer emojis 🔥🌿🚿 par 3 SVG fines (heroicons style outline 24px) :
  - Chaudières : icône flamme / fire
  - Pompes à chaleur : icône sun ou bolt
  - Sanitaire : icône droplet / wrench
- Conteneur icône : `w-11 h-11 rounded-lg bg-cuivre-soft text-cuivre flex items-center justify-center`.
- Titre H3 Inter 600 marine. Description stone-600.

### 4.4 Gamme adoucisseurs

- 2 cards `max-w-5xl mx-auto grid md:grid-cols-2 gap-8`.
- Fond `bg-stone-50` (vs `#F8FAFC` actuel — équivalent mais via token).
- Badges "Écologique" / "Best-seller" : transformés en chips ronds discrets en haut à droite (`text-xs px-3 py-1 rounded-full`), vert pour Écologique, marine pour Best-seller. Plus de bandeau plein angle.
- Conteneurs icône 💧🧂 : remplacés par SVG droplet et grains/sel, dans `w-14 h-14 rounded-lg bg-cuivre-soft text-cuivre`.
- Titres en Inter 700 marine.
- Listes ✓ : check cuivre (`text-cuivre`).
- Prix en Inter 800 marine, label stone-500.
- CTAs WhatsApp : `.btn-whatsapp` size sm.
- **Tableau comparatif** : refonte
  - Fond `bg-stone-50 rounded-2xl p-8`
  - Lignes séparées par `border-stone-200`
  - Headers : `text-stone-500 text-xs uppercase tracking-wider` (plus de vert/bleu fort)
  - Cellules "Aucune" qui étaient en vert/bleu gras → restent en gras mais en marine. Check cuivre.

### 4.5 Réalisations

- Fond `bg-stone-100` (vs marine actuel — la galerie respire mieux, et libère le marine pour les CTA forts).
- Eyebrow cuivre conservé.
- Grille `grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-5`.
- Cards : `rounded-2xl` (visuels), aspect `aspect-[4/3]`, `shadow-md`.
- Overlay gradient : `from-marine/70 via-marine/20 to-transparent` (vs noir actuel — plus cohérent palette).
- Légende blanche en bas.
- Lightbox : logique inchangée, juste skin (boutons fermer rounded-full bg-white/10).

### 4.6 Avis Google

- Fond `bg-stone-50`.
- **Carte score** : refonte en bandeau horizontal blanc centré max-w-2xl `rounded-2xl shadow-md p-6`, avec :
  - logo Google SVG à gauche
  - chiffre 4,9 (Inter 800 marine `text-5xl`) + "/ 5" stone-400
  - ★★★★★ (yellow-400)
  - "Basé sur 20 avis Google" stone-500
  - Lien "Voir tous les avis sur Google" cuivre
- **Grille reviews** : `grid md:grid-cols-2 lg:grid-cols-3 gap-5`.
  - Cards blanches, `border border-stone-200 rounded-lg p-6`.
  - Avatar : gradient `from-marine to-marine-soft`, conservé.
  - Nom Inter 600 stone-900, date stone-400 text-xs.
  - Étoiles yellow-400 conservées.
  - Quote stone-600 italic léger.
- **Mobile** : passer en `scroll snap horizontal` (`flex overflow-x-auto snap-x snap-mandatory gap-4 -mx-4 px-4`) pour éviter l'empilement vertical infini sur 20 cards. Desktop reste grille.

### 4.7 Zone d'intervention

- Fond `bg-white`.
- Encadré `bg-stone-50 rounded-2xl p-8 max-w-5xl mx-auto`.
- Grille communes `grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2`.
- Chaque commune : `<span>` → `<a href="#">` n'est pas demandé, mais on s'assure du touch target sur mobile : `text-sm text-stone-600 hover:text-cuivre hover:bg-cuivre-soft py-2 px-3 rounded-md` (passer de `py-1` à `py-2` pour atteindre ~36px tactile).

### 4.8 CTA final

- **Changement majeur :** fond `bg-marine` (vs cuivre plein actuel). Le cuivre était trop agressif en pleine largeur.
- Suppression du motif radial-gradient blanc.
- H2 blanc Inter 800 tracking-tight.
- Lead `text-stone-300`.
- 2 boutons : `.btn-primary` (cuivre) + `.btn-whatsapp`.

## 5. Autres pages (services, apropos, contact)

Sources non encore lues à la rédaction de ce spec. **Principe d'application uniforme** :

- Tokens couleur/typo/spacing identiques.
- Hero discret : H1 marine, lead stone-600, fond `bg-stone-50`, pas de gradient ni motif.
- Sections internes : containers `max-w-6xl`, `py-20 lg:py-28`, cards `rounded-lg border-stone-200`.
- Tous les `font-[family-name:Playfair_Display,serif]` retirés.
- Tous les `bg-[#1B3A5C]`, `text-[#E8521A]` remplacés par tokens.
- Email mis à jour à `chauffagesanitaire@outlook.com` partout où il apparaît.

Audit complet et adaptation détaillée pendant l'implémentation (lecture des 3 fichiers + application des mêmes patterns).

## 6. Mobile-first

- Cible 320px → 4K. Test obligatoire 320, 375, 414, 768, 1024 (Chrome devtools) + check sur téléphone réel avant livraison.
- Hero : photo top, texte ensuite, padding `pt-24` pour clear le header fixe.
- Tous les boutons et liens cliquables : `min-h-[44px]` (conservation de l'utilitaire CSS actuel `@media (max-width: 640px)`).
- Touch targets communes Hainaut : `py-2` minimum (vs `py-1` actuel).
- Galerie : 2 colonnes mobile (déjà OK).
- Avis : scroll horizontal snap mobile (changement vs empilement vertical actuel).
- Header mobile : burger conservé, fond menu blanc translucide marine sur texte.
- Pas d'élément qui dépasse de l'écran (les `overflow-x-hidden` actuels sur html/body sont préservés).

## 7. Composants à modifier (liste de fichiers)

```
src/styles/global.css           # tokens + utilitaires .btn-*, .section-*, suppression Playfair
tailwind.config.mjs             # nouveaux tokens couleurs, suppression brand-orange/blue/darkblue
src/layouts/Layout.astro        # supprimer link Google Fonts Playfair, fix email Schema.org
src/components/Header.astro     # restyle complet (fond, couleurs nav, soulignement)
src/components/Footer.astro     # restyle, suppression barre dégradée, fix email
src/pages/index.astro           # refonte section par section (8 sections)
src/pages/services.astro        # application tokens + fix email + refonte hero/sections
src/pages/apropos.astro         # application tokens + fix email + refonte hero/sections
src/pages/contact.astro         # application tokens + fix email + refonte hero/sections
```

ChatBot.astro et Lightbox.astro : **non modifiés** (logique préservée, skin pourra être ajusté seulement si le contraste casse — décision pendant implémentation).

## 8. Stratégie de livraison

1. Vérifier l'état du working tree de `chauffageetmoi-v2` (10+ fichiers modifiés non commités) — décider avec l'utilisateur : commit WIP ou stash avant de brancher.
2. Créer branche `redesign-2026-05`.
3. Mise à jour tokens (`tailwind.config.mjs` + `global.css`).
4. Refonte composants partagés (`Layout.astro`, `Header.astro`, `Footer.astro`).
5. Refonte `index.astro` section par section, dans l'ordre du fichier.
6. Lecture + refonte `services.astro`, `apropos.astro`, `contact.astro`.
7. Test local : `npm run dev`, audit responsive devtools (320/375/414/768/1024).
8. Build : `npm run build` → zéro erreur exigée.
9. Déploiement : `vercel --prod` ciblé sur le projet `chauffage-mirror` via le team `team_DOGcDOlXPgZzA5YKesanglgt`. (Le remote git pointe vers `UniTy01/chauffageetmoi` qui n'existe plus — push direct impossible, on contourne par Vercel CLI.)
10. Vérification post-déploiement : visite chaque page sur desktop et mobile, check tous les liens email/tel/WhatsApp.

## 9. Critères d'acceptation

- Visuellement : palette marine/cuivre cohérente, zéro Playfair Display, zéro emoji dans les icônes services/produits, zéro shadow-2xl, container `max-w-6xl` partout.
- Contenu : 100% identique à l'existant à 2 exceptions près — l'email passe à lowercase outlook, et les emojis services deviennent des SVG.
- Responsive : aucune coupure ou overflow horizontal sur 320px. Hero photo bien visible mobile. Tous boutons ≥ 44px.
- Performance : build Astro sans warning, pas de régression Lighthouse.
- Déploiement : la production `chauffage-mirror.vercel.app` reflète le nouveau design, les liens email pointent vers `chauffagesanitaire@outlook.com`.

## 10. Risques connus

- **Photo hero** : aucune des 8 photos disponibles n'a été inspectée visuellement. Le choix final dépendra de leur qualité/orientation. Plan B : si aucune ne convient en portrait `aspect-[4/5]`, on bascule sur du `aspect-[3/2]` paysage et on adapte le split (texte 60% / photo 40%).
- **Working tree dirty** : 10 fichiers modifiés non commités. À traiter avant tout autre changement pour ne pas perdre du travail.
- **Remote git mort** : impossible de pousser via git. Déploiement = Vercel CLI uniquement. Conséquence : pas d'auto-deploy sur push, chaque livraison sera manuelle.
- **Spec sur services/apropos/contact** : les 3 pages secondaires sont décrites par principe seulement. Si elles contiennent des composants exotiques (formulaire de contact custom, etc.), le plan d'implémentation devra les détailler en sous-étapes.
