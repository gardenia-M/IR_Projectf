from rank_bm25 import BM25Okapi
import pickle

class BM25Service:
    def __init__(self, k1=1.5, b=0.75):
        """
        تهيئة معاملات نموذج BM25 الاحتمالي مع إمكانية التحكم بها من الواجهة لاحقاً
        """
        self.k1 = k1
        self.b = b
        self.bm25 = None

    def fit_and_save(self, cleaned_documents, save_path):
        """
        بناء كشاف BM25 وحفظه محلياً
        """
        # نموذج BM25 يتوقع النصوص مقسمة إلى كلمات (Tokenized)
        tokenized_corpus = [doc.split() for doc in cleaned_documents]
        
        # بناء النموذج وتمرير المعاملات k1 و b
        self.bm25 = BM25Okapi(tokenized_corpus, k1=self.k1, b=self.b)
        
        # حفظ الكائن محلياً
        with open(save_path, 'wb') as f:
            pickle.dump(self.bm25, f)
            
        return self.bm25

    def get_scores(self, tokenized_query):
        """
        حساب درجات المطابقة النصية للاستعلام
        """
        if self.bm25 is None:
            raise ValueError(" يجب تدريب النموذج أولاً باستخدام fit_and_save")
        return self.bm25.get_scores(tokenized_query)