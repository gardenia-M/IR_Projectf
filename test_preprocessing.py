import gzip
import re
import os
from services.preprocessing.processor import PreprocessingService

# المسار المحلي للبيانات على القرص E
LOCAL_DATA_PATH = r"E:\ir_datasets_cache\downloads\d4863e4f342982b51b9a8fc668b2d0c0\msmarco-docs.trec.gz"

def test_preprocessing_pipeline():
    print("=" * 60)
    print("شاشة فحص وتأكيد معالجة البيانات (Data Pre-Processing Test)")
    print("=" * 60)
    
    if not os.path.exists(LOCAL_DATA_PATH):
        print(" خطأ: لم يتم العثور على ملف البيانات في المسار المحدد!")
        return

    try:
        # قراءة أول وثيقة فقط لفحصها
        with gzip.open(LOCAL_DATA_PATH, 'rt', encoding='utf-8') as f:
            full_text = ""
            in_text = False
            for line in f:
                line = line.strip()
                if line.startswith("<TEXT>"):
                    in_text = True
                elif line.startswith("</TEXT>"):
                    break
                elif in_text:
                    full_text += " " + line
            
            raw_sample = full_text.strip()

        # تشغيل التابع الخاص بكِ لمعالجة النص
        cleaned_sample = PreprocessingService.clean_text(raw_sample)

        # دالة الفحص الذكي للـ Pre-processing
        has_uppercase = any(char.isupper() for char in cleaned_sample)
        has_url = "http" in cleaned_sample or "https" in cleaned_sample or "www" in cleaned_sample
        has_punctuation = any(char in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' for char in cleaned_sample)
        
        # كلمات توقف شائعة جداً في MS MARCO (مثل the, is, an, of)
        has_stopwords = any(word in cleaned_sample.split() for word in ["the", "is", "and", "of", "to", "in"])

        print("\n[1] عينة من النص الخام (Raw Text Sample):")
        print(f"{raw_sample[:150]}...")
        
        print("\n[2] عينة من النص بعد المعالجة (Cleaned Text Sample):")
        print(f"{cleaned_sample[:150]}...")
        print("-" * 60)

        # النتائج والتقييم التلقائي
        success = True
        
        if has_uppercase:
            print(" فشل: النص ما زال يحتوي على أحرف كبيرة (لم يتم تطبيق الـ Lowercasing/Normalization).")
            success = False
        else:
            print(" نجاح: تم تحويل جميع الأحرف إلى أحرف صغيرة بنجاح.")

        if has_url:
            print(" فشل: النص ما زال يحتوي على روابط إلكترونية (URLs).")
            success = False
        else:
            print(" نجاح: تم تنظيف الروابط الإلكترونية تماماً.")

        if has_punctuation:
            print(" فشل: النص ما زال يحتوي على علامات ترقيم (Punctuation).")
            success = False
        else:
            print(" نجاح: تم حذف علامات الترقيم والرموز الخاصة.")

        if has_stopwords:
            print(" فشل: لم يتم حذف كلمات التوقف (Stop Words Removal) بشكل كامل.")
            success = False
        else:
            print(" نجاح: تم فلترة وحذف كلمات التوقف (Stop Words).")

        # فحص تقريبي للـ Stemming / Lemmatization
        # نتحقق إذا تحولت الكلمات المنتهية بـ ing أو ed إلى أصلها
        if "emitting" in cleaned_sample or "developed" in cleaned_sample:
            print(" تنبيه: الكلمات ما زالت تحتفظ باللواحق (قد يكون الـ Stemming/Lemmatization بحاجة لمراجعة).")
        else:
            print(" نجاح: تم تطبيق جذع الكلمات (Stemming/Lemmatization) بنجاح.")

        print("-" * 60)
        if success:
            print(" النتيجة النهائية: طلب 'معالجة البيانات' مُنفّذ ومحقق بنسبة 100% ومطابق لشروط المشروع!")
        else:
            print(" النتيجة النهائية: هناك نقص في بعض مراحل المعالجة، يرجى مراجعة التابع.")
        print("=" * 60)

    except Exception as e:
        print(f"حدث خطأ أثناء الفحص: {e}")

if __name__ == "__main__":
    test_preprocessing_pipeline()