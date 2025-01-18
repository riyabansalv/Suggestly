import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class GameRecommender:
    def __init__(self):
        # Load the preprocessed game data and similarity matrix
        self.games_data = pickle.load(open('game_data.pkl', 'rb'))
        self.similarity = pickle.load(open('games_similarity.pkl', 'rb'))
        self.new_df = self.games_data[['AppID', 'Name', 'Tags']]

        # Load image data for poster fetching
        self.image_data = pd.read_csv('game_image_data.csv')  # Open the image dataset
        self.image_data = self.image_data[['AppID', 'Headerimage']]  # Extract relevant columns
        self.image_data.set_index('AppID', inplace=True)  # Set AppID as index for easy lookup

    def fetch_image(self, app_id):
        """Fetch the header image URL for a game based on AppID."""
        try:
            # Check if the AppID exists in the dataset, return the corresponding header image
            return self.image_data.loc[app_id, 'Headerimage']
        except KeyError:
            # Return None or a default image if the AppID is not found
            return None

    def recommend(self, game_name):
        """Recommend similar games based on the given game name."""
        try:
            # Find the index of the given game in the dataframe
            game_index = self.new_df[self.new_df['Name'] == game_name].index[0]
            distances = sorted(list(enumerate(self.similarity[game_index])), reverse=True, key=lambda x: x[1])
            
            # Prepare lists for game recommendations and images
            recommended_games = []

            for i in distances[1:6]:  # Get top 5 similar games (excluding the input game itself)
                game_info = self.new_df.iloc[i[0]]
                game_name = game_info['Name']
                app_id = game_info['AppID']
                game_image = self.fetch_image(app_id)  # Fetch the image URL using AppID

                recommended_games.append({'name': game_name, 'app_id': app_id, 'image': game_image})

            return recommended_games
        except IndexError:
            return []
