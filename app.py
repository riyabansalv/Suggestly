from flask import Flask, request, jsonify, render_template
from recommendation import MusicRecommender

app = Flask(__name__)

# Initialize the recommender system with your CSV file
recommender = MusicRecommender("ex.csv")

@app.route("/")
def home():
    return render_template("index.html")  # Render the frontend

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    music_title = data.get("music_title", "")

    # Get recommendations
    recommendations = recommender.recommend(music_title)
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
