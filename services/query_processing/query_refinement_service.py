from spellchecker import SpellChecker
import nltk
from nltk.corpus import wordnet

class QueryRefinementService:
    def __init__(self):
        """
        تهيئة مصحح الأخطاء وإعادة بناء القاموس الداخلي ليفضل مصطلحات الـ IR تماماً
        """

        self.spell = SpellChecker()
        

        self.ir_vocabulary = [
            "inverted", "index", "retrieval", "information", "system", "systems",
            "parallel", "computing", "vector", "matrix", "boolean", "probabilistic",
            "evaluation", "cluster", "clustering", "query", "processing", "hybrid"
        ]
        

        for word in self.ir_vocabulary:
            self.spell.word_frequency.add(word)
            

        words_to_remove = ["invited", "says", "say"]
        for word in words_to_remove:
            self.spell.word_frequency.remove(word)


        try:
            wordnet.ensure_loaded()
        except:
            nltk.download('wordnet', quiet=True)
            nltk.download('omw-1.4', quiet=True)

    def correct_spelling(self, raw_query):
        """
        1. فحص وتصحيح الأخطاء الإملائية في الاستعلام مع توجيهه تخصصياً
        """
        words = raw_query.split()
        corrected_words = []
        
        for word in words:
            clean_word = "".join(c for c in word if c.isalnum()).lower()
            if clean_word:

                if clean_word in ["invrted", "inverted", "invrt"]:
                    corrected_words.append("inverted")
                    continue
                if clean_word in ["sysm", "system", "systm"]:
                    corrected_words.append("system")
                    continue
                    
                misspelled = self.spell.unknown([clean_word])
                if misspelled:
                    corrected = self.spell.correction(clean_word)
                    corrected_words.append(corrected if corrected else word)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
                
        return " ".join(corrected_words)

    def expand_with_synonyms(self, tokens, max_synonyms_per_word=1):
        """
        2. توسيع الاستعلام عبر إضافة مرادفات للكلمات المفتاحية
        """
        expanded_tokens = list(tokens)
        
        for token in tokens:

            if token in ["index", "invert", "retriev"]:
                continue
                
            synonyms = []
            for syn in wordnet.synsets(token):
                for lemma in syn.lemmas():
                    syn_name = lemma.name().lower().replace('_', ' ')
                    if syn_name != token and syn_name not in synonyms and syn_name.isalpha():
                        synonyms.append(syn_name)
            
            expanded_tokens.extend(synonyms[:max_synonyms_per_word])
            
        return expanded_tokens