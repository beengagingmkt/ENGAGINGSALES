"""Diagnóstico gratuito de presença digital: página HTML com gráficos (SVG), pronta para web e para PDF.

Funções puras: recebem o lead (data + intel), os concorrentes da mesma categoria e cidade, o perfil da
agência e, se houver, o texto do Claude. Não fazem rede nem banco.
"""
import html, math, re
from datetime import datetime

RED, INK, OK, WARN, BAD = "#d7141f", "#111318", "#16a34a", "#f59e0b", "#dc2626"


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))


def status(v):
    return ("Bom", OK) if v >= 75 else ("Atenção", WARN) if v >= 45 else ("Crítico", BAD)


def areas(d, i):
    """Nota 0 a 100 por área, com o que vimos e o que fazer."""
    rating, reviews, kind = i.get("rating") or 0, i.get("reviews") or 0, i.get("site_kind")
    insta, hours, photo = bool(i.get("instagram")), bool(d.get("open_hours")), bool(d.get("thumbnail"))
    desc = bool(d.get("descriptions") or d.get("about"))
    food = bool(re.search(r"restaur|hamburg|burger|pizz|lanch|bar|caf|padaria|confeit|sorvet|a[cç]a[ií]|sushi|churras|delivery|comida|pastel|marmit|petisc|xis|parrilla",
                          f"{d.get('category')} {d.get('categories')} {d.get('title')}", re.I))
    delivery = bool(re.search(r"delivery|entrega", f"{d.get('category')} {d.get('categories')} {d.get('title')}", re.I)) or kind == "plataforma"

    g = 100 - (30 if not photo else 0) - (20 if not hours else 0) - (25 if not insta else 0) - (10 if not desc else 0)
    av = clamp(round(clamp((rating - 3) / 2 * 60, 0, 60) + clamp(math.log10(reviews + 1) / math.log10(500) * 40, 0, 40))) if reviews else 5
    st = {"próprio": 100, "plataforma": 40, "rede social": 25}.get(kind, 0)
    ig = 100 if insta else 0
    ia = clamp((40 if kind == "próprio" else 10 if kind != "nenhum" else 0) + (30 if reviews >= 100 else 15 if reviews >= 30 else 0)
               + (15 if desc or d.get("categories") else 0) + (15 if hours else 0))

    def notes(lst):
        return [x for x in lst if x]

    out = [
        {"key": "google", "nome": "Perfil no Google", "nota": clamp(g),
         "vimos": notes([("Sem fotos no perfil" if not photo else "Tem foto de capa"),
                         ("Horário de funcionamento não preenchido" if not hours else "Horário preenchido"),
                         ("Instagram não conectado ao Google Meu Negócio" if not insta else "Instagram encontrado"),
                         ("Sem descrição do negócio" if not desc else None)]),
         "fazer": notes(["Subir fotos recentes" + (" dos pratos, do ambiente e do cardápio" if food else " do espaço e do trabalho") if not photo else None,
                         "Preencher os horários, inclusive feriados" if not hours else None,
                         "Conectar o Instagram no perfil do Google Meu Negócio" if not insta else None,
                         "Escrever uma descrição com as palavras que o cliente pesquisa" if not desc else None,
                         "Postar novidades no perfil toda semana, o Google valoriza perfil ativo"])},
        {"key": "avaliacoes", "nome": "Avaliações e reputação", "nota": av,
         "vimos": [f"{reviews} avaliações com nota {str(round(rating, 1)).replace('.', ',')}" if reviews else "Nenhuma avaliação encontrada"],
         "fazer": notes([("Deixar um flyer com QR code no balcão ou na mesa: a pessoa escaneia, avalia e ganha um brinde" if not (delivery and not food) else None)
                         if (rating < 4.5 or reviews < 100) else None,
                         "Mandar uma mensagem pedindo avaliação para quem já comprou, por uma plataforma de disparo" if delivery else None,
                         "Responder todas as avaliações, principalmente as negativas, com educação e solução",
                         "Criar a rotina de pedir avaliação no fim de todo atendimento"])},
        {"key": "site", "nome": "Site próprio", "nota": st,
         "vimos": [{"próprio": "Tem site próprio", "plataforma": "Depende de plataforma ou link de terceiros",
                    "rede social": "O link do Google leva só para a rede social", "nenhum": "Não tem site"}.get(kind, "Não tem site")],
         "fazer": notes(["Ter um site próprio rápido, com " + ("cardápio, reserva e pedido" if food else "serviços, fotos e botão de WhatsApp") if kind != "próprio" else
                         "Revisar se o site carrega rápido no celular e tem o endereço e o WhatsApp bem visíveis",
                         "Colocar o link do site no perfil do Google", "Usar no site as palavras que o cliente da região pesquisa"])},
        {"key": "instagram", "nome": "Instagram", "nota": ig,
         "vimos": ["Instagram encontrado e ligado ao negócio" if insta else "Não encontramos o Instagram ligado ao perfil do Google"],
         "fazer": notes(["Conectar o Instagram ao Google Meu Negócio e ao site" if not insta else "Manter a bio com o link de pedido, reserva ou WhatsApp",
                         "Postar com frequência fotos reais" + (" dos pratos" if food else " do trabalho") + " e depoimentos de clientes"])},
        {"key": "ia", "nome": "ChatGPT e buscas por IA", "nota": ia,
         "vimos": ["O ChatGPT e o Google indicam negócios que têm site, boas avaliações e informações completas"],
         "fazer": ["Ter site próprio com textos claros sobre o que vocês fazem e onde atendem",
                   "Aumentar o número de avaliações e manter a nota alta",
                   "Manter nome, endereço, telefone e horário iguais em todos os lugares"]},
    ]
    weights = {"google": 25, "avaliacoes": 25, "site": 20, "instagram": 15, "ia": 15}
    total = round(sum(a["nota"] * weights[a["key"]] for a in out) / 100)
    return out, total, food, delivery


