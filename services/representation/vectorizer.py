from sklearn.feature_extraction.text import TfidfVectorizer

class RepresentationService:
    def __init__(self):
       
        self.vectorizer = TfidfVectorizer()

    def train_model(self, corpus):
       
        return self.vectorizer.fit_transform(corpus)

    def get_tfidf_vector(self, text):
       
        return self.vectorizer.transform([text])