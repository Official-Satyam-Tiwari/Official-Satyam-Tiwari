"""Generates the animated SVGs used in README.md. Run: python make_assets.py"""
import math, os, random

os.makedirs("assets", exist_ok=True)
random.seed(4)

STYLE = """<style>
  .det{fill:#E4572E}.bore{stroke:#E4572E}.lor{stroke:#E4572E}.sc{stroke:#7C5CFF}.ann{fill:#7C5CFF}.txt{fill:#57606a}
  @media (prefers-color-scheme: dark){
    .det{fill:#6EE7C8}.bore{stroke:#6EE7C8}.lor{stroke:#6EE7C8}.sc{stroke:#FF9EC0}.ann{fill:#FF9EC0}.txt{fill:#8b949e}
  }
</style>"""

# ---------- PET ring: true coincidences + detector-scattered coincidences ----------
W, H, R = 900, 300, 112
cx, cy = W / 2, H / 2
N = 40
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Animated PET detector ring recording detector-scattered coincidences">', STYLE]
parts.append(f'<g transform="translate({cx} {cy})"><g>')
parts.append('<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="80s" repeatCount="indefinite"/>')
for i in range(N):
    parts.append(f'<rect class="det" x="-5" y="{-R-18}" width="10" height="18" rx="2" opacity=".85" transform="rotate({i*360/N})"/>')
parts.append('</g>')
parts.append(f'<circle r="{R-12}" fill="none" class="bore" stroke-width="1" stroke-dasharray="3 5" opacity=".5"/>')

CYCLE = 9.0
def at(a, r=R - 9):
    return r * math.cos(a), r * math.sin(a)

for k in range(9):
    t0 = k * CYCLE / 9
    a = random.uniform(0, math.pi)
    o = random.uniform(-45, 45)
    px, py = -math.sin(a) * o, math.cos(a) * o
    L = math.sqrt((R - 9) ** 2 - o ** 2)
    x1, y1 = px - math.cos(a) * L, py - math.sin(a) * L
    x2, y2 = px + math.cos(a) * L, py + math.sin(a) * L
    kt = f'keyTimes="0;{t0/CYCLE:.3f};{(t0+.15)/CYCLE:.3f};{min(t0+1.6,CYCLE-.01)/CYCLE:.3f};1"'
    fade = f'<animate attributeName="opacity" values="0;0;1;0;0" {kt} dur="{CYCLE}s" repeatCount="indefinite"/>'
    parts.append(f'<circle class="ann" cx="{px:.1f}" cy="{py:.1f}" r="3.5" opacity="0">{fade}</circle>')
    parts.append(f'<line class="lor" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="1.4" opacity="0">{fade}</line>')
    if k % 2 == 0:  # detector-scattered: second photon kicks to a neighbouring detector
        b = math.atan2(y2, x2) + random.choice([-1, 1]) * random.uniform(.5, 1.1)
        sx, sy = at(b)
        parts.append(f'<line class="sc" x1="{x2:.1f}" y1="{y2:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke-width="1.6" stroke-dasharray="4 3" opacity="0">{fade}</line>')
        parts.append(f'<circle class="ann" cx="{sx:.1f}" cy="{sy:.1f}" r="3" opacity="0">{fade}</circle>')
parts.append('</g>')
# legend
parts.append(f'<g font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="13" class="txt">'
             f'<line class="lor" x1="40" y1="{H-40}" x2="70" y2="{H-40}" stroke-width="2"/><text x="78" y="{H-36}">true coincidence</text>'
             f'<line class="sc" x1="40" y1="{H-18}" x2="70" y2="{H-18}" stroke-width="2" stroke-dasharray="4 3"/><text x="78" y="{H-14}">detector-scattered coincidence</text></g>')
parts.append('</svg>')
open("assets/pet-ring.svg", "w", encoding="utf-8").write("\n".join(parts))

# ---------- divider: a photon travelling along a thin line ----------
div = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 16" width="900" height="16" role="img" aria-label="divider">{STYLE}
<line class="lor" x1="0" y1="8" x2="900" y2="8" stroke-width="1" opacity=".25"/>
<circle class="ann" r="4" cy="8"><animate attributeName="cx" values="-10;910" dur="4s" repeatCount="indefinite"/></circle>
<circle class="det" r="3" cy="8"><animate attributeName="cx" values="910;-10" dur="4s" repeatCount="indefinite"/></circle>
</svg>'''
open("assets/divider.svg", "w", encoding="utf-8").write(div)
print("ok")
