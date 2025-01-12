import pickle

class GameRecommender:
    def __init__(self, games_data_path, similarity_data_path):
        # Load the preprocessed game data and similarity matrix
        self.games_data = pickle.load(open(games_data_path, 'rb'))
        self.similarity = pickle.load(open(similarity_data_path, 'rb'))

    def recommend(self, game_title):
        try:
            # Find the index of the game
            game_index = self.games_data[self.games_data['Name'] == game_title].index[0]
            distances = self.similarity[game_index]

            # Get the top 5 similar games
            recommended_games = sorted(
                list(enumerate(distances)), reverse=True, key=lambda x: x[1]
            )[1:6]
            return [self.games_data.iloc[i[0]]['Name'] for i in recommended_games]

        except IndexError:
            return ["Game not found. Please try another."]  # Handle cases where the game is not in the dataset
