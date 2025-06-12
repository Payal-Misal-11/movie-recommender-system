import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{id}?api_key=84c7bb2b2e31598840effd110611558e&language=en-US'
    )
    data = response.json()
    poster_path = data.get('poster_path')

    if not poster_path:
        print(f"No poster path for movie_id: {id}")
        return "https://via.placeholder.com/500x750?text=No+Image"

    return f"https://image.tmdb.org/t/p/original{poster_path}"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_title = movies.iloc[i[0]]['title']
        movie_tmdb_id = movies.iloc[i[0]]['id']  # Access correctly using ['movie_id']

        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_tmdb_id))

    return recommended_movies, recommended_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.title('Movie Recommender System')git lfs install

selected_movie_name = st.selectbox(
    'How would you like to select a movie?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
