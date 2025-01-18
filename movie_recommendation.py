import pickle
import requests

class MovieRecommender:
    def __init__(self, movies_path, similarity_path):
        self.movies = pickle.load(open(movies_path, "rb"))
        self.similarity = pickle.load(open(similarity_path, "rb"))
    
    def fetch_poster(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', '')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    
    def recommend(self, movie_title):
        try:
            index = self.movies[self.movies['title'] == movie_title].index[0]
            distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
            recommendations = []

            for i in distances:
                movie_id = self.movies.iloc[i[0]].id
                recommendations.append({
                    "title": self.movies.iloc[i[0]].title,
                    "poster": self.fetch_poster(movie_id)
                })
            return recommendations
        except IndexError:
            return [{"title": "Movie not found. Please try another.", "poster": ""}]