"""
Nous Observatory — Dashboard Generator
Run: python3 generate_dashboard.py
Output: dashboard.html (open in any browser)
"""
import urllib.request, json, os
from datetime import datetime

URL = "https://yjupiuxuoxmycehkbmwl.supabase.co"
KEY = "sb_publishable_RUyNAQRYQq37O0IvOJ9kbQ_Cj8V0Yrr"
HEADERS = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
OUT = os.path.join(os.path.dirname(__file__), "dashboard.html")

def fetch(path):
    req = urllib.request.Request(f"{URL}/rest/v1/{path}", headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

print("Fetching data from Supabase...")
entities     = fetch("entities?select=*")
milestones   = fetch("milestones?select=id,entity_id,date,event,significance,strategic_signal,forward_implication_score,stack_layer,source_event,tags&order=date.asc")
relationships = fetch("relationships?select=*")
metrics      = fetch("key_metrics?select=*")
print(f"  {len(entities)} entities, {len(milestones)} milestones, {len(relationships)} relationships, {len(metrics)} metrics")

# --- build lookup maps ---
eid_to_name = {e["id"]: e["name"] for e in entities}
eid_to_entity = {e["id"]: e for e in entities}

# milestone counts per entity
from collections import defaultdict
m_count = defaultdict(int)
for m in milestones:
    m_count[m["entity_id"]] += 1

r_count = defaultdict(int)
for r in relationships:
    r_count[r["entity_id"]] += 1

km_count = defaultdict(int)
for k in metrics:
    km_count[k["entity_id"]] += 1

score5 = [m for m in milestones if m.get("forward_implication_score") == 5]
competitors = [r for r in relationships if r["relationship_type"] == "competitor"]

# milestones by year for chart
by_year = defaultdict(lambda: defaultdict(int))
for m in milestones:
    year = m["date"][:4]
    eid = m["entity_id"]
    name = eid_to_name.get(eid, "Unknown")
    by_year[year][name] += 1

years = sorted(by_year.keys())
company_names = sorted(set(e["name"] for e in entities if e["type"] == "company"))
people_names  = sorted(set(e["name"] for e in entities if e["type"] == "person"))

# per-entity metrics
entity_metrics = defaultdict(list)
for k in metrics:
    entity_metrics[k["entity_id"]].append(k)

entity_rels = defaultdict(list)
for r in relationships:
    entity_rels[r["entity_id"]].append(r)

generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# Colour palette for entities (deterministic by name hash)
COLORS = ["#6366f1","#8b5cf6","#ec4899","#f43f5e","#f97316",
          "#eab308","#22c55e","#14b8a6","#06b6d4","#3b82f6",
          "#a855f7","#ef4444","#f59e0b","#10b981","#0ea5e9","#84cc16"]
def color(name):
    return COLORS[hash(name) % len(COLORS)]

# --- Build JS data blobs ---
js_entities     = json.dumps(entities)
js_milestones   = json.dumps(milestones)
js_relationships = json.dumps(relationships)
js_metrics      = json.dumps(metrics)
js_score5       = json.dumps(score5)
js_eid_to_name  = json.dumps(eid_to_name)

# Timeline chart data: milestones per year (all entities combined by company vs person)
timeline_labels = json.dumps(years)
company_yearly = [sum(by_year[y].get(n, 0) for n in company_names) for y in years]
people_yearly  = [sum(by_year[y].get(n, 0) for n in people_names) for y in years]

# --- Entity cards HTML ---
def rel_badge(rel):
    colors = {"competitor":"#ef4444","investor":"#22c55e","partner":"#3b82f6","compute_provider":"#f97316"}
    c = colors.get(rel["relationship_type"], "#6b7280")
    return f'<span style="background:{c}22;color:{c};border:1px solid {c}44;padding:2px 7px;border-radius:12px;font-size:11px;white-space:nowrap">{rel["relationship_type"]}: {rel["related_entity"]}</span>'

def entity_card(e):
    eid = e["id"]
    name = e["name"]
    col = color(name)
    mc = m_count.get(eid, 0)
    rc = r_count.get(eid, 0)
    kc = km_count.get(eid, 0)
    rels_html = " ".join(rel_badge(r) for r in entity_rels.get(eid, [])[:4])
    top_metrics = entity_metrics.get(eid, [])[:3]
    metrics_html = "".join(f'<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #f1f5f9"><span style="color:#64748b;font-size:12px">{k["metric_name"]}</span><span style="font-size:12px;font-weight:600;color:#1e293b">{k["metric_value"]}</span></div>' for k in top_metrics)
    valuation = e.get("current_valuation") or "—"
    category  = e.get("category") or ""
    founded   = e.get("founded") or "—"
    hq        = e.get("headquarters") or "—"
    summary   = (e.get("trajectory_summary") or "")[:200] + "..."
    type_badge = f'<span style="background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:10px;font-size:11px">{e["type"]}</span>'
    return f'''
<div class="entity-card" data-type="{e["type"]}" data-name="{name.lower()}"
     style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:20px;cursor:pointer;transition:box-shadow 0.2s"
     onmouseenter="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.1)'"
     onmouseleave="this.style.boxShadow='none'"
     onclick="showEntity('{eid}')">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
    <div style="width:10px;height:10px;border-radius:50%;background:{col};flex-shrink:0"></div>
    <div style="font-weight:700;font-size:16px;color:#1e293b;flex:1">{name}</div>
    {type_badge}
  </div>
  <div style="font-size:12px;color:#64748b;margin-bottom:10px">{category}</div>
  <div style="display:flex;gap:16px;margin-bottom:12px">
    <div style="text-align:center"><div style="font-size:20px;font-weight:800;color:{col}">{mc}</div><div style="font-size:10px;color:#94a3b8;text-transform:uppercase">milestones</div></div>
    <div style="text-align:center"><div style="font-size:20px;font-weight:800;color:{col}">{rc}</div><div style="font-size:10px;color:#94a3b8;text-transform:uppercase">relations</div></div>
    <div style="text-align:center"><div style="font-size:20px;font-weight:800;color:{col}">{kc}</div><div style="font-size:10px;color:#94a3b8;text-transform:uppercase">metrics</div></div>
  </div>
  <div style="font-size:11px;color:#94a3b8;margin-bottom:6px">Founded {founded} · {hq}</div>
  {f'<div style="font-size:12px;font-weight:600;color:#1e293b;margin-bottom:8px">💰 {valuation}</div>' if valuation != "—" else ""}
  <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px">{rels_html}</div>
  {f'<div style="margin-top:8px">{metrics_html}</div>' if metrics_html else ""}
</div>'''

companies_cards = "\n".join(entity_card(e) for e in sorted(entities, key=lambda x: x["name"]) if e["type"] == "company")
people_cards    = "\n".join(entity_card(e) for e in sorted(entities, key=lambda x: x["name"]) if e["type"] == "person")

# Score-5 highlights
def score5_row(m):
    name = eid_to_name.get(m["entity_id"], "Unknown")
    col = color(name)
    evt = m.get("event", "")[:100]
    src = m.get("source_event") or ""
    src_badge = f'<span style="background:#fef3c7;color:#92400e;padding:1px 6px;border-radius:8px;font-size:10px;margin-left:6px">{src}</span>' if src else ""
    return f'''<tr>
      <td style="padding:10px 12px;white-space:nowrap;color:#64748b;font-size:13px">{m["date"]}</td>
      <td style="padding:10px 12px"><span style="font-weight:600;color:{col}">{name}</span></td>
      <td style="padding:10px 12px;font-size:13px">{evt}{src_badge}</td>
      <td style="padding:10px 12px;text-align:center"><span style="background:#fef2f2;color:#dc2626;font-weight:700;padding:3px 10px;border-radius:8px">5</span></td>
    </tr>'''

score5_rows = "\n".join(score5_row(m) for m in score5)

# Competitor table
def comp_row(r):
    name = eid_to_name.get(r["entity_id"], r["entity_id"])
    col  = color(name)
    col2 = color(r["related_entity"])
    return f'''<tr>
      <td style="padding:8px 12px"><span style="font-weight:600;color:{col}">{name}</span></td>
      <td style="padding:8px 12px;text-align:center;color:#94a3b8">⚔</td>
      <td style="padding:8px 12px"><span style="font-weight:600;color:{col2}">{r["related_entity"]}</span></td>
    </tr>'''

comp_rows = "\n".join(comp_row(r) for r in sorted(competitors, key=lambda x: eid_to_name.get(x["entity_id"], "")))

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nous Observatory</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js"></script>
<style>
  :root {{ color-scheme: light; --accent: #6366f1; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8fafc; color: #1e293b; }}
  .header {{ background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: white; padding: 32px 40px; }}
  .header h1 {{ font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }}
  .header p {{ color: #94a3b8; margin-top: 4px; font-size: 14px; }}
  .stats-bar {{ display: flex; gap: 24px; padding: 24px 40px; background: #fff; border-bottom: 1px solid #e2e8f0; flex-wrap: wrap; }}
  .stat {{ text-align: center; }}
  .stat-num {{ font-size: 32px; font-weight: 800; color: var(--accent); }}
  .stat-label {{ font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }}
  .main {{ padding: 32px 40px; max-width: 1400px; margin: 0 auto; }}
  .section-title {{ font-size: 20px; font-weight: 700; color: #0f172a; margin-bottom: 16px; margin-top: 40px; display: flex; align-items: center; gap: 8px; }}
  .tabs {{ display: flex; gap: 4px; margin-bottom: 20px; }}
  .tab {{ padding: 8px 18px; border-radius: 8px; border: none; background: #f1f5f9; color: #64748b; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.15s; }}
  .tab.active {{ background: var(--accent); color: white; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
  .search-bar {{ width: 100%; padding: 10px 16px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; margin-bottom: 16px; outline: none; }}
  .search-bar:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; }}
  thead {{ background: #f8fafc; }}
  th {{ padding: 12px 12px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; font-weight: 600; }}
  tbody tr:hover {{ background: #f8fafc; }}
  tbody tr {{ border-top: 1px solid #f1f5f9; }}
  .chart-wrap {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; }}
  /* Modal */
  #modal {{ display:none; position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:100; align-items:center; justify-content:center; }}
  #modal.open {{ display:flex; }}
  #modal-inner {{ background:#fff; border-radius:16px; max-width:700px; width:90%; max-height:80vh; overflow-y:auto; padding:32px; position:relative; }}
  #modal-close {{ position:absolute; top:16px; right:20px; font-size:22px; cursor:pointer; color:#94a3b8; background:none; border:none; }}
  .badge-5 {{ display:inline-block;background:#fef2f2;color:#dc2626;font-weight:700;padding:1px 8px;border-radius:6px;font-size:12px }}
  footer {{ text-align:center; padding:24px; color:#94a3b8; font-size:12px; margin-top:40px; }}
</style>
</head>
<body>
<div class="header">
  <h1>🔭 Nous Observatory</h1>
  <p>AI Intelligence Knowledge Graph · Snapshot {generated_at}</p>
</div>

<div class="stats-bar">
  <div class="stat"><div class="stat-num">21</div><div class="stat-label">Entities</div></div>
  <div class="stat"><div class="stat-num">190</div><div class="stat-label">Milestones</div></div>
  <div class="stat"><div class="stat-num">95</div><div class="stat-label">Relationships</div></div>
  <div class="stat"><div class="stat-num">97</div><div class="stat-label">Key Metrics</div></div>
  <div class="stat"><div class="stat-num">{len(score5)}</div><div class="stat-label">Score-5 Events</div></div>
  <div class="stat"><div class="stat-num">16</div><div class="stat-label">Companies</div></div>
  <div class="stat"><div class="stat-num">5</div><div class="stat-label">People</div></div>
</div>

<div class="main">

  <!-- Timeline chart -->
  <div class="section-title">📅 Milestone Timeline</div>
  <div class="chart-wrap">
    <canvas id="timelineChart" height="80"></canvas>
  </div>

  <!-- Entities -->
  <div class="section-title">🏢 Entities</div>
  <input class="search-bar" id="entitySearch" placeholder="Search entities..." oninput="filterCards()">
  <div class="tabs">
    <button class="tab active" onclick="filterType('all', this)">All (21)</button>
    <button class="tab" onclick="filterType('company', this)">Companies (16)</button>
    <button class="tab" onclick="filterType('person', this)">People (5)</button>
  </div>
  <div class="grid" id="entityGrid">
    {companies_cards}
    {people_cards}
  </div>

  <!-- Score-5 milestones -->
  <div class="section-title">⚡ Highest-Impact Events (Score 5/5) <span style="font-size:14px;font-weight:400;color:#94a3b8">{len(score5)} events</span></div>
  <table>
    <thead><tr>
      <th>Date</th><th>Entity</th><th>Event</th><th style="text-align:center">Score</th>
    </tr></thead>
    <tbody>{score5_rows}</tbody>
  </table>

  <!-- Competitor map -->
  <div class="section-title">⚔ Competitor Relationships</div>
  <table style="max-width:500px">
    <thead><tr><th>Entity</th><th></th><th>Competitor</th></tr></thead>
    <tbody>{comp_rows}</tbody>
  </table>

</div>

<!-- Entity detail modal -->
<div id="modal">
  <div id="modal-inner">
    <button id="modal-close" onclick="closeModal()">✕</button>
    <div id="modal-content"></div>
  </div>
</div>

<footer>Nous Observatory · Data as of {generated_at} · Re-run generate_dashboard.py to refresh</footer>

<script>
const ENTITIES = {js_entities};
const MILESTONES = {js_milestones};
const RELATIONSHIPS = {js_relationships};
const METRICS = {js_metrics};
const EID_NAME = {js_eid_to_name};

// ---- Timeline chart ----
const years = {timeline_labels};
const companyData = {json.dumps(company_yearly)};
const peopleData  = {json.dumps(people_yearly)};

new Chart(document.getElementById('timelineChart'), {{
  type: 'bar',
  data: {{
    labels: years,
    datasets: [
      {{ label: 'Company milestones', data: companyData, backgroundColor: 'rgba(99,102,241,0.7)', borderRadius: 4 }},
      {{ label: 'People milestones',  data: peopleData,  backgroundColor: 'rgba(236,72,153,0.7)', borderRadius: 4 }},
    ]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }}, tooltip: {{ mode: 'index' }} }},
    scales: {{ x: {{ stacked: true, grid: {{ display: false }} }}, y: {{ stacked: true, beginAtZero: true }} }}
  }}
}});

// ---- Filter cards ----
let currentType = 'all';
function filterCards() {{
  const q = document.getElementById('entitySearch').value.toLowerCase();
  document.querySelectorAll('.entity-card').forEach(c => {{
    const nameMatch = c.dataset.name.includes(q);
    const typeMatch = currentType === 'all' || c.dataset.type === currentType;
    c.style.display = nameMatch && typeMatch ? '' : 'none';
  }});
}}
function filterType(type, btn) {{
  currentType = type;
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  filterCards();
}}

// ---- Entity modal ----
function showEntity(eid) {{
  const e = ENTITIES.find(x => x.id === eid);
  if (!e) return;
  const ms = MILESTONES.filter(m => m.entity_id === eid).sort((a,b) => a.date.localeCompare(b.date));
  const rels = RELATIONSHIPS.filter(r => r.entity_id === eid);
  const km = METRICS.filter(k => k.entity_id === eid);

  const relColors = {{competitor:'#ef4444',investor:'#22c55e',partner:'#3b82f6',compute_provider:'#f97316'}};
  const relsHtml = rels.map(r => `<span style="background:${{relColors[r.relationship_type]}}22;color:${{relColors[r.relationship_type]}};border:1px solid ${{relColors[r.relationship_type]}}44;padding:2px 8px;border-radius:10px;font-size:12px">${{r.relationship_type}}: ${{r.related_entity}}</span>`).join(' ');
  const kmHtml = km.map(k => `<tr><td style="padding:6px 10px;color:#64748b;font-size:13px">${{k.metric_name}}</td><td style="padding:6px 10px;font-weight:600;font-size:13px">${{k.metric_value}}</td><td style="padding:6px 10px;color:#94a3b8;font-size:12px">${{k.as_of_date||''}}</td></tr>`).join('');
  const msHtml = ms.map(m => {{
    const score = m.forward_implication_score;
    const scoreBadge = score === 5 ? `<span class="badge-5">${{score}}</span>` : `<span style="font-size:12px;color:#94a3b8">${{score}}</span>`;
    const src = m.source_event ? `<span style="background:#fef3c7;color:#92400e;padding:1px 5px;border-radius:6px;font-size:10px;margin-left:4px">${{m.source_event}}</span>` : '';
    return `<tr>
      <td style="padding:8px 10px;color:#64748b;font-size:12px;white-space:nowrap">${{m.date}}</td>
      <td style="padding:8px 10px;font-size:13px">${{m.event||''}}${{src}}</td>
      <td style="padding:8px 10px;text-align:center">${{scoreBadge}}</td>
    </tr>`;
  }}).join('');

  document.getElementById('modal-content').innerHTML = `
    <h2 style="font-size:22px;font-weight:800;margin-bottom:4px">${{e.name}}</h2>
    <p style="color:#64748b;font-size:13px;margin-bottom:14px">${{e.category||''}} · Founded ${{e.founded||'—'}} · ${{e.headquarters||'—'}}</p>
    ${{e.current_valuation ? `<p style="font-size:14px;font-weight:600;margin-bottom:10px">💰 ${{e.current_valuation}}</p>` : ''}}
    <p style="font-size:13px;color:#475569;line-height:1.6;margin-bottom:16px">${{e.trajectory_summary||''}}</p>
    ${{relsHtml ? `<div style="display:flex;flex-wrap:wrap;gap:5px;margin-bottom:20px">${{relsHtml}}</div>` : ''}}
    ${{kmHtml ? `<h3 style="font-size:14px;font-weight:700;margin-bottom:8px">Key Metrics</h3>
    <table style="margin-bottom:20px;font-size:13px"><tbody>${{kmHtml}}</tbody></table>` : ''}}
    <h3 style="font-size:14px;font-weight:700;margin-bottom:8px">Milestones (${{ms.length}})</h3>
    <table><thead><tr><th>Date</th><th>Event</th><th>Score</th></tr></thead><tbody>${{msHtml}}</tbody></table>
  `;
  document.getElementById('modal').classList.add('open');
}}
function closeModal() {{ document.getElementById('modal').classList.remove('open'); }}
document.getElementById('modal').addEventListener('click', e => {{ if (e.target === document.getElementById('modal')) closeModal(); }});
</script>
</body>
</html>"""

with open(OUT, "w") as f:
    f.write(HTML)

print(f"\n✅ Dashboard written to: {OUT}")
print("   Open dashboard.html in your browser to explore the knowledge graph.")
