from sklearn.feature_extraction.text import TfidfVectorizer

class RepresentationService:
    def __init__(self):
        # إنشاء مصفوفة TF-IDF
        self.vectorizer = TfidfVectorizer()

    def train_model(self, corpus):
        # تدريب النموذج على مجموعة الوثائق
        return self.vectorizer.fit_transform(corpus)

    def get_tfidf_vector(self, text):
        # تحويل نص واحد إلى متجه TF-IDF
        return self.vectorizer.transform([text])