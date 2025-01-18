from flask import Flask, request, jsonify, render_template
from music_recommendation import MusicRecommender
from book_recommendation import BookRecommender
from movie_recommendation import MovieRecommender
from game_recommendation import GameRecommender
import pandas as pd


app = Flask(__name__)

# Initialize both recommenders
music_recommender = MusicRecommender("ex.csv")
book_recommender = BookRecommender()
movie_recommender = MovieRecommender("movies_list.pkl", "similarity.pkl")
game_recommender = GameRecommender("game_data.pkl","games_similarity.pkl")

music_df = pd.read_csv('ex.csv')


@app.route("/")
def home():
    return render_template("try.html")  # Render the new intro page

# Music Recommendation Route with Poster URLs
@app.route("/recommend_music", methods=["POST"])
def recommend_music():
    data = request.json
    music_title = data.get("music_title", "")
    recommendations = music_recommender.recommend(music_title)

    # You can add poster URLs here if available for the music recommendations
    enhanced_recommendations = []
    for song in recommendations:
        # Replace the following with your actual logic for music poster URLs
        poster_url = fetch_music_poster(song)  # Assuming a function to get music poster URL
        enhanced_recommendations.append({"title": song, "poster_url": poster_url})

    return jsonify({"recommendations": enhanced_recommendations})

# Book Recommendation Route with Poster URLs
@app.route("/recommend_book", methods=["POST"])
def recommend_book():
    data = request.json
    book_title = data.get("book_title", "")
    book_recommendations = book_recommender.recommend(book_title)
    
    # Use an external API like Google Books API to fetch poster URLs
    enhanced_recommendations = []
    for book in book_recommendations:
        poster_url = fetch_book_poster(book)  # Fetch poster for the book
        enhanced_recommendations.append({"title": book, "poster_url": poster_url})
    
    return jsonify({"recommendations": enhanced_recommendations})

def fetch_book_poster(book_title):
    """
    Fetch the book poster URL using an external API.
    Replace `API_KEY` with your actual API key for Google Books or other services.
    """
    API_URL = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": book_title, "key": "AIzaSyD5z-A0jZ3E6bNm7dHIUpwSrXDP1gFzZNM"}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            # Get the first book's thumbnail image
            try:
                poster_url = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
                return poster_url
            except KeyError:
                pass  # Thumbnail not available
    return "https://via.placeholder.com/150"  # Placeholder URL if no image found

def fetch_music_poster(music_title):
    # Replace with your Last.fm API key
    API_KEY = "3292a7af41353b90c116f28724b6c8be"
    API_URL = "http://ws.audioscrobbler.com/2.0/"

    # Make a request to Last.fm API to get the album information
    params = {
        "method": "track.search",
        "api_key": API_KEY,
        "track": music_title,  # Searching by track name instead of album
        "format": "json"
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and "trackmatches" in data["results"]:
            tracks = data["results"]["trackmatches"]["track"]
            if tracks:
                # Fetch the first track's image
                track = tracks[0]
                if "image" in track:
                    images = track["image"]
                    large_image = next((img["#text"] for img in images if img["size"] == "large"), None)
                    if large_image:
                        return large_image

    # Return a placeholder if no image is found
    return "https://via.placeholder.com/150"



@app.route("/recommend_movie", methods=["POST"])
def recommend_movie():
    data = request.json
    movie_title = data.get("movie_title", "")
    recommendations = movie_recommender.recommend(movie_title)
    return jsonify({"recommendations": recommendations})



# Game Recommendation Route
@app.route("/recommend_game", methods=["POST"])
def recommend_game():
    data = request.json
    game_name = data.get("game_name", "")
    recommendations = []
    if game_name:
        try:
            recommendations = game_recommender.recommend(game_name)
        except ValueError as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No game name provided."})
    return jsonify({"recommendations": recommendations})



if __name__ == "__main__":
    app.run(debug=True)

