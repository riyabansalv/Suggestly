# from flask import Flask, request, jsonify, render_template
# from recommendation import MusicRecommender

# app = Flask(__name__)

# # Initialize the recommender system with your CSV file
# recommender = MusicRecommender("ex.csv")

# @app.route("/")
# def home():
#     return render_template("index.html")  # Render the frontend

# @app.route("/recommend", methods=["POST"])
# def recommend():
#     data = request.json
#     music_title = data.get("music_title", "")

#     # Get recommendations
#     recommendations = recommender.recommend(music_title)
#     return jsonify({"recommendations": recommendations})

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from recommendation import MusicRecommender
from book_recommendation import BookRecommender

app = Flask(__name__)

# Initialize both recommenders
music_recommender = MusicRecommender("ex.csv")
book_recommender = BookRecommender()

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

if __name__ == "__main__":
    app.run(debug=True)
