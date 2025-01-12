import pickle

class MovieRecommender:
    def __init__(self, movies_pickle_path, similarity_pickle_path):
        # Load the preprocessed movie data and similarity matrix
        self.movies_data = pickle.load(open(movies_pickle_path, 'rb'))
        self.similarity = pickle.load(open(similarity_pickle_path, 'rb'))

    def recommend(self, movie_title):
        try:
            # Find the index of the movie
            movie_index = self.movies_data[self.movies_data['title'] == movie_title].index[0]
            distances = self.similarity[movie_index]

            # Get the top 5 similar movies
            recommended_movies = sorted(
                list(enumerate(distances)), reverse=True, key=lambda x: x[1]
            )[1:6]
            return [self.movies_data.iloc[i[0]].title for i in recommended_movies]
        except IndexError:
            return ["Movie not found. Please try another."]  # Handle cases where the movie is not in the dataset
