
import json
import base64
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "trip_magelang.json"

st.set_page_config(page_title="DTP — Real Journey", page_icon="🌿", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data
def load_trip():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def image_to_base64(image_path: Path) -> str:
    with image_path.open("rb") as f:
        return base64.b64encode(f.read()).decode()

trip = load_trip()
tz = ZoneInfo("Asia/Jakarta")
now = datetime.now(tz)

hero_path = BASE_DIR / trip.get("hero_image", "")
hero_b64 = image_to_base64(hero_path) if hero_path.exists() else ""

st.markdown(f'''
<style>
:root {{
    --yellow: #FFD84D;
}}
.stApp {{
    background:
        radial-gradient(circle at 18% 5%, rgba(255,216,77,.10), transparent 22%),
        radial-gradient(circle at 90% 0%, rgba(255,170,0,.08), transparent 26%),
        linear-gradient(180deg, #050609 0%, #0a0c12 55%, #07090d 100%);
    color: #f7f2da;
}}
.block-container {{
    max-width: 840px;
    padding: 0.9rem 0.9rem 5rem;
}}
header[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer {{ visibility: hidden; }}
.hero {{
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    min-height: 290px;
    display: flex;
    align-items: flex-end;
    padding: 1.2rem 1.15rem 1.15rem;
    margin-bottom: 1rem;
    background:
        linear-gradient(180deg, rgba(8,10,14,.08), rgba(6,7,10,.72) 55%, rgba(6,7,10,.92) 100%),
        url("data:image/png;base64,{hero_b64}");
    background-size: cover;
    background-position: center center;
    border: 1px solid rgba(255,216,77,.34);
    box-shadow: 0 0 0 1px rgba(255,216,77,.06) inset, 0 0 24px rgba(255,183,3,.08), 0 18px 48px rgba(0,0,0,.35);
}}
.hero::before {{
    content: "";
    position: absolute;
    left: 5%;
    top: 0;
    width: 62%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--yellow), transparent);
    box-shadow: 0 0 16px var(--yellow);
}}
.hero-overlay {{ width:100%; position:relative; z-index:2; }}
.eyebrow {{
    font-size: .74rem;
    letter-spacing: .16em;
    text-transform: uppercase;
    font-weight: 900;
    color: #ffefab;
    text-shadow: 0 0 14px rgba(255,216,77,.25);
    margin-bottom: .35rem;
}}
.hero-title {{
    font-size: 2.25rem;
    line-height: 1.05;
    font-weight: 900;
    color: #fff8dc;
    text-shadow: 0 4px 18px rgba(0,0,0,.42);
}}
.hero-sub {{
    color: #f0e6bf;
    margin-top: .45rem;
    font-size: .95rem;
    text-shadow: 0 2px 10px rgba(0,0,0,.35);
}}
.hero-mini {{ margin-top:.8rem; display:flex; flex-wrap:wrap; gap:.45rem; }}
.pill {{
    display:inline-block; padding:.30rem .66rem; border-radius:999px; font-size:.70rem; font-weight:850;
    border:1px solid rgba(255,216,77,.25); color:#ffeaa4; background:rgba(255,216,77,.10);
}}
.status-good {{ color:#d6f7df; border-color:rgba(135,235,170,.34); background:rgba(76,155,104,.18); }}
.status-warn {{ color:#fff1b5; border-color:rgba(255,216,77,.34); background:rgba(255,183,3,.16); }}
.status-bad {{ color:#ffd5d5; border-color:rgba(235,124,124,.28); background:rgba(176,61,61,.16); }}
.section-title {{ font-size:1.02rem; color:#fff2ac; font-weight:900; margin:1.1rem 0 .62rem; }}
.card, .timeline-card, .journey-card {{
    background: linear-gradient(145deg, rgba(17,20,27,.94), rgba(10,12,18,.97));
    border:1px solid rgba(255,216,77,.18);
    box-shadow: 0 0 18px rgba(255,183,3,.05), 0 12px 28px rgba(0,0,0,.28);
}}
.grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:.72rem; }}
.summary-card {{ border-radius:18px; padding:.88rem .95rem; }}
.summary-label {{ color:#a9a797; font-size:.72rem; text-transform:uppercase; font-weight:800; letter-spacing:.08em; }}
.summary-value {{ color:#fff5bf; font-size:1.04rem; font-weight:900; margin-top:.22rem; line-height:1.35; }}
.story-card {{ border-radius:20px; padding:1rem 1.05rem; line-height:1.6; color:#ddd6bb; }}
.timeline-card {{ border-radius:16px; padding:.86rem .95rem; margin-bottom:.58rem; }}
.timeline-time {{ color:var(--yellow); font-size:.82rem; font-weight:900; }}
.timeline-title {{ color:#f8f2d6; font-size:.98rem; font-weight:860; margin:.1rem 0 .16rem; }}
.timeline-note {{ color:#b6b39f; font-size:.82rem; line-height:1.45; }}
.journey-card {{ border-radius:18px; padding:.9rem 1rem; margin-bottom:.68rem; }}
.journey-name {{ font-size:.97rem; font-weight:900; color:#fff0ad; }}
.journey-note {{ color:#d2cdb6; font-size:.84rem; line-height:1.5; margin-top:.28rem; }}
.note-box {{
    background: rgba(255,216,77,.06); border-left:3px solid var(--yellow); border-radius:12px;
    color:#d8d2bb; font-style:italic; font-size:.88rem; line-height:1.55; padding:.78rem .88rem; margin:.42rem 0 .72rem;
}}
div[data-testid="stTabs"] button {{ color:#a9a797; font-weight:800; }}
div[data-testid="stTabs"] button[aria-selected="true"] {{ color:var(--yellow); }}
div[data-baseweb="radio"] label, div[data-baseweb="radio"] span {{ color:#e4debf !important; }}
div[data-testid="stExpander"] {{
    border:1px solid rgba(255,216,77,.18); border-radius:16px; overflow:hidden; background:rgba(13,15,20,.88);
}}
.stLinkButton > a, .stButton > button {{
    border-radius:14px !important; border:1px solid rgba(255,216,77,.34) !important;
    color:#fff0a4 !important; background:linear-gradient(145deg, rgba(255,216,77,.12), rgba(255,183,3,.05)) !important; font-weight:850 !important;
}}
.footer-note {{ color:#7f807d; text-align:center; font-size:.72rem; margin-top:1.7rem; }}
@media (max-width:520px) {{
    .hero {{ min-height:240px; padding:1rem .95rem .95rem; }}
    .hero-title {{ font-size:1.72rem; }}
    .block-container {{ padding-left:.72rem; padding-right:.72rem; }}
}}
</style>
''', unsafe_allow_html=True)

st.markdown(f'''
<div class="hero">
  <div class="hero-overlay">
    <div class="eyebrow">🌿 DTP · Deddy Travel Planner</div>
    <div class="hero-title">{trip["title"]}</div>
    <div class="hero-sub">{trip["date_label"]} · {trip["tagline"]}</div>
    <div class="hero-mini">
      <span class="pill status-good">{trip["status_label"]}</span>
      <span class="pill">{trip["mood_label"]}</span>
      <span class="pill">{trip["overall_rating"]}</span>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)

home_tab, timeline_tab, guide_tab, real_tab = st.tabs(["⌂ Home", "◷ Timeline", "⌖ Spot Guide", "✦ Real Journey"])

with home_tab:
    s = trip["summary"]
    st.markdown("<div class='section-title'>Journey Summary</div>", unsafe_allow_html=True)
    st.markdown(f'''
    <div class="grid-2">
      <div class="card summary-card"><div class="summary-label">Best Food</div><div class="summary-value">{s["best_food"]}</div></div>
      <div class="card summary-card"><div class="summary-label">Best View</div><div class="summary-value">{s["best_view"]}</div></div>
      <div class="card summary-card"><div class="summary-label">Biggest Lesson</div><div class="summary-value">{s["biggest_lesson"]}</div></div>
      <div class="card summary-card"><div class="summary-label">Home Base</div><div class="summary-value">{s["home_base"]}</div></div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Real Journey Story</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card story-card'>{trip['trip_story']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Trip Database Snapshot</div>", unsafe_allow_html=True)
    st.markdown(f'''
    <div class="grid-2">
      <div class="card summary-card"><div class="summary-label">Visited</div><div class="summary-value">{s["visited_count"]}</div></div>
      <div class="card summary-card"><div class="summary-label">Cancelled</div><div class="summary-value">{s["cancelled_count"]}</div></div>
      <div class="card summary-card"><div class="summary-label">Optional / Reference</div><div class="summary-value">{s["optional_count"]}</div></div>
      <div class="card summary-card"><div class="summary-label">Current Time</div><div class="summary-value">{now.strftime('%H:%M')} WIB</div></div>
    </div>
    ''', unsafe_allow_html=True)

with timeline_tab:
    for day in trip["days"]:
        st.markdown(f"<div class='section-title'>Day {day['day']} · {day['label']}</div>", unsafe_allow_html=True)
        for item in day["planned_timeline"]:
            st.markdown(f'''
            <div class="timeline-card">
              <div class="timeline-time">{item["time"]} WIB</div>
              <div class="timeline-title">{item["title"]}</div>
              <div class="timeline-note">{item.get("summary","")}</div>
            </div>
            ''', unsafe_allow_html=True)

with guide_tab:
    labels = ["All Spots", "Day 1", "Day 2", "Day 3", "Hidden Gem"]
    selected = st.radio("Pilih panduan", labels, index=0, horizontal=True, label_visibility="collapsed")
    if selected == "All Spots":
        visible_spots = trip["spot_guide"]
        guide_title = "Complete Spot Guide"
    elif selected == "Hidden Gem":
        visible_spots = [s for s in trip["spot_guide"] if s.get("day") == 0]
        guide_title = "Hidden Gem"
    else:
        selected_day = int(selected.split()[-1])
        visible_spots = [s for s in trip["spot_guide"] if s.get("day") == selected_day]
        guide_title = f"{selected} Guide"

    st.markdown(f"<div class='section-title'>{guide_title}</div>", unsafe_allow_html=True)

    for idx, spot in enumerate(visible_spots):
        with st.expander(f"{spot['name']} · {spot.get('category','Spot')}", expanded=(idx==0)):
            st.markdown(f"<span class='pill'>{spot.get('rating','')}</span> <span class='pill'>{spot.get('status','')}</span>", unsafe_allow_html=True)
            st.markdown("**Best Time**")
            st.write(spot.get("best_time", "Fleksibel"))
            st.markdown("**Why I Recommend**")
            st.markdown(f"<div class='note-box'>{spot.get('why','')}</div>", unsafe_allow_html=True)
            if spot.get("chaty_note"):
                st.markdown("**Chaty's Notes**")
                st.markdown(f"<div class='note-box'>{spot['chaty_note']}</div>", unsafe_allow_html=True)
            left, right = st.columns(2)
            with left:
                st.markdown("**Best Spot**")
                for item in spot.get("best_spots", []):
                    st.write(f"◉ {item}")
                st.markdown("**Menu Recommended**")
                for item in spot.get("menu", []):
                    st.write(f"✓ {item}")
            with right:
                st.markdown("**Don't Miss**")
                for item in spot.get("dont_miss", []):
                    st.write(f"◻ {item}")
            st.markdown("**Attention**")
            st.warning(spot.get("attention", "Nikmati tanpa terburu-buru."))
            st.markdown("**Actual Database Note**")
            st.markdown(
                f"<div class='note-box'>Status: {spot.get('actual_status','-')}<br>"
                f"Note: {spot.get('actual_note','-')}<br>"
                f"Future decision: {spot.get('future_decision','-')}</div>",
                unsafe_allow_html=True,
            )
            if spot.get("maps_query"):
                maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(spot["maps_query"])
                st.link_button("Open in Google Maps", maps_url, key=f"maps_{idx}")

with real_tab:
    for day in trip["days"]:
        st.markdown(f"<div class='section-title'>Day {day['day']} · {day['label']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card story-card'>{day['actual_story']}</div>", unsafe_allow_html=True)
        for idx, stop in enumerate(day["actual_stops"]):
            status = stop.get("status", "")
            status_class = "status-good"
            if "Cancel" in status:
                status_class = "status-bad"
            elif status in ("Visited",):
                status_class = "status-good"
            else:
                status_class = "status-warn"
            st.markdown(f'''
            <div class="journey-card">
              <div class="journey-name">{stop["name"]}</div>
              <div style="margin-top:.25rem;">
                <span class="pill {status_class}">{stop.get("status","")}</span>
                <span class="pill">{stop.get("rating","")}</span>
              </div>
              <div class="journey-note">{stop.get("note","")}</div>
              <div class="journey-note"><b>Future decision:</b> {stop.get("future_decision","")}</div>
            </div>
            ''', unsafe_allow_html=True)

st.markdown("<div class='footer-note'>DTP V0.2 · Real Journey Theme Update · Every journey deserves a story.</div>", unsafe_allow_html=True)
