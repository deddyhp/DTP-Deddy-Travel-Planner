
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "trip_magelang.json"

st.set_page_config(
    page_title="DTP — Magelang Healing",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

@st.cache_data
def load_trip():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

trip = load_trip()
tz = ZoneInfo("Asia/Jakarta")
now = datetime.now(tz)

st.markdown(
    """
    <style>
    :root {
        --bg: #07090d;
        --panel: rgba(18, 20, 27, 0.92);
        --panel-soft: rgba(21, 24, 32, 0.78);
        --yellow: #ffd84d;
        --yellow-2: #ffb703;
        --text: #f6f3df;
        --muted: #a8a89f;
        --line: rgba(255, 216, 77, 0.32);
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 8%, rgba(255, 183, 3, .12), transparent 23%),
            radial-gradient(circle at 88% 3%, rgba(255, 216, 77, .10), transparent 22%),
            linear-gradient(180deg, #06070a 0%, #0a0c12 55%, #08090d 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 760px;
        padding: 1rem .9rem 5rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 1.35rem 1.2rem 1.2rem;
        border-radius: 25px;
        background:
            linear-gradient(145deg, rgba(26, 28, 36, .96), rgba(10, 11, 16, .98));
        border: 1px solid rgba(255, 216, 77, .35);
        box-shadow:
            0 0 0 1px rgba(255, 216, 77, .06) inset,
            0 0 28px rgba(255, 183, 3, .12),
            0 18px 50px rgba(0, 0, 0, .42);
        margin-bottom: 1rem;
    }

    .hero::before {
        content: "";
        position: absolute;
        top: 0;
        left: 8%;
        width: 62%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--yellow), transparent);
        box-shadow: 0 0 15px var(--yellow);
    }

    .hero::after {
        content: "";
        position: absolute;
        right: -65px;
        top: -65px;
        width: 165px;
        height: 165px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,216,77,.17), transparent 66%);
    }

    .eyebrow {
        font-size: .7rem;
        letter-spacing: .15em;
        text-transform: uppercase;
        font-weight: 800;
        color: var(--yellow);
        margin-bottom: .42rem;
    }

    .hero-title {
        font-size: 1.72rem;
        line-height: 1.08;
        font-weight: 900;
        color: #fffbe9;
        text-shadow: 0 0 20px rgba(255, 216, 77, .18);
    }

    .hero-sub {
        color: #c8c5b4;
        font-size: .9rem;
        margin-top: .45rem;
    }

    .mission-card,
    .metric-card,
    .timeline-card,
    .spot-shell {
        position: relative;
        background: linear-gradient(145deg, rgba(21, 24, 31, .94), rgba(12, 14, 19, .97));
        border: 1px solid rgba(255, 216, 77, .20);
        box-shadow:
            0 0 18px rgba(255, 183, 3, .055),
            0 12px 28px rgba(0, 0, 0, .28);
    }

    .mission-card {
        border-radius: 19px;
        padding: 1rem 1.05rem;
        margin-bottom: .78rem;
        border-left: 4px solid var(--yellow);
    }

    .mission-label,
    .metric-label {
        color: #a8a89f;
        font-size: .72rem;
        font-weight: 750;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .mission-main {
        color: #fff8cc;
        font-size: 1.12rem;
        line-height: 1.28;
        font-weight: 900;
        margin: .22rem 0 .28rem;
    }

    .mission-note,
    .timeline-note {
        color: #aeb0ae;
        font-size: .82rem;
        line-height: 1.45;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: .68rem;
        margin: .75rem 0;
    }

    .metric-card {
        border-radius: 17px;
        padding: .88rem .95rem;
        min-height: 85px;
    }

    .metric-value {
        color: #fff6be;
        font-size: 1.06rem;
        font-weight: 900;
        margin-top: .22rem;
    }

    .section-title {
        font-size: 1.02rem;
        color: #fff4ac;
        font-weight: 900;
        margin: 1.2rem 0 .62rem;
    }

    .timeline-card {
        border-radius: 17px;
        padding: .88rem .95rem;
        margin-bottom: .65rem;
    }

    .timeline-time {
        color: var(--yellow);
        font-size: .82rem;
        font-weight: 900;
        text-shadow: 0 0 12px rgba(255,216,77,.2);
    }

    .timeline-title {
        color: #f9f5df;
        font-size: .98rem;
        font-weight: 850;
        margin: .12rem 0 .16rem;
    }

    .pill {
        display: inline-block;
        padding: .26rem .6rem;
        margin-top: .38rem;
        border-radius: 999px;
        font-size: .68rem;
        font-weight: 850;
        border: 1px solid rgba(255,216,77,.25);
        color: #ffe98c;
        background: rgba(255,216,77,.08);
    }

    .status-done {
        color: #bcf4cf;
        border-color: rgba(111,231,154,.22);
        background: rgba(53,142,86,.12);
    }

    .status-next {
        color: #fff1a5;
        border-color: rgba(255,216,77,.42);
        background: rgba(255,183,3,.13);
        box-shadow: 0 0 14px rgba(255,183,3,.08);
    }

    .status-plan {
        color: #b6bbc4;
        border-color: rgba(180,185,195,.16);
        background: rgba(180,185,195,.06);
    }

    .note-box {
        background: rgba(255, 216, 77, .055);
        border-left: 3px solid var(--yellow);
        border-radius: 12px;
        color: #d7d4c4;
        font-size: .88rem;
        font-style: italic;
        line-height: 1.55;
        padding: .78rem .9rem;
        margin: .42rem 0 .8rem;
    }

    .spot-shell {
        border-radius: 19px;
        padding: .95rem 1rem;
        margin-bottom: .8rem;
    }

    .muted {
        color: var(--muted);
        font-size: .78rem;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(255,216,77,.17);
        border-radius: 16px;
        overflow: hidden;
        background: rgba(15,17,23,.88);
    }

    div[data-baseweb="select"] > div {
        background: rgba(18, 20, 27, .96);
        border-color: rgba(255,216,77,.22);
        color: #f7f1d0;
    }

    .stButton > button,
    .stLinkButton > a {
        border-radius: 14px !important;
        border: 1px solid rgba(255,216,77,.35) !important;
        color: #fff1a4 !important;
        background: linear-gradient(145deg, rgba(255,216,77,.12), rgba(255,183,3,.05)) !important;
        font-weight: 850 !important;
        box-shadow: 0 0 18px rgba(255,183,3,.07);
    }

    div[data-testid="stTabs"] button {
        color: #aaa99e;
        font-weight: 800;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--yellow);
    }

    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #ffb703, #ffe66d);
        box-shadow: 0 0 12px rgba(255,216,77,.32);
    }

    .footer-note {
        color: #7f807d;
        text-align: center;
        font-size: .72rem;
        margin-top: 1.7rem;
    }

    @media (max-width: 520px) {
        .hero-title { font-size: 1.46rem; }
        .block-container { padding-left: .72rem; padding-right: .72rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def parse_dt(date_text: str, time_text: str) -> datetime:
    return datetime.fromisoformat(f"{date_text}T{time_text}:00").replace(tzinfo=tz)

def get_status(item_dt: datetime) -> tuple[str, str]:
    diff = (item_dt - now).total_seconds()
    if diff < -3600:
        return "Visited ✔", "status-done"
    if -3600 <= diff <= 7200:
        return "Current / Next", "status-next"
    return "Planned", "status-plan"

def all_timeline_items():
    result = []
    for day in trip["days"]:
        for item in day["timeline"]:
            result.append((parse_dt(day["date"], item["time"]), item, day))
    return sorted(result, key=lambda row: row[0])

def current_mission():
    items = all_timeline_items()
    trip_start = datetime.fromisoformat(f"{trip['start_date']}T00:00:00").replace(tzinfo=tz)
    trip_end = datetime.fromisoformat(f"{trip['end_date']}T23:59:59").replace(tzinfo=tz)

    if now < trip_start:
        days_left = max(0, (trip_start.date() - now.date()).days)
        return (
            "Prepare for Magelang Healing",
            f"{days_left} hari lagi. Cek packing, kendaraan, obat, dan kopi Pagerwatu.",
            items[0],
        )

    if now > trip_end:
        return (
            "Trip completed",
            "Saatnya melengkapi jurnal dan menyusun Review Book.",
            items[-1],
        )

    for dt, item, day in items:
        if dt >= now:
            minutes = max(0, int((dt - now).total_seconds() // 60))
            return (
                f"Saatnya menuju {item['title']}",
                f"Agenda berikutnya pukul {item['time']} · sekitar {minutes} menit lagi.",
                (dt, item, day),
            )

    return ("Nikmati perjalanan", "Tidak ada agenda berikutnya hari ini.", items[-1])

mission_title, mission_note, next_item = current_mission()

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">🌿 Deddy Travel Planner</div>
        <div class="hero-title">{trip['title']}</div>
        <div class="hero-sub">{trip['date_label']} · {trip['tagline']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

home_tab, timeline_tab, spot_tab = st.tabs(["⌂ Home", "◷ Timeline", "⌖ Spot Guide"])

with home_tab:
    st.markdown(
        f"""
        <div class="mission-card">
            <div class="mission-label">Current Mission</div>
            <div class="mission-main">{mission_title}</div>
            <div class="mission-note">{mission_note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Current Time</div>
                <div class="metric-value">{now.strftime('%H:%M')} WIB</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Trip Progress</div>
                <div class="metric-value">{trip['progress_label']}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Distance Today</div>
                <div class="metric-value">{trip['distance_today']}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Fuel</div>
                <div class="metric-value">{trip['fuel_status']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(trip.get("progress_value", 0.08))

    st.markdown("<div class='section-title'>Today's Weather</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="spot-shell">
            <div class="timeline-title">Weather preview</div>
            <div class="timeline-note">
                Cuaca live belum diaktifkan pada V0.1. Fokus utilization awal adalah Home,
                Timeline, dan Spot Detail.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Trip Days</div>", unsafe_allow_html=True)
    columns = st.columns(len(trip["days"]))
    for index, day in enumerate(trip["days"], start=1):
        with columns[index - 1]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Day {index}</div>
                    <div class="metric-value">{day['short_label']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    _, item, day = next_item
    st.markdown("<div class='section-title'>Next Highlight</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="spot-shell">
            <div class="timeline-time">{day['label']} · {item['time']} WIB</div>
            <div class="timeline-title">{item['title']}</div>
            <div class="timeline-note">{item.get('summary', '')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with timeline_tab:
    for day_index, day in enumerate(trip["days"], start=1):
        st.markdown(
            f"<div class='section-title'>Day {day_index} · {day['label']}</div>",
            unsafe_allow_html=True,
        )

        for item in day["timeline"]:
            item_dt = parse_dt(day["date"], item["time"])
            status, status_class = get_status(item_dt)
            st.markdown(
                f"""
                <div class="timeline-card">
                    <div class="timeline-time">{item['time']} WIB</div>
                    <div class="timeline-title">{item['title']}</div>
                    <div class="timeline-note">{item.get('summary', '')}</div>
                    <span class="pill {status_class}">{status}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


with spot_tab:
    current_day_number = 0
    for index, day in enumerate(trip["days"], start=1):
        day_start = datetime.fromisoformat(f"{day['date']}T00:00:00").replace(tzinfo=tz)
        day_end = datetime.fromisoformat(f"{day['date']}T23:59:59").replace(tzinfo=tz)
        if day_start <= now <= day_end:
            current_day_number = index
            break

    day_labels = ["All Spots", "Day 1", "Day 2", "Day 3", "Hidden Gem"]
    default_index = current_day_number if current_day_number in (1, 2, 3) else 0
    selected_group = st.radio("Pilih panduan", day_labels, index=default_index, horizontal=True, label_visibility="collapsed")

    if selected_group == "All Spots":
        visible_spots, guide_title = trip["spots"], "Complete Spot Guide"
    elif selected_group == "Hidden Gem":
        visible_spots, guide_title = [s for s in trip["spots"] if s.get("day") == 0], "Hidden Gem"
    else:
        selected_day = int(selected_group.split()[-1])
        visible_spots, guide_title = [s for s in trip["spots"] if s.get("day") == selected_day], f"{selected_group} Guide"

    st.markdown(f"<div class='section-title'>{guide_title}</div>", unsafe_allow_html=True)

    for index, spot in enumerate(visible_spots):
        with st.expander(f"{spot['name']} · {spot.get('category', 'Spot')}", expanded=(index == 0)):
            st.markdown(f"<span class='pill'>{spot.get('rating','')}</span><span class='pill'>{spot.get('status','Planned')}</span>", unsafe_allow_html=True)
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
                for item in spot.get("best_spots", []): st.write(f"◉ {item}")
                st.markdown("**Menu Recommended**")
                for item in spot.get("menu", []): st.write(f"✓ {item}")
            with right:
                st.markdown("**Don't Miss**")
                for item in spot.get("dont_miss", []): st.write(f"◻ {item}")

            st.markdown("**Attention**")
            st.warning(spot.get("attention", "Nikmati tanpa terburu-buru."))
            if spot.get("maps_query"):
                maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(spot["maps_query"])
                st.link_button("Open in Google Maps", maps_url)

st.markdown(
    "<div class='footer-note'>DTP V0.1 · Every journey deserves a story.</div>",
    unsafe_allow_html=True,
)
