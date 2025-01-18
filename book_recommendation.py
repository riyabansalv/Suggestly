import pickle
import requests


class BookRecommender:
    def __init__(self, books_path, similarity_path):
        self.books = pickle.load(open(books_path, "rb"))
        self.similarity = pickle.load(open(similarity_path, "rb"))

    def fetch_book_poster(self, book_title):
        """
        Fetch book poster using Google Books API.
        """
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={book_title}&fields=items(volumeInfo(imageLinks/thumbnail))&maxResults=1"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            try:
                return data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
            except (KeyError, IndexError):
                return "https://via.placeholder.com/128x192?text=No+Image"  # Fallback for missing image
        return "https://via.placeholder.com/128x192?text=Error"

    def recommend(self, book_title):
        try:
            index = self.books[self.books['title'] == book_title].index[0]
            distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
            recommendations = []

            for i in distances:
                book_id = self.books.iloc[i[0]]
                recommendations.append({
                    "title": self.books.iloc[i[0]].title,
                    "poster": self.fetch_book_poster(self.books.iloc[i[0]].title)
                })
            return recommendations
        except IndexError:
            return [{"title": "Book not found. Please try another.", "poster": ""}]