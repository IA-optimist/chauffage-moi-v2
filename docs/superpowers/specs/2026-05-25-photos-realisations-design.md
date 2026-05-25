# Intégration photos chantiers — Enrichissement /realisations

**Date :** 2026-05-25
**Cible déployée :** https://chauffage-mirror.vercel.app/realisations (projet Vercel `chauffage-mirror`, équipe `unity01s-projects`)
**Working dir source (Astro) :** `C:\Users\maxen\chauffageetmoi-v2` — branche `redesign-2026-05`
**Working dir secondaire (AI OS) :** `C:\Users\maxen\Documents\Chauffage-et-moi-Site` (cleanup `Photos/`)
**Stack :** Astro 5 + Tailwind 3 + TypeScript, Node 22 (existant — pas de modif)
**Hors scope :** infra (pas d'API, pas de MinIO, pas de CMS) · migration `astro:assets` / WebP / AVIF · modif des autres pages Astro (index, services, apropos, contact) · modif du code AI OS (api, worker, dashboard, agents) · branche `phase-34-editable-policy` en cours sur le repo AI OS.

## Contexte & déclencheur

Un dossier `Photos/` est apparu le 23 mai 2026 à la racine du repo AI OS `Chauffage-et-moi-Site` :
- 85 fichiers, 19 Mo
- 62 photos FB-CDN (filenames `505XXXXXX_..._n.jpg`) — batch téléchargé depuis Facebook
- 10 captures d'écran Durlem (ajoutées par l'utilisateur le 25 mai)
- 11 photos WhatsApp (ajoutées le 25 mai)
- 2 fichiers de test (`fb-race-test.jpg`, `fb-test-photo-0.jpg`)
- Non commité, non gitignoré, aucune référence dans le code

Le repo AI OS est un Control Plane interne (postgres, redis, n8n, qdrant, ollama, MinIO, FastAPI auth) — **il n'a pas vocation à héberger les assets du site marketing**. Le site marketing existe : projet Vercel `chauffage-mirror` (Astro 5), source `C:\Users\maxen\chauffageetmoi-v2`, repo `github.com/UniTy01/chauffageetmoi`. La page `/realisations` existe déjà avec **23 photos curées en 4 sections** (commit `8867409` + `5bd901e`).

Conclusion : `Photos/` est au mauvais endroit. Le travail consiste à **(a) nettoyer le repo AI OS** et **(b) enrichir la galerie /realisations** avec les photos pertinentes du batch.

## Décisions cadrées (brainstorming)

- **Approche** : B — curation + intégration au site Astro (vs. minimal-only / vs. archi CMS lourde)
- **Curation** : auto-tri par Claude + validation finale par l'utilisateur du rapport markdown
- **Section PAC** : nouvelle section ajoutée **uniquement si** des photos PAC pertinentes sont trouvées dans le batch
- **Placement Durlem** : section actuelle "Adoucisseurs" **étendue** à "Solucalc & Durlem" (un seul tableau mixte, pas deux sous-sections)
- **Format** : conversion PNG → JPEG q=85 pour cohérence avec `public/photos/` (100% JPEG actuellement)
- **Pas d'optimisation `astro:assets`** : on suit le pattern existant `public/photos/` servi statiquement
- **Pas de modif des autres pages** : index/services/apropos/contact restent intacts
- **Hors-scope strict** : phase-34-editable-policy (branche en cours sur AI OS) reste totalement indépendante

## Objectif

Faire disparaître `Photos/` du repo AI OS et enrichir la galerie publique `/realisations` avec les photos pertinentes du batch, en respectant le design existant (4-5 sections, naming sémantique, captions FR, lightbox).

## 1. Inventaire source

| Origine | Count | Filename pattern | Notes |
|---|---|---|---|
| Facebook CDN | 62 | `505XXXXXXX_NNNNNNN_..._n.jpg` | 1200×1600, JPEG, EXIF stripé |
| Durlem (captures) | 10 | `Capture d'écran 2026-05-25 19XXXX.png` | PNG, probablement screenshots site/catalogue Durlem |
| WhatsApp | 11 | `WhatsApp Image 2026-05-25 at 14.32.XX.jpeg` | Contenu inconnu, inspection requise |
| Test artefact | 2 | `fb-race-test.jpg`, `fb-test-photo-0.jpg` | Auto-reject |
| **Total** | **85** | | **À curer : 83 (test exclus)** |

