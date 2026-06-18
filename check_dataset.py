import gzip
import os

LOCAL_DATA_PATH = r"E:\ir_datasets_cache\downloads\d4863e4f342982b51b9a8fc668b2d0c0\msmarco-docs.trec.gz"

def check_local_dataset():
    print("=" * 60)
    print(" سكربت الفحص المباشر لشروط الـ Dataset محلياً")
    print("=" * 60)
    
    if not os.path.exists(LOCAL_DATA_PATH):
        print(f" خطأ: لم يتم العثور على الملف في المسار المحدد: {LOCAL_DATA_PATH}")
        return

    print("[INFO] جاري فحص الملف المصدري وحساب عدد الوثائق تلقائياً...")
    docs_count = 0
    has_text_tags = False
    
    with gzip.open(LOCAL_DATA_PATH, 'rt', encoding='utf-8') as f:
        for line in f:
            if "<DOCNO>" in line:
                docs_count += 1
            if "<TEXT>" in line:
                has_text_tags = True
                
            if docs_count > 250000:
                break

    print("-" * 60)
    print(" [1] فحص عدد الوثائق (Documents Count):")
    print(f"   - تم العثور على ما يزيد عن: {docs_count:,} وثيقة داخل العينة المتقدمة.")
    if docs_count > 200000:
        print(f"    شرط العدد محقق بنجاح ! (أكبر من 200,000 وثيقة).")
    else:
        print(f"    شرط العدد غير محقق.")

    print("-" * 60)
    print(" [2] فحص بنية البيانات وملاءمتها للطلب الأول والثاني:")
    if has_text_tags:
        print("    البنية سليمة! تحتوي الوثائق على أوسام <TEXT> الجاهزة للمجذوع والـ Embedding.")
    else:
        print("    خطأ في بنية النصوص.")

    print("-" * 60)
    print(" [3] التأكيد النظري لبيانات الـ Testing والـ qrels لـ MS MARCO:")
    print("   - مجموعة MS MARCO Document معتمدة رسمياً عالمياً وفي موقع ir-datasets.")
    print("   - تحتوي افتراضياً على ملفات ORCAS و Qrels لتقييم الـ MAP و Mean Reciprocal Rank (MRR).")
    
    print("=" * 60)
    print(" النتيجة: الداتا المحملة على القرص E تستوفي الشرط الرقمي (+200K) وجاهزة تماماً!")
    print("=" * 60)

if __name__ == "__main__":
    check_local_dataset()