import os
import pickle
import numpy as np
from collections import defaultdict

class IndexingService:
    def __init__(self, storage_dir="E:\\IR.Projectf\\index_storage"):
        """
        تهيئة خدمة الفهرسة وتحديد مجلد لحفظ الفهارس المستخرجة محلياً
        """
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def build_inverted_index(self, cleaned_documents, doc_ids):
        """
        بناء فهرس مقلوب (Inverted Index) تقليدي لسرعة البحث النصي واستخراج الكلمات بكفاءة
        """
        print("[INFO] جاري بناء الفهرس المقلوب (Inverted Index)...")
        inverted_index = defaultdict(list)
        
        for doc_id, doc_text in zip(doc_ids, cleaned_documents):
            # تقسيم النص إلى مصطلحات الفهرسة
            terms = doc_text.split()
            # حساب التكرارات داخل الوثيقة للمصطلحات لمنع التكرار في القائمة
            unique_terms = set(terms)
            for term in unique_terms:
                # إضافة معرف الوثيقة إلى قائمة المصطلح المغذى
                inverted_index[term].append(doc_id)
                
        return dict(inverted_index)

    def save_indices(self, dataset_name, inverted_index, vsm_matrix, bm25_model, bert_embeddings, doc_ids):
        """
        حفظ جميع الفهارس والنماذج المبنية محلياً لضمان الفهرسة السريعة واستيرادها لاحقاً دون إعادة حساب
        """
        print(f"[INFO] جاري حفظ فهارس ونماذج المجموعة '{dataset_name}' في القرص محلياً...")
        
        data_to_save = {
            "doc_ids": doc_ids,
            "inverted_index": inverted_index,
            "vsm_matrix": vsm_matrix,
            "bm25_model": bm25_model,
            "bert_embeddings": bert_embeddings
        }
        
        save_path = os.path.join(self.storage_dir, f"{dataset_name}_complete_index.pkl")
        with open(save_path, "wb") as f:
            pickle.dump(data_to_save, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f" تم حفظ وتأمين الفهرس بنجاح في: {save_path}")
        return save_path

    def load_indices(self, dataset_name):
        """
        استدعاء الفهرس المخزن بسرعة عالية عند تشغيل محرك البحث (Retrieval)
        """
        save_path = os.path.join(self.storage_dir, f"{dataset_name}_complete_index.pkl")
        if not os.path.exists(save_path):
            raise FileNotFoundError(f" لم يتم العثور على فهرس مخزن للمجموعة: {dataset_name}")
            
        print(f"[INFO] جاري تحميل الفهرس الكامل للمجموعة '{dataset_name}' بسرعة وفعالية...")
        with open(save_path, "rb") as f:
            return pickle.load(f)