import numpy as np

class HybridService:
    @staticmethod
    def normalize_scores(scores):
       
        min_val = np.min(scores)
        max_val = np.max(scores)
        if max_val == min_val:
            return np.zeros_like(scores)
        return (scores - min_val) / (max_val - min_val)

    @staticmethod
    def parallel_fusion_combsum(bm25_scores, embedding_scores):
       
        norm_bm25 = HybridService.normalize_scores(bm25_scores)
        norm_emb = HybridService.normalize_scores(embedding_scores)
        
       
        final_scores = norm_bm25 + norm_emb
        return final_scores