## 2. État actuel de `/realisations` (à étendre)

Fichier : `src/pages/realisations.astro` (158 lignes)

Sections existantes :
- **`galChauffage`** (6) — chaudières Vaillant (cave/brique/pierre), vaillant-avant-apres, remplacement-avant-apres, radiateur-design-noir
- **`galSanitaire`** (7) — sdb-baignoire-ilot-moderne, sdb-double-vasque-bois, sdb-baignoire-balneo-marbre, douche-italienne-motifs, baignoire-ilot, douche-italienne, chauffe-eau-atlantic
- **`galAdoucisseur`** (3) — solucalc-bouteille-co2, solucalc-equipe-installation, solucalc-installateur-agree
- **`galEquipe`** (3) — equipe-chauffage-et-moi, technicien-bruleur, technicien

Photos présentes dans `public/photos/` mais **non référencées** dans la page (réserve curation antérieure) : `equipe-travail.jpg`, `plancher-chauffant2.jpg`, `sdb-renovation.jpg`, `tuyauterie-per.jpg` — **hors scope de cette spec** (ne pas activer sauf demande explicite).

Total affiché actuel : `{totalPhotos}` = 19 (somme des 4 tableaux).

## 3. Modèle de sections cible

| Section | Tableau Astro | Avant | Cible max après curation |
|---|---|---|---|
| Chauffage | `galChauffage` | 6 | jusqu'à ~15 |
| Sanitaire | `galSanitaire` | 7 | jusqu'à ~15 |
| **Adoucisseurs Solucalc & Durlem** *(titre étendu)* | `galAdoucisseur` | 3 | 3 + jusqu'à ~6 Durlem |
| **PAC** *(nouvelle, conditionnelle)* | `galPAC` | 0 | jusqu'à ~5 |
| Équipe | `galEquipe` | 3 | jusqu'à ~6 |

Cibles **indicatives**, pas des quotas. La curation décide en fonction du contenu réel ; le tableau peut rester à 0 (section PAC non créée) ou dépasser légèrement si justifié.

### 3.1 Modifications structurelles de `realisations.astro`

1. **Section Adoucisseurs** : `<span class="section-eyebrow">` reste "Adoucisseurs d'eau". `<h2>` passe de `Installations Solucalc` à `Installations Solucalc & Durlem`. `<p class="section-lead">` réécrit pour mentionner les deux technologies (Solucalc CO₂ écologique vs Durlem au sel — deux options selon préférences client).
2. **Section PAC** (si applicable) : nouvelle `<section>` insérée **entre Chauffage et Sanitaire** (ordre logique : chaud → froid → sanitaire). Eyebrow "Pompes à chaleur", h2 "Installations PAC", lead courte mentionnant air-eau / géothermie.
3. **Aucune autre modification structurelle** : layout, hero, CTA final, classes Tailwind restent identiques.
4. **`totalPhotos`** : reste calculé en somme des tableaux — pas de modif manuelle.

## 4. Naming convention

Pattern existant à respecter (lowercase, kebab-case, ASCII sans accents, ≤40 chars) :

| Catégorie | Pattern | Exemple existant | Exemple nouveau |
|---|---|---|---|
| Chaudière | `chaudiere-{marque}-{contexte}.jpg` | `chaudiere-vaillant-cave.jpg` | `chaudiere-bulex-cave.jpg` |
| Remplacement | `{marque}-avant-apres.jpg` ou `remplacement-{detail}.jpg` | `vaillant-avant-apres.jpg` | `remplacement-bruleur-fioul.jpg` |
| Radiateur | `radiateur-{style}-{couleur}.jpg` | `radiateur-design-noir.jpg` | `radiateur-vertical-blanc.jpg` |
| Salle de bain | `sdb-{feature}-{modif}.jpg` | `sdb-double-vasque-bois.jpg` | `sdb-baignoire-ovale.jpg` |
| Douche | `douche-italienne-{modif}.jpg` | `douche-italienne-motifs.jpg` | `douche-italienne-verre.jpg` |
| Baignoire seule | `baignoire-{forme}.jpg` | `baignoire-ilot.jpg` | `baignoire-balneo-pierre.jpg` |
| Chauffe-eau | `chauffe-eau-{marque}.jpg` | `chauffe-eau-atlantic.jpg` | `chauffe-eau-bulex.jpg` |
| Solucalc | `solucalc-{contexte}.jpg` | `solucalc-bouteille-co2.jpg` | (déjà couvert, pas besoin) |
| **Durlem** | **`durlem-{descripteur}.jpg`** | (nouveau) | `durlem-installation-cuisine.jpg` |
| **PAC** | **`pac-{type}-{modif}.jpg`** | (nouveau) | `pac-air-eau-exterieure.jpg`, `pac-monobloc-jardin.jpg` |
| Technicien | `technicien-{action}.jpg` | `technicien-bruleur.jpg` | `technicien-soudure.jpg` |
| Équipe | `equipe-{descripteur}.jpg` | `equipe-chauffage-et-moi.jpg` | `equipe-pose-sdb.jpg` |

