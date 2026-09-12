"""Global design system: fonts, tokens and component styling."""

import streamlit as st

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0B0F1A; --surface:#111726; --surface-2:#161E30; --line:#233047;
  --text:#E8ECF6; --muted:#93A0BA; --brand:#5B7CFA; --brand-2:#8B5CF6;
  --ok:#34D399; --warn:#FBBF24; --danger:#F87171;
  --radius:14px; --shadow:0 10px 30px rgba(0,0,0,.35);
}
html,body,[class*="css"]{font-family:'Manrope',system-ui,sans-serif;}
.stApp{background:
  radial-gradient(1100px 600px at 12% -8%, rgba(91,124,250,.16), transparent 60%),
  radial-gradient(900px 500px at 88% 0%, rgba(139,92,246,.12), transparent 60%),
  var(--bg); color:var(--text);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.6rem;padding-bottom:5rem;max-width:1180px;}

h1,h2,h3,h4{font-family:'Sora',sans-serif;letter-spacing:-.02em;color:var(--text);}
p,li,span,div{color:var(--text);}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"]{background:#0A0E18;border-right:1px solid var(--line);width:330px!important;}
section[data-testid="stSidebar"] .block-container{padding-top:1rem;}

/* ---------- brand ---------- */
.brand{display:flex;align-items:center;gap:.7rem;padding:.2rem 0 1rem;}
.brand-mark{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;
  background:linear-gradient(135deg,var(--brand),var(--brand-2));font-size:19px;
  box-shadow:0 6px 18px rgba(91,124,250,.35);}
.brand-name{font-family:'Sora';font-weight:600;font-size:15px;line-height:1.1;}
.brand-sub{font-size:11px;color:var(--muted);}

/* ---------- generic card ---------- */
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:.85rem 1rem;box-shadow:var(--shadow);}
.section-label{font-size:10.5px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;
  color:var(--muted);margin:1.1rem 0 .45rem;}

/* ---------- doc card ---------- */
.doc{display:flex;gap:.6rem;align-items:center;background:var(--surface);
  border:1px solid var(--line);border-radius:12px;padding:.55rem .7rem;margin-bottom:.4rem;}
.doc.active{border-color:rgba(91,124,250,.55);background:linear-gradient(180deg,rgba(91,124,250,.12),transparent);}
.doc-name{font-size:12.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.doc-meta{font-size:10.5px;color:var(--muted);}
.dot{width:7px;height:7px;border-radius:50%;flex:0 0 auto;}
.dot.ready{background:var(--ok);box-shadow:0 0 0 3px rgba(52,211,153,.15);}
.dot.processing{background:var(--warn);box-shadow:0 0 0 3px rgba(251,191,36,.15);}
.dot.error{background:var(--danger);box-shadow:0 0 0 3px rgba(248,113,113,.15);}

/* ---------- stats ---------- */
.stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.45rem;}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.55rem .6rem;}
.stat-v{font-family:'Sora';font-size:16px;font-weight:600;}
.stat-k{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;}

/* ---------- pipeline ---------- */
.pipe{display:flex;flex-wrap:wrap;gap:.35rem;}
.chip{display:inline-flex;align-items:center;gap:.35rem;font-size:10.5px;color:var(--muted);
  border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:.22rem .55rem;}
.chip .tick{color:var(--ok);}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem;justify-content:center;}
.flow .step{font-size:11px;color:var(--muted);border:1px solid var(--line);background:var(--surface);
  border-radius:999px;padding:.28rem .7rem;}
.flow .arrow{color:#33415C;font-size:11px;}

/* ---------- chat ---------- */
.msg-row{display:flex;gap:.75rem;margin:.4rem 0 1.1rem;}
.msg-row.user{justify-content:flex-end;}
.avatar{width:30px;height:30px;border-radius:10px;display:grid;place-items:center;flex:0 0 auto;font-size:14px;
  border:1px solid var(--line);background:var(--surface-2);}
.avatar.ai{background:linear-gradient(135deg,rgba(91,124,250,.25),rgba(139,92,246,.25));
  border-color:rgba(91,124,250,.4);}
.bubble-user{max-width:74%;background:linear-gradient(135deg,var(--brand),var(--brand-2));
  color:#fff;padding:.6rem .9rem;border-radius:16px 16px 4px 16px;font-size:13.5px;line-height:1.6;
  box-shadow:0 8px 22px rgba(91,124,250,.25);}
.bubble-ai{max-width:100%;background:var(--surface);border:1px solid var(--line);
  padding:.85rem 1.05rem;border-radius:16px 16px 16px 4px;font-size:13.8px;line-height:1.72;}
.bubble-ai code{font-family:'JetBrains Mono';font-size:12px;background:#0D1322;
  border:1px solid var(--line);padding:.08rem .32rem;border-radius:5px;}
.bubble-ai blockquote{border-left:2px solid var(--brand);margin:.6rem 0;padding:.1rem .8rem;color:var(--muted);}
.err{border:1px solid rgba(248,113,113,.4);background:rgba(248,113,113,.08);
  border-radius:12px;padding:.7rem .9rem;font-size:13px;}

/* ---------- source card ---------- */
.src{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.55rem .7rem;
  transition:.18s;}
.src:hover{border-color:rgba(91,124,250,.5);transform:translateY(-1px);}
.src-title{font-size:12.2px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.src-page{font-size:10.5px;color:var(--muted);}
.badge{font-size:10.5px;font-weight:700;color:#BFD0FF;background:rgba(91,124,250,.16);
  border:1px solid rgba(91,124,250,.3);border-radius:7px;padding:.1rem .4rem;}

/* ---------- score bar ---------- */
.sb-top{display:flex;justify-content:space-between;font-size:11.5px;color:var(--muted);margin-bottom:.22rem;}
.sb-top b{color:var(--text);font-variant-numeric:tabular-nums;}
.sb{height:6px;border-radius:999px;background:#0D1322;border:1px solid var(--line);overflow:hidden;}
.sb>i{display:block;height:100%;background:linear-gradient(90deg,var(--brand),var(--brand-2));}

/* ---------- welcome ---------- */
.hero{text-align:center;padding:2.4rem 0 1rem;}
.hero-mark{width:56px;height:56px;border-radius:18px;margin:0 auto .9rem;display:grid;place-items:center;
  font-size:26px;background:linear-gradient(135deg,rgba(91,124,250,.22),rgba(139,92,246,.22));
  border:1px solid rgba(91,124,250,.35);}
.hero h1{font-size:30px;margin:0;}
.hero p{color:var(--muted);font-size:14px;margin:.5rem 0 0;}

/* ---------- buttons / inputs ---------- */
.stButton>button{background:var(--surface-2);border:1px solid var(--line);color:var(--text);
  border-radius:11px;font-size:12.5px;font-weight:600;padding:.4rem .7rem;transition:.16s;width:100%;}
.stButton>button:hover{border-color:rgba(91,124,250,.55);color:#fff;background:#1B2438;}
div[data-testid="stSidebar"] .stButton>button{text-align:left;}
.stChatInput textarea{background:var(--surface)!important;color:var(--text)!important;}
div[data-testid="stChatInput"]{border:1px solid var(--line);border-radius:14px;background:var(--surface);}
.stDataFrame{border:1px solid var(--line);border-radius:12px;overflow:hidden;}
div[data-testid="stExpander"]{border:1px solid var(--line)!important;border-radius:12px!important;
  background:var(--surface);}
hr{border-color:var(--line);}
</style>
"""


def inject_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
