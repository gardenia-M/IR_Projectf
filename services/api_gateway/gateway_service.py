import os
from services.query_processing.query_service import QueryProcessingService
from services.query_processing.query_refinement_service import QueryRefinementService
from services.retrieval_and_ranking.ranking_service import RetrievalAndRankingService
from services.indexing.indexing_service import IndexingService

from services.query_processing.cache_service import IRCacheService

class APIGatewayService:
    def __init__(self, index_name="msmarco_sample"):
        """
        API Gateway المطور: يدير الخدمات المستقلة ويحتوي على ذاكرة كاش ذكية لرفع الأداء
        """
        self.index_name = index_name
        self.indexer = IndexingService()
        
        print(f"[API Gateway] جاري استدعاء [Indexing Service] لتحميل البيانات...")
        self.loaded_indices = self.indexer.load_indices(self.index_name)
       
        self.query_processor = QueryProcessingService()
        self.query_refiner = QueryRefinementService()
        self.ranker = RetrievalAndRankingService(self.loaded_indices)
        
        
        self.cache_service = IRCacheService()

    def route_search_request(self, raw_query, mode="parallel", alpha=0.5):
        """
        توجيه طلب البحث مع فحص الكاش مسبقاً لتفادي التأخير (Orchestration Pipeline with Caching)
        """
        print(f"\n [API Gateway] استقبل طلب بحث جديد: '{raw_query}'")
        
       
       
        cache_key = f"{raw_query}_{mode}_{alpha}"
        
       
       
        cached_response = self.cache_service.get_cached_results(cache_key)
        if cached_response:
            print(f" [ CACHE HIT] تم العثور على النتيجة في الذاكرة المؤقتة! تخطي خط الإنتاج ونموذج BERT بالكامل...")
           
           
            cached_response["is_cached"] = True
            return cached_response
            
        print(f" [ CACHE MISS] الاستعلام يُنفّذ لأول مرة. جاري تشغيل النماذج وتوليد متجهات BERT...")

       
        corrected_query = self.query_refiner.correct_spelling(raw_query)
        print(f" [API Gateway] -> [Query Refinement Service]: النص المصحح: '{corrected_query}'")
        
        query_data = self.query_processor.process_query(corrected_query)
        print(f" [API Gateway] -> [Query Processing Service]: الكلمات المجذوعة: {query_data['tokens']}")
        
        expanded_tokens = self.query_refiner.expand_with_synonyms(query_data['tokens'], max_synonyms_per_word=1)
        print(f"🔗 [API Gateway] -> [Synonym Expansion]: الكلمات الموسعة: {expanded_tokens}")
        
       
        from services.indexing.bert_service import BERTService
        bert_srv = BERTService()
        query_bert_embedding = bert_srv.transform_query(query_data['processed_string'])
        
        print(f"🔗 [API Gateway] -> [Retrieval & Ranking Service]: جاري حساب النتائج بنمط ({mode})...")
        if mode == "parallel":
            results = self.ranker.search_parallel_hybrid(query_data['tokens'], query_bert_embedding, alpha=alpha)
        else:
            results = self.ranker.search_serial_hybrid(query_data['tokens'], query_bert_embedding)
            
       
        final_response = {
            "status": "success",
            "original_query": raw_query,
            "refined_query": corrected_query,
            "tokens_used": query_data['tokens'],
            "search_mode": mode,
            "results": results[:3],
            "is_cached": False
        }
        
       
        self.cache_service.set_cache_results(cache_key, final_response)
        
        return final_response