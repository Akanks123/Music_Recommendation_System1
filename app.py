import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials (Replace these with your actual keys)
CLIENT_ID = "e69075fc89454058baa52a89f35bb357"
CLIENT_SECRET = "4822c08acac74869ad7f534db40ca2a1"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the precomputed data
try:
    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: Data files (df.pkl or similarity.pkl) not found!")
    st.stop()

def get_song_album_cover_url(song_name, artist_name):
    try:
        search_query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=search_query, type="track")
        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            return track["album"]["images"][0]["url"], track["external_urls"]["spotify"]
    except Exception as e:
        st.error(f"Error fetching album cover: {e}")
    return "https://i.postimg.cc/0QNxYz4V/social.png", ""

def recommend(song):
    if song not in music['song'].values:
        st.error("Song not found in dataset!")
        return [], [], []
    
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_links = []
    
    for i in distances[1:11]:  # Get top 10 recommendations
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        cover_url, song_url = get_song_album_cover_url(song_name, artist)
        recommended_music_names.append(song_name)
        recommended_music_posters.append(cover_url)
        recommended_music_links.append(song_url)

    return recommended_music_names, recommended_music_posters, recommended_music_links

def recommend_by_artist(artist_name):
    filtered_music = music[music['artist'].str.contains(artist_name, case=False, na=False)]

    if filtered_music.empty:
        st.error("Artist not found in dataset!")
        return [], [], []
    
    recommended_music_names = filtered_music['song'].tolist()[:10]
    recommended_music_posters = []
    recommended_music_links = []

    for song in recommended_music_names:
        cover_url, song_url = get_song_album_cover_url(song, artist_name)
        recommended_music_posters.append(cover_url)
        recommended_music_links.append(song_url)

    return recommended_music_names, recommended_music_posters, recommended_music_links

# ---------------------- STREAMLIT UI ---------------------- #
st.title("🎵 Music Recommender System 🎶")

option = st.radio("Choose Recommendation Type:", ("By Song", "By Artist"))

if option == "By Song":
    music_list = music['song'].values
    selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters, recommended_music_links = recommend(selected_song)
        
        if recommended_music_names:
            cols = st.columns(5)
            for i in range(len(recommended_music_names)):
                with cols[i % 5]:
                    st.image(recommended_music_posters[i], caption=recommended_music_names[i])
                    st.markdown(f"[▶️ Play on Spotify]({recommended_music_links[i]})")

elif option == "By Artist":
    artist_name = st.text_input("Enter Artist Name")

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters, recommended_music_links = recommend_by_artist(artist_name)
        
        if recommended_music_names:
            cols = st.columns(5)
            for i in range(len(recommended_music_names)):
                with cols[i % 5]:
                    st.image(recommended_music_posters[i], caption=recommended_music_names[i])
                    st.markdown(f"[▶️ Play on Spotify]({recommended_music_links[i]})")
