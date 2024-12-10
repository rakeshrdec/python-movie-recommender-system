import pandas as pd
import numpy as np
import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
# similarity = pickle.load(open('similarity.pkl', 'rb'))
# similarity = pd.DataFrame(similarity).to_numpy()

# Initialize an empty list to hold the reassembled matrix
reassembled_matrix = []

# Number of chunks
num_chunks = 8

# Load each chunk and append it to the reassembled matrix
for i in range(num_chunks):
    with open(f'similarity_chunk_{i + 1}.pkl', 'rb') as f:
        chunk = pickle.load(f)
        reassembled_matrix.extend(chunk)

# Optional: Convert back to the original format if needed (e.g., numpy array)
reassembled_matrix = np.array(reassembled_matrix)
similarity = reassembled_matrix

print("Successfully reassembled the similarity matrix!")



st.title("Movie Recommender System")

selected_movie_name = st.selectbox('How would you like to be contacted', movies['title'].values)

def fetch_movie_poster_by_id(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=6b2addccf795d62bf184141e39e5748c&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommended_movies(movie):
    movie_index = movies[movies['title']==movie].index[0]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key= lambda x: x[1])[1:6]

    recommended_movies_names = []
    recommended_movies_posters = []
    for i in movies_list:
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_movie_poster_by_id(movies.iloc[i[0]].movie_id))

    return recommended_movies_names, recommended_movies_posters

if st.button('Show Recommendation >'):
    recommended_movies_name, recommended_movies_posters = recommended_movies(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_posters[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_posters[4])