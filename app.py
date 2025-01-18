from flask import Flask, request, jsonify, render_template
from music_recommendation import MusicRecommender
from book_recommendation import BookRecommender
from movie_recommendation import MovieRecommender
from game_recommendation import GameRecommender
import pandas as pd


app = Flask(__name__)

# Initialize the recommenders
music_recommender = MusicRecommender("music_list.pkl", "music_similarity.pkl")
book_recommender = BookRecommender("book_list.pkl", "book_similarity.pkl")
movie_recommender = MovieRecommender("movies_list.pkl", "movie_similarity.pkl")

# Load the music dataframe globally
music_df = pd.read_pickle("music_list.pkl")
books_df = pd.read_pickle("book_list.pkl")
movies_df = pd.read_pickle("movies_list.pkl")


@app.route("/")
def home():
    return render_template("index.html")  # Render the new intro page

# Music Recommendation Route
@app.route("/recommend_music", methods=["POST"])
def recommend_music():
    data = request.json
    music_title = data.get("music_title", "").strip()
    if not music_title:
        return jsonify({"recommendations": []})
    
    recommendations = music_recommender.recommend(music_title)
    return jsonify({"recommendations": [{"title": rec.title()} for rec in recommendations]})

@app.route("/get_titles", methods=["GET"])
def get_titles():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify({"titles": []})

    try:
        matching_titles = (
            music_df[music_df['title'].str.lower().str.contains(query, case=False, na=False)]['title']
            .head(10)
            .str.title()
            .tolist()
        )

        return jsonify({"titles": matching_titles})
    except KeyError:
        return jsonify({"titles": []})





# Book Recommendation route
@app.route("/recommend_books", methods=["POST"])
def recommend_books():
    data = request.json
    book_title = data.get("book_title", "")
    recommendations = book_recommender.recommend(book_title)
    return jsonify({"recommendations": recommendations})

@app.route("/get_titles", methods=["GET"])
def get_titles():
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"titles": []})
    
    matching_titles = books_df[books_df['title'].str.lower().str.contains(query, na=False)]['title'].head(10).tolist()
    return jsonify({"titles": matching_titles})




# Movie recommendation routes
@app.route("/recommend_movies", methods=["POST"])
def recommend_movies():
    data = request.json
    movie_title = data.get("movie_title", "")
    recommendations = movie_recommender.recommend(movie_title)
    return jsonify({"recommendations": recommendations})

@app.route("/get_titles", methods=["GET"])
def get_titles():
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"titles": []})
    
    matching_titles = movies_df[movies_df['title'].str.lower().str.contains(query, na=False)]['title'].head(10).tolist()
    return jsonify({"titles": matching_titles})





if __name__ == "__main__":
    app.run(debug=True)

