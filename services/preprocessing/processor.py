import re
import string
from nltk.stem import PorterStemmer


stemmer = PorterStemmer()

class PreprocessingService:
   
    STOPWORDS = set([
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
        "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
        "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", 
        "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", 
        "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", 
        "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", 
        "about", "against", "between", "into", "through", "during", "before", "after", "above", 
        "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", 
        "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", 
        "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", 
        "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
    ])

    @staticmethod
    def clean_text(text):
        if not text:
            return ""
            
        
        text = text.lower()
        
       
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        
        text = re.sub(r'[^a-z\s]', '', text)
        
        
        tokens = text.split()
        
        
        cleaned_tokens = [
            stemmer.stem(word) 
            for word in tokens 
            if word not in PreprocessingService.STOPWORDS and len(word) > 1
        ]
        
        
        return " ".join(cleaned_tokens)