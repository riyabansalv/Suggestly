import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BookRecommender:
    def __init__(self):
        # Load and clean the dataset
        self.df = pd.read_csv('booksumm.csv')
        self.df.dropna(subset=['Book-title', 'Author', 'Plot-summary'], inplace=True)
        
        # Process genres (remove nested structure if present)
        self.df['Book genres'] = self.df['Book genres'].str.replace('[{}"/]', '', regex=True)
        
        # Create weighted tags column
        self.df['tags'] = (
            (self.df['Author'] + ' ') * 1 +  # Lower weight for Author
            (self.df['Book genres'].fillna('') + ' ') * 2 +  # Medium weight for genres
            (self.df['Plot-summary'] + ' ') * 3  # Higher weight for summary
        ).str.lower()
        
        # Prepare data for recommendations using TF-IDF
        self.new_df = self.df[['Book-title', 'tags']].rename(columns={'Book-title': 'title'})
        self.tfidf = TfidfVectorizer(max_features=2000, stop_words='english')
        self.vectors = self.tfidf.fit_transform(self.new_df['tags']).toarray()
        self.similarity = cosine_similarity(self.vectors)

    def recommend(self, book_title):
        try:
            # Find index of the given book
            book_index = self.new_df[self.new_df['title'].str.lower() == book_title.lower()].index[0]
            distances = self.similarity[book_index]

            # Get top 5 recommendations
            book_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
            return [self.new_df.iloc[i[0]].title for i in book_list]
        except IndexError:
            return ["Book not found. Please try another."]
