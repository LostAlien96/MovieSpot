 🎬 MovieSpot – IMDb-Style Movie Discovery Platform

MovieSpot is a full-featured IMDb-inspired movie discovery platform built using **Streamlit** and the **TMDB API**.  
It allows users to explore trending movies, top-rated films, search any movie, view detailed information including trailers, cast with character names, similar movie recommendations, and explore actor profiles — all within a single-page experience.

---
https://moviespot-sh5vv3wu2garxypb6dcktd.streamlit.app/ ->Try it Here

 🚀 Features

 🏠 Home Page
- Trending movies
- Top-rated movies
- Now-playing movies
- Clean poster-based layout

 🔍 Search
- Search movies by title
- Instant results with posters
- Dedicated results page

 🎥 Movie Detail Page
- Detailed overview
- IMDb-style metadata (rating, runtime, release date)
- Official trailers (YouTube)
- Full cast with character names
- Similar movie recommendations
- Seamless navigation (no page reloads)

 👤 Actor Detail Page
- Actor profile
- Biography
- Movies they appeared in

 🏆 Top 250 Movies
- IMDb-style ranked list
- Posters + overview
- Pagination support

---

 🛠 Tech Stack

- **Python**
- **Streamlit** – UI & state-based routing
- **TMDB API** – Movie, cast, and video data
- **Requests** – API communication

---

 🧠 Architecture Overview

- Session-based routing using `st.session_state`
- Modular UI components (cards, rows, pages)
- Separate API calls for:
  - Movie metadata
  - Credits (cast)
  - Videos (trailers)
  - Similar movies
- Pagination for large datasets
- Graceful fallback handling for missing API data

---

 ⚙️ Installation & Setup

 1️⃣ Clone the repository
```bash
git clone https://github.com/LostAlien96/MovieSpot.git
cd moviespot
