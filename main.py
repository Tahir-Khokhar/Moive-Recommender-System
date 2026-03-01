import streamlit as st
import pickle
import requests

# Load movies and similarity matrix
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies_df['title'].values

# Fetch Poster
def fetch_poster(movie_id):
    data = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4d87a385396706edd79c431cc70e7cb7&language=en-US'
    ).json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Recommendation function
def recommend(movie_name):
    idx = movies_df[movies_df['title'] == movie_name].index[0]
    movies_sorted = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]
    return [(movies_df.iloc[i[0]].title, fetch_poster(movies_df.iloc[i[0]].movie_id)) for i in movies_sorted]

# Streamlit UI
st.set_page_config(layout="wide")
st.title('🎬 Movie Recommendation System')

movie = st.selectbox("Select a movie", movies_list)

if st.button('Recommend'):
    st.write("### Recommended Movies:")

    recommendations = recommend(movie)
    cols = st.columns(len(recommendations))  # Create one column per movie

    for col, (name, poster) in zip(cols, recommendations):
        with col:
            st.image(poster, width=150)
            st.caption(name)  # Movie name under poster