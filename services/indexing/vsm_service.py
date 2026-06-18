from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class VSMService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_and_save(self, cleaned_documents, save_path):
       
        tfidf_matrix = self.vectorizer.fit_transform(cleaned_documents)
      
        with open(save_path, 'wb') as f:
            pickle.dump((self.vectorizer, tfidf_matrix), f)
        return tfidf_matrix

    def transform_query(self, cleaned_query):
        return self.vectorizer.transform([cleaned_query])