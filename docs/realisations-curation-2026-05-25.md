# Curation report — batch photos 2026-05-25

**Spec :** [`docs/superpowers/specs/2026-05-25-photos-realisations-design.md`](superpowers/specs/2026-05-25-photos-realisations-design.md)
**Plan :** [`docs/superpowers/plans/2026-05-25-photos-realisations.md`](superpowers/plans/2026-05-25-photos-realisations.md)
**Source archive :** `fb-photos-raw/` (gitignored, 90 fichiers)
**Generated:** generate_report.py from inventory + dedup + decisions

---

## Action utilisateur requise

Avant d'intégrer les 11 photos flagged GDPR_REVIEW (visages visibles,
tatouages, nom de technicien sur vêtement, etc.), contacter les clients
concernés pour demander leur consentement explicite à la ré-utilisation
des photos sur le site web Chauffage & Moi. À défaut → REJECT toute
photo dont le consentement ne peut être confirmé.

Note : les photos chevalier1-5 sont déjà REJECT (résolution insuffisante
/ HD non récupérée) et ne font pas partie des 11 GDPR_REVIEW.

---

## Summary stats

- **Total photos:** 90
- **RETAIN:** 39
- **REJECT:** 40
- **GDPR_REVIEW:** 11

### RETAIN by section

- chauffage: 20
- equipe: 1
- sanitaire: 18

### REJECT by reason category

- duplicate_of: 13
- branding_concern: 10
- resolution_low: 5
- internal_redundancy: 3
- quality_low: 3
- out_of_scope: 3
- test_artifact: 2
- gdpr_flag: 1

### GDPR / Consent flagged (user action required)

- `505856078_1367142621594832_3900921926060207193_n.jpg` — gdpr_flag:visage technicien identifiable dans miroir
- `506072748_1367142341594860_6894498717806398846_n.jpg` — gdpr_flag:visage technicien identifiable dans miroir
- `511259034_1379096173732810_7170544604337121982_n.jpg` — gdpr_flag:visage technicien identifiable
- `511271326_1379096240399470_3039710788010401142_n.jpg` — gdpr_flag:visage technicien identifiable de profil dans miroir
- `553439450_1461454378830322_3163556979362798352_n.jpg` — gdpr_flag:visage technicien identifiable de profil
- `557575390_1471961454446281_395246518502713190_n.jpg` — gdpr_flag:visages techniciens partiellement visibles, branding Solucalc
- `616826946_1565444018431357_2487977771249251836_n.jpg` — gdpr_flag:visage technicien clairement identifiable frontal
- `617041559_1565444345097991_531383307728102204_n.jpg` — gdpr_flag:visage technicien identifiable de profil
- `669663315_1640203424288749_6507569792376976246_n.jpg` — gdpr_flag:deux visages frontaux identifiables au salon
- `671505513_1640203337622091_4561133998002988089_n.jpg` — gdpr_flag:visage identifiable + prénom Sébastien lisible sur sweat
- `WhatsApp Image 2026-05-25 at 14.32.33 (4).jpeg` — gdpr_flag:visage technicien identifiable de profil

### Sections sans nouvelle photo dans ce batch

- **adoucisseur**: aucune photo Durlem retenue (catalog screenshots avec watermark). Le titre Adoucisseurs ne sera **pas renommé** en 'Solucalc & Durlem'.
- **pac**: aucune photo PAC trouvée dans le batch. La nouvelle section PAC ne sera **pas créée** dans Task 11.

---

## Décisions détaillées (table)