**Tie-breaker en cas de collision de nom** : suffixe numérique `-2`, `-3` (ex. `chaudiere-vaillant-cave-2.jpg`).

## 5. Captions (FR)

Caractéristiques des captions existantes :
- Phrases courtes (3-7 mots)
- Style éditorial : "Chaudière Vaillant — installation cave", "Salle de bain — baignoire îlot &amp; douche italienne"
- Séparateur `—` (em-dash) entre objet et contexte
- Entités HTML pour `&` (`&amp;`) et `²` (`&sup2;` ou caractère direct)
- Pas de point final

Reprise du même style pour les nouvelles photos. Examples :
- `Chaudière Bulex — installation cave`
- `PAC air-eau — unité extérieure`
- `Durlem — adoucisseur au sel installé`
- `Salle de bain — baignoire ovale &amp; vasque pierre`

## 6. Conversion PNG → JPEG (10 captures Durlem)

- Outil : `Pillow` (Python) ou ImageMagick — peu importe, choix laissé au plan d'implémentation
- Sortie : JPEG quality 85, conservation des dimensions originales
- Profil colorimétrique sRGB (par défaut Pillow)
- Si la capture contient de la transparence (alpha non plein), fond blanc avant conversion (rare pour des screenshots web)
- Fichier source PNG : **conservé en archive** dans `fb-photos-raw/` (gitignored), pas re-supprimé après conversion

## 7. Règles de curation (déterministes)

Appliquées dans cet ordre — la première règle qui matche décide :

1. **Auto-REJECT — fichier de test** : `fb-race-test.jpg`, `fb-test-photo-0.jpg`. Raison : `test_artifact`.
2. **REJECT — doublon perceptuel** des 23 photos déjà intégrées dans `public/photos/`. Méthode : perceptual hash via `imagehash.phash` (ou équivalent), hamming distance ≤ 5. Raison : `duplicate_of:<filename>`.
3. **REJECT — qualité dégradée** : flou évident, sujet trop éloigné, mal cadré, exposition cramée/sombre. Raison : `quality_low:<detail>`.
4. **REJECT — RGPD** : visage client identifiable, plaque d'immatriculation, adresse postale visible, document personnel. Raison : `gdpr_flag:<detail>`. **REJECT par défaut** sauf consentement écrit existant (alors RETAIN avec note).
5. **REJECT — hors périmètre** : sujet pas dans chaudière/PAC/sanitaire/adoucisseur/équipe (paysages, selfies non équipe, animaux, etc.). Raison : `out_of_scope`.
6. **REJECT — redondance interne** : si N photos quasi-identiques du même chantier (perceptual hash similaire entre photos du batch lui-même, distance ≤ 5), garder les 1-2 meilleures. Raison : `internal_redundancy:<kept_file>`.
7. **REJECT — Durlem watermark / catalogue** : si capture d'écran contient watermark Durlem ou logo de site tiers ostentatoire. Raison : `branding_concern:durlem_watermark`.
8. **RETAIN** : tout le reste. Classification dans Chauffage / Sanitaire / Adoucisseurs / PAC / Équipe selon contenu visuel.

**Edge case** : photo borderline (ex. visage flouté naturellement, ou seulement partiellement visible) → flag `gdpr_review` au lieu d'auto-decision, attendre validation user.

## 8. Curation report

