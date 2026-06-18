import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RetrievalAndRankingService:
    def __init__(self, loaded_indices):
        """
        حقن الفهارس والنماذج المحملة من خدمة الفهرسة لاستخدامها في المطابقة
        """
        self.doc_ids = loaded_indices["doc_ids"]
        self.inverted_index = loaded_indices["inverted_index"]
        self.vsm_matrix = loaded_indices["vsm_matrix"]
        self.bm25_model = loaded_indices["bm25_model"]
        self.bert_embeddings = loaded_indices["bert_embeddings"]

    def _normalize_scores(self, scores):
        """
        تسوية الدرجات لتصبح بين 0 و 1 لضمان دمج عادل (Score Fusion)
        """
        min_s, max_s = np.min(scores), np.max(scores)
        if max_s == min_s:
            return np.zeros_like(scores)
        return (scores - min_s) / (max_s - min_s)

    def search_bm25(self, query_tokens):
        """ حساب درجات BM25 للاستعلام """
        return self.bm25_model.get_scores(query_tokens)

    def search_parallel_hybrid(self, query_tokens, query_bert_emb, alpha=0.5):
        """
        التمثيل الهجين المتوازي (Parallel)
        يجمع بين درجات BM25 النصية و BERT الدلالية بالتوازي مع دمج النتائج
        """
        # . حساب درجات BM25 وتسويتها
        bm25_scores = self.search_bm25(query_tokens)
        norm_bm25 = self._normalize_scores(bm25_scores)

        # . حساب درجات تشافه BERT وتسويتها
        query_emb_2d = query_bert_emb.reshape(1, -1)
        bert_scores = cosine_similarity(query_emb_2d, self.bert_embeddings).flatten()
        norm_bert = self._normalize_scores(bert_scores)

        # . دمج الدرجات (Score Fusion) باستخدام معادلة التثقيل الخطية
        final_scores = alpha * norm_bm25 + (1 - alpha) * norm_bert

        # ترتيب الوثائق تنازلياً حسب الأعلى تشابهاً
        ranked_indices = np.argsort(final_scores)[::-1]
        
        return [(self.doc_ids[idx], final_scores[idx]) for idx in ranked_indices]

    def search_serial_hybrid(self, query_tokens, query_bert_emb, top_n_initial=3):
        """
        التمثيل الهجين التسلسلي (Serial)
        مرحلة 1: تصفية نصية سريعة بـ BM25 لاستخراج أعلى وثائق مرشحة.
        مرحلة 2: إعادة ترتيب دلالي (Reranking) للمرشحين فقط باستخدام BERT.
        """
        # المرحلة الأولى: تصفية أولية سريعة بـ BM25
        bm25_scores = self.search_bm25(query_tokens)
        initial_ranked_indices = np.argsort(bm25_scores)[::-1][:top_n_initial]
        
        # المرحلة الثانية: إعادة ترتيب المصفوفة المصغرة بـ BERT
        candidate_embeddings = self.bert_embeddings[initial_ranked_indices]
        query_emb_2d = query_bert_emb.reshape(1, -1)
        bert_scores = cosine_similarity(query_emb_2d, candidate_embeddings).flatten()
        
        # ترتيب المرشحين بناءً على التقييم الدلالي الجديد
        reranked_candidate_sub_indices = np.argsort(bert_scores)[::-1]
        final_ranked_indices = [initial_ranked_indices[idx] for idx in reranked_candidate_sub_indices]
        
        return [(self.doc_ids[idx], bert_scores[i]) for i, idx in enumerate(final_ranked_indices)]