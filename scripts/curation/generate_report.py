"""Generate the markdown curation report from inventory + dedup + decisions."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def render_table(decisions: list[dict], dups: dict) -> str:
    rows = ["| # | Filename source | Origin | Decision | Section | New name | Caption | Reason / notes |",
            "|---|---|---|---|---|---|---|---|"]
    for i, d in enumerate(decisions, 1):
        reason = d.get("reason") or ""
        if d["filename"] in dups:
            m = dups[d["filename"]]
            reason = f"duplicate_of:{m['match']} (phash dist {m['distance']})"
        rows.append(
            f"| {i} | {d['filename']} | {d['origin']} | {d['decision']} | "
            f"{d.get('section') or '—'} | {d.get('new_name') or '—'} | "
            f"{d.get('caption') or '—'} | {reason} |"
        )
    return "\n".join(rows)


def render_summary(decisions: list[dict]) -> str:
    by_decision = Counter(d["decision"] for d in decisions)
    by_section = Counter(d["section"] for d in decisions if d["decision"] == "RETAIN")
    by_reject = Counter(d["reason"].split(":")[0] for d in decisions if d["decision"] == "REJECT")
    gdpr = [d for d in decisions if d.get("gdpr_flag")]

    out = ["## Summary stats", ""]
    out.append(f"- **Total photos:** {len(decisions)}")
    for k in ("RETAIN", "REJECT", "GDPR_REVIEW"):
        out.append(f"- **{k}:** {by_decision.get(k, 0)}")
    out += ["", "### RETAIN by section", ""]
    for sec, n in sorted(by_section.items()):
        out.append(f"- {sec}: {n}")
    out += ["", "### REJECT by reason category", ""]
    for r, n in sorted(by_reject.items(), key=lambda x: -x[1]):
        out.append(f"- {r}: {n}")
    out += ["", "### GDPR / Consent flagged (user action required)", ""]
    if gdpr:
        for d in gdpr:
            out.append(f"- `{d['filename']}` — {d.get('reason') or ''}")
    else:
        out.append("- (none)")
    return "\n".join(out)


def main():
    inventory = json.load(open(sys.argv[1]))           # /tmp/inventory.json
    dups = json.load(open(sys.argv[2]))["vs_reference"] # /tmp/dedup.json
    decisions_path = Path(sys.argv[3])                  # curation-decisions.json
    decisions = [json.loads(l) for l in decisions_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    out_path = Path(sys.argv[4])                        # final report path

    body = f"""# Curation report — batch photos 2026-05-25

**Spec :** [`docs/superpowers/specs/2026-05-25-photos-realisations-design.md`](superpowers/specs/2026-05-25-photos-realisations-design.md)
**Plan :** [`docs/superpowers/plans/2026-05-25-photos-realisations.md`](superpowers/plans/2026-05-25-photos-realisations.md)
**Source archive :** `fb-photos-raw/` (gitignored, {inventory['total']} fichiers)
**Generated:** {Path(__file__).name} from inventory + dedup + decisions

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

{render_summary(decisions)}

---

## Décisions détaillées (table)

{render_table(decisions, dups)}
"""
    out_path.write_text(body, encoding="utf-8")
    print(f"Report written: {out_path}")


if __name__ == "__main__":
    main()
