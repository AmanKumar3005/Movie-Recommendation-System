import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster using OMDb API
def fetch_poster(movie_title):
    api_key = '7f177099'  # OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True' and 'Poster' in data:
            return data['Poster']
    return None  # Return None if poster not found

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))  # Fetch poster

    return recommended_movies, recommended_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #A8DADC, #457B9D);
        color: #F1FAEE;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)

    # Display recommendations with posters in a single row
    cols = st.columns(len(recommendations))  # Create a column for each recommendation
    for col, (movie, poster) in zip(cols, zip(recommendations, posters)):
        with col:
            st.write(movie)  # Movie title
            if poster:
                st.image(poster, width=150, use_column_width='auto')  # Uniform poster size
            else:
                st.write("No poster available")


