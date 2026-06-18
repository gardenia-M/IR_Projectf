import numpy as np

class EvaluationService:
    def __init__(self):
        """
        خدمة التقييم وحساب المقاييس القياسية لنظم استرجاع المعلومات (IR Evaluation)
        محدثة ومعايرة وفق المعايير الأكاديمية القياسية الشاملة.
        """
        pass

    def calculate_precision_at_k(self, retrieved_ids, relevant_ids, k=10):
        """
        حساب الدقة عند الترتيب K (Precision@K)
        """
        if not retrieved_ids or k <= 0:
            return 0.0
        
        # أخذ أعلى K وثيقة مسترجعة فقط
        top_k = retrieved_ids[:k]
        relevant_retrieved = [doc for doc in top_k if doc in relevant_ids]
        
        return len(relevant_retrieved) / float(k)

    def calculate_recall(self, retrieved_ids, relevant_ids):
        """
        حساب الاستدعاء (Recall) نسبةً إلى جميع الوثائق ذات الصلة الحقيقية في ملف الـ qrels
        """
        if not relevant_ids:
            return 0.0
        
        relevant_retrieved = [doc for doc in retrieved_ids if doc in relevant_ids]
        return len(relevant_retrieved) / float(len(relevant_ids))

    def calculate_average_precision(self, retrieved_ids, relevant_ids):
        """
        حساب متوسط الدقة (Average Precision) للاستعلام الواحد
        """
        if not relevant_ids or not retrieved_ids:
            return 0.0
        
        score = 0.0
        num_hits = 0.0
        
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_ids:
                num_hits += 1.0
                # حساب الدقة التراكمية عند الموضع الحالي (i + 1)
                score += num_hits / (i + 1.0)
                
        if num_hits == 0:
            return 0.0
            
        # القسمة الأكاديمية على الحجم الإجمالي لكافة الوثائق ذات الصلة المتاحة
        return score / float(len(relevant_ids))

    def calculate_ndcg(self, retrieved_ids, relevant_ids, k=10):
        """
        حساب الكسب التراكمي المخصوم المميّز (nDCG@K) لتقييم كفاءة وجودة الترتيب
        """
        if not retrieved_ids or not relevant_ids or k <= 0:
            return 0.0
            
        top_k = retrieved_ids[:k]
        dcg = 0.0
        
        # 1. حساب الـ DCG الفعلي للترتيب المسترجع من نظامكِ
        for i, doc_id in enumerate(top_k):
            rel = 1 if doc_id in relevant_ids else 0
            dcg += rel / np.log2(i + 2)  # i + 2 لتفادي المقام صفر ولوغاريتم 1
            
        # 2. حساب الـ IDCG المثالي (أفضل ترتيب ممكن للوثائق الحقيقية المتاحة في الـ qrels لغاية الموضع K)
        idcg = 0.0
        # نعتبر أن جميع الوثائق ذات الصلة الحقيقية المتاحة ترتبت في الصدارة أولاً بوزن 1
        ideal_rels = sorted([1 for _ in relevant_ids], reverse=True)[:k]
        
        for i, rel in enumerate(ideal_rels):
            idcg += rel / np.log2(i + 2)
            
        if idcg == 0.0:
            return 0.0
            
        return dcg / idcg