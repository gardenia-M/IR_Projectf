import os
import glob

def verify_queries_and_qrels():
    print("=" * 60)
    print(" فحص التحقق من ملفات الاستعلامات (Queries) والتقييم (Qrels)")
    print("=" * 60)
    
    base_cache_path = r"E:\ir_datasets_cache"
    
    print(f"[INFO] جاري البحث في مجلد الكاش المعتمد: {base_cache_path}\n")
    
    if not os.path.exists(base_cache_path):
        print(f" تنبيه: المجلد غير موجود في هذا المسار!")
        return

    all_files = glob.glob(os.path.join(base_cache_path, "**", "*"), recursive=True)
    
    queries_found = []
    qrels_found = []
    
    for file_path in all_files:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path).lower()
            
            if "query" in file_name or "queries" in file_name or "orcas" in file_name:
                queries_found.append(file_path)
                
            file_name_without_ext = os.path.splitext(file_name)[0]
            if "qrels" in file_name or "qrel" in file_name_without_ext:
                qrels_found.append(file_path)
                
    print(" [1] ملفات الاستعلامات (Queries / Testing Data):")
    if queries_found:
        print(f"    تم العثور على {len(queries_found)} ملف(ات) مرشحة للاستعلامات:")
        for path in queries_found[:3]: # عرض أول 3 ملفات فقط للاختصار
            print(f"     - {os.path.relpath(path, base_cache_path)}")
    else:
        print("   تنبيه: لم يتم العثور على ملفات باسم queries مباشرة في الكاش الرئيسي.")

    print("-" * 60)

    # عرض نتائج الـ qrels
    print("📋 [2] ملفات الأحكام والملائمة (Qrels / Ground Truth):")
    if qrels_found:
        print(f"    تم العثور على {len(qrels_found)} ملف(ات) مرشحة للأحكام والتقييم:")
        for path in qrels_found[:3]:
            print(f"     - {os.path.relpath(path, base_cache_path)}")
    else:
        print("    تنبيه: لم يتم العثور على ملفات باسم qrels مباشرة في الكاش الرئيسي.")

    print("=" * 60)

if __name__ == "__main__":
    verify_queries_and_qrels()