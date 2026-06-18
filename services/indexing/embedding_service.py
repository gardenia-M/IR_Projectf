from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self):
        # تحميل النموذج محلياً (سيتحمل لمرة واحدة فقط عند أول تشغيل)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def encode_documents(self, documents):
        # تحويل النصوص كاملة إلى متجهات
        return self.model.encode(documents, show_progress_bar=True)

    def encode_query(self, query):
        return self.model.encode(query)