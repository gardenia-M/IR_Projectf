from sentence_transformers import SentenceTransformer
import pickle
import os

class BERTService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        تهيئة نموذج BERT الدلالي محلياً للتحويل إلى متجهات دلالية
        """
        print(f"[INFO] جاري تهيئة نموذج BERT: {model_name} محلياً...")
        self.model = SentenceTransformer(model_name)

    def fit_and_save(self, cleaned_documents, save_path):
        """
        توليد الـ Embeddings وحفظها في ملف محلي
        """
        print("[INFO] جاري تحويل النصوص إلى متجهات دلالية (Dense Vectors)...")
        # حساب المتجهات (Embeddings)
        embeddings = self.model.encode(cleaned_documents, show_progress_bar=True)
        
        # حفظ المتجهات محلياً لسرعة الاستدعاء اللاحق
        with open(save_path, 'wb') as f:
            pickle.dump(embeddings, f)
        return embeddings

    def transform_query(self, cleaned_query):
        """
        تحويل استعلام المستخدم المعالج إلى متجه دلالي بنفس أبعاد الوثائق
        """
        return self.model.encode(cleaned_query)