def gauge(v):
    lbl, col = status(v)
    a = math.pi * (1 - v / 100)
    x, y = 150 + 110 * math.cos(a), 140 - 110 * math.sin(a)
    big = 0
    return f"""<svg viewBox="0 0 300 175" class="gauge"><path d="M40 140 A110 110 0 0 1 260 140" fill="none" stroke="#eceef3" stroke-width="22" stroke-linecap="round"/>
<path d="M40 140 A110 110 0 {big} 1 {x:.1f} {y:.1f}" fill="none" stroke="{col}" stroke-width="22" stroke-linecap="round"/>
<text x="150" y="128" text-anchor="middle" font-size="54" font-weight="800" fill="{INK}">{v}</text>
<text x="150" y="160" text-anchor="middle" font-size="15" font-weight="700" fill="{col}">{lbl.upper()}</text></svg>"""


def bars(ars):
    rows = []
    for k, a in enumerate(ars):
        lbl, col = status(a["nota"])
        y = k * 46
        w = max(6, 4.2 * a["nota"])
        rows.append(f"""<text x="0" y="{y + 17}" font-size="14" font-weight="600" fill="{INK}">{e(a['nome'])}</text>
<rect x="0" y="{y + 24}" width="420" height="12" rx="6" fill="#eceef3"/><rect x="0" y="{y + 24}" width="{w:.0f}" height="12" rx="6" fill="{col}"/>
<text x="440" y="{y + 35}" font-size="14" font-weight="800" fill="{col}">{a['nota']}</text>""")
    return f'<svg viewBox="0 0 480 {len(ars) * 46}" class="bars">{"".join(rows)}</svg>'


