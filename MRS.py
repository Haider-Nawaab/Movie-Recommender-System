# Rana Ali Haider || Ahmad Yousaf
# 201370020 || 191400091


import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommender System')


def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=cbc214eb8e62187139c3f80d26e31108")
    data = response.json()

    # Check if the poster path is available before accessing it
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)

        # fetch the movie poster
        poster_path = fetch_poster(movie_id)
        if poster_path:
            recommended_movie_posters.append(poster_path)

    return recommended_movie_names, recommended_movie_posters


# Load data
try:
    with open('movie_dict.pkl', 'rb') as file:
        movies_dict = pickle.load(file)
    print("Successfully loaded 'movie_dict.pkl'")
except FileNotFoundError:
    print("Error: 'movie_dict.pkl' not found.")
except Exception as e:
    print(f"Error loading 'movie_dict.pkl': {e}")
    movies_dict = {}

movies = pd.DataFrame(movies_dict)

try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    print("Successfully loaded 'similarity.pkl'")
except FileNotFoundError:
    print("Error: 'similarity.pkl' not found.")
except Exception as e:
    print(f"Error loading 'similarity.pkl': {e}")
    similarity = []

selected_movie_name = st.selectbox(
    'Hi Dear! I hope you are happy. Select the movie you want',
    (movies['title'].values)
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    if recommended_movie_names and recommended_movie_posters:
        for name, poster in zip(recommended_movie_names, recommended_movie_posters):
            st.text(name)
            st.image(poster)
    else:
        st.text("No recommendations available.")