| # | Filename source | Origin | Decision | Section | New name | Caption | Reason / notes |
|---|---|---|---|---|---|---|---|
| 1 | 505715303_1367150891594005_8359931051889009865_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-pose.jpg | Plancher chauffant — pose en cours | ok |
| 2 | 505739580_1367142524928175_3882255712567675403_n.jpg | fb_cdn | RETAIN | sanitaire | sdb-baignoire-ilot-marbre.jpg | Salle de bain — baignoire îlot & vasques | ok |
| 3 | 505745796_1367143448261416_7463600088483636864_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-collecteur.jpg | Plancher chauffant — collecteur | ok |
| 4 | 505752607_1367143614928066_7363171778454237721_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-pose-2.jpg | Plancher chauffant — boucles posées | ok |
| 5 | 505762122_1367143634928064_2878281686866966067_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-pose-3.jpg | Plancher chauffant — vue ensemble | ok |
| 6 | 505778189_1367151424927285_8010192064447884492_n.jpg | fb_cdn | RETAIN | sanitaire | tuyauterie-per-attentes.jpg | Tuyauterie PER — attentes sanitaires | ok |
| 7 | 505781344_1367143658261395_2451199717174460876_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-pose-4.jpg | Plancher chauffant — boucles et attentes | ok |
| 8 | 505809818_1367151324927295_130113487534596999_n.jpg | fb_cdn | RETAIN | sanitaire | tuyauterie-per-cave.jpg | Tuyauterie PER — passage en cave | ok |
| 9 | 505850206_1367142438261517_3998240218856399798_n.jpg | fb_cdn | RETAIN | sanitaire | douche-italienne-marbre.jpg | Douche italienne — marbre et robinetterie noire | ok |
| 10 | 505856078_1367142621594832_3900921926060207193_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien identifiable dans miroir |
| 11 | 505917546_1367151364927291_6818782755831528363_n.jpg | fb_cdn | RETAIN | sanitaire | tuyauterie-per-attentes-2.jpg | Tuyauterie PER — attentes au sol | ok |
| 12 | 505946141_1367142424928185_160378837578612467_n.jpg | fb_cdn | RETAIN | sanitaire | sdb-marbre-vasque-radiateur.jpg | Salle de bain — marbre et sèche-serviettes | ok |
| 13 | 505984752_1367143458261415_8430822973836388834_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-pose-5.jpg | Plancher chauffant — préparation séjour | ok |
| 14 | 506000874_1367143528261408_9070580305535782837_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-detail.jpg | Plancher chauffant — détail des boucles | ok |
| 15 | 506026148_1367143534928074_977970733424288984_n.jpg | fb_cdn | REJECT | — | — | — | internal_redundancy:505762122_1367143634928064_2878281686866966067_n.jpg |
| 16 | 506050053_1367151391593955_6926509918580892020_n.jpg | fb_cdn | REJECT | — | — | — | internal_redundancy:505809818_1367151324927295_130113487534596999_n.jpg |
| 17 | 506068299_1367143711594723_7512096908092396721_n.jpg | fb_cdn | RETAIN | chauffage | plancher-chauffant-finition.jpg | Plancher chauffant — finition | ok |
| 18 | 506072748_1367142341594860_6894498717806398846_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien identifiable dans miroir |
| 19 | 506155571_1367143744928053_4073484974642366638_n.jpg | fb_cdn | REJECT | — | — | — | quality_low:sujet vide, préparation sans valeur visuelle |
| 20 | 506221135_1367142434928184_7694144466731108434_n.jpg | fb_cdn | RETAIN | sanitaire | sdb-marbre-wc-vasque.jpg | Salle de bain — WC et vasque marbre | ok |
| 21 | 506269464_1367142541594840_6500118612137345960_n.jpg | fb_cdn | RETAIN | sanitaire | sdb-ensemble-vasques-douche.jpg | Salle de bain — ensemble vasques et douche | ok |
| 22 | 506395398_1367142344928193_1076551269166995612_n.jpg | fb_cdn | RETAIN | sanitaire | douche-italienne-radiateur-design.jpg | Douche italienne et radiateur design | ok |
| 23 | 510392443_1379096177066143_7225970190946925854_n.jpg | fb_cdn | RETAIN | chauffage | chauffe-eau-vaillant-gaz.jpg | Chauffe-eau Vaillant — gaz mural | ok |
| 24 | 511259034_1379096173732810_7170544604337121982_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien identifiable |
| 25 | 511271326_1379096240399470_3039710788010401142_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien identifiable de profil dans miroir |
| 26 | 511955646_1378041427171618_2673421204817530092_n.jpg | fb_cdn | REJECT | — | — | — | out_of_scope:image promo marketing avec overlay texte, pas une installation réelle |
| 27 | 514314724_1386472809661813_1004118655756434806_n.jpg | fb_cdn | RETAIN | sanitaire | tuyauterie-per-cave-2.jpg | Tuyauterie PER — desserte en cave | ok |
| 28 | 515299436_1386472766328484_680624745855678790_n.jpg | fb_cdn | RETAIN | sanitaire | collecteur-sanitaire-cave.jpg | Collecteur sanitaire — cave voûtée | ok |
| 29 | 553439450_1461454378830322_3163556979362798352_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien identifiable de profil |
| 30 | 556824223_1470153641293729_632089620159420923_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-mazout-jaune.jpg | Chaudière mazout — cave | ok |
| 31 | 557575390_1471961454446281_395246518502713190_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visages techniciens partiellement visibles, branding Solucalc |
| 32 | 559205457_1478198673822559_6351489735977666709_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-bulex-cave-pierre.jpg | Chaudière Bulex — cave en pierre | ok |
| 33 | 559932657_1478198647155895_4495355457524993415_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-mazout-ancienne.jpg | Ancienne chaudière mazout — avant remplacement | ok |
| 34 | 560260804_1481647080144385_2889602032549299492_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-vaillant-cuisine.jpg | Chaudière Vaillant — intégrée cuisine | ok |
| 35 | 561347495_1481647076811052_1948641619351308549_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-vaillant-collecteur.jpg | Chaudière Vaillant — collecteur détaillé | ok |
| 36 | 566227794_1489299406045819_2816806803850950169_n.jpg | fb_cdn | RETAIN | chauffage | radiateur-classique-blanc.jpg | Radiateur classique — installation neuve | ok |
| 37 | 567466137_1488232172819209_8793140319627643472_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-entretien-avant.jpg | Chaudière — chambre de combustion avant nettoyage | ok |
| 38 | 569859579_1488232176152542_6959485024647516488_n.jpg | fb_cdn | REJECT | — | — | — | internal_redundancy:567466137_1488232172819209_8793140319627643472_n.jpg |
| 39 | 571120557_1489299402712486_2119913224468578150_n.jpg | fb_cdn | RETAIN | chauffage | radiateur-ancien-fonte.jpg | Ancien radiateur — avant remplacement | ok |
| 40 | 597387450_1532913091684450_4902159909975629084_n.jpg | fb_cdn | RETAIN | sanitaire | sdb-renovation-complete.jpg | Salle de bain — rénovation complète | ok |
| 41 | 605132268_1544261043882988_1142087667529373180_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-vaillant-garage.jpg | Chaudière Vaillant — garage | ok |
| 42 | 605169282_1549824309993328_3070978278460022861_n.jpg | fb_cdn | RETAIN | chauffage | chaudiere-vaillant-sdb.jpg | Chaudière Vaillant — salle de bain | ok |
| 43 | 616826946_1565444018431357_2487977771249251836_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien clairement identifiable frontal |
| 44 | 617041559_1565444345097991_531383307728102204_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien identifiable de profil |
| 45 | 619425107_1569883801320712_8325618435518124697_n.jpg | fb_cdn | REJECT | — | — | — | gdpr_flag:document personnel avec nom (attestation formation Vaillant) |
| 46 | 669663315_1640203424288749_6507569792376976246_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:deux visages frontaux identifiables au salon |
| 47 | 669845710_1640203287622096_8463383596457286116_n.jpg | fb_cdn | REJECT | — | — | — | out_of_scope:selfie thermique salon, pas une installation; gdpr_flag visage identifiable |
| 48 | 671505513_1640203337622091_4561133998002988089_n.jpg | fb_cdn | GDPR_REVIEW | — | — | — | gdpr_flag:visage identifiable + prénom Sébastien lisible sur sweat |
| 49 | 699731127_1671564807819277_109218284738484393_n.jpg | fb_cdn | RETAIN | chauffage | poele-pellets-noir.jpg | Poêle à pellets — salon | ok |
| 50 | Capture d'écran 2026-05-25 191033.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit, pas une installation |
| 51 | Capture d'écran 2026-05-25 191042.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 52 | Capture d'écran 2026-05-25 191048.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 53 | Capture d'écran 2026-05-25 191053.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 54 | Capture d'écran 2026-05-25 191101.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 55 | Capture d'écran 2026-05-25 191105.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 56 | Capture d'écran 2026-05-25 191110.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 57 | Capture d'écran 2026-05-25 191115.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 58 | Capture d'écran 2026-05-25 191122.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 59 | Capture d'écran 2026-05-25 191130.png | durlem | REJECT | — | — | — | branding_concern:durlem_watermark; catalog/produit |
| 60 | WhatsApp Image 2026-05-25 at 14.32.33 (1).jpeg | whatsapp | RETAIN | sanitaire | sdb-cabine-douche.jpg | Salle de bain — cabine de douche et vasque | ok |
| 61 | WhatsApp Image 2026-05-25 at 14.32.33 (2).jpeg | whatsapp | RETAIN | sanitaire | sanitaire-arrivees-eau.jpg | Sanitaire — arrivées eau avant pose | ok |
| 62 | WhatsApp Image 2026-05-25 at 14.32.33 (3).jpeg | whatsapp | RETAIN | equipe | technicien-pose-enduit.jpg | Technicien — préparation murs douche | ok |
| 63 | WhatsApp Image 2026-05-25 at 14.32.33 (4).jpeg | whatsapp | GDPR_REVIEW | — | — | — | gdpr_flag:visage technicien identifiable de profil |
| 64 | WhatsApp Image 2026-05-25 at 14.32.33.jpeg | whatsapp | RETAIN | sanitaire | sdb-carrelage-attentes-douche.jpg | Salle de bain — carrelage et attentes douche | ok |
| 65 | WhatsApp Image 2026-05-25 at 14.32.34 (1).jpeg | whatsapp | REJECT | — | — | — | quality_low:gros plan étanchéité, sujet peu valorisant |
| 66 | WhatsApp Image 2026-05-25 at 14.32.34 (2).jpeg | whatsapp | RETAIN | sanitaire | sdb-vasque-meuble-bois.jpg | Salle de bain — vasque sur meuble bois | ok |
| 67 | WhatsApp Image 2026-05-25 at 14.32.34 (3).jpeg | whatsapp | RETAIN | sanitaire | douche-italienne-receveur-noir.jpg | Douche italienne — receveur noir | ok |
| 68 | WhatsApp Image 2026-05-25 at 14.32.34 (4).jpeg | whatsapp | REJECT | — | — | — | out_of_scope:animal (chien) domine la photo au premier plan |
| 69 | WhatsApp Image 2026-05-25 at 14.32.34.jpeg | whatsapp | REJECT | — | — | — | quality_low:chantier intermédiaire (étanchéité), sujet pas valorisant |
| 70 | WhatsApp Image 2026-05-25 at 14.32.35.jpeg | whatsapp | RETAIN | sanitaire | sdb-renovation-douche.jpg | Salle de bain — rénovation douche italienne | ok |
| 71 | 505835700_1367142644928163_6604257248505875663_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:douche-italienne-motifs.jpg (phash dist 0) |
| 72 | 505884755_1367142348261526_822390829856563562_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:sdb-baignoire-balneo-marbre.jpg (phash dist 0) |
| 73 | 505946141_1367142598261501_8589627597247799015_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:sdb-double-vasque-bois.jpg (phash dist 0) |
| 74 | 506520710_1367142534928174_2202700572756059072_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:radiateur-design-noir.jpg (phash dist 0) |
| 75 | 510810508_1379096210399473_502783475168340195_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:chauffe-eau-atlantic.jpg (phash dist 0) |
| 76 | 523360329_1402863128022781_3621832922668640343_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:equipe-chauffage-et-moi.jpg (phash dist 0) |
| 77 | 557605317_1471961494446277_442497104161034362_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:solucalc-equipe-installation.jpg (phash dist 0) |
| 78 | 558866546_1470153794627047_1470493806414523559_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:chaudiere-vaillant-brique.jpg (phash dist 0) |
| 79 | 558880201_1478198650489228_6813298401772047650_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:chaudiere-vaillant-cave.jpg (phash dist 0) |
| 80 | 558884123_1471961467779613_6518078313470074353_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:solucalc-bouteille-co2.jpg (phash dist 0) |
| 81 | 559120829_1478198680489225_1276054509151199158_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:chaudiere-vaillant-pierre.jpg (phash dist 0) |
| 82 | 596296151_1532913061684453_3763110001333624553_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:sdb-baignoire-ilot-moderne.jpg (phash dist 0) |
| 83 | 615894827_1563758791933213_4644901959511154799_n.jpg | fb_cdn | REJECT | — | — | — | duplicate_of:solucalc-installateur-agree.jpg (phash dist 0) |
| 84 | chevalier1.webp | chevalier | REJECT | — | — | — | resolution_low:125x125; chevalier_hd_unavailable; consent_not_obtained |
| 85 | chevalier2.webp | chevalier | REJECT | — | — | — | resolution_low:125x125; chevalier_hd_unavailable; consent_not_obtained |
| 86 | chevalier3.webp | chevalier | REJECT | — | — | — | resolution_low:125x125; chevalier_hd_unavailable; consent_not_obtained |
| 87 | chevalier4.webp | chevalier | REJECT | — | — | — | resolution_low:125x125; chevalier_hd_unavailable; consent_not_obtained |
| 88 | chevalier5.webp | chevalier | REJECT | — | — | — | resolution_low:125x125; chevalier_hd_unavailable; consent_not_obtained |
| 89 | fb-race-test.jpg | test | REJECT | — | — | — | test_artifact |
| 90 | fb-test-photo-0.jpg | test | REJECT | — | — | — | test_artifact |