def compare(me, avg, lead, label, fmt, maxv=None):
    vals = [("Vocês", me, RED), ("Média da região", avg, "#9aa1b2"), ("Líder", lead, INK)]
    mx = maxv or max(1, *(v for _, v, _ in vals))
    rows = []
    for k, (n, v, c) in enumerate(vals):
        y = k * 34
        w = max(4, 300 * (v or 0) / mx)
        rows.append(f"""<text x="0" y="{y + 20}" font-size="13" fill="#5b6273">{n}</text>
<rect x="120" y="{y + 7}" width="{w:.0f}" height="18" rx="5" fill="{c}"/><text x="{128 + w:.0f}" y="{y + 21}" font-size="13" font-weight="800" fill="{INK}">{fmt(v)}</text>""")
    return f'<div class="cmp"><h4>{e(label)}</h4><svg viewBox="0 0 480 104">{"".join(rows)}</svg></div>'


def render(d, i, peers, pf, ai=None, logo="", city="", when=None):
    when = when or datetime.now()
    ai = ai or {}
    ars, total, food, delivery = areas(d, i)
    for a in ars:
        t = (ai.get("areas") or {}).get(a["key"])
        if t:
            a["ia"] = t
    name = d.get("title") or ""
    cat = d.get("category") or ""
    lbl, col = status(total)
    rating, reviews = i.get("rating") or 0, i.get("reviews") or 0
    pow_ = lambda x: (x.get("rating") or 0) * math.log10((x.get("reviews") or 0) + 1)
    pr = [p for p in peers if p.get("reviews")]
    cmp_html, rank_html = "", ""
    if len(pr) >= 3:
        avg_r = sum(p["reviews"] for p in pr) / len(pr)
        avg_n = sum(p["rating"] for p in pr) / len(pr)
        lead = max(pr, key=pow_)
        allp = sorted(pr + ([{"rating": rating, "reviews": reviews, "me": True}] if not any(p.get("me") for p in pr) else []),
                      key=pow_, reverse=True)
        pos = next((k + 1 for k, p in enumerate(allp) if p.get("me")), None)
        nfmt = lambda v: str(round(v or 0, 1)).replace(".", ",")
        cmp_html = (compare(reviews, round(avg_r), lead["reviews"], "Quantidade de avaliações no Google", lambda v: f"{round(v or 0)}")
                    + compare(rating, avg_n, lead["rating"], "Nota no Google", nfmt, maxv=5))
        if pos:
            rank_html = f"""<div class="rank"><div class="pos">#{pos}</div><div><b>de {len(allp)} {e(cat.lower() or 'negócios')} analisados{(' em ' + e(city)) if city else ''}</b>
<p>Posição pela força no Google (nota combinada com quantidade de avaliações). O líder é <b>{e(lead.get('title') or 'outro negócio')}</b>.</p></div></div>"""
    checks = [("Fotos no perfil", bool(d.get("thumbnail"))), ("Horário preenchido", bool(d.get("open_hours"))),
              ("Site próprio", i.get("site_kind") == "próprio"), ("Instagram conectado", bool(i.get("instagram"))),
              ("Mais de 100 avaliações", reviews >= 100), ("Nota 4,5 ou mais", rating >= 4.5), ("WhatsApp no perfil", bool(i.get("wa")))]
    acao = "reservar a mesa ou pedir delivery" if food and not delivery else "fazer o pedido" if food else "agendar ou chamar no WhatsApp"
    resumo = ai.get("resumo") or (
        f"Analisamos a presença digital de {name} com base nos dados públicos do Google. "
        + ("A base é boa e o cliente aprova o trabalho de vocês. " if rating >= 4.5 and reviews >= 50 else "")
        + "Abaixo estão os pontos que mais influenciam quem pesquisa no Google e no ChatGPT antes de escolher onde "
        + ("comer" if food else "comprar") + ", e o que dá para ajustar já.")
    plano = ai.get("plano") or [
        "Semana 1: completar o perfil do Google (fotos, horário, descrição e Instagram conectado)",
        "Semana 2: começar a rotina de avaliações com QR code e brinde" + (" e disparo para quem já comprou" if delivery else ""),
        "Semana 3: colocar no ar um site ou link da bio conectado ao Google, com " + ("reserva e pedido" if food else "WhatsApp e serviços"),
        "Semana 4: postar novidades no Google e no Instagram e medir as ligações, rotas e cliques no WhatsApp"]
    wa = re.sub(r"\D", "", pf.get("me_whatsapp") or "")
    site_label = re.sub(r"^https?://(www\.)?", "", pf.get("me_site") or "").rstrip("/")
    wa_txt = f"Oi {pf.get('me_name')}! Vi o diagnóstico da {name} e quero saber mais."
    services = [("📍", "Posicionamento no Google", "Perfil completo, otimizado e ativo para aparecer nas buscas da região e no ChatGPT."),
                ("🔗", "Link da bio conectado ao Google", f"Uma página bonita onde o cliente consegue {acao}, com ofertas do dia e avaliação no Google."),
                ("🌐", "Site próprio", "Rápido, feito para o celular e com o texto que o Google e o ChatGPT usam para indicar negócios."),
                ("🎯", "Tráfego pago", "Anúncios" + (" para restaurantes e delivery" if food else "") + " focados em quem está perto e com fome de comprar."),
                ("📸", "Fotografia" + (" e cardápio" if food else ""), "Fotos profissionais que vendem no Google, no Instagram e" + (" no cardápio." if food else " no site."))]
    if pf.get("me_method"):
        services.append(("🚀", pf["me_method"], pf.get("me_method_desc") or "Nosso método para vender mais com canal próprio."))
    area_html = "".join(f"""<div class="area"><div class="ah"><h3>{e(a['nome'])}</h3><span class="pill" style="background:{status(a['nota'])[1]}">{status(a['nota'])[0]} · {a['nota']}</span></div>
<div class="cols"><div><h5>O que vimos</h5><ul>{''.join(f'<li>{e(x)}</li>' for x in a['vimos'])}</ul></div>
<div><h5>O que fazer</h5><ul class="do">{''.join(f'<li>{e(x)}</li>' for x in a['fazer'][:4])}</ul></div></div>
{f'<p class="ai">{e(a["ia"])}</p>' if a.get('ia') else ''}</div>""" for a in ars)
    thumb = d.get("thumbnail") if str(d.get("thumbnail") or "").startswith("https://") else ""
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive"><title>Diagnóstico gratuito · {e(name)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:Inter,-apple-system,Segoe UI,Roboto,sans-serif;color:{INK};background:#f3f4f7;line-height:1.5}}
.page{{max-width:820px;margin:0 auto;background:#fff}}
.top{{display:flex;justify-content:space-between;align-items:center;padding:22px 36px;border-bottom:4px solid {RED}}}
.top img{{height:58px;margin:-12px -18px}}.top .by{{text-align:right;font-size:12px;color:#5b6273}}.top .by b{{display:block;color:{INK};font-size:14px}}
.hero{{padding:34px 36px 24px;display:grid;grid-template-columns:1fr 300px;gap:24px;align-items:center;background:linear-gradient(135deg,#fff 55%,#fff1f1)}}
.tag{{display:inline-block;background:{RED};color:#fff;font-size:11px;font-weight:800;letter-spacing:.14em;padding:5px 10px;border-radius:99px;text-transform:uppercase}}
h1{{font-size:34px;line-height:1.1;font-weight:900;margin:12px 0 6px;letter-spacing:-.02em}}.sub{{color:#5b6273;font-size:14px}}
.hero .ph{{width:74px;height:74px;border-radius:16px;background:#eee center/cover;margin-bottom:12px;border:3px solid #fff;box-shadow:0 6px 20px rgba(0,0,0,.12)}}
.gauge{{width:100%}}.gcap{{text-align:center;font-size:12px;color:#5b6273;margin-top:-6px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}}
section{{padding:26px 36px;border-top:1px solid #eceef3}}h2{{font-size:20px;font-weight:900;margin-bottom:12px;letter-spacing:-.01em}}
h2 small{{display:block;font-size:12px;color:{RED};letter-spacing:.14em;text-transform:uppercase;font-weight:800;margin-bottom:2px}}
.resumo{{font-size:15px;color:#2b303b}}
.checks{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;margin-top:14px}}
.chk{{display:flex;gap:10px;align-items:center;padding:10px 12px;border-radius:12px;background:#f6f7fa;font-size:13.5px;font-weight:600}}
.chk i{{width:22px;height:22px;border-radius:50%;display:grid;place-items:center;color:#fff;font-style:normal;font-size:13px;font-weight:900;flex:none}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}}.bars{{width:100%}}
.cmp h4{{font-size:13px;color:#5b6273;font-weight:700;margin-bottom:6px}}.cmp svg{{width:100%}}.cmp+.cmp{{margin-top:14px}}
.rank{{display:flex;gap:16px;align-items:center;margin-top:16px;padding:14px 16px;border-radius:14px;background:{INK};color:#fff}}
.rank .pos{{font-size:40px;font-weight:900;color:#fff;background:{RED};border-radius:12px;padding:4px 14px}}.rank p{{font-size:13px;color:#c8ccd6}}
.area{{border:1px solid #eceef3;border-radius:16px;padding:16px 18px;margin-bottom:12px;break-inside:avoid}}
.ah{{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px}}.ah h3{{font-size:16px;font-weight:800}}
.pill{{color:#fff;font-size:11.5px;font-weight:800;padding:4px 10px;border-radius:99px;white-space:nowrap}}
.cols{{display:grid;grid-template-columns:1fr 1.2fr;gap:18px}}h5{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8a90a0;margin-bottom:6px}}
ul{{list-style:none;font-size:13.5px}}li{{padding:3px 0 3px 18px;position:relative}}li:before{{content:"•";position:absolute;left:4px;color:#9aa1b2}}
ul.do li:before{{content:"→";color:{RED};font-weight:900;left:0}}
.ai{{margin-top:10px;padding:10px 12px;border-radius:10px;background:#fff6f6;border-left:3px solid {RED};font-size:13.5px}}
.why{{background:{INK};color:#fff}}.why h2{{color:#fff}}.why p{{color:#d4d7df;font-size:14.5px}}
.plan li{{padding:8px 0 8px 34px;border-bottom:1px dashed #e3e5ea;font-size:14px}}.plan li:before{{content:counter(s);counter-increment:s;left:0;top:7px;width:24px;height:24px;border-radius:50%;background:{RED};color:#fff;display:grid;place-items:center;font-size:12px;font-weight:800}}
.plan{{counter-reset:s}}
.svc{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.sv{{padding:14px;border-radius:14px;background:#f6f7fa;break-inside:avoid}}
.sv b{{display:block;font-size:14.5px;margin-bottom:3px}}.sv span{{font-size:13px;color:#5b6273}}.sv em{{font-style:normal;font-size:20px;display:block;margin-bottom:4px}}
.cta{{background:linear-gradient(135deg,{RED},#8f0b13);color:#fff;text-align:center;padding:30px 36px}}
.cta h2{{color:#fff;font-size:22px}}.cta p{{color:#ffd9db;font-size:14px;max-width:560px;margin:0 auto 16px}}
.btns{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}}.btns a{{display:inline-block;padding:12px 18px;border-radius:12px;font-weight:800;font-size:14px;text-decoration:none}}
.b1{{background:#fff;color:{RED}}}.b2{{background:rgba(255,255,255,.14);color:#fff;border:1px solid rgba(255,255,255,.4)}}
.example{{margin-top:12px;font-size:13px}}.example a{{color:{RED};font-weight:700}}
footer{{padding:16px 36px;font-size:11.5px;color:#8a90a0;text-align:center}}
@media (max-width:700px){{.hero,.grid2,.cols,.svc{{grid-template-columns:1fr}}h1{{font-size:28px}}.top,.hero,section{{padding-left:18px;padding-right:18px}}}}
@page{{size:A4;margin:0}}@media print{{body{{background:#fff}}.page{{max-width:none}}section,.area{{break-inside:avoid}}}}
</style></head><body><div class="page">
<div class="top">{f'<img src="{e(logo)}" alt="{e(pf.get("me_agency"))}">' if logo else f'<b>{e((pf.get("me_agency") or "Diagnóstico").upper())}</b>'}<div class="by"><b>{e(pf.get('me_agency'))}</b>{e(pf.get('me_city'))}{' · ' if pf.get('me_city') else ''}{when.strftime('%d/%m/%Y')}</div></div>
<div class="hero"><div>{f'<div class="ph" style="background-image:url({e(thumb)})"></div>' if thumb else ''}<span class="tag">Diagnóstico gratuito</span>
<h1>{e(name)}</h1><p class="sub">{e(cat)}{(' · ' + e(city)) if city else ''}<br>Como o seu negócio aparece hoje no Google e no ChatGPT</p></div>
<div>{gauge(total)}<div class="gcap">Nota de presença digital</div></div></div>
<section><h2><small>Resumo</small>O que encontramos</h2><p class="resumo">{e(resumo)}</p>
<div class="checks">{''.join(f'<div class="chk"><i style="background:{OK if ok else BAD}">{"✓" if ok else "✕"}</i>{e(n)}</div>' for n, ok in checks)}</div></section>
<section><div class="grid2"><div><h2><small>Raio X</small>Nota por área</h2>{bars(ars)}</div>
<div><h2><small>Concorrência</small>Vocês x região</h2>{cmp_html or '<p class="sub">Ainda não temos concorrentes suficientes da mesma categoria nesta região para comparar.</p>'}</div></div>{rank_html}</section>
<section class="why"><h2><small style="color:#ff8a90">Por que agora</small>A busca mudou</h2><p>Tem crescido muito a busca por {'restaurantes' if food else 'negócios locais'} direto no Google e no ChatGPT. Quem tem perfil completo, site próprio e muitas avaliações aparece primeiro e é indicado pela inteligência artificial. Quem não tem, fica invisível, principalmente nas épocas de mais venda.</p></section>
<section><h2><small>Ponto a ponto</small>O que dá para melhorar</h2>{area_html}</section>
<section><h2><small>Primeiros 30 dias</small>Plano de ação sugerido</h2><ul class="plan">{''.join(f'<li>{e(x)}</li>' for x in plano[:6])}</ul></section>
<section><h2><small>{e(pf.get('me_agency'))}</small>Como podemos ajudar</h2><div class="svc">{''.join(f'<div class="sv"><em>{a}</em><b>{e(b)}</b><span>{e(c)}</span></div>' for a, b, c in services)}</div>
{f'<p class="example">Exemplo de link da bio conectado ao Google de um cliente nosso: <a href="{e(pf.get("me_link"))}">{e(pf.get("me_link"))}</a></p>' if food and pf.get('me_link') else ''}</section>
<div class="cta"><h2>Quer ajuda para colocar isso em prática?</h2><p>{('Somos de ' + e(pf.get('me_city')) + ' e trabalhamos com vários negócios da região. ') if pf.get('me_city') else ''}Fica aqui a nossa sugestão, e se em algum momento fizer sentido, estamos à disposição para somar.</p>
<div class="btns">{f'<a class="b1" href="https://wa.me/{wa}?text={e(wa_txt)}">Falar no WhatsApp</a>' if wa else ''}{f'<a class="b2" href="{e(pf.get("me_instagram"))}">Instagram @{e(pf.get("me_instagram","").rstrip("/").split("/")[-1])}</a>' if pf.get('me_instagram') else ''}{f'<a class="b2" href="{e(pf.get("me_site"))}">{e(site_label)}</a>' if pf.get('me_site') else ''}</div></div>
<footer>Diagnóstico feito com base em dados públicos do Google em {when.strftime('%d/%m/%Y')}. Os números podem mudar a cada dia.</footer>
</div></body></html>"""
