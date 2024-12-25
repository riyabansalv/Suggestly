import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MusicRecommender:
    def __init__(self, csv_path):
        # Load and clean the dataset
        self.df = pd.read_csv(csv_path)
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)

        # Process columns
        self.df['User-Rating'] = self.df['User-Rating'].str[:3]
        self.df['Album/Movie'] = self.df['Album/Movie'].str.replace(' ', '')
        self.df['Singer/Artists'] = self.df['Singer/Artists'].str.replace(' ', '').str.replace(',', ' ')

        # Create tags column
        self.df['tags'] = (self.df['Singer/Artists'] + ' ' +
                           self.df['Genre'] + ' ' +
                           self.df['Album/Movie'] + ' ' +
                           self.df['User-Rating']).str.lower()

        # Prepare data for recommendations
        self.new_df = self.df[['Song-Name', 'tags']].rename(columns={'Song-Name': 'title'})
        self.cv = CountVectorizer(max_features=2000)
        self.vectors = self.cv.fit_transform(self.new_df['tags']).toarray()
        self.similarity = cosine_similarity(self.vectors)

    def recommend(self, music_title):
        try:
            # Find index of the given song
            music_index = self.new_df[self.new_df['title'] == music_title].index[0]
            distances = self.similarity[music_index]

            # Get top 5 recommendations
            music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
            return [self.new_df.iloc[i[0]].title for i in music_list]
        except IndexError:
            return ["Song not found. Please try another."]
