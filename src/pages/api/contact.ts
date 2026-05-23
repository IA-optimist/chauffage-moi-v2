import type { APIRoute } from 'astro';
import { Resend } from 'resend';

export const prerender = false;

const FROM_EMAIL = 'Chauffage & Moi <contact@chauffageetmoi.com>';
const TO_EMAIL = 'chauffagesanitaire@outlook.com';

interface ContactPayload {
  typeDemande?: string;
  prenom?: string;
  nom?: string;
  telephone?: string;
  email?: string;
  ville?: string;
  logement?: string;
  chauffageActuel?: string;
  travaux?: string[];
  delai?: string;
  dispo?: string;
  message?: string;
  hp?: string;
}

const typeLabels: Record<string, string> = {
  chauffage: 'Installation chauffage',
  pac: 'Pompe à chaleur',
  sanitaire: 'Sanitaire / Salle de bain',
  depannage: 'Dépannage urgent',
};

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function row(label: string, value: string | undefined | null): string {
  if (!value || (Array.isArray(value) && value.length === 0)) return '';
  return `<tr><td style="padding:8px 12px;background:#f5f5f4;font-weight:600;color:#0F2A44;width:160px;">${escapeHtml(label)}</td><td style="padding:8px 12px;color:#1c1917;">${escapeHtml(String(value))}</td></tr>`;
}

function buildHtml(d: ContactPayload): string {
  const typeLabel = typeLabels[d.typeDemande || ''] || d.typeDemande || '—';
  const nomComplet = `${d.prenom || ''} ${d.nom || ''}`.trim() || '—';
  const travaux = (d.travaux && d.travaux.length) ? d.travaux.join(', ') : null;
  const messageHtml = d.message ? `<div style="margin-top:24px;padding:16px;background:#fff1e6;border-left:4px solid #C2632A;border-radius:4px;"><p style="margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:#A8521F;font-weight:700;">Message du client</p><p style="margin:0;white-space:pre-wrap;color:#1c1917;">${escapeHtml(d.message)}</p></div>` : '';

  return `<!doctype html><html><body style="margin:0;padding:0;background:#f5f5f4;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
<div style="max-width:640px;margin:0 auto;padding:32px 16px;">
  <div style="background:#0F2A44;color:#fff;padding:24px 32px;border-radius:8px 8px 0 0;">
    <h1 style="margin:0 0 4px;font-size:20px;font-weight:800;letter-spacing:-0.02em;">Nouvelle demande de devis</h1>
    <p style="margin:0;color:#94a3b8;font-size:14px;">Reçue via chauffage-mirror.vercel.app</p>
  </div>
  <div style="background:#fff;padding:24px 32px;border-radius:0 0 8px 8px;border:1px solid #e7e5e4;border-top:none;">
    <p style="margin:0 0 16px;font-size:16px;color:#1c1917;"><strong style="color:#C2632A;">${escapeHtml(typeLabel)}</strong></p>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      ${row('Nom', nomComplet)}
      ${row('Téléphone', d.telephone)}
      ${row('Email', d.email)}
      ${row('Ville / CP', d.ville)}
      ${row('Logement', d.logement)}
      ${row('Chauffage actuel', d.chauffageActuel)}
      ${row('Travaux souhaités', travaux)}
      ${row('Délai', d.delai)}
      ${row('Disponibilités', d.dispo)}
    </table>
    ${messageHtml}
    <p style="margin:24px 0 0;padding-top:16px;border-top:1px solid #e7e5e4;font-size:12px;color:#78716c;">Réponds directement à cet email pour contacter le client (Reply-To configuré).</p>
  </div>
</div>
</body></html>`;
}

function buildText(d: ContactPayload): string {
  const typeLabel = typeLabels[d.typeDemande || ''] || d.typeDemande || '—';
  const lines = [
    'Nouvelle demande de devis — Chauffage & Moi',
    '',
    `Type : ${typeLabel}`,
    `Nom : ${d.prenom || ''} ${d.nom || ''}`.trim(),
    `Téléphone : ${d.telephone || '—'}`,
    d.email ? `Email : ${d.email}` : null,
    `Ville/CP : ${d.ville || '—'}`,
    '',
    d.logement ? `Logement : ${d.logement}` : null,
    d.chauffageActuel ? `Chauffage actuel : ${d.chauffageActuel}` : null,
    (d.travaux && d.travaux.length) ? `Travaux : ${d.travaux.join(', ')}` : null,
    d.delai ? `Délai : ${d.delai}` : null,
    d.dispo ? `Disponibilités : ${d.dispo}` : null,
    '',
    d.message ? `Message :\n${d.message}` : null,
  ].filter(Boolean);
  return lines.join('\n');
}

export const POST: APIRoute = async ({ request }) => {
  let payload: ContactPayload;
  try {
    payload = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'invalid_json' }), { status: 400, headers: { 'Content-Type': 'application/json' } });
  }

  // Honeypot anti-spam : si hp est rempli, c'est un bot
  if (payload.hp && payload.hp.trim() !== '') {
    return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }

  // Validation minimale
  if (!payload.typeDemande || !payload.prenom || !payload.nom || !payload.telephone || !payload.ville) {
    return new Response(JSON.stringify({ error: 'missing_required_fields' }), { status: 400, headers: { 'Content-Type': 'application/json' } });
  }

  const apiKey = import.meta.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error('RESEND_API_KEY not configured');
    return new Response(JSON.stringify({ error: 'server_not_configured' }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }

  const resend = new Resend(apiKey);
  const typeLabel = typeLabels[payload.typeDemande] || payload.typeDemande;
  const nomComplet = `${payload.prenom} ${payload.nom}`.trim();

  try {
    const { error } = await resend.emails.send({
      from: FROM_EMAIL,
      to: [TO_EMAIL],
      replyTo: payload.email && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(payload.email) ? payload.email : undefined,
      subject: `Demande de devis — ${typeLabel} — ${nomComplet}`,
      html: buildHtml(payload),
      text: buildText(payload),
    });

    if (error) {
      console.error('Resend error:', error);
      return new Response(JSON.stringify({ error: 'send_failed', detail: error.message }), { status: 502, headers: { 'Content-Type': 'application/json' } });
    }

    return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } catch (e: any) {
    console.error('Unexpected error:', e);
    return new Response(JSON.stringify({ error: 'unexpected', detail: String(e?.message || e) }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
};
