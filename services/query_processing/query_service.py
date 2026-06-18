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
        # الاعتماد على قائمة الكلمات المفتاحية الشائعة الإنجليزية
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            # قائمة احتياطية في حال عدم تحميل nltk stopwords محلياً
            self.stop_words = {"i", "me", "my", "myself", "we", "our", "ours", "the", "a", "an", "and"}

    def clean_text(self, text):
        """
        تقنيات تنظيف النصوص (الطلب الأول): إزالة الروابط، الحروف الخاصة، وتحويل لحروف صغيرة
        """
        text = text.lower()
        text = re.sub(r'https?://\S+|www\&.\S+', '', text)  # حذف الروابط إن وجدت
        text = re.sub(r'[^a-zA-Z\s]', '', text)             # الإبقاء على الحروف الإنجليزية فقط
        return text

    def process_query(self, raw_query):
        """
        المعالجة المسبقة الكاملة للاستعلام: تنظيف -> تقسيم -> حذف كلمات الربط -> تجذيع
        """
        # . التنظيف الأساسي
        cleaned = self.clean_text(raw_query)
        
        # . التقسيم (Tokenization)
        words = cleaned.split()
        
        # . حذف الـ Stop words والتجذيع (Stemming)
        stemmed_words = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
        
        # إعادة دمج الكلمات المعالجة في نص واحد للنماذج التي تتوقع نصاً
        processed_query_str = " ".join(stemmed_words)
        
        return {
            "raw": raw_query,
            "processed_string": processed_query_str,
            "tokens": stemmed_words  # جاهز لـ BM25 و Inverted Index
        }