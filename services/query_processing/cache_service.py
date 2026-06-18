class IRCacheService:
    def __init__(self):
        # قاموس تخزين مؤقت في الذاكرة العشوائية
        self.search_cache = {}

    def get_cached_results(self, query_string):
        """ استرجاع النتائج إذا كانت محفوظة مسبقاً """
        return self.search_cache.get(query_string.lower().strip(), None)

    def set_cache_results(self, query_string, response_data):
        """ حفظ الاستعلام ونتائجه في الكاش """
        self.search_cache[query_string.lower().strip()] = response_data