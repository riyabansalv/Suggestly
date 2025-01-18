from flask import Flask, request, jsonify, render_template
from recommendation import MusicRecommender
from book_recommendation import BookRecommender
from movie_recommendation import MovieRecommender
from games_recommendation import GameRecommender
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

# Music Recommendation Route
@app.route("/recommend_music", methods=["POST"])
def recommend_music():
    data = request.json
    music_title = data.get("music_title", "")
    recommendations = music_recommender.recommend(music_title)
    return jsonify({"recommendations": recommendations})

# Book Recommendation Route
@app.route("/recommend_book", methods=["POST"])
def recommend_book():
    data = request.json
    book_title = data.get("book_title", "")
    recommendations = book_recommender.recommend(book_title)
    return jsonify({"recommendations": recommendations})


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
