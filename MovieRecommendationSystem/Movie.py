import streamlit as st
import pickle
import requests
import time





# Set Streamlit page layout
st.set_page_config(page_title="Movie Recommender System", layout="wide")

# Load CSS for styling
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Title with glowing animation
st.markdown(
    """
    <h1 class="glowing-text" style="text-align: center;">
    🎥 Movie Recommender System 🎬</h1>
    """,
    unsafe_allow_html=True,
)

# Load movies and similarity matrix
movies_data = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies_data['title'].values

# Dropdown for selecting movie with increased font size and animation
selected_movie_name = st.selectbox(
    "✨ Select a movie to get recommendations ✨",
    movies_list,
    index=0,
    key="movie_select",
    help="Select a movie to see similar recommendations.",
    label_visibility="visible"
)

# Function to fetch movie posters and details
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}", data['homepage'] or f"https://www.imdb.com/title/{data['imdb_id']}"

# Function to recommend movies
def recommend(selected_movie_name):
    movie_index = movies_data[movies_data['title'] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:10]

    recommended_movies = []
    recommended_posters = []
    recommended_links = []

    for i in movie_indices:
        movie_id = movies_data.iloc[i[0]].movie_id
        movie_title = movies_data.iloc[i[0]].title
        poster_url, movie_link = fetch_poster(movie_id)
        
        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)
        recommended_links.append(movie_link)

    return recommended_movies, recommended_posters, recommended_links

# Button to trigger recommendation with image
if st.button("✨ Show Recommendations ✨", help="Click to get movie recommendations"):
    # Show spinner while waiting for the recommendations
    with st.spinner('Fetching recommendations...🍿🤩🥳'):
        time.sleep(2)  # Simulate loading time
        
        # Get recommendations after the "fetching" time
        recommended_movies, recommended_posters, recommended_links = recommend(selected_movie_name)

    # Add spinner HTML next to "Fetching recommendations..."
    st.markdown(
        """
        <div style="display: inline-flex; align-items: center;">
            <span class="spinner-text">Fetching recommendations...</span>
            <div class="spinner-container">
                <img src="https://your_image_path_here/popcorn.png" alt="Popcorn" />
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show recommendations with background and animation
    st.markdown(
        """
        <div class="recommendation-section">
            <h2 class="animated-text">
            Here are some movies you might like:
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display movies in a compact grid with hover effect
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    
    cols = [col1, col2, col3, col4, col5, col6, col7, col8, col9]

    for i, (movie, poster, link) in enumerate(zip(recommended_movies, recommended_posters, recommended_links)):
        with cols[i]:
            st.markdown(
                f"""
                <a href="{link}" target="_blank">
                    <div class="movie-card">
                        <img src="{poster}" class="movie-poster" alt="{movie}">
                        <div class="movie-title">{movie}</div>
                    </div>
                </a>
                """, 
                unsafe_allow_html=True
            )