Fichier : `chauffageetmoi-v2/docs/realisations-curation-2026-05-25.md`

Format (table markdown), une ligne par photo :

```markdown
| # | Filename source | Origin | Decision | Section | New name | Caption | Reason / notes |
|---|---|---|---|---|---|---|---|
| 1 | 505715303_...jpg | FB | RETAIN | Chauffage | chaudiere-vaillant-renovation-mons.jpg | Chaudière Vaillant — rénovation Mons | clean install, finition propre |
| 2 | 505739580_...jpg | FB | REJECT | — | — | — | duplicate_of:chaudiere-vaillant-cave.jpg (phash dist 3) |
| 3 | 505745796_...jpg | FB | REJECT | — | — | — | gdpr_flag:visage_client_visible |
| ... |
```

Sections en fin de fichier :
- **Summary stats** : total / retain / reject par catégorie + par raison de rejet
- **Section breakdown** : nb retenu par section cible, avec sous-total
- **GDPR flagged** : liste séparée des photos en `gdpr_review` (borderline) nécessitant décision utilisateur

Le report est **commité dans `chauffageetmoi-v2`** (sur la branche `redesign-2026-05` ou une feature branch dédiée — décision au plan d'impl).

## 9. Phases d'exécution

| Phase | Repo | Étapes | Validation user |
|---|---|---|---|
| 1. Cleanup AI OS | Chauffage-et-moi-Site | Add `Photos/` à `.gitignore` ; ne pas supprimer le dossier physiquement avant d'avoir copié les sources vers le repo Astro ; commit séparé sur une branche dédiée (ne pas polluer `phase-34-editable-policy`) | Non bloquant |
| 2. Préparation Astro repo | chauffageetmoi-v2 | Créer (ou réutiliser) `fb-photos-raw/`, vérifier qu'il est gitignored ; copier les 85 photos depuis AI OS vers `fb-photos-raw/` ; créer une feature branch (ex. `feat/realisations-batch-2026-05`) | Non bloquant |
| 3. Curation auto | chauffageetmoi-v2 | **(a)** Détection doublons (règle 2 §7) via script Python `imagehash.phash` — produit une liste machine de doublons + distances. **(b)** Inspection visuelle Claude des autres photos pour règles 3-8 §7 (qualité, RGPD, scope, redondance interne, watermark Durlem, classification). **(c)** Génération de `docs/realisations-curation-2026-05-25.md` selon format §8. **(d)** Conversion PNG Durlem → JPEG via Pillow en parallèle. | **Bloquant — user lit le rapport** |
| 4. Intégration | chauffageetmoi-v2 | Copier photos retenues vers `public/photos/` avec nouveaux noms ; éditer `realisations.astro` (extend `gal*`, créer section PAC si applicable, mettre à jour titre Adoucisseurs) ; `npm run build` doit passer | Visuel local possible (`npm run dev`) |
| 5. Commit & deploy | chauffageetmoi-v2 + AI OS | Commit/push feature branch chauffageetmoi-v2 → PR (ou merge direct selon habitude) → Vercel auto-deploy ; séparément, commit `.gitignore` AI OS sur sa branche dédiée | User valide visuel prod |
| 6. Cleanup final | Chauffage-et-moi-Site | Supprimer physiquement `Photos/` (sources désormais dans `fb-photos-raw/` du repo Astro) | — |

**Note** : la phase 6 ne supprime le dossier source qu'après confirmation que le batch est sauvegardé dans `chauffageetmoi-v2/fb-photos-raw/` (gitignored mais préservé sur disque). Pas de perte de données.

## 10. Risques & mitigations

| # | Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Captures Durlem = visuels catalogue avec watermark / basse qualité | Moyenne | Cohérence visuelle de la galerie | Règle 7 §7 : REJECT auto si watermark détecté ; sinon flag visuel pour validation |
| R2 | Visages clients identifiables (RGPD) | Élevée sur photos chantier intérieur | Risque légal | Règle 4 §7 : REJECT par défaut, flag `gdpr_review` pour borderline |
| R3 | Contenu WhatsApp totalement hors sujet (photos perso, captures conversation, etc.) | Moyenne | Pollution curation | Règle 5 §7 : auto-REJECT si pas dans périmètre métier |
| R4 | Batch FB déjà entièrement curé → 0 photo nouvelle utile | Faible (62 vs 23 déjà extraites = théoriquement encore 39 à examiner) | Aucun — design supporte le cas | Report vide est un résultat valide ; `Photos/` quand même supprimé du AI OS |
| R5 | Poids des images sur Vercel (pas d'optim astro:assets) | Moyenne si on ajoute beaucoup | Lighthouse score, mobile perf | Hors scope cette spec ; compensé par `loading="lazy"` déjà en place et JPEG q=85 sur conversions |
| R6 | Merge conflict sur `realisations.astro` si la branche `redesign-2026-05` continue d'évoluer | Faible | Travail de merge manuel | Feature branch dédiée + rebase régulier ; éviter de modifier `realisations.astro` ailleurs pendant ce travail |
| R7 | Dépassement scope vers d'autres pages (services PAC mentionne PAC sans illustration, etc.) | Élevée — tentation naturelle | Scope creep | §"Hors scope" en haut de spec ; aucune modif autre page ; ouvrir tickets séparés si besoins identifiés |

## 11. Critère de "done"

- [ ] `Photos/` ne figure plus sur disque dans `Chauffage-et-moi-Site/`
- [ ] `.gitignore` du repo AI OS contient une ligne `Photos/` (ou pattern équivalent), commitée
- [ ] Le commit `.gitignore` du repo AI OS est sur une branche **autre que** `phase-34-editable-policy` (typiquement `master` après PR, ou branche dédiée `chore/gitignore-photos`)
- [ ] `chauffageetmoi-v2/fb-photos-raw/` contient les 85 fichiers source (gitignored, préservés)
- [ ] `chauffageetmoi-v2/docs/realisations-curation-2026-05-25.md` existe, complet, **validé** par l'utilisateur
- [ ] N photos curées copiées dans `chauffageetmoi-v2/public/photos/` avec noms sémantiques (§4)
- [ ] `src/pages/realisations.astro` étendu :
  - `galChauffage`, `galSanitaire`, `galAdoucisseur`, `galEquipe` étendus avec nouvelles entrées
  - `galPAC` créé + nouvelle `<section>` PAC si applicable (sinon : pas de section vide)
  - `<h2>` Adoucisseurs renommé `Installations Solucalc & Durlem`
  - `section-lead` Adoucisseurs réécrite pour mentionner Durlem
- [ ] `npm run build` passe localement, 0 warning lié aux nouvelles images
- [ ] Commit feature branch poussé sur `github.com/UniTy01/chauffageetmoi`
- [ ] Vercel a déployé avec succès (status `Ready` sur `chauffage-mirror`)
- [ ] `https://chauffage-mirror.vercel.app/realisations` affiche le nouveau total dans le hero, charge toutes les images sans 404, sections visibles et alignées
- [ ] Aucune photo en violation RGPD visible en prod

## 12. Artefacts produits

| Fichier | Repo | Statut |
|---|---|---|
| `docs/superpowers/specs/2026-05-25-photos-realisations-design.md` | chauffageetmoi-v2 | Cette spec |
| `docs/realisations-curation-2026-05-25.md` | chauffageetmoi-v2 | Curation report (phase 3) |
| `public/photos/{N nouveaux fichiers}.jpg` | chauffageetmoi-v2 | Photos curées (phase 4) |
| `src/pages/realisations.astro` (modifié) | chauffageetmoi-v2 | Page étendue (phase 4) |
| `fb-photos-raw/{85 fichiers}` | chauffageetmoi-v2 | Archive batch source (gitignored, préservé) |
| `.gitignore` (1 ligne ajoutée) | Chauffage-et-moi-Site (AI OS) | Cleanup (phase 1) |

## 13. Liens & références

- Site déployé : https://chauffage-mirror.vercel.app/realisations
- Repo Astro (source) : https://github.com/UniTy01/chauffageetmoi (privé)
- Repo AI OS (cleanup) : https://github.com/IA-optimist/chauffage-et-moi-ai-os (privé)
- Spec précédente du repo Astro : `docs/superpowers/specs/2026-05-22-redesign-pro-epure-design.md` (refonte design)
- Commit ayant introduit `/realisations` : `8867409`
- Commit photos FB intégrées (vague précédente) : `5bd901e`
