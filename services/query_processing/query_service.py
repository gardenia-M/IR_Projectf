import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class QueryProcessingService:
    def __init__(self):
        """
        تهيئة أدوات المعالجة المسبقة للاستعلام لضمان مطابقتها تماماً لمعالجة الوثائق
        """
        self.stemmer = PorterStemmer()

        try:
            self.stop_words = set(stopwords.words('english'))
        except:

            self.stop_words = {"i", "me", "my", "myself", "we", "our", "ours", "the", "a", "an", "and"}

    def clean_text(self, text):
        """
        تقنيات تنظيف النصوص (الطلب الأول): إزالة الروابط، الحروف الخاصة، وتحويل لحروف صغيرة
        """
        text = text.lower()
        text = re.sub(r'https?://\S+|www\&.\S+', '', text) 
        text = re.sub(r'[^a-zA-Z\s]', '', text)             
        return text

    def process_query(self, raw_query):
        """
        المعالجة المسبقة الكاملة للاستعلام: تنظيف -> تقسيم -> حذف كلمات الربط -> تجذيع
        """
        
        cleaned = self.clean_text(raw_query)
        

        words = cleaned.split()
        

        stemmed_words = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
        

        processed_query_str = " ".join(stemmed_words)
        
        return {
            "raw": raw_query,
            "processed_string": processed_query_str,
            "tokens": stemmed_words 
        }