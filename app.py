import streamlit as st
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

# ================= CONFIG =================
st.set_page_config(page_title="MovieSpot", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background: 
            linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
            url("https://images5.alphacoders.com/445/thumb-1920-445161.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Make containers slightly transparent */
    section[data-testid="stSidebar"],
    div[data-testid="stVerticalBlock"] {
        background-color: rgba(0, 0, 0, 0.55);
        border-radius: 12px;
        padding: 10px;
    }

    /* Improve text readability */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
BASE = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Image"

# ================= HTTP =================
def session():
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429,500,502,503,504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s

HTTP = session()

@st.cache_data(show_spinner=False)
def tmdb(path, params=None):
    if params is None:
        params = {}
    params["api_key"] = TMDB_API_KEY
    try:
        r = HTTP.get(BASE + path, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return {}

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "movie_id" not in st.session_state:
    st.session_state.movie_id = None
if "person_id" not in st.session_state:
    st.session_state.person_id = None
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "top_page" not in st.session_state:
    st.session_state.top_page = 1

# ================= NAV FROM URL =================
qp = st.query_params

if "home" in qp:
    st.session_state.page = "home"
    qp.clear()
    st.rerun()

if "top250" in qp:
    st.session_state.page = "top250"
    qp.clear()
    st.rerun()

# ================= HEADER =================
def header():
    col1, col2, col3 = st.columns([2,3,1])

    with col1:
        if st.button("🎬 MovieSpot", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.movie_id = None
            st.session_state.person_id = None
            st.rerun()

    with col2:
        if st.button("Top Rated"):
            st.session_state.page = "top250"
            st.rerun()

    with col3:
        st.text_input("Search", key="search_query")
        if st.button("Go"):
            st.session_state.page = "search"
            st.rerun()

# ================= UI HELPERS =================
def poster(p):
    return IMG + p if p else PLACEHOLDER

def movie_card(m, key):
    st.image(poster(m.get("poster_path")))
    st.markdown(f"**{m.get('title','')}**")
    st.caption(f"⭐ {m.get('vote_average','N/A')}")
    if st.button("View", key=key):
        st.session_state.movie_id = m["id"]
        st.session_state.page = "movie"
        st.rerun()

def horizontal(title, movies, prefix):
    st.markdown(f"### {title}")
    cols = st.columns(6)
    for i, m in enumerate(movies[:6]):
        with cols[i]:
            movie_card(m, f"{prefix}_{m['id']}")

# ================= PAGES =================
def home():
    header()
    horizontal("🔥 Trending", tmdb("/trending/movie/day").get("results", []), "trend")
    horizontal("⭐ Top Rated", tmdb("/movie/top_rated").get("results", []), "top")
    horizontal("🎬 Now Playing", tmdb("/movie/now_playing").get("results", []), "now")

def search():
    header()
    q = st.session_state.search_query
    st.markdown(f"### Results for **{q}**")
    results = tmdb("/search/movie", {"query": q}).get("results", [])
    if not results:
        st.warning("No results found")
        return
    cols = st.columns(5)
    for i, m in enumerate(results[:20]):
        with cols[i % 5]:
            movie_card(m, f"search_{m['id']}")

def movie_page():
    m = tmdb(f"/movie/{st.session_state.movie_id}")
    credits = tmdb(f"/movie/{st.session_state.movie_id}/credits")
    videos = tmdb(f"/movie/{st.session_state.movie_id}/videos")
    similar = tmdb(f"/movie/{st.session_state.movie_id}/similar").get("results", [])

    header()

    col1, col2 = st.columns([1,2])
    col1.image(poster(m.get("poster_path")))
    with col2:
        st.markdown(f"## {m.get('title')}")
        st.markdown(m.get("overview","No overview available"))
        st.caption(f"⭐ {m.get('vote_average')} | ⏱ {m.get('runtime','N/A')} min")

    for v in videos.get("results", []):
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            st.video(f"https://youtube.com/watch?v={v['key']}")
            break

    st.markdown("### Cast")
    cols = st.columns(6)
    for i, c in enumerate(credits.get("cast", [])[:6]):
        with cols[i]:
            st.image(poster(c.get("profile_path")))
            st.markdown(c["name"])
            st.caption(c["character"])
            if st.button("Actor", key=f"actor_{c['id']}"):
                st.session_state.person_id = c["id"]
                st.session_state.page = "person"
                st.rerun()

    horizontal("Similar Movies", similar, "sim")

def person_page():
    p = tmdb(f"/person/{st.session_state.person_id}")
    credits = tmdb(f"/person/{st.session_state.person_id}/movie_credits")

    header()
    col1, col2 = st.columns([1,2])
    col1.image(poster(p.get("profile_path")))
    col2.markdown(f"## {p.get('name')}")
    col2.write(p.get("biography","No biography"))

    horizontal("Movies", credits.get("cast", []), "pm")

def top250():
    header()
    page = st.session_state.top_page
    data = tmdb("/movie/top_rated", {"page": page}).get("results", [])

    st.markdown("## Top Rated Movies")

    for i, m in enumerate(data):
        rank = (page - 1) * 20 + i + 1
        col1, col2 = st.columns([1,4])

        with col1:
            st.image(poster(m.get("poster_path")), width=120)

        with col2:
            st.markdown(f"### #{rank} {m['title']}")
            st.markdown(f"⭐ {m['vote_average']} | 🗓 {m.get('release_date','N/A')}")
            st.caption(m.get("overview", "")[:300] + "...")
            if st.button("View Details", key=f"top_{m['id']}"):
                st.session_state.movie_id = m["id"]
                st.session_state.page = "movie"
                st.rerun()

        st.divider()

    col1, col2 = st.columns(2)
    if col1.button("⬅ Prev") and page > 1:
        st.session_state.top_page -= 1
        st.rerun()
    if col2.button("Next ➡"):
        st.session_state.top_page += 1
        st.rerun()

# ================= ROUTER =================
if st.session_state.page == "home":
    home()
elif st.session_state.page == "search":
    search()
elif st.session_state.page == "movie":
    movie_page()
elif st.session_state.page == "person":
    person_page()
elif st.session_state.page == "top250":
    top250()



